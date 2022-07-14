#!/usr/bin/env python

import argparse
import nicer

from multiprocessing import Pool
from itertools import repeat

from sent_tools import *

PATH = "preprocessed_sents/"

def clean_sent(line, keep_punct=False, add_spacing=False):
    _, sent = split_sentence_id(line)
    alias_list = list(ALIASES)

    if keep_punct:
        # tokens = [w.lower() if not check_alias(w, alias_list) else w for w in tokenize(sent)]
        tokens = [w.lower() if not check_alias(w, alias_list) else clean_word(w, alias_list) for w in tokenize(sent)]
    
    else:
        # tokens = [w.lower() if not check_alias(w, alias_list) else w for w in tokenize(sent) if w not in PUNCTUATION]
        tokens = [w.lower() if not check_alias(w, alias_list) else clean_word(w, alias_list) for w in tokenize(sent) if w not in PUNCTUATION]

    if add_spacing:
        tokens = [""] + tokens + [""]

    return " ".join(tokens)

def clean_word_naive(word, alias_list):
    lcword = word.lower()
    for alias in alias_list:
        if alias in word:
            lcword = lcword.replace(alias.lower(), alias)
    return lcword

def clean_word(word, alias_list):
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
                fname = PATH + fd.name.split("/")[-1].split(".")[0] + "_" + args.extension + ".txt"

            with open(fname, "w") as o:
                lines = "\n".join(cleaned)
                o.write(lines)


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
