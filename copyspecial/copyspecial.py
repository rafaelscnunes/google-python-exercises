#!/usr/bin/python
# Copyright 2010 Google Inc.
# Licensed under the Apache License, Version 2.0
# http://www.apache.org/licenses/LICENSE-2.0

# Google's Python Class
# http://code.google.com/edu/languages/google-python-class/

# Problem description:
# https://developers.google.com/edu/python/exercises/copy-special


import sys
import re
import os
import shutil
import subprocess

"""Copy Special exercise

"""


def get_special_paths(dir):
    return [dir for dir in os.listdir(dir) if re.findall(r'__.*__', dir)]


def main():
    # This basic command line argument parsing code is provided.
    # Add code to call your functions below.

    # Make a list of command line arguments, omitting the [0] element
    # which is the script itself.
    args = sys.argv[1:]
    if not args:
        print("usage: [--todir dir][--tozip zipfile] dir [dir ...]")
        sys.exit(1)

    # todir and tozip are either set from command line
    # or left as the empty string.
    # The args array is left just containing the dirs.
    todir = ''
    if args[0] == '--todir':
        todir = args[1]
        del args[0:2]

    tozip = ''
    if args[0] == '--tozip':
        tozip = args[1]
        del args[0:2]

    if len(args) == 0:
        print("error: must specify one or more dirs")
        sys.exit(1)

    for dir in args:
        files = get_special_paths(dir)

        if todir:
            os.makedirs(todir, exist_ok=True)
            for file in files:
                shutil.copy2(file, os.path.join(todir, file), follow_symlinks=True)
        elif tozip:
            os.makedirs(os.path.dirname(tozip), exist_ok=True)
            cmd = ['zip', '-j', tozip] + files
            print(' '.join(cmd))
            subprocess.run(cmd)
        else:
            print('\n'.join(files))


if __name__ == "__main__":
    main()
