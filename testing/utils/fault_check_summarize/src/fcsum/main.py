from argparse import ArgumentParser
import csv
from pathlib import Path


def parse_args() -> tuple[Path, int]:
    parser = ArgumentParser()
    parser.add_argument(
        "sample_out_dir", help="the directory containing fault finding sample output"
    )
    parser.add_argument(
        "expected_samples", help="the number of samples to expect", type=int
    )

    args = parser.parse_args()

    return Path(args.sample_out_dir), args.expected_samples


def main() -> None:
    sample_out_dir, expected_samples = parse_args()

    executable_errors = 0
    counts = {}
    for sample_index in range(expected_samples):
        sample_dir = sample_out_dir / str(sample_index)
        if not sample_dir.exists():
            executable_errors += 1
            continue

        with open(sample_dir / "check_statuses.csv", newline="") as file:
            reader = csv.DictReader(file)
            for row in reader:
                check = row["check"]
                if check not in counts:
                    counts[check] = {"pass": 0, "skip": 0, "fail": 0, "error": 0}
                match row["status"]:
                    case "PASSED":
                        counts[check]["pass"] += 1
                    case "SKIPPED":
                        counts[check]["skip"] += 1
                    case "FAILED":
                        counts[check]["fail"] += 1
                    case "ERROR":
                        counts[check]["error"] += 1

    order = list(counts)
    order.sort()

    longest_check_length = max([len(check) for check in counts])

    print(f"{executable_errors} out of {expected_samples} runs exited with an error.")
    print(
        f"| {'Check'.ljust(longest_check_length)} | Passed | Skipped | Failed | Errored |"
    )
    for check in order:
        check_counts = counts[check]
        print(
            f"| {check.ljust(longest_check_length)} "
            f"| {str(check_counts['pass']):<6} "
            f"| {str(check_counts['skip']):<7} "
            f"| {str(check_counts['fail']):<6} "
            f"| {str(check_counts['error']):<7} |"
        )


if __name__ == "__main__":
    main()
