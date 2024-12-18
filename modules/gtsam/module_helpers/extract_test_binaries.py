#!/bin/python3

import os

DIRS_TO_WALK = ["gtsam"]

TEST_DIR = "tests"

OUT_FILE_NAME = "bzl/gen_cc_tests.bzl"

EXCLUDE_TEST = ["testRot3Q.cpp", "testGeographicLib.cpp", "testGPSFactor.cpp"]

deps_and_opts_txt = '''            deps = [
                "//:CppUnitLite",
                "//:gtsam",
            ],
        ),
'''


def strip_gtsam(path):
    # return path[len("gtsam/"):]
    return path


def gen_build_commands_for_file(root, file):
    path = os.path.join(root, file)
    path = strip_gtsam(path)
    command = f'''
        native.cc_test(
            name = "{file.strip('.cpp')}",
            srcs = ["{path}"],
'''
    command += deps_and_opts_txt
#             deps = [
#                 "//CppUnitLite:CppUnitLite",
#                 ":gtsam",
#             ],
#             copts = ["-I."],
#         ),
# '''
    return command


def gen_build_commands_for_file_with_headers(root, file, headers):
    path = os.path.join(root, file)
    path = strip_gtsam(path)
    command = f'''
        native.cc_test(
            name = "{file.strip('.cpp')}",
            srcs = [
                "{path}",
'''
    for h in headers:
        hpath = os.path.join(root, h)
        hpath = strip_gtsam(hpath)
        command += f'                "{hpath}",\n'

    command += "            ],\n"
    command += deps_and_opts_txt
#         command += '''                    ],
#             deps = [
#                 "//CppUnitLite:CppUnitLite",
#                 ":gtsam",
#             ],
#             copts = ["-I."],
#         ),
# '''
    return command


def process_directory(directory):
    build_commands = []
    for root, dirs, files in os.walk(directory):
        if TEST_DIR not in root:
            continue

        test_sources = [sf for sf in files if sf.endswith('.cpp')]
        test_headers = [hf for hf in files if hf.endswith('.h')]

        for s in test_sources:
            if s in EXCLUDE_TEST:
                print(f"Exluded from test: {s}..\n")
                continue

            if len(test_headers) == 0:
                build_commands.append(gen_build_commands_for_file(root, s))
            else:
                build_commands.append(gen_build_commands_for_file_with_headers(root, s, test_headers))

    return build_commands


def export_build_file(file_name, content):
    print(f"Writing build commands to: {OUT_FILE_NAME}...\n")
    with open(file_name, 'w') as fout:

        fout.write("def generate_cc_tests():\n")
        fout.write("    return [\n")

        for c in content:
            for cc in c:
                fout.write(cc)

        fout.write("\n")
        fout.write("    ]")


if __name__ == "__main__":

    build_file_content = []

    for dir in DIRS_TO_WALK:
        if not os.path.isdir(dir):
            print(f"Error: '{dir}' is not a valid directory!\n")
        else:
            build_file_content.append(process_directory(dir))
            print(f"Directory '{dir}' has been processed!\n")

    export_build_file(OUT_FILE_NAME, build_file_content)

    print("Done!\n")
