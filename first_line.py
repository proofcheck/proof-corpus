#!/usr/bin/env python

import argparse
from collections import Counter
from concurrent.futures import process
import os, re, nicer

from multiprocessing import Pool

from nltk.tokenize.destructive import NLTKWordTokenizer
from nltk.probability import FreqDist

word_tokenizer = NLTKWordTokenizer()

def output(dist):
    ngrams_text = "\nTop 30 most frequent words at the beginning of the sentence\n"
    output.write(ngrams_text)
    for x in dist.most_common(30):
        output.write(str(x[0]) + '  ' + str(x[1]))
        output.write("\n")
    output.write("\n")

def merge(word_list):
    dist = FreqDist()
    for l in word_list:
        dist.update(l)
    return dist


def firstline(fname):
    f = open(fname, "r")
    sentences = f.readlines()
    first_words = []
    for sent in sentences:
        first_words += [word_tokenizer.tokenize(sent)[0]]
        
    return first_words

def main(args):
    if args.file:
        dist = merge([firstline(args.file)])
        

    else:
        with Pool(processes=args.cores) as p:
                    
                    word_list = p.starmap(
                        firstline,
                            zip(args.list),
                        1
                    )
                    dist = merge(word_list)
    output(dist)

if __name__ == '__main__':
    nicer.make_nice()
    parser = argparse.ArgumentParser()

    parser.add_argument("--file", "-f",
                            help="txt file to read proof from")

    parser.add_argument("--list", "-l", nargs='*',
                            help="list of txt files to read proof from")
    
    parser.add_argument("--output", "-o", type=argparse.FileType('w'),
                            help="txt file to write results to")

    parser.add_argument( "--cores", "-c",
                            help="Number of cores to use", type=int, default=4)

    args = parser.parse_args()

    main(args)

