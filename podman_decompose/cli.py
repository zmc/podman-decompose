import argparse
import sys

from typing import List

from podman_decompose.decompose import decompose, destroy
from podman_decompose.util import read


def parse_args(args: List[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "path",
        type=str,
        help="The docker-compose file to decompose",
    )
    parser.add_argument(
        "-d,--destroy",
        help="Generate commands to destroy, rather than create",
        dest="destroy",
        action="store_true",
    )
    return parser.parse_args(args)


def main():
    args = parse_args(sys.argv[1:])
    obj = read(args.path)
    if args.destroy:
        destroy(obj)
    else:
        decompose(obj)
    return 0


if __name__ == "__main__":
    sys.exit(main())
