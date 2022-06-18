#!/usr/bin/env python

import argparse

import nicer
from multiprocessing import Pool
from itertools import repeat

from load_ontonotes_pos import *
from train_tagger import *
from load_tagged_sent import load_tag_lines

PATH = "word_bins/unique/"

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

def do_experiments(args):
    # Prints accuracy, number of VBs mistakenly tagged as NPP, number of mislabelled tokens overall
    # for default and trained taggers 
    # Tests tagger on args.test and WSJ corpus
    train_num_list = [int(num) for num in args.train_num_list.split(",")]
    iter_num_list = [int(num) for num in args.iter_num_list.split(",")]
    
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
                repeat(args.num_trials),
                repeat(args.wsj_test),
            ),
            1,
        )
    args.train.close()
    args.test.close()

def do_one_iteration(testing, training_set, zipped_arg, extension="", num_trials=10, wsj_test=False):
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
    while i < num_trials:
        trained_tagger = train_tagger(training, nr_iter=nr_iter)
        trained_results_test += [get_one_iteration_results(testing, trained_tagger)]
        if wsj_test:
            trained_results_wsj += [get_one_iteration_results(WSJ_TEST, trained_tagger)]
        i += 1

    save_results(trained_results_test, output_test)

    if wsj_test:
        save_results(trained_results_wsj, output_wsj)

def main(args):
    do_experiments(args)

if __name__ == '__main__':
    nicer.make_nice()
    parser = argparse.ArgumentParser()

    parser.add_argument("--train", "-tr",type=argparse.FileType('r'),
                            help="txt file to read training set")

    parser.add_argument("--test", "-te",type=argparse.FileType('r'),
                            help="txt file to read testing set")
    
    parser.add_argument("--extension", "-e",
                            help="file extension")
    
    parser.add_argument("--cores", "-c", type=int, default=5,
                            help="cores")

    parser.add_argument("--num_trials", "-nt", type=int, default=10,
                            help="number of trials")
    
    parser.add_argument("--train_num_list", "-tnl", default="5,10",
                            help="number of sentences to train on (list in string format)")

    parser.add_argument("--iter_num_list", "-inl", default="5,10",
                            help="number of iterations (list in string format)")

    parser.add_argument("--wsj_test", "-wt", action='store_true',
                            help="test on WSJ?")

    args = parser.parse_args()

    main(args)