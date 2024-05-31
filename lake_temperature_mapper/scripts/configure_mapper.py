from pathlib import Path
from typing import Mapping

from config.config_writer import ConfigWriter


def main():
    import testing.config as mapper_config
    mapper_config_writer = ConfigWriter(mapper_config)
    mapper_config_writer.configure_interactively()


if __name__ == "__main__":
    main()
