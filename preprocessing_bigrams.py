#!/usr/bin/env python

"""Preprocess sentences for bigram analysis."""

import argparse
import nicer

from multiprocessing import Pool
from itertools import repeat

from sent_tools import *

"""
Input :
    --files : tsv files of sentences
    (other arguments)

Output :
    txt files of preprocessed sentences (in preprocessed_sents/)

    File name is automatically formatted using input file name.
        fname = PATH + fd.name.split("/")[-1].split(".")[0] + "_" + args.extension + ".txt"
"""

"""
Typical usage :
    nohup python3 preprocessing_bigrams.py -f ../../stone/proof-corpus/sent*.tsv -c 25 -e
"""

PATH = "preprocessed_sents/"

def clean_sent(line, keep_punct=False, add_spacing=False):
    # Lower everything but aliases
    _, sent = split_sentence_id(line)
    alias_list = list(ALIASES)

    if keep_punct:
        tokens = [w.lower() if not check_alias(w, alias_list) else clean_word(w, alias_list) for w in tokenize(sent)]
    
    else:
        tokens = [w.lower() if not check_alias(w, alias_list) else clean_word(w, alias_list) for w in tokenize(sent) if w not in PUNCTUATION]

    if add_spacing:
        tokens = [""] + tokens + [""]

    return " ".join(tokens)

def clean_word_naive(word, alias_list):
    # Clean word naively
    lcword = word.lower()
    for alias in alias_list:
        if alias in word:
            lcword = lcword.replace(alias.lower(), alias)
    return lcword

def clean_word(word, alias_list):
    # Clean word (find indices of aliases, then lower)
    lower_list = list(word.lower())
    indices = []
    for alias in alias_list:
        current = word
        i = current.find(alias)
        while i != -1:
            indices += [(alias, i)]
            if i + len(alias) >= len(word):
                break
            i = word.find(alias, i+1) 

    for alias, ind in indices:
        lower_list[ind:ind+len(alias)] = list(alias)
    
    return "".join(lower_list)

def check_alias(word, alias_list):
    # Check if word contains an alias
    for alias in alias_list:
        if alias in word:
            return True
    
    return False

def main(args):
    for fd in args.files:
        with Pool(processes=args.cores) as p:
            cleaned = p.starmap(
                clean_sent,
                    zip(
                        fd.readlines(),
                        repeat(False),
                        repeat(True),
                        ),
                    50
                )

            if args.extension:
                fname = PATH + fd.name.split("/")[-1].split(".")[0] + "_" + args.extension + ".txt"
            else:
                fname = PATH + fd.name.split("/")[-1].split(".")[0] + ".txt"

            with open(fname, "w") as o:
                lines = "\n".join(cleaned)
                o.write(lines)
                
        print(fd, "done", flush=True)


if __name__ == "__main__":
    nicer.make_nice()
    parser = argparse.ArgumentParser()

    parser.add_argument("--files", "-f", nargs="*", type=argparse.FileType("r"),
                        help="txt file to read sents from")

    parser.add_argument("--cores", "-c", type=int, default=4,
                        help="number of cores")

    parser.add_argument("--extension", "-e",
                        help="file extension")

    args = parser.parse_args()

    main(args)
