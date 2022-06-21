#!/usr/bin/env python

import argparse
from nltk.tag.perceptron import PerceptronTagger
import nicer
from multiprocessing import Pool
import sys
import pickle

from sent_tools import *
from load_tagged_sent import load_tags
from load_ontonotes_pos import *

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

def make_default_tagger():
    # Creates default tagger by training on WSJ
    file_path = "default_tagger.pk"
    try:
        with open(file_path, "rb") as resource:
            default_tagger = pickle.load(resource)

    except FileNotFoundError:
        with open(file_path, "wb") as resource:
            default_tagger = PerceptronTagger(load=False)
            default_tagger.train(make_wsj_train())
            pickle.dump(default_tagger, resource)

    return default_tagger

DEFAULT_TAGGER = make_default_tagger()

def sent_tagger(line):
    # input: one line from sent**.tsv
    # returns: id, tagged sentence
    sent_id, sent = split_sentence_id(line)
    tokenized = tokenize(sent)
    tagged = DEFAULT_TAGGER.tag(tokenized)
    return sent_id, tagged

def write_tags(ids, sents, output=None): 
    for i in range(len(sents)):
        save_sent = ""
        if ids != []:
            this_id = ids[i]
            save_sent += this_id
            save_sent += "\t"
        words = ["_".join(word) for word in sents[i]]
        save_sent += " ".join(words)
        save_sent += "\n"
        if output:
            output.write(save_sent)
        else:
            print(save_sent)
            print()

def main(args):
    # input must be sent**.tsv
    for fd in args.files:
        print(fd)
        if args.cores > 20:
            args.cores = 20
        with Pool(processes=args.cores) as p:
            sent_tuples = p.imap(
                sent_tagger,
                fd.readlines(),
                250,
            )
                
            sent_ids, sents = zip(*sent_tuples)
            
            if args.test == False:
                write_tags(sent_ids, sents, args.output)
                
            else:
                write_tags(sent_ids, sents)
                    
    if args.output:
        args.output.close()
                        
if __name__ == '__main__':
    nicer.make_nice()
    parser = argparse.ArgumentParser()

    parser.add_argument("--files", "-f", nargs='*',type=argparse.FileType("r"), default=[sys.stdin],
                            help="list of txt files to read proof from")
    
    parser.add_argument("--output", "-o", type=argparse.FileType("w"),
                            help="txt file to write results to")

    parser.add_argument( "--cores", "-c",
                            help="Number of cores to use", type=int, default=4)

    parser.add_argument( "--test", "-t",
                            help="test", action="store_true")

    args = parser.parse_args()
    main(args)
    
