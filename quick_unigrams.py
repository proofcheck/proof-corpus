#!/usr/bin/env python

"""Report unigram counts for file(s) or stdin."""

# E.g.,

#  ./quick_unigrams.py today/sent00.tsv | less
#  ./quick_unigrams.py today/sent*.tsv > unigrams.txt

# Look for words not in the dictionary (mostly math jargon or typos)
#  ./quick_unigrams.py --spellcheck today/sent00.tsv | less
#  ./quick_unigrams.py --spellcheck today/sent*.tsv > spellcheck.txt


import argparse
from collections import Counter
import sys

from datasets import load_dataset


aliases = {"CASE", "CITE", "MATH", "NAME", "REF", "VERBATIM", "URL"}
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


def read_dataset(dataset, keep_punctuation, answer):
    if keep_punctuation:
        return [d['sentence'].split("\t")[-1].split() for d in dataset]
    else:
        answer.extend(
            (
                [
                    w.lower() if w not in aliases else w
                    for w in d['sentence'].split("\t")[-1].split()
                    if w not in punctuation
                ]
                for d in dataset.take(10000)
            )
        )



def get_unigrams(list_of_sentences):
    # Returns unigrams counter
    cnt = Counter()
    for s in list_of_sentences:
        # s = ["<s>"] + s + ["</s>"]
        cnt.update(s)
    return cnt


def main(args):

    sentences = []

    if args.files:
        for fd in args.files:
            quick_read(fd, args.keep_punctuation, sentences)
    else:
        print("Loading sentence dataset")
        dataset = load_dataset('proofcheck/prooflang', 'sentences', split='train', streaming=True)
        print("Going through sentences")
        read_dataset(dataset, args.keep_punctuation, sentences)


    cnt_uni = get_unigrams(sentences)

    if args.spellcheck:
        known_words: set[str] = set()
        with open("words_alpha.txt") as fd:
            for word in fd.readlines():
                word = word.strip()
                known_words.add(word)
            known_words.add("profinite")
            known_words.add("interpolants")
            known_words.add("maximality")
            known_words.add("poissonization")
            known_words.add("hamiltonians")
            known_words.add("lorentzian")
            known_words.add("injectivity")
        for (w, c) in cnt_uni.most_common():
            w1 = w.lower().removeprefix("math-").removeprefix("non-").removeprefix("-").removeprefix("sub-")
            if w1 not in known_words and w1.removesuffix("s") not in known_words:
                print(f"{c}\t{w}")
        return

    for (w, c) in cnt_uni.most_common(args.n):
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
        "--dataset",
        action="store_true",
        default=False,
        help="keep punctuation",
    )

    parser.add_argument(
        "-n",
        type=int,
        default=None,
        help="Number of words to show"
    )

    parser.add_argument(
        "--spellcheck",
        action="store_true",
        default=False,
        help="Show only words not in the dictionary",
    )

    parser.add_argument(
        "files",
        nargs="*",
        default=[sys.stdin],
        type=argparse.FileType("r"),
        help="files to read",
    )

    args = parser.parse_args()

    if args.dataset:
        args.files = []

    main(args)
