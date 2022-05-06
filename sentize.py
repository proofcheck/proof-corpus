#!/usr/bin/env python

"""
Extracts proofs from .tex files.
"""

import argparse
from nltk.tokenize import PunktSentenceTokenizer, sent_tokenize
from nltk.tokenize.destructive import NLTKWordTokenizer
import re
import sys

suspicious = re.compile("[&_^\x00-\x1f\x80-\xff]")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--train", help="Punkt training input", type=str)
    parser.add_argument("files", nargs="+")
    args = parser.parse_args()

    if args.train:
        sys.stderr.write(f"training on {args.train}\n")
        with open(args.train, "r") as fd:
            training_text = fd.read()
            sent_tokenizer = PunktSentenceTokenizer(training_text)
    else:
        sys.stderr.write(f"Using default training\n")
        sent_tokenizer = PunktSentenceTokenizer()

    word_tokenizer = NLTKWordTokenizer()

    for filename in args.files:
        sys.stderr.write(f"tokenizing {filename}\n")
        sys.stderr.flush()
        with open(filename, "r") as fd:
            for line in fd:
                line = line.strip()

                if not line:
                    # Empty line
                    continue

                if re.search(suspicious, line):
                    # TeX extraction failed.
                    continue

                sents = sent_tokenizer.tokenize(line)
                for sent in sents:

                    lefts = sent.count("(")
                    rights = sent.count(")")

                    if lefts != rights:
                        #  Suspicious: unbalanced parentheses.
                        continue

                    if (
                        lefts == 1
                        and rights == 1
                        and sent[0] == "("
                        and sent[-1] == ")"
                    ):
                        # Remove parentheses around parenthesized sentences
                        sent = sent[1:-1]

                    if not sent:
                        continue

                    if sent[0] < "A" or sent[0] > "Z":
                        continue

                    words = word_tokenizer.tokenize(sent)
                    print(" ".join(words))
