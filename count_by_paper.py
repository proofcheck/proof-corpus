#!/usr/bin/env python

"""Report unigram counts for file(s) or stdin."""

import argparse
from collections import Counter
import sys


aliases = {"CASE", "CITE", "MATH", "NAME", "REF"}
punctuation = {
    ".",
    ",",
    ":",
    ";",
    "'",
    '"',
    "-",
    "?",
    "!",
    "(",
    ")",
    "{",
    "}",
    "[",
    "]",
    "`",
    "–",
    "''",
    '""',
    "``",
    "...",
    "…",
    "="
}




def main(args):

    word_dict = {}
    for fd in args.files:
        for line in fd:
            proofID, text = line.strip().split("\t")
            words = [w.lower() if w not in aliases else w
                    for w in text.split(" ")
                    if w not in punctuation]
            if proofID in word_dict:
                word_dict[proofID].update(words)
            else:
                word_dict[proofID] = set(words)

    for proofID, words in word_dict.items():
        print(f"{proofID}\t{' '.join(list(words))}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "files",
        nargs="*",
        default=[sys.stdin],
        type=argparse.FileType("r"),
        help="files to read",
    )

    args = parser.parse_args()

    main(args)
