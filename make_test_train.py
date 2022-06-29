#!/usr/bin/env python

import argparse
import nicer
import os
import nltk

from load_ontonotes_pos import *
from train_tagger import DEFAULT_TAGGER, mislabeled_vb, num_mislabelings, pick_sents, write_fixed_sents

PATH = "/mnt/research/proofcheck/noda/proof-corpus/word_bins/unique/"

def get_train_test_files(word_list_tags, num):
    word_list = [word.split('_')[0] for word in word_list_tags]
    train_word_list = word_list[:num]
    test_word_list = word_list[num:]
    path = PATH
    train_list = []
    test_list = []
    
    for (root, dirs, files) in os.walk(path):
        for f in files:
            verb = f.split(".")[0]
            if verb in train_word_list:
                train_list += [f]
            if verb in test_word_list:
                test_list += [f]
    return train_list, test_list

def make_training_from_bin(train_files, train_num, output, word_list=[], test_lines=[]): 
    training_set = []
    for train_file in train_files:
        path_to_file = PATH + train_file
        with open(path_to_file, "r") as f:
            f.seek(0)
            lines_one_file = f.read().splitlines()
            training_set += pick_sents(lines_one_file, n=train_num, compare=test_lines)
    return write_fixed_sents(training_set, output, word_list)

def make_testing_from_bin(test_files, output, word_list, train_lines=[]):
    testing_set = []
    num_lines_one_file = 5000 // len(test_files)

    for test_file in test_files:
        with open(PATH + test_file, "r") as f:
            lines_one_file = f.read().splitlines()
            if len(lines_one_file) < num_lines_one_file:
                num_lines_this_file = None
            else:
                num_lines_this_file = num_lines_one_file
            
            testing_set += pick_sents(lines_one_file, n=num_lines_this_file, compare=train_lines)
    
    return write_fixed_sents(testing_set, output, word_list) 

def make_train_test(args):
    word_list = args.word_list.read().splitlines()
    num_train_bins = len(word_list) - args.num_test_bins
    train_files, test_files = get_train_test_files(word_list, num_train_bins)

    save_test = "testing_set/" + args.test_extension + ".txt"

    if os.path.exists(save_test):
        print("Testing exists")
        return 0

    if not args.train: 
        save_train = "training_set/" + args.train_extension + ".txt"
    
        if os.path.exists(save_train):
            print("Training exists")
            return 0

        training = make_training_from_bin(train_files, args.num_train_sents, save_train, word_list)
        with open(save_train, "r") as train:
            fixed_training_lines = train.read().splitlines()
    else:
        fixed_training_lines = args.train.read().splitlines()
    
    testing = make_testing_from_bin(test_files, save_test, word_list, fixed_training_lines)

    nltk.data.clear_cache()
    default_tagger = DEFAULT_TAGGER
    default_confusion = default_tagger.confusion(testing)

    default_results = [default_tagger.accuracy(testing), 
                        default_confusion['VB', 'NNP'],
                        default_confusion['VBG', 'NNP'],
                        default_confusion['VB', 'NN'],
                        mislabeled_vb(default_confusion),
                        num_mislabelings(default_confusion),
                      ]
    
    output_default = "experiments/experiment_default_tagger_" + args.test_extension + ".txt"
    with open(output_default, "w") as o:
        str_results = list(map(str, default_results))
        o.write("\t".join(str_results))

def main(args):
    make_train_test(args)

if __name__ == '__main__':
    nicer.make_nice()
    parser = argparse.ArgumentParser()

    parser.add_argument("--train", "-tr",type=argparse.FileType('r'),
                            help="txt file to read training set")

    parser.add_argument("--num_train_sents", "-ntr",type=int, default=5,
                            help="number of training sentences")
    
    parser.add_argument("--num_test_bins", "-nte",type=int, default=1,
                            help="number of testing word bins")

    parser.add_argument("--train_extension", "-tr_e",
                            help="file extension")

    parser.add_argument("--test_extension", "-te_e",
                            help="file extension")
    
    parser.add_argument("--word_list", "-wl",type=argparse.FileType('r'),
                            help="txt file to read imperative verbs")


    args = parser.parse_args()

    main(args)