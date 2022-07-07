#!/usr/bin/env python
import pickle
import argparse
import sys
import nicer
import math
from collections import Counter
from scipy.stats.contingency import chi2_contingency
from scipy.stats.chi2 import *

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
        if ind % 100000 == 0:
            print(round(ind/len_sent*100), "%", sep="")
        ngrams.extend([return_ngrams(sent, n)])

    print("dumping")
    with open(output, "wb") as resource:
        pickle.dump(ngrams, resource)

    unigrams = [sentences for sent in sentences for word in sent]

    return ngrams, unigrams

def pointwise_mutual_information(ngram, ngram_dist, unigram_dist):
    p_ngram = get_probability(ngram_dist, ngram)
    p_unigram_product = get_unigram_probability_product(unigram_dist, ngram)
    return math.log(p_ngram/p_unigram_product, 2)

# def mutual_information(ngram, ngram_dist, unigram_dist):
#     return

def get_probability(dist, ngrams):
    return dist[ngrams] / dist.total()

def get_unigram_probability_product(unigram_dist, ngram):
    probability = 1
    for unigram in ngram:
        probability *= get_probability(unigram_dist, unigram)
    return probability

def chi_squared_bigram(ngram, ngram_dist, unigram_dist):
    obs =   [
                [   ngram_dist[ngram],                        get_ngrams_not_second(ngram, ngram_dist)          ],
                [   get_ngrams_not_first(ngram, ngram_dist),  get_ngrams_not_first_or_second(ngram, ngram_dist) ]
            ]

    chi2float, p, dof, expectedndarray = chi2_contingency(obs)
    print(p, dof, expectedndarray)
    return chi2float, dof

def get_ngrams_not_first(ngram, ngram_dist):
    count = 0
    for key in ngram_dist.keys():
        if key[0] is not ngram[0] and key[1] is ngram[1]:
            count += ngram_dist[key]
    return count

def get_ngrams_not_second(ngram, ngram_dist):
    count = 0
    for key in ngram_dist.keys():
        if key[0] is ngram[0] and key[1] is not ngram[1]:
            count += ngram_dist[key]
    return count

def get_ngrams_not_first_or_second(ngram, ngram_dist):
    count = 0
    for key in ngram_dist.keys():
        if key[0] is not ngram[0] and key[1] is not ngram[1]:
            count += ngram_dist[key]
    return count

def compare_critical(chi, dof, confidence_level):
    critical = chi2.ppf(confidence_level, dof)
    if abs(chi) >= critical:
        return True
    else:
        return False

def make_ngram_dist(ngrams):
    dist = Counter()
    for sent in ngrams:
        dist.update(sent)
    return dist

def main(args):
    if args.files:
        ngrams, unigrams = save_ngrams(args.files, args.ngram_file, args.n)

    else:
        with open(args.ngram_file, "rb") as resource:
            ngrams = pickle.load(resource)
        
        unigrams = [ngram[0] for ngram in ngrams]
            
    ngram_cnt = make_ngram_dist(ngrams)
    unigram_cnt = Counter(unigrams)

    if args.frequency:
        ngram_dict = ngram_cnt
        ngrams_sorted = [ngram for ngram in ngram_cnt.keys() if ngram_cnt[ngram] < args.threshold]
        ngrams_sorted.sort(key=lambda x: ngram_dict[x])
    
    if args.mutual_information:
        ngram_dict = {ngram : pointwise_mutual_information(ngram, ngram_cnt, unigram_cnt) for ngram in ngram_cnt.keys()}
        ngrams_sorted = [ngram for ngram in ngram_dict.keys() if ngram_dict[ngram] > args.threshold]
        ngrams_sorted.sort(key=lambda x: ngram_dict[x])

    if args.chi_squared:
        ngram_dict = {ngram : chi_squared_bigram(ngram, ngram_cnt, unigram_cnt)[0] for ngram in ngram_cnt.keys()}
        ngrams_sorted = [ngram for ngram in ngram_dict.keys() if compare_critical(ngram_dict[ngram], 1, args.threshold)]

    with open(args.output, "w") as o:
        for ngram in ngrams_sorted:
            ngram_string = " ".join(ngram)
            o.write(str(ngram_dict[ngram]) + "\t" + ngram_string + "\n")

if __name__ == "__main__":
    nicer.make_nice()
    parser = argparse.ArgumentParser()

    parser.add_argument("--files", "-f", nargs="*", type=argparse.FileType("r"),
                        help="txt file to read proof from",)

    parser.add_argument("--ngram_file", "-nf",
                        help="file to read/write ngrams",)
    
    parser.add_argument("--n", "-n", type=int, default=2,
                        help="value of n for ngrams",)

    parser.add_argument("--threshold", "-t", type=int, default=2,
                        help="threshold/significance level for statistic\nfrequency, mutual_information: bottom n\nchi_squared: > significance level",
                        )

    parser.add_argument("--frequency", "-F", action="store_true",
                        help="use frequency?",)

    parser.add_argument("--mutual_information", "-MI", action="store_true",
                        help="use mutual information?",)

    parser.add_argument("--chi_squared", "-X", action="store_true",
                        help="use chi squared?",)

    parser.add_argument("--output", "-o",
                        help="file to write results to",)

    
    

    args = parser.parse_args()

    main(args)
