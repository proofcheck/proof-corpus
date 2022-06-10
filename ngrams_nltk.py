#!/usr/bin/env python
import argparse
import nicer
from multiprocessing import Pool
from itertools import repeat

import os
os.environ['OPENBLAS_NUM_THREADS'] = '1'

from nltk.util import ngrams
from nltk.probability import FreqDist

def results(output, dist):
    common_list = dist.most_common(10000)
    for ind, gram in enumerate(common_list):
        if ind%100 == 0:
            print("{}".format(ind))
        output.write(str(gram[0]) + '  ' + str(gram[1]))
        output.write("\n")
    output.write("\n")

def make_counter(words, n):
    fdist = FreqDist()
    for sent in words:
        ngrams_list = ngrams(sent, n)
        fdist.update(ngrams_list)
    return fdist

def read_one_sent(sent): 
    split_sentences = sent.split("\t")[-1].split()
    return split_sentences

def return_ngrams(sent, n):
    sents = read_one_sent(sent)
    grams = ngrams(sents, n)
    return grams

def update_dist(sent, n, dist):
    ngrams = return_ngrams(sent, n)
    for grams in ngrams:
        if grams in dist:
            dist[grams] += 1
        else:
            dist[grams] = 1

    return dist


def main(args): 
    dist = FreqDist()
    for fd in args.files:
        print(fd)
        with Pool(processes=args.cores) as p:
            for grams in p.starmap(
                        return_ngrams,
                        zip(
                            fd.readlines(), 
                            repeat(args.ngrams),
                            #repeat(dist),
                        ),
                        10000
                ):
                    dist.update(grams)
    results(args.output, dist)
    args.output.close()

if __name__ == '__main__':
    nicer.make_nice()
    parser = argparse.ArgumentParser()

    parser.add_argument("--files", "-f", nargs='*', type=argparse.FileType('r'),
                            help="txt file to read proof from")

    parser.add_argument("--ngrams", "-n", type=int, nargs='?', default=2,
                            help="specifies (n)grams")
    
    parser.add_argument("--output", "-o", type=argparse.FileType('w'),
                            help="txt file to write results to")

    parser.add_argument( "--cores", "-c",
                            help="Number of cores to use", type=int, default=4)

    args = parser.parse_args()

    main(args)
