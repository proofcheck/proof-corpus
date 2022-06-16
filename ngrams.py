#!/usr/bin/env python
import argparse

import nicer
from multiprocessing import Pool
from itertools import repeat

from nltk.util import ngrams
from nltk.probability import FreqDist

from sent_tools import *

# Writes top 10000 ngrams using nltk
# Input : sent**.tsv, number of max ngrams

def results(f, dist):
    # Writes top 10000 ngrams in file
    with open(f, "w") as output:
        common_list = dist.most_common(10000)
        for ind, gram in enumerate(common_list):
            if ind%100 == 0:
                print("{}".format(ind))
            output.write(str(gram[0]) + '\t' + str(gram[1]) + '\n')

def return_ngrams(sent, n):
    # Creates ngrams from a sentence (list)
    # Input : sentence (list)
    grams = ngrams(sent, n)
    return grams

def update_dist(sent, n, dist):
    # Updates ngram distribution
    # Input : sentence (string), n, distribution
    ngrams = return_ngrams(sent, n)
    for grams in ngrams:
        if grams in dist:
            dist[grams] += 1
        else:
            dist[grams] = 1

    return dist

def main(args): 
    ids, sents = read_files_tokenized(args.files, args.cores)

    for n in range(1, args.ngrams+1):
        dist = FreqDist()
        with Pool(processes=args.cores) as p:
            for grams in p.starmap(
                        return_ngrams,
                        zip(
                            sents, 
                            repeat(n),
                        ),
                        250
                ):
                    dist.update(grams)
        output = "ngrams/" + str(n) + "grams_top_10000_" + args.extension + ".txt"
        results(output, dist)

if __name__ == '__main__':
    nicer.make_nice()
    parser = argparse.ArgumentParser()

    parser.add_argument("--files", "-f", nargs='*', type=argparse.FileType('r'),
                            help="txt file to read proof from")

    parser.add_argument("--ngrams", "-n", type=int, nargs='?', default=2,
                            help="max number of ngrams")
    
    parser.add_argument("--extension", "-e",
                            help="extension for file name")

    parser.add_argument( "--cores", "-c",
                            help="Number of cores to use", type=int, default=4)

    args = parser.parse_args()

    main(args)
