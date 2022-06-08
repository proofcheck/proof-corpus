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
}


def quick_read(fd, keep_punctuation, answer):
    if keep_punctuation:
        return [s.split("\t")[-1].split() for s in fd.readlines()]
    else:
        answer.extend(
            (
                [
                    w.lower() if w not in aliases else w
                    for w in s.split("\t")[-1].split()
                    if w not in punctuation
                ]
                for s in fd.readlines()
            )
        )
        print("done", fd)


def get_unigrams(list_of_sentences):
    # Returns unigrams counter
    cnt = Counter()
    for s in list_of_sentences:
        # s = ["<s>"] + s + ["</s>"]
        cnt.update(s)
    return cnt


def main(args):

    sentences = []
    for fd in args.files:
        quick_read(fd, args.keep_punctuation, sentences)

    cnt_uni = get_unigrams(sentences)

    for (w, c) in cnt_uni.most_common():
        print(f"{c}\t{w}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--keep_punctuation",
        "-k",
        action="store_true",
        default=False,
        help="keep punctuation",
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
