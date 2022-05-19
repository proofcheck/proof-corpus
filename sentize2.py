#!/usr/bin/env python

"""Split lines into sentences."""

import argparse
import sys
from typing import List

from nltk.tokenize import PunktSentenceTokenizer
from nltk.tokenize.destructive import NLTKWordTokenizer

import nicer

# suspicious = re.compile("[&_^\x00-\x1f\x80-\xff]")
def inner_parens(s):
    d = {"(": 1, ")": -1}
    tot = 0
    for x in s:
        if x in d.keys():
            tot += d[x]
        if tot < 0:
            return False
    return True


# collected by running
#   grep '[a-z]\.[a-z] \.$' all-sentences.txt
# but perhaps better would be
#   egrep -oh '\b([A-Za-z]+\.)+[a-z]+\.\ ' proofs*.raw | sort | uniq | tee abbrevs.txt
MATH_ABBREVS = set(
    [
        "a.a",
        "a.c.i.m",
        "a.c",
        "a.e",
        "a.k.a",
        "a.m.s",
        "a.m",
        "a.s",
        "a.u",
        "al",
        "b.c.i",
        "c.a.i",
        "c.b",
        "c.c.c.t",
        "c.c",
        "c.d.f",
        "c.e",
        "c.f",
        "c.i",
        "c.p.c",
        "c.p",
        "c.u.c",
        "c.u.p",
        "d.g",
        "d.o.f",
        "d.t.s",
        "dr",
        "e.g",
        "et",  # not really, but it's a very common mistake.
        "f.e",
        "f.g.p.m",
        "f.g",
        "g.c.d",
        "g.l.n",
        "g.l.s",
        "i.e",
        "i.h",
        "i.i.d.r.v",
        "i.i.d",
        "i.o",
        "I.T.",
        "i.u.r",
        "inc",
        "l.c.a.i",
        "l.c.m",
        "l.c",
        "l.h.s",
        "L.H.S",
        "l.m.g.f",
        "l.o.t",
        "l.s.c",
        "m.p",
        "mr",
        "mrs",
        "n.b",
        "N.B",
        "n.c",
        "o.d.e",
        "O.D.E",
        "p.h",
        "p.h",
        "p.l",
        "p.m",
        "p.o",
        "p.s.h",
        "p.s.h",
        "prof",
        "q.c.i",
        "q.c",
        "q.e",
        "q.p",
        "q.s",
        "q.v",
        "r.c.a.i",
        "r.e",
        "r.h.s",
        "R.H.S",
        "r.l.s.c",
        "r.r.v",
        "r.v",
        "s.m.u",
        "u.c.p",
        "u.e",
        "u.i",
        "u.s.c",
        "vs",
        "w.h.e",
        "w.h.p",
        "w.l.o.g",
        "w.p",
        "w.r.t",
        "w.r",
    ]
)

if __name__ == "__main__":
    nicer.make_nice()

    parser = argparse.ArgumentParser()
    # parser.add_argument(
    #     "-d", "--debug", help="Show tracing output", action="store_true"
    # )
    parser.add_argument(
        "files", nargs="*", type=argparse.FileType("r"), default=[sys.stdin]
    )
    args = parser.parse_args()

    for fd in args.files:
        sent_tokenizer = PunktSentenceTokenizer()
        sent_tokenizer._params.abbrev_types = MATH_ABBREVS

        word_tokenizer = NLTKWordTokenizer()
        for line in fd.readlines():
            # if re.search(suspicious, line):
            #     continue
            text: str = line.strip()

            if "\t" in text:
                (prefix, text) = text.split("\t")
                prefix += "\t"
            else:
                (prefix, text) = ("", text)

            # sents is the list of sentences in this single proofs.
            sents: List[str] = list(sent_tokenizer.tokenize(text))

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

                print(prefix + " ".join(words))
