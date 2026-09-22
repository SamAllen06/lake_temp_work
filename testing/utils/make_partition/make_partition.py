# Creating the partition file used for acts_csv_to_ncdf used to be manual. An automated script was made using claude
# Anthropic. (2026). Claude (September 22 version) [Large language model]. https://claude.com
"""
Build a SPEL partition netCDF file (e.g. lake_temp_partition.nc) from:
  * a range file   (FUT_lake_range.txt): alternating lines of  <name>  /  <min> - <max>
  * a config file  (lake_temp_combinatorial.conf): [Parameter] section listing
    each parameter's test indices, e.g.  tkwat (int) : 0,1,2,...,10

For every parameter:
  * dimension  <name>_test_value  with length = number of indices in the .conf
  * variable   <name>(<name>_test_value)
      - double : values linearly interpolated over [min, max]
      - int    : boolean/flag parameters (integer range like "0 - 1"),
                 values taken directly from the integers in the range (0, 1)

Usage:
  python make_lake_partition.py \
      --range FUT_lake_range.txt \
      --conf  lake_temp_combinatorial.conf \
      --out   lake_temp_partition.nc
"""
import argparse
import re
import sys

import numpy as np
from netCDF4 import Dataset

# Order used in the requested CDL layout (doubles first, then int flags).
# Any parameter not listed here is appended in config-file order.
PREFERRED_ORDER = [
    "tkwat", "tkice", "tkair", "thk_bedrock", "cpliq", "cpice", "denh2o",
    "denice", "hfus", "grav", "vkc", "cnfac", "dtime_mod", "betavis",
    "depthcrit", "mixfact", "pudz",
    "lakepuddling", "lake_no_ed", "use_lch4",
]


def is_int_token(tok):
    """True if a number string is written as an integer (no '.', no exponent)."""
    return re.fullmatch(r"[+-]?\d+", tok) is not None


def read_ranges(path):
    """Return {name: (lo, hi, is_int)} from the range file."""
    with open(path) as f:
        lines = [ln.strip() for ln in f if ln.strip()]
    if len(lines) % 2:
        sys.exit(f"Error: {path} should contain name/range line pairs.")

    ranges = {}
    range_re = re.compile(r"^\s*(\S+)\s+-\s+(\S+)\s*$")
    for name, rng in zip(lines[0::2], lines[1::2]):
        m = range_re.match(rng)
        if not m:
            sys.exit(f"Error: could not parse range for '{name}': '{rng}'")
        lo_s, hi_s = m.groups()
        is_int = is_int_token(lo_s) and is_int_token(hi_s)
        ranges[name] = (float(lo_s), float(hi_s), is_int)
    return ranges


def read_conf(path):
    """Return ordered {name: [indices]} from the [Parameter] section."""
    params = {}
    section = None
    param_re = re.compile(r"^(\w+)\s*\((\w+)\)\s*:\s*(.+)$")
    with open(path) as f:
        for raw in f:
            line = raw.strip()
            if not line or line.startswith("--") or line.startswith("#"):
                continue
            if line.startswith("[") and line.endswith("]"):
                section = line[1:-1].strip().lower()
                continue
            if section != "parameter":
                continue
            m = param_re.match(line)
            if m:
                name, _ptype, vals = m.groups()
                params[name] = [int(v) for v in vals.split(",") if v.strip()]
    return params


def build_values(lo, hi, is_int, n):
    if is_int:
        vals = np.arange(int(lo), int(hi) + 1, dtype=np.int32)
        if len(vals) != n:
            sys.exit(f"Error: integer range {int(lo)}-{int(hi)} gives "
                     f"{len(vals)} values but config lists {n}.")
        return vals
    return np.linspace(lo, hi, n, dtype=np.float64)


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--range", default="FUT_lake_range.txt")
    ap.add_argument("--conf", default="lake_temp_combinatorial.conf")
    ap.add_argument("--out", default="lake_temp_partition.nc")
    args = ap.parse_args()

    ranges = read_ranges(args.range)
    conf = read_conf(args.conf)

    missing = [p for p in conf if p not in ranges]
    if missing:
        sys.exit(f"Error: no range given for config parameter(s): {missing}")
    extra = [p for p in ranges if p not in conf]
    if extra:
        print(f"Warning: range file parameters not in config (skipped): {extra}")

    order = [p for p in PREFERRED_ORDER if p in conf]
    order += [p for p in conf if p not in order]

    with Dataset(args.out, "w", format="NETCDF4") as ds:
        # Dimensions first (matches CDL layout), then variables.
        for name in order:
            ds.createDimension(f"{name}_test_value", len(conf[name]))

        for name in order:
            lo, hi, is_int = ranges[name]
            vals = build_values(lo, hi, is_int, len(conf[name]))
            dtype = "i4" if is_int else "f8"
            var = ds.createVariable(name, dtype, (f"{name}_test_value",))
            var[:] = vals

    print(f"Wrote {args.out} with {len(order)} parameters.")


if __name__ == "__main__":
    main()
