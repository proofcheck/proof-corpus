#!/usr/bin/env python

import argparse
import nicer
import sys
import dill
import dill as pickle

from nltk.util import ngrams
from nltk.lm.preprocessing import padded_everygram_pipeline
from nltk.lm import MLE

from sent_tools import *

def output(args):
    ids, tokenized = read_files_tokenized(args.files, args.cores)
    train, vocab = padded_everygram_pipeline(2, tokenized)
    lm = MLE(2)
    lm.fit(train, vocab)

    with open(args.output, 'wb') as fout:
        pickle.dump(lm, fout)

def log_probability(lm, sent, n):
    tokenized = tokenize(sent)
    sent_ngram = list(ngrams(tokenized, n))
    return lm.entropy(sent_ngram) * (-len(sent_ngram))

def sentence_ranker(lm, sentences, n):
    log_prob_dict = {sent : log_probability(lm, sent, n) for sent in sentences}
    log_prob_sorted = sorted(log_prob_dict.keys(), key=lambda x:log_prob_dict[x], reverse=True)

    return log_prob_dict, log_prob_sorted

def experiment(args):
    with open('lm_bigrams.pk', 'rb') as fin:
        lm = pickle.load(fin)
        # sent = [('Suppose', 'MATH'), ('MATH', '.')]
        # n = len(sent)
        # perplexity = lm.perplexity(sent)
        # entropy = lm.entropy(sent)
        # p_perplexity = pow((1/perplexity), n)
        # p_entropy = pow(2, (entropy*-1*n))
        # log_p = entropy*-1*n

        # print(p_perplexity)
        # print(p_entropy)
        # print(log_p)

        sents = ["Suppose MATH .",
                "Let MATH .",
                "Using MATH , we know that MATH is MATH .",
                "Set the value of MATH to be MATH ."
                ]

        prob_dict, sorted_list = sentence_ranker(lm, sents, 2)
        for sent in sorted_list:
            print(sent)
            print(prob_dict[sent])
        
        """
        Let MATH .
        -2.06146989026305
        Suppose MATH .
        -3.677577446095698
        Using MATH , we know that MATH is MATH .
        -26.062647544439073
        Set the value of MATH to be MATH .
        -37.16969940313428
        """


def main(args):
    experiment(args)

if __name__ == '__main__':
    nicer.make_nice()
    parser = argparse.ArgumentParser()

    parser.add_argument("--files", "-f", nargs='*',type=argparse.FileType("r"),
                            help="List of txt files to read sentences from")

    parser.add_argument( "--cores", "-c",
                            help="Number of cores to use", type=int, default=4)

    parser.add_argument( "--output", "-o",
                            help="Name of output file")


    args = parser.parse_args()
    main(args)