#!/usr/bin/env python
import pickle
import argparse
import sys
import nicer
import math
from collections import Counter
from scipy.stats.contingency import chi2_contingency

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
        ngrams.extend([return_ngrams(sent, n)])

    print("dumping")
    with open(output, "wb") as resource:
        pickle.dump(ngrams, resource)

    unigrams = [sentences for sent in sentences for word in sent]

    return ngrams, unigrams

def pointwise_mutual_information(ngram, ngram_dist, unigram_dist):
    p_ngram = get_ngram_probability(ngram_dist, ngram)
    p_unigram_product = get_unigram_probability_product(unigram_dist, ngram)
    return math.log(p_ngram/p_unigram_product, 2)

def get_ngram_probability(dist, ngrams):
    return dist[ngrams] / dist.total()

def get_unigram_probability_product(unigram_dist, ngram):
    probability = 1
    for unigram in ngram:
        probability *= get_ngram_probability(unigram_dist, unigram)
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

def make_ngram_cnt(ngrams):
    cnt = Counter()
    for sent in ngrams:
        cnt.update(sent)
    return cnt

def main(args):
    if args.files:
        ngrams, unigrams = save_ngrams(args.files, args.ngram_file, args.n)

    else:
        with open(args.ngram_file, "rb") as resource:
            ngrams = pickle.load(resource)
        
        unigrams = [ngram[0] for ngram in ngrams]
            
    ngram_cnt = make_ngram_cnt(ngrams)
    print(ngram_cnt)
    unigram_cnt = Counter(unigrams)

    # Filter by frequency
    frequency_filtered = [ngram for ngram in ngram_cnt.keys() if ngram_cnt[ngram] > 100]
    
    mi_dict = {ngram : pointwise_mutual_information(ngram, ngram_cnt, unigram_cnt) for ngram in frequency_filtered}
    mi_filtered = [ngram for ngram in mi_dict.keys() if mi_dict[ngram] > 5]

    chi_dict = {ngram : chi_squared_bigram(ngram, ngram_cnt, unigram_cnt)[0] for ngram in mi_filtered}
    chi_filtered = [ngram for ngram in mi_filtered if compare_critical(ngram_dict[ngram], 1, 0.95)]

    with open(args.output, "w") as o:
        for ngram in chi_filtered:
            ngram_string = " ".join(ngram)
            o.write(ngram_string + "\t" +
                    str(ngram_cnt[ngram]) + "\t" +
                    str(mi_dict[ngram]) + "\t" +
                    str(chi_filtered[ngram]) + "\t" + "\n")

if __name__ == "__main__":
    nicer.make_nice()
    parser = argparse.ArgumentParser()

    parser.add_argument("--files", "-f", nargs="*", type=argparse.FileType("r"),
                        help="txt file to read proof from",)

    parser.add_argument("--ngram_file", "-nf",
                        help="pk file to read/write ngrams",)
    
    parser.add_argument("--n", "-n", type=int, default=2,
                        help="value of n for ngrams",)

    parser.add_argument("--output", "-o",
                        help="file to write results to",)

    args = parser.parse_args()

    main(args)
