#!/usr/bin/env python

import argparse
import nicer
import random
from multiprocessing import Pool
from itertools import repeat
import pickle
import os
os.environ['OPENBLAS_NUM_THREADS'] = '1'

from nltk.tag.perceptron import PerceptronTagger, load
import nltk

from nltk_tagger import write_tags
from load_tagged_sent import load_one_sent, load_tags, is_sent
from load_ontonotes_pos import *

# Trains tagger on {5, 10, 50, 100, 500} random sentences from args.train
    # Prints accuracy, number of VBs mistakenly tagged as NPP, number of mislabelled tokens overall
    # for default and trained taggers 
    # Tests tagger on args.test and WSJ corpus

#random.seed(42)

def make_default_tagger():
    file_path = "default_tagger.pickle"
    try:
        with open(file_path, "rb") as resource:
            default_tagger = pickle.load(resource)

    except FileNotFoundError:
        with open(file_path, "wb") as resource:
            default_tagger = PerceptronTagger(load=False)
            default_tagger.train(make_wsj_train())
            pickle.dump(default_tagger, resource)

    return default_tagger

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
            o.write("\n")
            for lines in sampled_lines:
                o.write(lines)

    if compare == []:
        sents = [load_one_sent(line)[1] for line in sampled_lines if is_sent(load_one_sent(line)[1])]

    else:
        # compare the random sentences to ensure there are no overlapping sentences
        sents = [load_one_sent(line)[1] for line in sampled_lines if line not in compare and is_sent(load_one_sent(line)[1])]

        if n:
            while len(sents) < n:
                new_sent = random.sample(lines, 1)[0]
                new_tagged_sent = load_one_sent(new_sent)[1]
                if new_sent not in sents and new_sent not in compare and is_sent(new_tagged_sent):
                    test_sents += new_tagged_sent
    
    return fix_NNP(sents)

def fix_NNP(tags):
    # changes the tag of the first word from NNP to VB
    # input: list of tagged sentences
    for sent in tags:
        first_word = sent[0][0]
        sent[0] = first_word, 'VB'
    return tags

def make_wsj_test():
    # creates testing set of "normal sentences" from WSJ
    sentences = []
    file_path = "wsj_test.txt"

    try:
        with open(file_path, "r") as resource:
            sentences = list(load_tags(resource, cores=50)[1])
            print("loaded")

    except FileNotFoundError:
        
        with Pool(processes=3) as p:
                for loaded_section in p.imap(
                    load_section,
                    range(22, 25),
                    1000,
                ):
                    sentences.extend(loaded_section)
        output = open(file_path, "w")
        write_tags([], sentences, output)

    return sentences

def make_wsj_train():
    # creates training set from WSJ
    sentences = []
    file_path = "wsj_train.txt"

    try:
        with open(file_path, "r") as resource:
            sentences = list(load_tags(resource, cores=50)[1])

    except FileNotFoundError:
        with Pool(processes=18) as p:
                for loaded_section in p.imap(
                    load_section,
                    range(0, 19),
                    1000,
                ):
                    sentences.extend(loaded_section)

        output = open(file_path, "w")
        write_tags([], sentences, output)

    return sentences

def num_mislabelings(confusion):
    # counts the number of mislabeled tokens from confusion matrix
    mislabelings = confusion._total - confusion._correct
    return mislabelings 

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
        wsj_train = make_wsj_train()
    
    else:
        wsj_train = []

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
    default_tagger = make_default_tagger()


    training = make_training_set(train_lines, args.numtrain, sample_all=args.sample_all, output=save)
    
    trained_tagger = train_tagger(training, wsj_train)

    if args.test:
        for test_file in args.test:
            default_results, trained_results = do_one_experiment(test_file, trained_tagger, default_tagger, args.numtest, training, save)
            print_results(default_results, trained_results, args.numtrain, args.output)

    default_results, trained_results = do_one_experiment(None, trained_tagger, default_tagger, args.numtest, training, save)
    print_results(default_results, trained_results, args.numtrain, args.output)


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

def train_tagger(training, wsj_train):
    nltk.data.clear_cache()
    tagger = PerceptronTagger(load=False)
    print("training")
    tagger.train(training + wsj_train)
    print("done training")
    return tagger

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

    args = parser.parse_args()

    main(args)
