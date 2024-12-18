#!/bin/python3

import sys


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Please provide patch file to fix!\n")

    patch_file = sys.argv[1]

    print(f"Fixing patch file: {patch_file}\n")

    file_content = open(patch_file, "r").readlines()

    out_content = []
    for line in file_content:
        if "diff --git" in line:
            out_content.append('\n')

        out_content.append(line)

    with open(patch_file, "w") as fout:
        for line in out_content:
            fout.write(line)

    print("Done!")
