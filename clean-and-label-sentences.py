#!/usr/bin/env python

"""
Combines all the .txt files in a directory into labeled sections.

Finds all the .txt files in a directory tree, applies cleanup, and splits
   into sentences. Output is labeled so that "bad" sentences can be easily
   traced back to their source.
"""

# E.g.,
#    ./clean-and-label-sentences proofs > labeled-sentences.txt

import sys
from pathlib import Path
from typing import List

from nltk.tokenize import PunktSentenceTokenizer
from nltk.tokenize.destructive import NLTKWordTokenizer

import cleanup
import nicer

# suspicious = re.compile("[&_^\x00-\x1f\x80-\xff]")

if __name__ == "__main__":
    nicer.make_nice()
    sent_tokenizer = PunktSentenceTokenizer()
    word_tokenizer = NLTKWordTokenizer()

    dirs = sys.argv[1:] if len(sys.argv) >= 2 else ["proofs"]
    for dir in dirs:
        for filepath in Path(dir).rglob("*.txt"):
            with open(filepath, "r") as fd:
                for line in fd.readlines():
                    # if re.search(suspicious, line):
                    #     continue
                    text = line.strip()
                    text = cleanup.clean_proof(text)
                    sents: List[str] = list(sent_tokenizer.tokenize(text))
                    # Remove parentheses around parenthesized sentences
                    for sent in sents:
                        if sent[0] == "(" and sent[-1] == ")":
                            interior = sent[1:-1]
                            if "(" not in interior and ")" not in interior:
                                sent = interior
                        words = word_tokenizer.tokenize(sent)
                        print(
                            str(Path(*filepath.parts[-3:-1]))
                            + "\t"
                            + " ".join(words)
                        )
