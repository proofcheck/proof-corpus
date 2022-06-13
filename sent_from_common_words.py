#!/usr/bin/env python

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

f = open("common_words.txt", "r")
common_words = f.readlines()
f.close()
common_words = common_words[1:]
common_words = [x.split("\t")[1][:-1] for x in common_words]
common_words = common_words[:200]
punctuation.update(common_words)
# print(punctuation)


def main(args):
    bigcount = 0
    count = 0
    for fd in args.files:
        for line in fd:
            proofID, text = line.strip().split("\t")
            words = set([w.lower() if w not in aliases else w
                    for w in text.split(" ")
                    if (w.lower() not in punctuation and w not in punctuation)])
            if len(words) < 3:
                count += 1
            bigcount += 1
    print(f"{count} out of {bigcount}")
    # for proofID, words in word_dict.items():
    #     print(f"{proofID}\t{' '.join(list(words))}")


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