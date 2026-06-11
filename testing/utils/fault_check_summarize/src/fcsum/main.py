from argparse import ArgumentParser
import csv
from pathlib import Path
import textwrap


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
    create_summary()
    create_results_per_check()


def create_summary():
    sample_out_dir, expected_samples = parse_args()

    executable_errors = 0
    counts = {}
    for sample_index in range(expected_samples):
        #add 1 to sample index so it matches the indexing used in the console output and filesystem
        actual_sample_index = sample_index + 1
        sample_dir = sample_out_dir / str(actual_sample_index)
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


def create_results_per_check():
    sample_out_dir, expected_samples = parse_args()
    results_per_check: dict[str, list[int]] = {}
    
    for sample_index in range(expected_samples):
        #add 1 to sample index so it matches the indexing used in the console output and filesystem
        actual_sample_index = sample_index + 1
        sample_dir = sample_out_dir / str(actual_sample_index)
        executable_errors = 0

        if not sample_dir.exists():
            executable_errors += 1
            continue
        
        with open(sample_dir / "check_statuses.csv", newline="") as file:
            reader = csv.DictReader(file)
            for row in reader:
                check_and_status = row["check"] + " " + row["status"]
                if check_and_status not in results_per_check:
                    results_per_check[check_and_status] = []
                results_per_check[check_and_status].append(actual_sample_index)

    results_per_check = dict(sorted(results_per_check.items()))
    
    print("\nSamples per check result:")
    for check, sample_indices in results_per_check.items():
        print(f"| {str(check):<97} |")
        sample_numbers = textwrap.fill(f"{', '.join([str(index) for index in sample_indices])}", width=93)
        for line in sample_numbers.splitlines():
            print(f"|     {str(line):<93} |")


if __name__ == "__main__":
    main()
