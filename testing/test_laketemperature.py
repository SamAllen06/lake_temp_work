import json
from pathlib import Path
import subprocess
import sys

DOCKER_DIRECTORY = Path(__file__).parent
IMAGE_NAME = "lake_temp"

def main() -> None:
    try:
        delete_image_if_exists()
        build_and_run_laketemp()
        delete_image_if_exists()
    except KeyboardInterrupt:
        print("Stopping...")
    except RuntimeError as error:
        print(error, file=sys.stderr)
        sys.exit(1)


def delete_image_if_exists() -> None:
    image_data = read_docker_output("docker images")

    for image in image_data:
        if image["Repository"] == IMAGE_NAME:
            if type(int(image["Containers"])) == 'N/A' or int(image["Containers"]) > 0:
                delete_containers_for_image(image["ID"])
            subprocess.run(
                ["docker", "rmi", image["ID"]],
                cwd=DOCKER_DIRECTORY,
            )

            return


def delete_containers_for_image(image_id: str) -> None:
    container_data = read_docker_output("docker ps -a")

    for container in container_data:
        if not container["Image"] == IMAGE_NAME:
            continue

        if container["Status"].startswith("Up"):
            raise RuntimeError(f"Cannot remove running container {container['ID']}")

        subprocess.run(
            ["docker", "rm", container["ID"]],
            cwd=DOCKER_DIRECTORY,
        )


# Returns JSON containing the information from each line of output.
def read_docker_output(command: str) -> list:
    output = subprocess.check_output(f"{command} --format json", shell=True)

    if output:
        data = [json.loads(line) for line in output.strip().split(b"\n")]
    else:
        data = {}

    return data


def build_and_run_laketemp() -> None:
    subprocess.run(
        ["docker", "buildx", "build", ".", "-t", IMAGE_NAME],
        cwd=DOCKER_DIRECTORY,
    )
    subprocess.run(
        ["docker", "run", "-it", IMAGE_NAME],
        cwd=DOCKER_DIRECTORY,
    )


if __name__ == "__main__":
    main()
