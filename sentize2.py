#!/usr/bin/env python

"""Split lines into sentences."""

import sys
from typing import List

from nltk.tokenize import PunktSentenceTokenizer
from nltk.tokenize.destructive import NLTKWordTokenizer

import nicer

# suspicious = re.compile("[&_^\x00-\x1f\x80-\xff]")
def inner_parens(s):
    d = {'(':1, ')':-1}
    tot = 0
    for x in s:
        if x in d.keys():
            tot += d[x]
        if tot < 0:
            return False
    return True

if __name__ == "__main__":
    nicer.make_nice()

    for filename in sys.argv[1:]:
        with open(filename, "r") as fd:
            sent_tokenizer = PunktSentenceTokenizer()
            sent_tokenizer._params.abbrev_types = set(["dr", "vs", "mr", "mrs", "prof", "inc",
            "i.e", "e.g", "al", "a.m", "p.m",
            "c.p", "c.p.c", "u.c.p", "a.e", "a.s",
            "o.d.e", "l.h.s", "r.h.s", "O.D.E", "L.H.S", "R.H.S", "l.c.m", "g.c.d",
            "p.h", "q.e", "r.c.a.i", "f.e", "c.b", "c.c", "c.u.p", "r.e", "d.g", "i.i.d",
            "n.b", "N.B", "f.g", "i.h", "s.m.u", "c.i", "I.T."
            ])

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
                            if inner_parens(interior):
                                sent = interior
                        elif sent[-2:] == ").":
                            interior = sent[1:-2]
                            if inner_parens(interior):
                                sent = interior.strip() + " ."
                        elif sent[-3:] == ") .":
                            interior = sent[1:-3]
                            if inner_parens(interior):
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


