#!/usr/bin/env python

import argparse

from more_itertools import flatten
import nicer
from multiprocessing import Pool
import os

from load_ontonotes_pos import *
from train_tagger import *
from train_tagger_loop_fixed_sentences import get_one_iteration_results, save_results
from load_tagged_sent import load_tag_lines

# Trains on n sentences (element in TRAIN_NUM_LIST) from num_train bins
# Iterates for nr_itr times (element in ITER_NUM_LIST)
# Runs 10 loops for each experiment
# Tests on WSJ and testing set (all sentences in unused bins)

TRAIN_NUM_LIST = [5, 10, 20, 50, 100]
ITER_NUM_LIST = [5, 10, 20]

TRAIN_NUM_LIST_SMALL = list(range(1, 11))
ITER_NUM_LIST_SMALL = [5, 10]

TRAIN_NUM_LIST_BEST = [5]
ITER_NUM_LIST_BEST = [10]

PATH = "word_bins/unique/"

def get_train_test_files(word_list_tags, num):
    word_list = [word.split('_')[0] for word in word_list_tags]
    train_word_list = word_list[:num]
    test_word_list = word_list[num:]
    path = PATH
    train_list = []
    test_list = []
    
    for (root, dirs, file) in os.walk(path):
        for f in file:
            verb = f.split(".")[0]
            if verb in train_word_list:
                train_list += [f]
            if verb in test_word_list:
                test_list += [f]
    return train_list, test_list

def make_training_from_bin(train_files, train_num_list, output, word_list=[], test_lines=[]): 
    training_set = []
    for train_file in train_files:
        with open(PATH + train_file, "r") as f:
            lines_one_file = f.readlines()
            training_set += pick_sents(lines_one_file, n=train_num_list[-1], compare=test_lines)
    
    write_fixed_sents(training_set, output, word_list)
    return training_set

def make_testing_from_bin(test_files, output, word_list, train_lines=[]):
    testing_set = []
    num_lines_one_file = 5000 // len(test_files)

    for test_file in test_files:
        with open(PATH + test_file, "r") as f:
            lines_one_file = f.readlines()
            if len(lines_one_file) < num_lines_one_file:
                num_lines_this_file = None
            else:
                num_lines_this_file = num_lines_one_file
            testing_set += pick_sents(lines_one_file, n=num_lines_this_file, compare=train_lines)
    write_fixed_sents(testing_set, output, word_list)
    return testing_set

def make_train_test(args):
    train_num_list = TRAIN_NUM_LIST_BEST
    word_list = args.wordlist.read().splitlines()
    num_train_bins = len(word_list) - args.num_test_bins
    train_files, test_files = get_train_test_files(word_list, num_train_bins)

    save_test = "testing_set/" + args.extension + ".txt"

    if os.path.exists(save_test):
        print("Testing exists")
        return 0

    if not args.train: 
        save_train = "training_set/" + args.extension + ".txt"
    
        if os.path.exists(save_train):
            print("Training exists")
            return 0

        training = make_training_from_bin(train_files, train_num_list, save_train, word_list)
        training_lines = flatten(training)

    else:
        training_lines = args.train.read().splitlines()

    testing = fix_sents(make_testing_from_bin(test_files, save_test, word_list, training_lines))

    nltk.data.clear_cache()
    default_tagger = make_default_tagger()
    default_confusion = default_tagger.confusion(testing)

    default_results = [default_tagger.accuracy(testing), 
                        default_confusion['VB', 'NNP'],
                        mislabeled_vb(default_confusion),
                        num_mislabelings(default_confusion),
                      ]
    
    output_default = "experiments/experiment_default_tagger_test_" + args.extension + ".txt"
    with open(output_default, "w") as o:
        str_results = list(map(str, default_results))
        o.write("\t".join(str_results))

def do_experiments(args):
    # Prints accuracy, number of VBs mistakenly tagged as NPP, number of mislabelled tokens overall
    # for default and trained taggers 
    # Tests tagger on args.test and WSJ corpus
    train_num_list = TRAIN_NUM_LIST_BEST
    iter_num_list = ITER_NUM_LIST_BEST

    if args.debug:
        args.extension = args.extension + "_test"
    
    training_lines = args.train.read().splitlines()
    training_loaded = load_tag_lines(training_lines)[1]
    num_lines_verb = train_num_list[-1]
    training_set = [training_loaded[x:x+num_lines_verb] for x in range(0, len(training_lines), num_lines_verb)]
    
    testing_lines = args.test.read().splitlines()
    testing = load_tag_lines(testing_lines)[1]

    train_num_list_zip = train_num_list*len(iter_num_list)
    iter_num_list_zip = [num for num in iter_num_list for i in range(len(train_num_list))]
    zipped_args = zip(train_num_list_zip, iter_num_list_zip)

    with Pool(processes=args.cores) as p:
        p.starmap(
            do_one_iteration,
            zip(
                repeat(testing),
                repeat(training_set),
                zipped_args,
                repeat(args.extension),
                repeat(args.trial_num),
                repeat(args.wsj_test),
            ),
            1,
        )
    args.train.close()
    args.test.close()

def do_one_iteration(testing, training_set, zipped_arg, extension="", trial_num=10, wsj_test=False):
    num_train_sent, nr_iter = zipped_arg
    training = []
    for imperative_verb in training_set:
        training += imperative_verb[:num_train_sent]
    
    if wsj_test:
        output_wsj = "experiments/experiment_" + str(num_train_sent) + "sents_" + str(nr_iter) + "iters_wsj_" + extension + ".txt"
        trained_results_wsj = []

    output_test = "experiments/experiment_" + str(num_train_sent) + "sents_" + str(nr_iter) + "iters_test_" + extension + ".txt"
    trained_results_test = []
    i = 0
    while i < trial_num:
        trained_tagger = train_tagger(training, nr_iter=nr_iter)
        trained_results_test += [get_one_iteration_results(testing, trained_tagger)]
        if wsj_test:
            trained_results_wsj += [get_one_iteration_results(WSJ_TEST, trained_tagger)]
        i += 1

    save_results(trained_results_test, output_test)

    if wsj_test:
        save_results(trained_results_wsj, output_wsj)

def main(args):
    if args.save_sentences:
        make_train_test(args)
        
    else:
        do_experiments(args)

if __name__ == '__main__':
    nicer.make_nice()
    parser = argparse.ArgumentParser()

    parser.add_argument("--train", "-tr",type=argparse.FileType('r'),
                            help="txt file to read training set")

    parser.add_argument("--test", "-te",type=argparse.FileType('r'),
                            help="txt file to read testing set")
    
    parser.add_argument("--num_test_bins", "-nte",type=int, default=1,
                            help="number of training words")
    
    parser.add_argument("--save_sentences", "-s", action='store_true',
                            help="save sentences")

    parser.add_argument("--extension", "-e",
                            help="file extension")
    
    parser.add_argument("--cores", "-c", type=int, default=5,
                            help="cores")
                            
    parser.add_argument("--debug", "-d", action='store_true',
                            help="testing?")
    
    parser.add_argument("--wordlist", "-wl",type=argparse.FileType('r'),
                            help="txt file to read imperative verbs")

    parser.add_argument("--trial_num", "-tn",type=int, default=10,
                            help="number of trials")

    parser.add_argument("--wsj_test", "-wt", action='store_true',
                            help="test on WSJ?")

    args = parser.parse_args()

    main(args)