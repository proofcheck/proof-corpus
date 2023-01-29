#!/usr/bin/env python

"""Main experiment script for finding the optimal tagger that tags imperative verbs accurately."""

import argparse

import nicer
from multiprocessing import Pool
from itertools import repeat
import pickle
from nltk.metrics import ConfusionMatrix

from load_ontonotes_pos import *
from train_tagger import WSJ_TEST, DEFAULT_TAGGER, mislabeled_vb, num_mislabelings, train_tagger
from tagger import untag_sent_to_tokens
from load_tagged_sent import load_tag_lines

"""
Input :
    --training_set : training set (txt file in training_set/)
    --testing_set : testing set (txt file in testing_set/)
    (other arguments)

    Both training and testing sets are "correctly" tagged.
    They can be outputs of make_test_train.py but note that make_test_train only "corrects" the first word, according to the word list.

Output :
    txt file of results (in experiments/)
    (depending on flags used) pickled taggers (in tagger/)

    The file name is formatted automatically depending on the parameters
        output_test = "experiments/experiment_" + str(num_train_sent) + "sents_" + str(nr_iter) + "iters_" + extension + ".txt"

    If the -d flag is added, the taggers are dumped for future use (use dumped_main_experiment.py)
        The file name is formatted automatically (similar to the results, but with the trial ID added at the end)
            output_dump = "tagger/" + str(num_train_sent) + "sents_" + str(nr_iter) + "iters_" + extension + "_" + str(trial_id) + ".pk"

How to read results :
    (Differs slightly depending on when the experiment was done)
    If there are 4 numbers : accuracy
                            \t# of VBs mislabeled as NNP
                            \t# of VBs mislabeled
                            \t# of mislabellings

    Otherwise :             accuracy
                            \t# of VBs mislabeled as NNP
                            \t# of VBGs mislabeled as NNP
                            \t# of VBs mislabeled as NN
                            \t# of NNs mislabeled as JJ
                            \t# of NNs mislabeled as VB
                            \t# of NNSs mislabeled as VBZ
                            \t# of JJ mislabeled as NN
                            \t# of RB mislabeled as NN
                            \t# of VBs mislabeled
                            \t# of mislabellings
"""

"""
Typical usage :
    nohup python3 main_experiment.py -tr training_set/optimal_handtagged.txt -te testing_set/optimal_handtagged3.txt -e optimal3 -p 25 -nt 50 -tnl 2 -inl 5 -wt -d -dr 
"""

def save_results(results, output):
    with open(output, "w") as o:
        result_string = ""

        sorted_results = [results[0]] + sorted(results[1:], key=lambda x: int(x[0].split("trial")[-1]))
        for trial in sorted_results:
            str_trial = [str(item) if type(item) is not str else item for item in trial]
            result_string += "\t".join(str_trial) + "\n"            
        o.write(result_string)

def get_first_n_confusion(testing, tagger, n=3):
    # Compare tag of first n words only
    golden_tags = []
    trained_tags = []

    for golden in testing:
        tokenized = untag_sent_to_tokens(golden)
        trained = tagger.tag(tokenized)
        first_n_golden = [golden[i][1] for i in range(min(n, len(golden)))]
        first_n_trained = [trained[i][1] for i in range(min(n, len(trained)))]

        golden_tags += first_n_golden
        trained_tags += first_n_trained

    confusion = ConfusionMatrix(golden_tags, trained_tags)
    return confusion

def get_first_three_confusion(testing, tagger):
    # Compare tag of first three words only.
    return get_first_n_confusion(testing, tagger, 3)

def get_one_trial_results(testing, tagger, trial_id, dump_file=None, tag_n=3):
    if not tag_n:
        trained_confusion = tagger.confusion(testing)

    else:
        trained_confusion = get_first_n_confusion(testing, tagger, tag_n)
    trained_results = [ trial_id,
                        tagger.accuracy(testing), 
                        get_confusion_results(trained_confusion, ['VB', 'NNP']),
                        get_confusion_results(trained_confusion, ['VBG', 'NNP']),
                        get_confusion_results(trained_confusion, ['VB', 'NN']),
                        get_confusion_results(trained_confusion, ['NN', 'JJ']),
                        get_confusion_results(trained_confusion, ['NN', 'VB']),
                        get_confusion_results(trained_confusion, ['NNS', 'VBZ']),
                        get_confusion_results(trained_confusion, ['JJ', 'NN']),
                        get_confusion_results(trained_confusion, ['RB', 'NN']),
                        mislabeled_vb(trained_confusion),
                        num_mislabelings(trained_confusion),
                    ]
    if dump_file:
        dump_file = dump_file + "_" + str(trial_id) + ".pk"
        with open(dump_file, "wb") as resource:
            pickle.dump(tagger, resource)

    return trained_results

def do_experiments(args):
    train_num_list = [int(num) for num in args.train_num_list.split(",")]
    iter_num_list = [int(num) for num in args.iter_num_list.split(",")]
    
    training_lines = args.train.read().splitlines()
    training_loaded = load_tag_lines(training_lines)[1]
    num_lines_verb = train_num_list[-1]
    training_set = [training_loaded[x:x+num_lines_verb] for x in range(0, len(training_lines), num_lines_verb)]
    
    testing_lines = args.test.read().splitlines()
    testing = load_tag_lines(testing_lines)[1]

    if args.default_results:
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
        output_default = "experiments/experiment_default_tagger_" + args.extension + ".txt"
        with open(output_default, "w") as o:
            str_results = list(map(str, default_results))
            o.write("\t".join(str_results))

    train_num_list_zip = train_num_list*len(iter_num_list)
    iter_num_list_zip = [num for num in iter_num_list for i in range(len(train_num_list))]
    zipped_args = zip(train_num_list_zip, iter_num_list_zip)

    for arg in zipped_args:
        do_one_condition(testing, training_set, arg, args.extension, 
                            args.num_trials, args.wsj_test, args.cores, 
                            args.print_mislabels, args.dump, args.tag_n)

    args.train.close()
    args.test.close()

def do_one_condition(testing, training_set, zipped_arg, extension="", num_trials=10, wsj_test=False, cores=5, print_mislabels=False, dump=False, tag_n=3): 
    num_train_sent, nr_iter = zipped_arg
    training = []
    for imperative_verb in training_set:
        training += imperative_verb[:num_train_sent]

    if dump:
        output_dump = "tagger/" + str(num_train_sent) + "sents_" + str(nr_iter) + "iters_" + extension

    else:
        output_dump = None

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
                [training]*num_trials,
                [nr_iter]*num_trials,
                [testing]*num_trials,
                list(range(1, num_trials+1)),
                [wsj_test]*num_trials,
                repeat(print_mislabels),
                repeat(output_dump),
                repeat(tag_n)
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

def do_one_trial(training, nr_iter, testing, trial_id=None, wsj_test=False, print_mislabels=False, dump_file=None, tag_n=3):
    trained_tagger = train_tagger(training, nr_iter)
    trial_id = "trial" +  str(trial_id)
    trained = get_one_trial_results(testing, trained_tagger, trial_id, dump_file, tag_n)

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

def get_confusion_results(confusion, mislabel_pair):
    try:
        return confusion[mislabel_pair]

    except KeyError:
        return None

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
    
    parser.add_argument("--cores", "-p", type=int, default=5,
                            help="cores")

    parser.add_argument("--num_trials", "-nt", type=int, default=10,
                            help="number of trials")
    
    parser.add_argument("--train_num_list", "-tnl", default="5,10",
                            help="number of sentences to train on (list in string format)")

    parser.add_argument("--iter_num_list", "-inl", default="5,10",
                            help="number of iterations (list in string format)")

    parser.add_argument("--wsj_test", "-wt", action='store_true',
                            help="test on WSJ?")

    parser.add_argument("--print_mislabels", "-p", action='store_true',
                            help="output non-VB tags?")

    parser.add_argument("--dump", "-d", action='store_true',
                            help="dump tagger?")
    
    parser.add_argument("--tag_n", "-tn", type=int, default=None,
                            help="number of words to tag in each sentence (first n)")

    parser.add_argument("--default_results", "-dr", action='store_true',
                            help="rewrite default results?")

    args = parser.parse_args()

    main(args)

