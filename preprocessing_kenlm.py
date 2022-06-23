#!/usr/bin/env python

import kenlm
import sys
import os
import nicer
import argparse

from multiprocessing import Pool
from itertools import repeat

from sent_tools import *

# remove all punctuation, lower alias
def clean_sent(line, keep_punct=False):
    _, sent = split_sentence_id(line)
    if keep_punct:
        tokens = [w.lower() if w not in ALIASES else w for w in tokenize(sent)]
    else:
        tokens = [w.lower() if w not in ALIASES else w for w in tokenize(sent) if w not in PUNCTUATION]
    
    return " ".join(tokens)

def main(args):
    for fd in args.files:
        with Pool(processes=args.cores) as p:
            for cleaned_sent in p.starmap(
                clean_sent,
                zip(
                fd.readlines(),
                repeat(args.keep_punct)
                ),
                250
            ):
                args.output.write(cleaned_sent+"\n")

        fd.close()

if __name__ == '__main__':
    nicer.make_nice()
    parser = argparse.ArgumentParser()

    parser.add_argument( "--files", "-f", nargs='*',type=argparse.FileType("r"),
                            help="List of txt files to read sentences from (for generating lm)")

    parser.add_argument( "--cores", "-c",
                            help="Number of cores to use", type=int, default=4)

    parser.add_argument( "--output", "-o", type=argparse.FileType("w"),
                            help="txt file to write results to")
    
    parser.add_argument( "--keep_punct", "-p", action="store_true",
                            help="keep punctuation?")

    args = parser.parse_args()
    main(args)