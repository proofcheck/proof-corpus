#!/usr/bin/env python

"""Split lines into sentences."""

import sys
from typing import List

from nltk.tokenize import PunktSentenceTokenizer
from nltk.tokenize.destructive import NLTKWordTokenizer

import nicer

# suspicious = re.compile("[&_^\x00-\x1f\x80-\xff]")

if __name__ == "__main__":
    nicer.make_nice()

    for filename in sys.argv[1:]:
        with open(filename, "r") as fd:
            sent_tokenizer = PunktSentenceTokenizer()
            word_tokenizer = NLTKWordTokenizer()
            for line in fd.readlines():
                # if re.search(suspicious, line):
                #     continue
                text = line.strip()
                sents: List[str] = list(sent_tokenizer.tokenize(text))
                # Remove parentheses around parenthesized sentences
                for sent in sents:
                    if sent[0] == "(" and sent[-1] == ")":
                        interior = sent[1:-1]
                        if "(" not in interior and ")" not in interior:
                            sent = interior
                    words = word_tokenizer.tokenize(sent)
                    print(" ".join(words))
