#!/usr/bin/env python

import os
os.environ['OPENBLAS_NUM_THREADS'] = '1'

import argparse
from more_itertools import flatten

import nicer
import dill as pickle

from nltk.util import ngrams
from nltk.lm.preprocessing import padded_everygram_pipeline
from nltk.lm import MLE, KneserNeyInterpolated

from sent_tools import *

SENTS = ["Suppose MATH .",
                "Let MATH .",
                "Using MATH , we know that MATH is MATH .",
                "Set the value of MATH to be MATH ."
        ]

"""Using mle_bigrams.pk
        Let MATH .
        -2.06146989026305
        Suppose MATH .
        -3.677577446095698
        Using MATH , we know that MATH is MATH .
        -26.062647544439073
        Set the value of MATH to be MATH .
        -37.16969940313428
"""

def output(args):
    ids, tokenized = read_files_tokenized(args.files, args.cores)
    train, vocab = padded_everygram_pipeline(args.ngrams, tokenized)
    # lm = MLE(2)
    lm = KneserNeyInterpolated(args.ngrams)
    lm.fit(train, vocab)

    with open(args.lm, 'wb') as fout:
        pickle.dump(lm, fout)

def length_sent(sent):
    tokenized = tokenize(sent)
    return len(tokenized)

def unigram_lp(lm, sent):
    score = 0
    tokenized = tokenize(sent)
    for token in tokenized:
        score += lp_word(lm, token)
    return score

def lp_sent(lm, sent, n):
    tokenized = tokenize(sent)
    sent_ngram = list(ngrams(tokenized, n))
    return lm.entropy(sent_ngram) * (-len(tokenized))

def mean_lp(lm, sent, n):
    return lp_sent(lm, sent, n) / length_sent(sent)

def norm_lp_div(lm, sent, n):
    return - lp_sent(lm, sent, n) / unigram_lp(lm, sent)

def norm_lp_sub(lm, sent, n):
    return lp_sent(lm, sent, n) - unigram_lp(lm, sent)

def slor(lm, sent, n):
    return norm_lp_sub(lm, sent, n) / length_sent(sent)

def lp_word(lm, token):
    return lm.logscore(token)

def sentence_ranker(lm, sentences, prob_function, n):
    log_prob_dict = {sent : prob_function(lm, sent, n) for sent in sentences}
    log_prob_sorted = sorted(log_prob_dict.keys(), key=lambda x:log_prob_dict[x], reverse=True)

    return log_prob_dict, log_prob_sorted

def word_ranker(lm, prob_function, sentences):
    tokens = list(set(flatten(sentences)))
    log_prob_dict = {token : prob_function(lm, token) for token in tokens}
    log_prob_sorted = sorted(log_prob_dict.keys(), key=lambda x:log_prob_dict[x], reverse=True)

    return log_prob_dict, log_prob_sorted

def sort_by_prob():
    # Make 0 and inf return default value instead
    return

def experiment(args):
    if args.output:
        results = ""

    with open(args.lm, 'rb') as fin:
        lm = pickle.load(fin)
        
    with open(args.sentences, "r") as s:
        sents = s.read().splitlines()

    for prob_func in [lp_sent, mean_lp, norm_lp_div, norm_lp_sub, slor]:
        prob_dict, sorted_list = sentence_ranker(lm, sents, prob_func, 2)
        if args.output:
            results += "\n" + prob_func.__name__ + "\n"
        print(prob_func.__name__)
        for sent in sorted_list:
            print(sent)
            print(prob_dict[sent])
            if args.output:
                results += sent + "\t" + str(prob_dict[sent]) + "\n"

    if args.output:
        with open(args.output, "w") as o:
            o.write(results)

def main(args):
    if args.files:
        output(args)
    else:
        experiment(args)

if __name__ == '__main__':
    nicer.make_nice()
    parser = argparse.ArgumentParser()

    parser.add_argument("--files", "-f", nargs='*',type=argparse.FileType("r"),
                            help="List of txt files to read sentences from (for generating lm)")

    parser.add_argument( "--cores", "-c",
                            help="Number of cores to use", type=int, default=4)

    parser.add_argument( "--lm", "-lm",
                            help="Name of lm file")
    
    parser.add_argument( "--ngrams", "-n", type=int, default=2,
                            help="ngrams to use")

    parser.add_argument("--sentences", "-s",
                            help="txt file to read sentences from (for testing on lm)")

    parser.add_argument("--output", "-o", 
                            help="txt file to write resuls to")



    args = parser.parse_args()
    main(args)