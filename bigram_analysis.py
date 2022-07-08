#!/usr/bin/env python

import os
os.environ["OPENBLAS_NUM_THREADS"] = "1"

import pickle
import argparse
import sys
import nicer
import math
import gc

from multiprocessing import Pool
from itertools import repeat
from collections import Counter
from scipy.stats.contingency import chi2_contingency
from scipy.stats import chi2

from ngrams import return_ngrams
from sent_tools import *

# remove all punctuation, lower alias
def clean_sent(line, keep_punct=False):
    _, sent = split_sentence_id(line)
    if keep_punct:
        tokens = [w.lower() if w not in ALIASES else w for w in tokenize(sent)]
    else:
        tokens = [w.lower() if w not in ALIASES else w for w in tokenize(sent) if w not in PUNCTUATION]
    
    return " ".join(tokens)

def save_ngrams(files, output, n):
    sentences = []
    for fd in files:
        for line in fd.readlines():
            sentences.extend([  tokenize(clean_sent(line))  ])
        print("done", fd)
        fd.close()

    ngrams = []
    len_sent = len(sentences)
    for ind, sent in enumerate(sentences):
        if ind % 1000000 == 0:
            print("Percent done: {}%".format(round(ind/len_sent*100, 2)))
        ngram = list(return_ngrams(sent, n))
        if ngram is not []:
            ngrams.extend(ngram)

    print("dumping")
    with open(output, "wb") as resource:
        pickle.dump(ngrams, resource)

    unigrams = [word for sent in sentences for word in sent]

    return ngrams, unigrams

def pointwise_mutual_information(ngram, ngram_cnt, unigram_cnt):
    p_ngram = get_ngram_probability(ngram_cnt, ngram)
    p_unigram_product = get_unigram_probability_product(unigram_cnt, ngram)
    return math.log(p_ngram/p_unigram_product, 2)

def get_ngram_probability(dist, ngrams):
    return dist[ngrams] / sum(dist.values())

def get_unigram_probability_product(unigram_cnt, ngram):
    probability = 1
    for unigram in ngram:
        probability *= get_ngram_probability(unigram_cnt, unigram)
    return probability

def bigram_with_mi(ngram, ngram_cnt, unigram_cnt):
    return ngram, pointwise_mutual_information(ngram, ngram_cnt, unigram_cnt)

def chi_squared_bigram(ngram, ngram_cnt, unigram_cnt=None):
    obs =   [
                [   ngram_cnt[ngram],                        get_ngrams_not_second(ngram, ngram_cnt)          ],
                [   get_ngrams_not_first(ngram, ngram_cnt),  get_ngrams_not_first_or_second(ngram, ngram_cnt) ]
            ]

    chi2float, p, dof, expectedndarray = chi2_contingency(obs)
    return chi2float

def get_ngrams_not_first(ngram, ngram_cnt):
    count = 0
    for key in ngram_cnt.keys():
        if key[0] is not ngram[0] and key[1] is ngram[1]:
            count += ngram_cnt[key]
    return count

def get_ngrams_not_second(ngram, ngram_cnt):
    count = 0
    for key in ngram_cnt.keys():
        if key[0] is ngram[0] and key[1] is not ngram[1]:
            count += ngram_cnt[key]
    return count

def get_ngrams_not_first_or_second(ngram, ngram_cnt):
    count = 0
    for key in ngram_cnt.keys():
        if key[0] is not ngram[0] and key[1] is not ngram[1]:
            count += ngram_cnt[key]
    return count

def compare_critical(chi, dof, confidence_level):
    critical = chi2.ppf(confidence_level, dof)
    if abs(chi) >= critical:
        return True
    else:
        return False

def bigram_with_chi_squared(ngram, ngram_cnt, unigram_cnt):
    return ngram, chi_squared_bigram(ngram, ngram_cnt, unigram_cnt)

def make_ngram_cnt(ngrams):
    cnt = Counter()
    for ngram in ngrams:
        cnt[ngram] += 1
    return cnt

def main(args):
    if args.files:
        ngrams, unigrams = save_ngrams(args.files, args.ngram_file, args.n)

    else:
        with open(args.ngram_file, "rb") as resource:
            print("loading ngrams")
            ngrams = pickle.load(resource)
            print("done loading ngrams")
        
        unigrams = [ngram[0] for ngram in ngrams]
            
    ngram_cnt = make_ngram_cnt(ngrams)
    del ngrams
    gc.collect()
    
    unigram_cnt = Counter(unigrams)
    del unigrams
    gc.collect()
    
    print("frequency")
    frequency_filtered = [ngram for ngram in ngram_cnt.keys() if ngram_cnt[ngram] > 100]
    
    print("MI")
    # mi_dict = {ngram : pointwise_mutual_information(ngram, ngram_cnt, unigram_cnt) for ngram in frequency_filtered}
    
    with Pool(processes=args.cores) as p:
        mi_dict = {}
        for ngram, mi_val in p.starmap(
                    bigram_with_mi,
                    zip(
                        frequency_filtered,
                        repeat(ngram_cnt),
                        repeat(unigram_cnt),
                    ),
                    50
                ):
            mi_dict[ngram] = mi_val

    del frequency_filtered
    gc.collect()
    mi_filtered = [ngram for ngram in mi_dict.keys() if mi_dict[ngram] > 5]

    print("chi")
    # chi_dict = {ngram : chi_squared_bigram(ngram, ngram_cnt, unigram_cnt) for ngram in mi_filtered}

    with Pool(processes=args.cores) as p:
        chi_dict = {}
        for ngram, chi_val in p.starmap(
                    bigram_with_chi_squared,
                    zip(
                        mi_filtered,
                        repeat(ngram_cnt),
                        repeat(unigram_cnt),
                    ),
                    50
                ):
            chi_dict[ngram] = chi_val

    del mi_filtered
    gc.collect()


    print("done making dict")
    chi_filtered = [ngram for ngram in chi_dict.keys() if compare_critical(chi_dict[ngram], 1, 0.95)]

    print("done calculating")
    for ngram in chi_filtered:
        ngram_string = " ".join(ngram)
        args.output.write(ngram_string + "\t" 
                            + str(ngram_cnt[ngram]) + "\t" 
                            + str(mi_dict[ngram]) + "\t" 
                            + str(chi_dict[ngram]) + "\n")
    args.output.close()

if __name__ == "__main__":
    nicer.make_nice()
    parser = argparse.ArgumentParser()

    parser.add_argument("--files", "-f", nargs="*", type=argparse.FileType("r"),
                        help="txt file to read proof from")

    parser.add_argument("--ngram_file", "-nf",
                        help="pk file to read/write ngrams")
    
    parser.add_argument("--n", "-n", type=int, default=2,
                        help="value of n for ngrams")

    parser.add_argument("--output", "-o", default=sys.stdout, type=argparse.FileType("w"),
                        help="file to write results to")

    parser.add_argument("--cores", "-c", type=int, default=4,
                        help="Number of cores to use")

    args = parser.parse_args()

    main(args)


    