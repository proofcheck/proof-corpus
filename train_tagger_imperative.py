#!/usr/bin/env python

import argparse
import nicer
import random
import re
from multiprocessing import Pool
from itertools import repeat
import pickle
import os
os.environ['OPENBLAS_NUM_THREADS'] = '1'

from nltk.tag.perceptron import PerceptronTagger
import nltk

from tagger import write_tags
from load_tagged_sent import load_one_sent_tags, load_tags, is_sent
from load_ontonotes_pos import *
from train_tagger import *
from train_tagger_loop_fixed_sentences import do_one_iteration_experiment


"""

100 sentences from each bin (45 most common bins, test on 5 least common) 
5, 10, 20 iter

"""

TRAIN_NUM_LIST = [5, 10, 20, 50, 100]
ITER_NUM_LIST = [5, 10, 20]

def get_train_test_files(train_word_list):
    path="word_bins/unique"
    
    train_list = []
    test_list = []
    
    for (root, dirs, file) in os.walk(path):
        for f in file:
            for word in train_word_list:
                if word in f:
                    train_list += f
                else:
                    test_list += f
    
    return train_list, test_list

def make_training_from_bin(train_files, train_num_list, output=None): 
    training_set = []
    for train_file in train_files:
        with open(train_file, "r") as f:
            lines_one_file = f.readlines()
            training_set += [make_fixed_sents(lines_one_file, train_num_list[-1], output=output)]
                
    return training_set

def make_testing_from_bin(test_files):
    testing_set = []
    for test_file in test_files:
        with open(test_file, "r") as f:
            lines_one_file = f.readlines()
            testing_set += make_fixed_sents(lines_one_file)

    return testing_set

def sum_vb(confusion):
    sum_vb = 0
    for test in confusion.test:
        sum_vb += confusion['VB', test]
    
    return sum_vb

def do_experiments(args):
    # Prints accuracy, number of VBs mistakenly tagged as NPP, number of mislabelled tokens overall
    # for default and trained taggers 
    # Tests tagger on args.test and WSJ corpus
    train_num_list = TRAIN_NUM_LIST
    iter_num_list = ITER_NUM_LIST

    if args.save_sentences:
        save = args.output
    else:
        save = None
    
    nltk.data.clear_cache()
    wsj_train = make_wsj_train()

    with open(args.train_word_file, "r") as wl:
        train_word_list = wl.readlines()
    train_files, test_files = get_train_test_files(train_word_list)
    training_set = make_training_from_bin(train_files, train_num_list, output=save)
    testing = make_testing_from_bin(test_files)

    nltk.data.clear_cache()
    default_tagger = make_default_tagger()
    default_confusion = default_tagger.confusion(testing)

    default_results = [default_tagger.accuracy(testing), 
                    default_confusion['VB', 'NNP'],
                    sum_vb(default_confusion),
                    num_mislabelings(default_confusion),
                ]

    for num in train_num_list:
        training = []
        for imperative_verb in training_set:
            training += imperative_verb[:num]
        
        for nr_itr in iter_num_list:
            i = 0
            while i < 10:
                do_one_iteration_experiment(testing, training, wsj_train, nr_itr)
                i += 1


    default_results, trained_results = do_one_experiment(testing, trained_tagger, default_tagger, args.numtest, training, save)
    print_results(default_results, trained_results, args.numtrain, args.output)

    default_results, trained_results = do_one_experiment(None, trained_tagger, default_tagger, args.numtest, training, save)
    print_results(default_results, trained_results, args.numtrain, args.output)


def do_one_experiment(test_file, trained_tagger, default_tagger, numtest=None, compare=[], output=None):
    # creates testing set
    if test_file == None:
        testing = [sent for sent in make_wsj_test() if sent not in compare]
        if numtest:
             print("Testing on {} sentences from WSJ".format(numtest))
        else:
            print("Testing on all sentences from WSJ")

    else:
        test_lines = test_file.readlines()
        test_file.close()
        testing = make_fixed_sents(test_lines, numtest, compare)
        if numtest:
            print("Testing on {} sentences from {}".format(numtest, test_file.name))
        else:
            print("Testing on all sentences from", test_file.name)
    
    default_confusion = default_tagger.confusion(testing)
    default_results = [default_tagger.accuracy(testing), 
                    default_confusion['VB', 'NNP'],
                    num_mislabelings(default_confusion),
                ]
    trained_confusion = trained_tagger.confusion(testing)
    results = [trained_tagger.accuracy(testing), 
                    trained_confusion['VB', 'NNP'],
                    num_mislabelings(trained_confusion),
                ]
    
    if output:
        with open(output, "a") as o:
            if test_file:
                o.write("\n"+test_file.name+"\n")
            else:
                o.write("\nWSJ\n")

    return default_results, results



def main(args):
    if args.output:
        with open(args.output, "a") as o:
            o.write("\n----------------------------------------------------------------------------------------------------------------\n")
    do_experiments(args)

if __name__ == '__main__':
    nicer.make_nice()
    parser = argparse.ArgumentParser()

    parser.add_argument("--train", "-tr",type=argparse.FileType('r'), nargs='*',
                            help="txt file to read training sentences from")
    
    parser.add_argument("--test", "-te", type=argparse.FileType('r'), nargs='*', default=None,
                            help="txt file to read testing sentences from")
    
    parser.add_argument("--numtrain", "-ntr",type=int, default=None,
                            help="number of training sentences")
    
    parser.add_argument("--numtest", "-nte", default=None,
                            help="number of testing sentences")
    
    parser.add_argument("--sample_all", "-sa", action='store_true',
                            help="sample sentences randomly across files")
    
    parser.add_argument("--combine_wsj", "-c", action='store_true',
                            help="combine wsj training set")
    
    parser.add_argument("--save_sentences", "-s", action='store_true',
                            help="save training set")

    parser.add_argument("--output", "-o",
                            help="txt file to write confusion matrices and sentences to")

    parser.add_argument("--word", "-w",
                            help="Word to check for in keys")

    parser.add_argument("--compare_weights", "-cw", action='store_true',
                            help="compare weights dictionary")


    args = parser.parse_args()

    main(args)