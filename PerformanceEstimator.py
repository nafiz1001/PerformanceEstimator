#!/usr/bin/env python3

import pathlib
import re
import sys
import typing

def yaml_paths(root_dir: str):
    path = pathlib.Path(root_dir)
    if not path.is_dir():
        raise FileNotFoundError(f"{root_dir} is not accessible")
    return path.rglob('*.yaml')

# a list of pattern and its associated complexity "points"
## 1 complexity per line
## 10 complexity per pattern
## 10 complexity per ... or $METAVAR
## 30 complexity per deep expression matching with <...>

pattern_and_complexity_list : list[tuple[typing.Pattern, int]] = [
    (re.compile(r"(pattern)"), 10),
    (re.compile(r"([.][.][.])"), 10),
    (re.compile(r"(<[.][.][.])"), 30),
    (re.compile(r"(\n)"), 1),
    (re.compile(r"([$][A-Z])"), 10)
]

# starting directory for finding *.yaml files
root_dirs = sys.argv[1:] if len(sys.argv) > 1 else "."

# list of path to yaml and its associated total complexity
yaml_path_and_complexity_list = list[tuple[pathlib.Path, int]]()

try:
    for root_dir in root_dirs:
        for yaml_path in yaml_paths(root_dir):
            yaml_complexity = 0
            for yaml_line in open(yaml_path):
                for pattern, complexity in pattern_and_complexity_list:
                    if (m := pattern.search(yaml_line)):
                        # m.groups(): all matches to the pattern in yaml_line
                        yaml_complexity += len(m.groups()) * complexity

            yaml_path_and_complexity_list.append((yaml_path, yaml_complexity))

        for yaml_path, yaml_complexity in sorted(yaml_path_and_complexity_list, key=lambda y_c: y_c[1], reverse=True):
            print(f"{yaml_path}: {yaml_complexity}")
except BrokenPipeError:
    pass
