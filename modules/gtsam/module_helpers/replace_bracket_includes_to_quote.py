#!/bin/python3

import os
import re
import sys


# mode 0: overwrite files
# mode 1: export list with all used include
MODE = 0
if len(sys.argv) > 1:
    if sys.argv[1] == "-x":
        MODE = 1
        print("Extracting current includes...\n")
    else:
        print('''Please run the script from the root directory without arguments
in order to overwrite includes in source code (from <> brackets to "" quotes).

If you want to extract a list with current includes use the flag '-x'.

To customize what includes are overwritten edit the script.
''')
        exit(0)


EXLUDE_DIRS = ["Eigen", "GeographicLib"]
ROOT_DIRS_TO_CORRECT = ["gtsam/", "gtsam_unstable/", "CppUnitLite/", "Spectra/", "tests/", "examples/", "GeographicLib/", "metis", "gk_", "gklib_defs", "GKlib"]

# THIRDPARTY_INCLUDES = ["gk_", "gklib_defs", "GKlib", "metis", "SymEigs"]

DIRS_TO_WALK = ["gtsam", "examples", "tests"]


s_all_includes = []


def tmp_test_process_file(file_path):
    with open(file_path, 'r') as file:
        # print(f"opening: {file_path}\n")
        lines = file.readlines()

    # pattern = re.compile(r'#include\s*[<"](.*)[>"]')
    pattern = re.compile(r'#include\s*<(.*)>')

    for line in lines:
        match = pattern.search(line)

        if match:
            include = match.group(1)
            if any(x in include for x in ROOT_DIRS_TO_CORRECT):
                s_all_includes.append(line.strip('\n'))

            # if any(x in include for x in THIRDPARTY_INCLUDES):
            #     print(f"3rdparty includes from file: {file_path}")


def process_file(file_path):
    """Process a single file to replace #include <gtsam/...> with #include "gtsam/...".
    """
    with open(file_path, 'r') as file:
        lines = file.readlines()

    # updated_lines = []
    modified = False

    pattern = re.compile(r'#include\s*<(.*)>')

    for i in range(len(lines)):
        line = lines[i]
        match = pattern.search(line)

        if not match:
            continue

        matched = match.group(1)
        if not any(x in matched for x in ROOT_DIRS_TO_CORRECT):
            continue

        lines[i] = line.replace('<', '"').replace('>', '"')
        modified = True

    if modified:
        with open(file_path, 'w') as file:
            file.writelines(lines)
        print(f"Updated {file_path}")

    # for r in ROOT_DIRS_TO_CORRECT:
    #
    #     # pattern_str = f'#include\s*<{r}/(.*)>'
    #     pattern = re.compile(r'#include\s*<' + r + r'/(.*)>')
    #
    #     for i in range(len(lines)):
    #         match = pattern.search(lines[i])
    #         if match:
    #             # Replace with #include "gtsam/..."
    #             new_line = f'#include "{r}/{match.group(1)}"\n'
    #             lines[i] = new_line
    #             modified = True
    #
    # # Write back the file if any modifications were made
    # if modified:
    #     with open(file_path, 'w') as file:
    #         file.writelines(lines)
    #     print(f"Updated: {file_path}")


def process_directory(directory):
    """Recursively process all .cpp and .cc files in a directory."""
    for root, dirs, files in os.walk(directory):
        if any(ex_r in root for ex_r in EXLUDE_DIRS):
            continue
        for file in files:
            if file.endswith(('.cpp', '.cc', '.h', '.hh', '.hpp')):
                file_path = os.path.join(root, file)
                if MODE == 0:
                    process_file(file_path)
                else:
                    tmp_test_process_file(file_path)


# its not meant to be included so just dropping main
# if __name__ == "__main__":
    # Specify the directory to process
    # directory_to_process = input("Enter the directory to process: ").strip()


for dir in DIRS_TO_WALK:
    if not os.path.isdir(dir):
        print(f"Error: '{dir}' is not a valid directory!\n")
    else:
        process_directory(dir)
        print(f"Directory: {dir} has been finished!\n")

if MODE == 1:
    s_all_includes = list(dict.fromkeys(s_all_includes))
    out_file = "all_includes.txt"
    with open(out_file, "w") as fout:
        print(f"Writing current includes to file: {out_file}")
        for line in s_all_includes:
            fout.write(line + "\n")

print("Processing complete.")
