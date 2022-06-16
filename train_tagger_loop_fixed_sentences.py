#!/usr/bin/env python

import argparse
import nicer
import os
os.environ['OPENBLAS_NUM_THREADS'] = '1'

import nltk

from load_ontonotes_pos import *
from train_tagger import *


def do_fixed_iteration_experiments(args):
    # Prints accuracy, number of VBs mistakenly tagged as NPP, number of mislabelled tokens overall
    # for default and trained taggers 
    # Tests tagger on args.test and WSJ corpus

    if args.combine_wsj:
        print("Training on WSJ corpus and sampled sentences")
    wsj_train = args.combine_wsj

    train_lines = [train_file.readlines() for train_file in args.train]
    for train_file in args.train:
        train_file.close()

    default_results = []
    test_lines = args.test.readlines()
    args.test.close()
    sents = pick_sents(test_lines)
    testing = fix_sents(sents)
    nltk.data.clear_cache()
    default_tagger = make_default_tagger()
    default_confusion = default_tagger.confusion(testing)
    default_results = [default_tagger.accuracy(testing), 
                    default_confusion['VB', 'NNP'],
                    num_mislabelings(default_confusion),
                ]

    training = make_training_set(train_lines)
    with open(args.output, "a") as o:
        o.write("Default : ")
        for num in default_results:
            o.write(str(num)+"\t")
        o.write("\n")
        
    i = 0
    trained_results = []
    while i < args.num:
        trained_tagger = train_tagger(training, wsj_train, args.nr_itr)
        trained_results += [get_one_iteration_results(testing, trained_tagger)]
        i+= 1

    save_results(trained_results, args.output)

def save_results(results, output):
    with open(output, "w") as o:
        result_string = ""
        for trial in results:
            str_trial = [str(num) for num in trial]
            result_string += "\t".join(str_trial) + "\n"            
        o.write(result_string)

def get_one_iteration_results(testing, tagger):
    trained_confusion = tagger.confusion(testing)
    trained_results = [tagger.accuracy(testing), 
                        trained_confusion['VB', 'NNP'],
                        mislabeled_vb(trained_confusion),
                        num_mislabelings(trained_confusion),
                    ]
    return trained_results

def main(args):
    do_fixed_iteration_experiments(args)

if __name__ == '__main__':
    nicer.make_nice()
    parser = argparse.ArgumentParser()

    parser.add_argument("--train", "-tr",type=argparse.FileType('r'), nargs='*',
                            help="txt file to read training sentences from")
    
    parser.add_argument("--test", "-te", type=argparse.FileType('r'), default=None,
                            help="txt file to read testing sentences from")
    
    parser.add_argument("--num", "-n",type=int, default=5,
                            help="number of loops")

    parser.add_argument("--nr_itr", "-ni",type=int, default=5,
                            help="number of iterations for shuffling")
    
    parser.add_argument("--combine_wsj", "-c", action='store_true',
                            help="combine wsj training set")
 
    parser.add_argument("--output", "-o",
                            help="txt file to write confusion matrices and sentences to")

    args = parser.parse_args()

    main(args)
