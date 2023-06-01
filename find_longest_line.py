#!/usr/bin/env python

"Find the longest line in a file."

import argparse
import sys


if __name__ == "__main__":

    parser = argparse.ArgumentParser()

    parser.add_argument("files", nargs="*", type=argparse.FileType("r"),
                        default=[sys.stdin],
                        help="tsv files to update")
    args = parser.parse_args()

    for fd in args.files:
        max_len = -1
        longest_line = ""
        for line in fd.readlines():
            if len(line) > max_len:
                max_len = len(line)
                longest_line = line
        print(fd.name)
        print(max_len)
        if max_len > 80:
            print(longest_line[:40] + "..." + longest_line[-40:])
        else:
            print(longest_line)
