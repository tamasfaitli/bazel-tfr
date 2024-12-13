#!/bin/python3

# Author: Tamas Faitli
# Date: 13/12/2024
# Description: A small plugin that iterates through every file
#   from current directory and computes the integrity, prints
#   it in a format copyable to source.json file (for patches
#   or overlays).
# Note: It uses the registry python module from the
#   github:bazelbuild/bazel-central-registry/tools but its not
#   included here to remove clutter.

import os
from registry import integrity, read


def compute_integrity_for_file(file):
    return integrity(read(file))


def gen_source_json_entry(file, sha):
    return f'        "{file}": "{sha}",'


def walk_dir_and_calc_integrity(dir):
    files_with_integrity = []
    for root, _, files in os.walk(dir):
        for file in files:
            path = os.path.relpath(os.path.join(root, file), dir)
            sha = compute_integrity_for_file(path)
            files_with_integrity.append(gen_source_json_entry(path, sha))
    return files_with_integrity


if __name__ == "__main__":
    pwd = os.getcwd()

    content_source_json = walk_dir_and_calc_integrity(pwd)

    for it in content_source_json:
        print(it)
