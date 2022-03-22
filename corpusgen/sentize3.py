#!/usr/bin/env python

"""Extracts sentences from lines of text."""

import re
import sys

import spacy

if __name__ == "__main__":
    nlp = spacy.load("en_core_web_sm")
    for filename in sys.argv[1:]:
        with open(filename, "r") as fd:
            for line in fd.readlines():
                text = line.strip()
                doc = nlp(text)
                for sentence in doc.sents:
                    sent = sentence.text
                    if sent[0] == "(" and sent[-1] == ")":
                        interior = sent[1:-1]
                        if "(" not in interior and ")" not in interior:
                            sent = interior
                    if sent[0] == "(" and sent[-2:] == ").":
                        interior = sent[1:-2]
                        if "(" not in interior and ")" not in interior:
                            sent = interior + "."
                    # words = word_tokenizer.tokenize(sent)
                    # print(" ".join(words))
                    print(sent)
            # # Sort
            # sent.sort()
            # for s in sent:
            #     print(s)
