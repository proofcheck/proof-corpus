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

from nltk.tag.perceptron import PerceptronTagger, load
import nltk

from tagger import DEFAULT_TAGGER, write_tags, make_default_tagger, make_wsj_train, make_wsj_test

from load_tagged_sent import load_one_sent_tags, load_tags, is_sent
from load_ontonotes_pos import *

WSJ_TRAIN = make_wsj_train()
WSJ_TEST = make_wsj_test()

# Trains tagger on {5, 10, 50, 100, 500} random sentences from args.train
    # Prints accuracy, number of VBs mistakenly tagged as NPP, number of mislabelled tokens overall
    # for default and trained taggers 
    # Tests tagger on args.test and WSJ corpus

#random.seed(42)

def make_fixed_sents(lines, n=None, compare=[], output=None):
    # Creates a random list of n tagged sentences
    # Input: lines (unique lines from tagged file)
    #        number of random sentences
    #        list of tagged sentences (if we need to make sure there are no overlaps)
    
    if n:
        sampled_lines = random.sample(lines, n)
        
    else:
        sampled_lines = lines
    
    if output:
        with open(output, "a") as o:
            for lines in sampled_lines:
                o.write(lines)

    if compare == []:
        sents = [load_one_sent_tags(line)[1] for line in sampled_lines if is_sent(load_one_sent_tags(line)[1])]

    else:
        # compare the random sentences to ensure there are no overlapping sentences
        sents = [load_one_sent_tags(line)[1] for line in sampled_lines if line not in compare and is_sent(load_one_sent_tags(line)[1])]

        if n:
            while len(sents) < n:
                new_sent = random.sample(lines, 1)[0]
                new_tagged_sent = load_one_sent_tags(new_sent)[1]
                if new_sent not in sents and new_sent not in compare and is_sent(new_tagged_sent):
                    test_sents += new_tagged_sent
    
    return fix_NNP(sents)

def fix_NNP(tags):
    # changes the tag of the first word from to VB
    # input: list of tagged sentences
    for sent in tags:
        first_word = sent[0][0]
        sent[0] = first_word, 'VB'
    return tags



def num_mislabelings(confusion):
    # counts the number of mislabeled tokens from confusion matrix
    mislabelings = confusion._total - confusion._correct
    return mislabelings

def mislabeled_vb(confusion):
    i = confusion._indices['VB']
    sum_vb = sum(confusion._confusion[i]) - confusion['VB', 'VB']
    return sum_vb

def make_training_set(train_lines, train_num=None, sample_all=False, testing=[], output=None):
    if sample_all:
        training_set = make_fixed_sents(train_lines, train_num, testing, output)
        
    else:    
        training_set = []

        for lines_one_file in train_lines:
            training_set += make_fixed_sents(lines_one_file, train_num, testing, output)
    print(len(training_set))
    return training_set

def do_experiments(args):
    # Prints accuracy, number of VBs mistakenly tagged as NPP, number of mislabelled tokens overall
    # for default and trained taggers 
    # Tests tagger on args.test and WSJ corpus

    if args.save_sentences:
        save = args.output
    else:
        save = None
    
    if args.combine_wsj:
        print("Training on WSJ corpus and sampled sentences")
    wsj_train = args.combine_wsj
    

    if args.sample_all:
        print("Training on sentences sampled from all training files combined")
        train_lines = []
        for train_file in args.train:
            train_lines += train_file.readlines()
            train_file.close()
        
    else:
        print("Training on sentences extracted evenly from each file")
        train_lines = [train_file.readlines() for train_file in args.train]
        for train_file in args.train:
            train_file.close()

    nltk.data.clear_cache()
    default_tagger = DEFAULT_TAGGER


    training = make_training_set(train_lines, args.numtrain, sample_all=args.sample_all, output=save)
    
    trained_tagger = train_tagger(training, wsj_train=wsj_train)

    if args.compare_weights:
        compare_weights(default_tagger, trained_tagger, args.word, args.output)

    else:
        if args.test:
            for test_file in args.test:
                default_results, trained_results = do_one_basic_experiment(test_file, trained_tagger, default_tagger, args.numtest, training, save)
                print_results(default_results, trained_results, args.numtrain, args.output)

        default_results, trained_results = do_one_basic_experiment(None, trained_tagger, default_tagger, args.numtest, training, save)
        print_results(default_results, trained_results, args.numtrain, args.output)

def get_word_key(model_dict, word):
    word_key = [key for key in model_dict.keys() if word.lower() in key]
    return word_key

def compare_weights(default_tagger, trained_tagger, word, output=None):
    default_dict = default_tagger.model.weights
    #default_keys = get_word_key(default_dict, word)
    default_keys = default_dict.keys()
    trained_dict = trained_tagger.model.weights
    #trained_keys = get_word_key(trained_dict, word)
    trained_keys = trained_dict.keys()

    all_keys = set(default_keys + trained_keys)
    output_string = ""

    for key in all_keys:
        if key in default_dict.keys() and key in trained_dict.keys() and default_dict[key] != trained_dict[key]:
            output_string += key + "\t" + str(default_dict[key]) + "\t" + str(trained_dict[key]) + "\n"
        
        elif key in default_dict.keys() and key in trained_dict.keys() and default_dict[key] == trained_dict[key]:
            continue

        elif key in trained_dict.keys():
            output_string += key + "\t\t" + str(trained_dict[key]) + "\n"
        
        else:
            continue

        if output:
            with open(output, "a") as o:
                o.write(output_string)
            
        
        else:
            print(output_string)


def print_results(default_results, trained_results, num, output=None):
    
    print("Training on {} sentences from each file".format(num))
    print("Default vs Trained")
    print("Accuracy :\t{} \t{}".format(default_results[0], trained_results[0]))
    print("VB words tagged as NNP :\t{} \t{}".format(default_results[1], trained_results[1]))
    print("Mislabeled words overall :\t{} \t{}".format(default_results[2], trained_results[2]))

    print()

    if output:
        with open(output, "a") as o:
            o.write("\nTraining on {} sentences from each file\n".format(num))
            o.write("Default vs Trained\n")
            o.write("Accuracy :\t{} \t{}\n".format(default_results[0], trained_results[0]))
            o.write("VB words tagged as NNP :\t{} \t{}\n".format(default_results[1], trained_results[1]))
            o.write("Mislabeled words overall :\t{} \t{}\n".format(default_results[2], trained_results[2]))

def train_tagger(training, wsj_train=True, nr_iter=5):
    nltk.data.clear_cache()
    tagger = PerceptronTagger(load=False)
    print("training")
    if wsj_train:
        tagger.train(training + WSJ_TRAIN, nr_iter=nr_iter)
    else:
        tagger.train(training, nr_iter=nr_iter)
    print("done training")
    return tagger

def do_one_basic_experiment(test_file, trained_tagger, default_tagger, numtest=None, compare=[], output=None):
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
            # o.write("\nDefault\n")
            # o.write(default_confusion.pretty_format())
            # o.write("Trained tagger\n")
            # o.write(trained_confusion.pretty_format())

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
