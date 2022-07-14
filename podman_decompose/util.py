import yaml

from typing import List


def read(path: str) -> dict:
    with open(path) as file_obj:
        return yaml.safe_load(file_obj.read())


def run(cmd: List[str]):
    print(" ".join([str(c) for c in cmd]))
