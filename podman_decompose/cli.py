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
        "-d",
        "--destroy",
        help="Generate commands to destroy, rather than create",
        dest="destroy",
        action="store_true",
    )
    parser.add_argument(
        "--build",
        help="Include commands to build containers (the default)",
        dest="build",
        action="store_true",
        default=True,
    )
    parser.add_argument(
        "--no-build",
        help="Do not include commands to build containers",
        dest="build",
        action="store_false",
    )
    parser.add_argument(
        "-p",
        "--pretty",
        help="Pretty-print generated commands",
        dest="pretty",
        action="store_true",
        default=True,
    )
    parser.add_argument(
        "-c",
        "--compact",
        help="Print generated commands without making them pretty",
        dest="pretty",
        action="store_false",
    )
    return parser.parse_args(args)


def main():
    args = parse_args(sys.argv[1:])
    obj = read(args.path)
    if args.destroy:
        destroy(obj, args)
    else:
        decompose(obj, args)
    return 0


if __name__ == "__main__":
    sys.exit(main())
