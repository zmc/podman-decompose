import shlex
import yaml

from typing import List


def read(path: str) -> dict:
    with open(path) as file_obj:
        return yaml.safe_load(file_obj.read())


def run(cmd: List[str], pretty=True):
    if len(shlex.join(cmd)) < 100:
        pretty = False
    cmd_str = ""
    indent = " " * 4 if pretty else ""
    newline = f"\\\n" if pretty else ""
    for item in cmd:
        if not isinstance(item, str):
            item = str(item)
        item = shlex.quote(item)
        if item.startswith("-"):
            cmd_str = f"{cmd_str} {newline}{indent}{item}"
        else:
            cmd_str = f"{cmd_str} {item}"
    print(cmd_str.strip())
