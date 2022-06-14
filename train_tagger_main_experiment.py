#!/usr/bin/env python

import argparse
import nicer
from multiprocessing import Pool
import os

from load_ontonotes_pos import *
from train_tagger import *
from train_tagger_loop_fixed_sentences import do_one_iteration_results

# Trains on n sentences (element in TRAIN_NUM_LIST) from num_train bins
# Iterates for nr_itr times (element in ITER_NUM_LIST)
# Runs 10 loops for each experiment
# Tests on WSJ and testing set (all sentences in unused bins)

TRAIN_NUM_LIST = [5, 10, 20, 50, 100]
ITER_NUM_LIST = [5, 10, 20]

def get_train_test_files(word_list, num):
    train_word_list = word_list[:num]
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

def do_experiments(args):
    # Prints accuracy, number of VBs mistakenly tagged as NPP, number of mislabelled tokens overall
    # for default and trained taggers 
    # Tests tagger on args.test and WSJ corpus
    train_num_list = TRAIN_NUM_LIST
    iter_num_list = ITER_NUM_LIST

    if args.save_sentences:
        save = "training_set/" + args.extension + ".txt"
    else:
        save = None
    
    nltk.data.clear_cache()

    with open(args.train, "r") as wl:
        word_list = wl.readlines()
    train_files, test_files = get_train_test_files(word_list, args.num_train_bins)
    training_set = make_training_from_bin(train_files, train_num_list, output=save)
    testing = make_testing_from_bin(test_files)

    nltk.data.clear_cache()
    default_tagger = make_default_tagger()
    default_confusion = default_tagger.confusion(testing)

    default_results = [default_tagger.accuracy(testing), 
                    default_confusion['VB', 'NNP'],
                    mislabeled_vb(default_confusion),
                    num_mislabelings(default_confusion),
                ]
    
    output_default = "experiments/experiment_defaulttagger_test" + args.extension + ".txt"
    with open(output_default, "w") as o:
        for num in default_results:
            o.write(str(num)+"\t")
            o.write("\n")

    with Pool(processes=args.cores) as p:
        for num_train_sent in train_num_list:
            for nr_iter in iter_num_list:
                p.starmap(
                    do_one_iteration,
                    zip(
                        repeat(testing),
                        repeat(training_set),
                        num_train_sent,
                        nr_iter,
                        repeat(args.extension),
                    ),
                    1
                )

def do_one_iteration(testing, training_set, num_train_sent, nr_iter, extension=""):
    training = []
    for imperative_verb in training_set:
        training += imperative_verb[:num_train_sent]
        
    output_wsj = "experiments/experiment_" + str(num_train_sent) + "sents_" + str(nr_iter) + "iters_wsj_" + extension + ".txt"
    output_test = "experiments/experiment_" + str(num_train_sent) + "sents_" + str(nr_iter) + "iters_test_" + extension + ".txt"

    i = 0
    while i < 10:
        trained_tagger = train_tagger(training, nr_iter=nr_iter)
        do_one_iteration_results(testing, trained_tagger, output_test)
        do_one_iteration_results(WSJ_TEST, trained_tagger, output_wsj)
        i += 1

def main(args):
   do_experiments(args)

if __name__ == '__main__':
    nicer.make_nice()
    parser = argparse.ArgumentParser()

    parser.add_argument("--train", "-tr",type=argparse.FileType('r'),
                            help="txt file to read imperative verbs from")
    
    parser.add_argument("--num_train_bins", "-ntr",type=int, default=45,
                            help="number of training words")
    
    parser.add_argument("--save_sentences", "-s", action='store_true',
                            help="save sentences")

    parser.add_argument("--extension", "-e",
                            help="file extension")

    args = parser.parse_args()

    main(args)