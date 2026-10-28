"""Isolate one smoke target so its working files and network restrictions cannot leak."""

import argparse
from pathlib import Path

from common.testing import execute_script


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--live", action="store_true")
    parser.add_argument("path", type=Path)
    args, remainder = parser.parse_known_args()
    execute_script(args.path, remainder, offline=not args.live)


if __name__ == "__main__":
    main()
