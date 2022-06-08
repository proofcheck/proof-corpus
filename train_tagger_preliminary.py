#!/usr/bin/env python

import argparse
import nicer
import random
import os
os.environ['OPENBLAS_NUM_THREADS'] = '1'

from nltk.tag.perceptron import PerceptronTagger
import nltk

from load_tagged_sent import load_one_sent
from load_ontonotes_pos import *



def make_fixed_sents(lines, n, compare=None):
    # Creates a random list of n tagged sentences
    # Input: lines (unique lines from tagged file)
    #        number of random sentences
    #        list of tagged sentences (if we need to make sure there are no overlaps)
    sampled_lines = random.sample(lines, n)
    if compare == None:
        sents = [load_one_sent(line)[1] for line in sampled_lines]

    else:
        # compare the random sentences to ensure there are no overlapping sentences
        sents = [load_one_sent(line)[1] for line in sampled_lines if line not in compare]
        while len(sents) < n:
            new_sent = random.sample(lines)
            new_tagged_sent = load_one_sent(new_sent)[1]
            if new_sent not in sents and new_sent not in compare:
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
    for sect in range(22, 25):
        #print(load_section(sect))
        sentences += load_section(sect)
    return sentences

def num_mislabelings(confusion):
    # counts 
    mislabelings = confusion._total - confusion._correct
    return mislabelings 

def do_one_experiment(training, testing):
    nltk.data.clear_cache()
    default_tagger = PerceptronTagger()
    default_confusion = default_tagger.confusion(testing)

    default_results = [default_tagger.accuracy(testing), 
                        default_confusion['VB', 'NNP'],
                        num_mislabelings(default_confusion),
                        ]

    nltk.data.clear_cache()
    training_list = list(training)
    trained_tagger = PerceptronTagger()
    trained_tagger.train(training_list)
    trained_confusion = trained_tagger.confusion(testing)

    trained_results = [trained_tagger.accuracy(testing), 
                        trained_confusion['VB', 'NNP'],
                        num_mislabelings(trained_confusion),
                        ]
    
    return default_results, trained_results


def do_experiments(args):
    train_lines = args.train.readlines()
    args.train.close()
    # set testing sentences
    # {suppose sentences, fix sentences, "non-math" (e.g., conll) sentences}
    #testing_sets = [make_fixed_sents(f, args.numtest) for f in args.test] + make_wsj_test()
    
    
    for f in args.test + ['WSJ']:
        if f == 'WSJ':
            testing = make_wsj_test()
            print(f)
        else:
            test_lines = f.readlines()
            f.close()
            testing = make_fixed_sents(test_lines, args.numtest)
            print(f.name)

        # for each testing set
        # try training on different number of sentences
        #  {5 suppose sentences, or 10, or 20, 50, 100, 500} 
        for train_num in [5, 10, 20, 50, 100, 500]:
            print("Training on {} sentences".format(train_num))
            print("Default vs Trained")
            training = make_fixed_sents(train_lines, train_num, compare=testing)
            default_results, trained_results = do_one_experiment(training, testing)
            print("Accuracy :\t{} \t{}".format(default_results[0], trained_results[0]))
            print("VB words tagged as NNP :\t{} \t{}".format(default_results[1], trained_results[1]))
            print("Mislabeled words overall :\t{} \t{}".format(default_results[2], trained_results[2]))

            print()
        print()
    
    

def main(args):
    #training, testing = create_train_test(args.train, args.test, args.numtrain, args.numtest)
    #train_imperative(training, testing)
    do_experiments(args)

if __name__ == '__main__':
    nicer.make_nice()
    parser = argparse.ArgumentParser()

    parser.add_argument("--train", "-tr",type=argparse.FileType('r'),
                            help="txt file to read training sentences from")
    
    parser.add_argument("--test", "-te", type=argparse.FileType('r'), nargs='*', default=None,
                            help="txt file to read testing sentences from")
    
    parser.add_argument("--numtrain", "-ntr",type=int, default=5,
                            help="number of training sentences")
    
    parser.add_argument("--numtest", "-nte",type=int, default=100,
                            help="number of testing sentences")
    

    parser.add_argument("--output", "-o",
                            help="txt file to write results to")

    args = parser.parse_args()

    main(args)


"""
python3 train_tagger.py -tr first_suppose.txt -te first_suppose.txt first_fixt.txt -nte 100

    output:

    first_suppose.tsv
    Training on 5 sentences
    Default vs Trained
    Accuracy :      0.8930581613508443      0.9765478424015009
    VB words tagged as NNP :        87      0
    Mislabeled words overall :      114     25

    Training on 10 sentences
    Default vs Trained
    Accuracy :      0.8930581613508443      0.9699812382739212
    VB words tagged as NNP :        87      3
    Mislabeled words overall :      114     32

    Training on 20 sentences
    Default vs Trained
    Accuracy :      0.8930581613508443      0.9784240150093808
    VB words tagged as NNP :        87      0
    Mislabeled words overall :      114     23

    Training on 50 sentences
    Default vs Trained
    Accuracy :      0.8930581613508443      0.9727954971857411
    VB words tagged as NNP :        87      0
    Mislabeled words overall :      114     29

    Training on 100 sentences
    Default vs Trained
    Accuracy :      0.8930581613508443      0.9624765478424016
    VB words tagged as NNP :        87      0
    Mislabeled words overall :      114     40

    Training on 500 sentences
    Default vs Trained
    Accuracy :      0.8930581613508443      0.9690431519699813
    VB words tagged as NNP :        87      0
    Mislabeled words overall :      114     33


    first_fix.tsv
    Training on 5 sentences
    Default vs Trained
    Accuracy :      0.9238805970149254      0.9798507462686568
    VB words tagged as NNP :        97      8
    Mislabeled words overall :      102     27

    Training on 10 sentences
    Default vs Trained
    Accuracy :      0.9238805970149254      0.9589552238805971
    VB words tagged as NNP :        97      36
    Mislabeled words overall :      102     55

    Training on 20 sentences
    Default vs Trained
    Accuracy :      0.9238805970149254      0.917910447761194
    VB words tagged as NNP :        97      76
    Mislabeled words overall :      102     110

    Training on 50 sentences
    Default vs Trained
    Accuracy :      0.9238805970149254      0.917910447761194
    VB words tagged as NNP :        97      97
    Mislabeled words overall :      102     110

    Training on 100 sentences
    Default vs Trained
    Accuracy :      0.9238805970149254      0.9119402985074627
    VB words tagged as NNP :        97      98
    Mislabeled words overall :      102     118

    Training on 500 sentences
    Default vs Trained
    Accuracy :      0.9238805970149254      0.9119402985074627
    VB words tagged as NNP :        97      77
    Mislabeled words overall :      102     118


    WSJ
    Training on 5 sentences
    Default vs Trained
    Accuracy :      0.8737085567374869      0.8726668004702239
    VB words tagged as NNP :        27      21
    Mislabeled words overall :      13214   13323

    Training on 10 sentences
    Default vs Trained
    Accuracy :      0.8737085567374869      0.8729630797755923
    VB words tagged as NNP :        27      23
    Mislabeled words overall :      13214   13292

    Training on 20 sentences
    Default vs Trained
    Accuracy :      0.8737085567374869      0.8734887366076975
    VB words tagged as NNP :        27      26
    Mislabeled words overall :      13214   13237

    Training on 50 sentences
    Default vs Trained
    Accuracy :      0.8737085567374869      0.8737659011191712
    VB words tagged as NNP :        27      27
    Mislabeled words overall :      13214   13208

    Training on 100 sentences
    Default vs Trained
    Accuracy :      0.8737085567374869      0.8727145874549608
    VB words tagged as NNP :        27      28
    Mislabeled words overall :      13214   13318

    Training on 500 sentences
    Default vs Trained
    Accuracy :      0.8737085567374869      0.8727623744396976
    VB words tagged as NNP :        27      26
    Mislabeled words overall :

"""