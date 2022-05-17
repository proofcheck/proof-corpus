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

                # sents is the list of sentences in this single proofs.
                sents: List[str] = list(sent_tokenizer.tokenize(text))

                # sent_tokens is basically a copy of the list sents, but with
                # each sentence broken up into individual "words".
                sent_tokens: List[List[str]] = []

                # Loop throught the sentences, clean them slightly,
                # break them into words, and store them in sent_tokens.
                for sent in sents:
                    if sent[0] == "(":
                        if sent[-1] == ")":
                            interior = sent[1:-1]
                            if "(" not in interior and ")" not in interior:
                                sent = interior
                        elif sent[-2:] == ").":
                            interior = sent[1:-2]
                            if "(" not in interior and ")" not in interior:
                                sent = interior.strip() + " ."
                        elif sent[-3:] == ") .":
                            interior = sent[1:-3]
                            if "(" not in interior and ")" not in interior:
                                sent = interior.strip() + " ."
                    # If we have multiple sentences inside parentheses
                    # they will show up as (sent and sent)
                    # This should fix that
                    if sent[0] == "(":
                        if sent.count("(") - 1 == sent.count(")"):
                            sent = sent[1:]
                    elif sent[-1] == ")":
                        if sent.count("(") + 1 == sent.count(")"):
                            sent = sent[:-1]


                    words: List[str] = word_tokenizer.tokenize(sent)

                    # So, the NLTK tokenizer spents sentences too eagerly in
                    # phrases like "there are no r.v.'s in the range, ..."
                    # giving us "there are no r.v." and "'s in the range..."
                    #
                    # Look for these sorts of splits and un-merge them.
                    if not words:
                        continue
                    if words[0] == "'s" and sent_tokens:
                        sent_tokens[-1] = (
                            sent_tokens[-1][:-1]
                            + [sent_tokens[-1][-1] + words[0]]
                            + words[1:]
                        )
                    



                    else:
                        sent_tokens += [words]
                for tokens in sent_tokens:
                    print(" ".join(tokens))
