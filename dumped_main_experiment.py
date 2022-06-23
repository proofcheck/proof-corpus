#!/usr/bin/env python

import argparse

import nicer
from multiprocessing import Pool
from itertools import repeat
import pickle

from load_ontonotes_pos import *
from train_tagger import *

from load_tagged_sent import load_tag_lines
from main_experiment import save_results, get_one_trial_results

PATH = "word_bins/unique/"

def do_dumped_experiments(args):
    
    testing_lines = args.test.read().splitlines()
    testing = load_tag_lines(testing_lines)[1]
       
    args.test.close()

    if wsj_test:
        output_wsj = "experiments/experiment_" + str(num_train_sent) + "sents_" + str(nr_iter) + "iters_" + extension + "-wsj.txt"
        trained_results_wsj = []

    output_test = "experiments/experiment_" + str(num_train_sent) + "sents_" + str(nr_iter) + "iters_" + extension + ".txt"
    
    trained_results_wsj = []
    trained_results = []
    mislabellings = []
    
    with Pool(processes=cores) as p:
        for trained, wsj, mislabeled in p.starmap(
            do_one_trial,
            zip(
                args.tagger,
                [testing]*num_trials,
                list(range(1, num_trials+1)),
                [wsj_test]*num_trials,
                repeat(print_mislabels),
            ),
            1,
        ):
            if wsj_test:
                trained_results_wsj += [wsj]

            if print_mislabels:
                mislabellings += [mislabeled]

            trained_results += [trained]

    save_results(trained_results, output_test)
    
    if wsj_test:
        save_results(trained_results_wsj, output_wsj)

    if print_mislabels:
        output_mislabels = "experiments/experiment_" + str(num_train_sent) + "sents_" + str(nr_iter) + "iters_" + extension + "_mislabels" + ".txt"
        output_string = "\n".join(mislabellings)
        with open(output_mislabels, "w") as o:
            o.write(output_string)

def do_dumped_trial(tagger_file, testing, trial_id=None, wsj_test=False, print_mislabels=False, dump_file=None):
    with open(tagger_file, "rb") as resource:
        trained_tagger = pickle.load(resource)

    trained = get_one_trial_results(testing, trained_tagger, trial_id, dump_file)

    if print_mislabels:
        output_string = ""
        for sent in testing:
            tokens = get_tokens_from_tags(sent)
            tags = trained_tagger.tag(tokens)
            if tags[0][1] not in {'VB', 'VBG', 'VBN'}:
                output_string += " ".join(tokens) + "\t" + tags[0][1] + "\n"
            
        output_string += "----------------\n"

    else:
        output_string = None
            
    if wsj_test:
        wsj = get_one_trial_results(WSJ_TEST, trained_tagger, trial_id)

    else:
        wsj = None

    return trained, wsj, output_string

def main(args):
    do_dumped_experiments(args)

if __name__ == '__main__':
    nicer.make_nice()
    parser = argparse.ArgumentParser()

    parser.add_argument("--tagger", "-ta",type=argparse.FileType('r'), nargs="*",
                            help="txt files to read tagger")

    parser.add_argument("--test", "-te",type=argparse.FileType('r'),
                            help="txt file to read testing set")
    
    parser.add_argument("--extension", "-e",
                            help="file extension")
    
    parser.add_argument("--cores", "-c", type=int, default=5,
                            help="cores")

    parser.add_argument("--wsj_test", "-wt", action='store_true',
                            help="test on WSJ?")

    parser.add_argument("--print_mislabels", "-p", action='store_true',
                            help="output non-VB tags?")

    args = parser.parse_args()

    main(args)

