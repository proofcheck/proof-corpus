#!/usr/bin/env python

import argparse
import nicer
from multiprocessing import Pool
import os

from load_ontonotes_pos import *
from train_tagger import *
from train_tagger_loop_fixed_sentences import get_one_iteration_results, save_results

# Trains on n sentences (element in TRAIN_NUM_LIST) from num_train bins
# Iterates for nr_itr times (element in ITER_NUM_LIST)
# Runs 10 loops for each experiment
# Tests on WSJ and testing set (all sentences in unused bins)

TRAIN_NUM_LIST = [5, 10, 20, 50, 100]
ITER_NUM_LIST = [5, 10, 20]

TRAIN_NUM_LIST_SMALL = range(1, 11)
ITER_NUM_LIST_SMALL = [5, 10]

PATH = "word_bins/unique/"

def get_train_test_files(word_list, num):
    train_word_list = word_list[:num]
    path = PATH
    
    train_list = []
    test_list = []
    
    for (root, dirs, file) in os.walk(path):
        for f in file:
            verb = f.split(".")[0]
            if verb in train_word_list:
                train_list += [f]
            else:
                test_list += [f]
    
    return train_list, test_list

def make_training_from_bin(train_files, train_num_list, output=None): 
    training_set = []
    for train_file in train_files:
        with open(PATH + train_file, "r") as f:
            lines_one_file = f.readlines()
            training_set += [make_fixed_sents(lines_one_file, train_num_list[-1], output=output)]
    
    return training_set

def make_testing_from_bin(test_files, output=None):
    testing_set = []
    for test_file in test_files:
        with open(PATH + test_file, "r") as f:
            lines_one_file = f.readlines()
            testing_set += make_fixed_sents(lines_one_file, 1000, output=output)
    return testing_set

def make_train_test(args):
    train_num_list = TRAIN_NUM_LIST_SMALL
    if args.save_sentences:
        save_train = "training_set/" + args.extension + ".txt"
        save_test = "testing_set/" + args.extension + ".txt"

        if os.path.exists(save_train) or os.path.exists(save_test):
            print("Exists")
            return 0

    else:
        save_train = None
        save_test = None

    word_list = args.wordlist.read().splitlines()
    train_files, test_files = get_train_test_files(word_list, args.num_train_bins)
    training_set = make_training_from_bin(train_files, train_num_list, output=save_train)
    testing = make_testing_from_bin(test_files, output=save_test)

    nltk.data.clear_cache()
    default_tagger = make_default_tagger()
    default_confusion = default_tagger.confusion(testing)

    default_results = [default_tagger.accuracy(testing), 
                    default_confusion['VB', 'NNP'],
                    mislabeled_vb(default_confusion),
                    num_mislabelings(default_confusion),
                ]
    
    output_default = "experiments/experiment_defaulttagger_test_" + args.extension + ".txt"
    with open(output_default, "w") as o:
        for num in default_results:
            o.write(str(num)+"\t")


def do_experiments(args):
    # Prints accuracy, number of VBs mistakenly tagged as NPP, number of mislabelled tokens overall
    # for default and trained taggers 
    # Tests tagger on args.test and WSJ corpus
    train_num_list = TRAIN_NUM_LIST_SMALL
    iter_num_list = ITER_NUM_LIST_SMALL

    if args.debug:
        args.extension = args.extension + "_test"
    
    training_pre = args.train.read().splitlines()
    training_single_list = make_fixed_sents(training_pre)
    num_lines_verb = train_num_list[-1]
    training_set = [training_single_list[x:x+num_lines_verb] for x in range(0, len(training_pre), num_lines_verb)]

    testing_pre = args.test.read().splitlines()
    testing = make_fixed_sents(testing_pre)

    train_num_list_zip = train_num_list*len(iter_num_list)
    iter_num_list_zip = iter_num_list*len(train_num_list)
    zipped_args = zip(train_num_list_zip, iter_num_list_zip)
    print(list(zipped_args))

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
        trained_results_test += [get_one_iteration_results(testing, trained_tagger, output_test)]
        if wsj_test:
            trained_results_wsj += [get_one_iteration_results(WSJ_TEST, trained_tagger, output_wsj)]
        i += 1

    save_results(trained_results_test, output_test)

    if wsj_test:
        save_results(trained_results_wsj, output_wsj)

def main(args):
    if args.wordlist:
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
    
    parser.add_argument("--num_train_bins", "-ntr",type=int, default=45,
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