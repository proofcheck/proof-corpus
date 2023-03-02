#!/usr/bin/env python

"""Makes bigrams from preprocessed sent file, dumps them, and writes the bigrams that pass the metrics (frequency, MI, chi-squared) with their scores."""

import os
os.environ['OPENBLAS_NUM_THREADS'] = '1'

import pickle
import argparse
import sys
import nicer
import math
import gc

from collections import Counter
from scipy.stats.contingency import chi2_contingency
from scipy.stats import chi2

from ngrams import return_ngrams
from sent_tools import *

"""
Inputs :
    --files : preprocessed (punctuation removed, sents separated by \n) files (in preprocessed_sents/) to make bigrams from (unnecessary if using dumped bigrams)
    --bigram_file : file to dump/load bigrams (in bigrams/)
    (other arguments)

Output :
    --output : txt file of results, formatted as follows:
                    w1 w2\tfrequency\tMI\tchi-squared
                if (w1 w2) pass the threshold.
                (in bigram_analysis/)
"""

"""
Typical usage :
    python3 bigram_analysis.py -f merged_sents/*.txt -bf bigrams/merged_7_14.pk -o bigram_analysis/bigram_analysis_merged_7_14.txt -F 500

Use dumped bigrams :
    python3 bigram_analysis.py -bf bigrams/sent00/bigrams_sent00.pk -o bigram_analysis/sent00/bigram_analysis_sent00_all.txt

Don't filter (return results for all bigrams) :
    python3 bigram_analysis.py -bf bigrams/sent00/bigrams_sent00.pk -o bigram_analysis/sent00/bigram_analysis_sent00_all.txt -A
"""

FRENCH_BIGRAM_PATH = "french/bigrams/"
FRENCH_ANALYSIS_PATH = "french/bigram_analysis/"

def save_bigrams_sents(files, output):
    sentences = []
    for fd in files:
        for line in fd.readlines():
            tokens = tokenize(line.strip())
            sentences.extend([tokens])
        print("done", fd, flush=True)
        fd.close()

    bigrams = []
    len_sent = len(sentences)

    for ind, sent in enumerate(sentences):
        if ind % 1000000 == 0:
            print("Percent done: {}%".format(round(ind/len_sent*100, 2)), flush=True)
        
        sent_bigrams = list(return_ngrams(sent, 2))
        if sent_bigrams is not []:
            bigrams.extend([sent_bigrams])

    del sentences
    gc.collect()

    print("dumping", flush=True)
    with open(output, "wb") as resource:
        pickle.dump(bigrams, resource)

    return bigrams

def pointwise_mutual_information(bigram, bigram_cnt, unigram_cnt, bigram_sum=None, unigram_sum=None):
    if not bigram_sum:
        bigram_sum = sum(bigram_cnt.values())

    if not unigram_sum:
        unigram_sum = sum(unigram_cnt.values())

    p_bigram = get_bigram_probability(bigram_cnt, bigram, bigram_sum)
    p_unigram_product = get_unigram_probability_product(unigram_cnt, bigram, unigram_sum)
    
    return math.log(p_bigram/p_unigram_product, 2)

def get_bigram_probability(cnt, bigram, cnt_sum):
    return cnt[bigram] / cnt_sum

def get_unigram_probability_product(unigram_cnt, bigram, unigram_sum):
    probability = 1
    for unigram in bigram:
        probability *= get_bigram_probability(unigram_cnt, unigram, unigram_sum)
    return probability

def bigram_with_mi(bigram, bigram_cnt, unigram_cnt):
    return bigram, pointwise_mutual_information(bigram, bigram_cnt, unigram_cnt)

def chi_squared_bigram(bigram, bigram_cnt, unigram_cnt=None, bigram_sum=None):
    if not bigram_sum or not unigram_cnt:
        obs =   [
                    [   bigram_cnt[bigram],                        get_bigrams_not_second(bigram, bigram_cnt)          ],
                    [   get_bigrams_not_first(bigram, bigram_cnt),  get_bigrams_not_first_or_second(bigram, bigram_cnt) ]
                ]
    
    else:
        w1_w2 = bigram_cnt[bigram]
        w1_notw2 = unigram_cnt[bigram[0]] - w1_w2
        notw1_w2 = unigram_cnt[bigram[1]] - w1_w2

        obs =   [
                    [   w1_w2   ,  w1_notw2                                      ],
                    [   notw1_w2,  bigram_sum - w1_w2 - w1_notw2 - notw1_w2      ]
                ]

    chi2float, _, _, _ = chi2_contingency(obs)
    return chi2float

def get_bigrams_not_first(bigram, bigram_cnt):
    count = 0
    for key in bigram_cnt.keys():
        if key[0] is not bigram[0] and key[1] is bigram[1]:
            count += bigram_cnt[key]
    return count

def get_bigrams_not_second(bigram, bigram_cnt):
    count = 0
    for key in bigram_cnt.keys():
        if key[0] is bigram[0] and key[1] is not bigram[1]:
            count += bigram_cnt[key]
    return count

def get_bigrams_not_first_or_second(bigram, bigram_cnt):
    count = 0
    for key in bigram_cnt.keys():
        if key[0] is not bigram[0] and key[1] is not bigram[1]:
            count += bigram_cnt[key]
    return count

def compare_critical(chi, dof, confidence_level):
    critical = chi2.ppf(confidence_level, dof)
    if abs(chi) >= critical:
        return True
    else:
        return False

def bigram_with_chi_squared(bigram, bigram_cnt, unigram_cnt):
    return bigram, chi_squared_bigram(bigram, bigram_cnt, unigram_cnt)

def make_bigram_cnt(bigrams, freq_threshold=None):
    cnt = Counter(bigrams)

    if freq_threshold:
        keys = list(cnt.keys())
        for key in keys:
            if cnt[key] < freq_threshold:
                del cnt[key]
    return cnt

def make_unigram_cnt(unigrams, bigram_cnt):
    freq_unigrams = set([uni for bigram in bigram_cnt.keys() for uni in bigram])
    unigram_cnt = Counter([unigram for unigram in unigrams if unigram in freq_unigrams])
    return unigram_cnt

def make_unigrams_from_bigrams_sents(sents):
    unigrams = []
    for sent in sents:
        length = len(sent)
        for ind, bigram in enumerate(sent):
            unigrams.append(bigram[0])
            if ind == length - 1:
                unigrams.append(bigram[1])

    return unigrams

def main(args):
    if args.files:
        bigrams_sents = save_bigrams_sents(args.files, args.bigram_file)
        print("done dumping", flush=True)
        gc.collect()

    else:
        print("loading bigrams", flush=True)
        with open(args.bigram_file, "rb") as resource:
            bigrams_sents = pickle.load(resource)
            print("done loading bigrams", flush=True)
    
    print("making unigrams", flush=True)
    unigrams = make_unigrams_from_bigrams_sents(bigrams_sents)

    print("frequency", flush=True)
    sent_count = len(bigrams_sents)

    bigrams = [bigram for sent in bigrams_sents for bigram in sent]
    del bigrams_sents
    gc.collect()

    bigram_sum = len(bigrams)
    unigram_sum = len(unigrams)

    if args.all:
        bigram_cnt = make_bigram_cnt(bigrams)
    
    else:
        bigram_cnt = make_bigram_cnt(bigrams, args.frequency)

    del bigrams
    gc.collect()

    print("making unigram counter", flush=True)
    # unigram_cnt = make_unigram_cnt(unigrams, bigram_cnt)
    unigram_cnt = Counter(unigrams)
    del unigrams
    gc.collect()

    print("MI", flush=True)
    mi_dict = {bigram : pointwise_mutual_information(bigram, bigram_cnt, unigram_cnt, bigram_sum, unigram_sum) for bigram in bigram_cnt.keys()}
    
    # args.cores = min(args.cores, 15)

    # with Pool(processes=args.cores) as p:
    #     mi_dict = {}
    #     mi_dict.update(
    #               p.starmap(
    #                     bigram_with_mi,
    #                     zip(
    #                         bigram_cnt.keys(),
    #                         repeat(bigram_cnt),
    #                         repeat(unigram_cnt),
    #                     ),
    #                    25
    #                 )
    #               )

    if args.all:
        mi_filtered = [bigram for bigram in mi_dict.keys()]
    else:
        mi_filtered = [bigram for bigram in mi_dict.keys() if mi_dict[bigram] > args.mi]

    print("chi", flush=True)
    bigram_sum = bigram_sum + 2 * sent_count
    chi_dict = {bigram : chi_squared_bigram(bigram, bigram_cnt, unigram_cnt, bigram_sum) for bigram in mi_filtered}

    # with Pool(processes=args.cores) as p:
    #     chi_dict = {}
    #     chi_dict.update(
    #               p.starmap(
    #                 bigram_with_chi_squared,
    #                 zip(
    #                     mi_filtered,
    #                     repeat(bigram_cnt),
    #                     repeat(unigram_cnt),
    #                 ),
    #                 25
    #               )
    #       )

    del mi_filtered
    gc.collect()

    print("done making dict", flush=True)
    if args.all:
        chi_filtered = [bigram for bigram in chi_dict.keys()]
    else:
        chi_filtered = [bigram for bigram in chi_dict.keys() if compare_critical(chi_dict[bigram], 1, args.chi_2)]

    print("done calculating", flush=True)
    for bigram in chi_filtered:
        bigram_string = " ".join(bigram)
        args.output.write(bigram_string + "\t" 
                            + str(bigram_cnt[bigram]) + "\t" 
                            + str(mi_dict[bigram]) + "\t" 
                            + str(chi_dict[bigram]) + "\n")
    args.output.close()

if __name__ == "__main__":
    nicer.make_nice()
    parser = argparse.ArgumentParser()

    parser.add_argument("--files", "-f", nargs="*", type=argparse.FileType("r"),
                        help="txt file to read proof from")

    parser.add_argument("--bigram_file", "-bf",
                        help="pk file to read/write bigrams")
    
    # parser.add_argument("--n", "-n", type=int, default=2,
    #                     help="value of n for bigrams")

    # parser.add_argument("--cores", "-p", type=int, default=4,
    #                     help="number of cores")

    parser.add_argument("--output", "-o", default=sys.stdout, type=argparse.FileType("w"),
                        help="file to write results to")

    parser.add_argument("--frequency", "-F", type=int, default=100,
                        help="threshold for frequency")

    parser.add_argument("--mi", "-MI", type=int, default=5,
                        help="threshold for MI")

    parser.add_argument("--chi_2", "-C", type=float, default=0.95,
                        help="confidence interval for chi-squared")

    parser.add_argument("--all", "-A", action='store_true',
                        help="do not apply filter")

    args = parser.parse_args()

    main(args)
