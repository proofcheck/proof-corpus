#!/usr/bin/env python

import argparse
import nicer
import random
from multiprocessing import Pool
from itertools import repeat
import pickle
import os
os.environ['OPENBLAS_NUM_THREADS'] = '1'

from nltk.tag.perceptron import PerceptronTagger, load
import nltk

from nltk_tagger import write_tags
from load_tagged_sent import load_one_sent, load_tags, is_sent
from load_ontonotes_pos import *
from train_tagger import *


def fixed_experiments(args):
    # Prints accuracy, number of VBs mistakenly tagged as NPP, number of mislabelled tokens overall
    # for default and trained taggers 
    # Tests tagger on args.test and WSJ corpus

    if args.combine_wsj:
        print("Training on WSJ corpus and sampled sentences")
        wsj_train = make_wsj_train()
    
    else:
        wsj_train = []

    train_lines = [train_file.readlines() for train_file in args.train]
    for train_file in args.train:
        train_file.close()

    default_results = []
    test_lines = args.test.readlines()
    args.test.close()
    testing = make_fixed_sents(test_lines)
    nltk.data.clear_cache()
    default_tagger = make_default_tagger()
    default_confusion = default_tagger.confusion(testing)
    default_results = [default_tagger.accuracy(testing), 
                    default_confusion['VB', 'NNP'],
                    num_mislabelings(default_confusion),
                ]

    training = make_training_set(train_lines)
    with open(args.output, "a") as o:
        for num in default_results:
            o.write(str(num)+"\t")
        o.write("\n")
    i = 0
    while i < args.num_itr:
        do_one_fixed_experiment(testing, training, wsj_train)
        i+= 1

def do_one_fixed_experiment(testing, training, wsj_train):
    with open(args.output, "a") as o:
        trained_tagger = train_tagger(training, wsj_train)
        trained_confusion = trained_tagger.confusion(testing)
        trained_results = [trained_tagger.accuracy(testing), 
                        trained_confusion['VB', 'NNP'],
                        num_mislabelings(trained_confusion),
                    ]
        for num in trained_results:
            o.write(num+"\t")
        o.write("\n")

def main(args):
    fixed_experiments(args)

if __name__ == '__main__':
    nicer.make_nice()
    parser = argparse.ArgumentParser()

    parser.add_argument("--train", "-tr",type=argparse.FileType('r'), nargs='*',
                            help="txt file to read training sentences from")
    
    parser.add_argument("--test", "-te", type=argparse.FileType('r'), default=None,
                            help="txt file to read testing sentences from")
    
    parser.add_argument("--num_itr", "-n",type=int, default=5,
                            help="number of iterations")
    
    parser.add_argument("--combine_wsj", "-c", action='store_true',
                            help="combine wsj training set")
 
    parser.add_argument("--output", "-o",
                            help="txt file to write confusion matrices and sentences to")

    args = parser.parse_args()

    main(args)
