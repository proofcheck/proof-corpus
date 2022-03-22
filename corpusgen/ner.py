#!/usr/bin/env python

"""Replaces people's names with NAME."""

import argparse

# import spacy

# def ner(proof):
#     nlp = spacy.load("en_core_web_sm")
#     doc = nlp(proof)

#     for ent in doc.ents:
#         if ent.text != "MATH":
#             print(ent.text, ent.start_char, ent.end_char, ent.label_)

known_words = set()
with open("/Users/stone/Downloads/words_alpha.txt") as fd:
    for word in fd.readlines():
        word = word.strip()
        known_words.add(word)


def ner(proof):
    answer = []
    for w in proof.split():
        if w[0].isupper() and not w.startswith("MATH"):
            w2 = w.strip("\n\t ,.-?!.:`'\"[]()")
            if w2.lower() not in known_words:
                print(w2)
                if w2.endswith("'s"):
                    answer.append("NAME 's")
                else:
                    answer.append("NAME")
                continue
        answer.append(w)
    return " ".join(answer)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-d", "--debug", help="Show tracing output", action="store_true"
    )
    parser.add_argument("file")
    args = parser.parse_args()

    with open(args.file) as f:
        for orig in f.readlines():
            clean = ner(orig)
            if args.debug:
                print(orig)
                print(clean)
                print()
            else:
                print(clean)
