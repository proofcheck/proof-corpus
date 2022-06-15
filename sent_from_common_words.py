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

# f = open("common_words.txt", "r")
# common_words = f.readlines()
# f.close()
# common_words = common_words[1:]
# common_words = [x.split("\t")[1][:-1] for x in common_words]
# common_words = common_words[:50]
# punctuation.update(common_words)
# print(punctuation)


def main(args):
    c = 0
    # print(args.com_words)
    amounts = [int(x) for x in args.com_words[0][1:-1].split(",")]
    common_words = [{p for p in punctuation} for x in amounts]
    f = open("common_words.txt", "r")
    common = f.readlines()
    f.close()
    common = common[1:]
    common = [x.split("\t")[1][:-1] for x in common]
    for n, x in enumerate(amounts):
        common_words[n].update(common[:x])
    # punctuation.update(common_words)
    counts = [{} for x in amounts]
    for y in counts:
        for x in range(56):
            y[x] = 0
    for fd in args.files:
        for line in fd:
            for x in range(len(counts)):

                proofID, text = line.strip().split("\t")
                text = text.split(" ")
                # text = line.strip(' ').split(" ")[1:-1]
                words = set([w.lower() if w not in aliases else w
                        for w in text
                        if (w not in common_words[x] and w.lower() not in common_words[x])])
                if len(words) in counts[x]:
                    counts[x][len(words)] += 1
                else:
                    counts[x][len(words)] = 1
            # counts[x]["Total"] = 38041358
    for y in counts:
        for x in range(150):
            if x in y and y[x] > 5:
               print(f"{x} {y[x]}")
    
    print(counts)
    # for proofID, words in word_dict.items():
    #     print(f"{proofID}\t{' '.join(list(words))}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    
    parser.add_argument(
        "com_words",
        nargs=1,
        default="100",
        type=ascii,
        help="number of common words to use",
    )
    
    parser.add_argument(
        "files",
        nargs="*",
        default=[sys.stdin],
        type=argparse.FileType("r"),
        help="files to read",
    )

    args = parser.parse_args()

    main(args)