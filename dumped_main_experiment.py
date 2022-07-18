#!/usr/bin/env python

"""Test dumped taggers on sentences and return accuracy, # of mislabelled tags etc"""

import argparse
import nicer
from multiprocessing import Pool
from itertools import repeat
import pickle

from load_ontonotes_pos import *
from train_tagger import WSJ_TEST, DEFAULT_TAGGER, mislabeled_vb, num_mislabelings
from tagger import untag_sent_to_tokens
from load_tagged_sent import load_tag_lines
from main_experiment import save_results, get_one_trial_results, get_first_n_confusion, get_confusion_results

"""
Typical usage:
    nohup python3 dumped_main_experiment.py -ta tagger/7_5/*.pk -te testing_set/refer_handtagged.txt -e refer -c 25 -tn 3

Test on WSJ_TEST (output is in separate file):
    nohup python3 dumped_main_experiment.py -ta tagger/7_5/*.pk -te testing_set/refer_handtagged.txt -e refer -c 25 -wt -tn 3

"""

PATH = "word_bins/unique/"

def do_dumped_experiments(args):
    testing_lines = args.test.read().splitlines()
    testing = load_tag_lines(testing_lines)[1]
       
    args.test.close()

    # Get testing/training conditions for automatically formatting output filename
    conditions = "_".join(args.tagger[0].split("/")[-1].split(".")[0].split("_")[:-1]) + "_"

    if args.wsj_test:
        output_wsj = "experiments/experiment_" + conditions + args.extension + "-wsj.txt"
        trained_results_wsj = []

    output_test = "experiments/experiment_" + conditions + args.extension + ".txt"
    
    trained_results_wsj = []
    trained_results = []

    # default tagger results
    default_tagger = DEFAULT_TAGGER
    if not args.tag_n:
        default_confusion = default_tagger.confusion(testing)
    else:
        default_confusion = get_first_n_confusion(testing, default_tagger, args.tag_n)
        
    default_results = ["default", default_tagger.accuracy(testing), 
                        get_confusion_results(default_confusion, ['VB', 'NNP']),
                        get_confusion_results(default_confusion, ['VBG', 'NNP']),
                        get_confusion_results(default_confusion, ['VB', 'NN']),
                        get_confusion_results(default_confusion, ['NN', 'JJ']),
                        get_confusion_results(default_confusion, ['NN', 'VB']),
                        get_confusion_results(default_confusion, ['NNS', 'VBZ']),
                        get_confusion_results(default_confusion, ['JJ', 'NN']),
                        get_confusion_results(default_confusion, ['RB', 'NN']),
                        mislabeled_vb(default_confusion),
                        num_mislabelings(default_confusion),
                      ]

    trained_results += [default_results]
    mislabellings = []
    
    # Do experiment for all taggers
    with Pool(processes=args.cores) as p:
        for trained, wsj, mislabeled in p.starmap(
            do_dumped_trial,
            zip(
                args.tagger,
                repeat(testing),
                repeat(args.wsj_test),
                repeat(args.print_mislabels),
                repeat(args.tag_n),
            ),
            1,
        ):
            if args.wsj_test:
                trained_results_wsj += [wsj]

            if args.print_mislabels:
                mislabellings += [mislabeled]

            trained_results += [trained]
    
    # Save results for all taggers in output file
    save_results(trained_results, output_test)
    
    if args.wsj_test:
        save_results(trained_results_wsj, output_wsj)

    if args.print_mislabels:
        output_mislabels = "experiments/experiment_" + conditions + args.extension + "_mislabels" + ".txt"
        output_string = "\n".join(mislabellings)
        with open(output_mislabels, "w") as o:
            o.write(output_string)

def do_dumped_trial(tagger_file, testing, wsj_test=False, print_mislabels=False, tag_n=3):
    """Do experiment for one tagger"""
    with open(tagger_file, "rb") as resource:
        trained_tagger = pickle.load(resource)

    trial_id = tagger_file.split("/")[-1].split(".")[0].split("_")[-1]
    trained = get_one_trial_results(testing, trained_tagger, trial_id, tag_n=tag_n)

    if print_mislabels:
        output_string = ""
        for sent in testing:
            tokens = untag_sent_to_tokens(sent)
            tags = trained_tagger.tag(tokens)
            if tags[0][1] not in {'VB', 'VBG', 'VBN'}:
                output_string += " ".join(tokens) + "\t" + tags[0][1] + "\n"
            
        output_string += "----------------\n"

    else:
        output_string = None
            
    if wsj_test:
        wsj = get_one_trial_results(WSJ_TEST, trained_tagger, trial_id, tag_n=None)

    else:
        wsj = None

    return trained, wsj, output_string

def main(args):
    do_dumped_experiments(args)

if __name__ == '__main__':
    nicer.make_nice()
    parser = argparse.ArgumentParser()

    parser.add_argument("--tagger", "-ta", nargs="*",
                            help="txt files to read tagger")

    parser.add_argument("--test", "-te",type=argparse.FileType('r'),
                            help="txt file to read testing set")
    
    parser.add_argument("--extension", "-e",
                            help="file extension for output")
    
    parser.add_argument("--cores", "-c", type=int, default=5,
                            help="cores")

    parser.add_argument("--wsj_test", "-wt", action='store_true',
                            help="test on WSJ?")

    parser.add_argument("--print_mislabels", "-p", action='store_true',
                            help="output non-VB tags?")

    parser.add_argument("--tag_n", "-tn", type=int, default=None,
                            help="number of words to tag in each sentence (first n)")

    args = parser.parse_args()

    main(args)

