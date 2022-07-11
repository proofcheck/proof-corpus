#!/usr/bin/env python

import os

os.environ["OPENBLAS_NUM_THREADS"] = "1"

import argparse
import nicer
import gc
from multiprocessing import Pool
from itertools import repeat

from nltk.util import ngrams
from nltk.probability import FreqDist

from sent_tools import *

# Writes ngrams
# Input : sent**.tsv, number of max ngrams

def my_ngrams(sent, n):
    zip_list = []
    # Create list of lists to zip for creating ngrams
    for i in range(n):
        if i == n - 1:
            zip_list += [sent[i:]]
        else:
            zip_list += [sent[i : i - n + 1]]
    ngram_list = zip(*zip_list)
    return ngram_list

def results(f, dist):
    with open(f, "w") as output:
        sorted_keys = sorted(dist.keys(), key=lambda x: dist[x], reverse=True)
        for ind, key in enumerate(sorted_keys):
            if ind % 100 == 0:
                print("{}".format(ind))

            freq = dist[key]

            if freq > 10:
                grams = " ".join(key)
                output.write(str(freq) + "\t" + grams + "\n")

            else:
                break


def return_ngrams(sent, n):
    # Creates ngrams from a sentence (list)
    # Input : sentence (list)

    # Don't use nltk ngrams (Memory Error!)
    # grams = ngrams(sent, n)
    grams = my_ngrams(sent, n)
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


def process_for_grams(s):
    tokenized = split_sentence_id_tokenized(s)[1]
    return [w.lower() if w not in ALIASES else w for w in tokenized]

def write_ngrams(sentences, n, extension=""):
    dist = FreqDist()
    for sent in sentences:
        grams = return_ngrams(sent, n)
        dist.update(grams)

    output = "ngrams/" + str(n) + "grams_" + extension + ".txt"
    results(output, dist)


def main(args):
    sentences = []
    for fd in args.files:
        for line in fd.readlines():
            sentences.extend([process_for_grams(line)])

        # print("done", fd)
        fd.close()

    for n in range(args.start, args.stop + 1):
        dist = FreqDist()

        for sent in sentences:
            grams = return_ngrams(sent, n)
            dist.update(grams)

        output = "ngrams/" + str(n) + "grams_" + args.extension + ".txt"
        results(output, dist)
        del dist
        gc.collect()

    # with Pool(processes=args.cores) as p:
    #     p.starmap(
    #         write_ngrams,
    #         zip(
    #             repeat(sentences),
    #             list(range(args.start, args.stop+1)),
    #             repeat(args.extension)
    #         ),
    #         1
    #     )

if __name__ == "__main__":
    nicer.make_nice()
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--files",
        "-f",
        nargs="*",
        type=argparse.FileType("r"),
        help="txt file to read proof from",
    )

    parser.add_argument(
        "--start", type=int, nargs="?", default=2, help="min number of ngrams"
    )

    parser.add_argument(
        "--stop", type=int, nargs="?", default=2, help="max number of ngrams"
    )

    parser.add_argument("--extension", "-e", help="extension for file name")

    args = parser.parse_args()

    main(args)
