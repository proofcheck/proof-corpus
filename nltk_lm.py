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
        "Set the value of MATH to be MATH .",
        "Inferring MATH from REF , MATH holds .",
        "三角形 の 内角 の 和 は 百八十度 で ある 。",
        "Suppose that hence MATH , MATH .",
        "People won't talk like this .",
        "We can assume without a loss of generality that MATH , since there exists MATH such that MATH ."
        
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

def length_sent(line):
    tokenized = tokenize(line)
    return len(tokenized) + 2

def nltk_word_lp(lm, token):
    return lm.logscore(token)

def unigram_lp(lm, line, lp_word=nltk_word_lp, lp_sent=None, n=None):
    score = 0
    tokenized = tokenize(line)
    for token in tokenized:
        score += lp_word(lm, token)
    return score

def nltk_sent_lp(lm, line, lp_word=None, sent_lp=None, n=None):
    tokenized = tokenize(line)
    sent_ngram = ngrams(tokenized, n)
    return lm.entropy(sent_ngram) * (-length_sent(line))

def mean_lp(lm, line, lp_word=None, lp_sent=nltk_sent_lp, n=None):
    return lp_sent(lm, line, n=n) / length_sent(line)

def norm_lp_div(lm, line, lp_word=nltk_word_lp, lp_sent=nltk_sent_lp, n=None):
    return - lp_sent(lm, line, n) / unigram_lp(lm, line, lp_word)

def norm_lp_sub(lm, line, lp_word=nltk_word_lp, lp_sent=nltk_sent_lp, n=None):
    return lp_sent(lm, line, n) - unigram_lp(lm, line, lp_word)

def slor(lm, line, lp_word=nltk_word_lp, lp_sent=nltk_sent_lp, n=None):
    return norm_lp_sub(lm, line, lp_word, lp_sent, n) / length_sent(line)

def sentence_ranker(lm, sentences, prob_function, lp_word=nltk_word_lp, lp_sent=nltk_sent_lp, n=None):
    log_prob_dict = {sent : prob_function(lm, sent, lp_word, lp_sent, n) for sent in sentences}
    log_prob_sorted = sorted(log_prob_dict.keys(), key=lambda x:log_prob_dict[x], reverse=True)

    return log_prob_dict, log_prob_sorted

def word_ranker(lm, prob_function, sentences):
    tokens = list(set(flatten(sentences)))
    log_prob_dict = {token : prob_function(lm, token) for token in tokens}
    log_prob_sorted = sorted(log_prob_dict.keys(), key=lambda x:log_prob_dict[x], reverse=True)

    return log_prob_dict, log_prob_sorted

def rank_sentences_from_file(lm, sentence_file, prob_function, lp_word=nltk_word_lp, lp_sent=nltk_sent_lp, n=None):
    with open(sentence_file, "r") as sent_file:
        sentences = sent_file.read().splitlines()
    
    log_prob_dict, log_prob_sorted = sentence_ranker(lm, sentences, prob_function, lp_word, lp_sent, n)
    for sent in log_prob_sorted:
        print(log_prob_dict[sent], "\t", sent)

def experiment(args):
    if args.output:
        results = ""

    with open(args.lm, 'rb') as fin:
        lm = pickle.load(fin)
        
    with open(args.sentences, "r") as s:
        sents = s.read().splitlines()

    for prob_func in [lp_sent, unigram_lp, mean_lp, norm_lp_div, norm_lp_sub, slor]:
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

    parser.add_argument( "--files", "-f", nargs='*',type=argparse.FileType("r"),
                            help="List of txt files to read sentences from (for generating lm)")

    parser.add_argument( "--cores", "-c",
                            help="Number of cores to use", type=int, default=4)

    parser.add_argument( "--lm", "-lm",
                            help="Name of lm file")
    
    parser.add_argument( "--ngrams", "-n", type=int, default=2,
                            help="ngrams to use")

    parser.add_argument( "--sentences", "-s",
                            help="txt file to read sentences from (for testing on lm)")

    parser.add_argument( "--output", "-o", 
                            help="txt file to write resuls to")



    args = parser.parse_args()
    main(args)