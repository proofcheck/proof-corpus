#!/usr/bin/env python

import argparse
from collections import Counter, defaultdict
from email.policy import default
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
common_words = common_words[:50]
punctuation.update(common_words)
# print(punctuation)


def main(args):
    counts = {}
    for x in range(56):
        counts[x] = 0
    for fd in args.files:
        for line in fd:
            proofID, text = line.strip().split("\t")
            words = set([w.lower() if w not in aliases else w
                    for w in text.split(" ")
                    if (w.lower() not in punctuation and w not in punctuation)])
            if len(words) in counts:
                counts[len(words)] += 1
            else:
                counts[len(words)] = 1
        counts["Total"] = 38041358
    for x in range(150):
        if x in counts and counts[x] > 5:
            print(f"{x} {counts[x]}")


    print(counts)
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