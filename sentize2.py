#!/usr/bin/env python

"""
Extracts proofs from .tex files.
"""

import argparse
import re
import sys

from nltk.tokenize import PunktSentenceTokenizer
from nltk.tokenize.destructive import NLTKWordTokenizer

# suspicious = re.compile("[&_^\x00-\x1f\x80-\xff]")

if __name__ == "__main__":
    for filename in sys.argv[1:]:
        with open(filename, "r") as fd:
            sent_tokenizer = PunktSentenceTokenizer()
            word_tokenizer = NLTKWordTokenizer()
            print("ok")
            for line in fd.readlines():
                # if re.search(suspicious, line):
                #     continue
                text = line.strip()
                sents = list(sent_tokenizer.tokenize(text))
                # Remove parentheses around parenthesized sentences
                for sent in sents:
                    if sent[0] == "(" and sent[-1] == ")":
                        interior = sent[1:-1]
                        if "(" not in interior and ")" not in interior:
                            sent = interior
                    words = word_tokenizer.tokenize(sent)
                    print(" ".join(words))
            # # Sort
            # sent.sort()
            # for s in sent:
            #     print(s)
