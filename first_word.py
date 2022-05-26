#!/usr/bin/env python

import argparse
import nicer
from multiprocessing import Pool
from itertools import repeat

from nltk.probability import FreqDist
from nltk_tagger import read_one_tagger
from nltk.corpus import wordnet

def results(args, dist):
    if args.synset:
        if args.synset == "v":
            pos_word = "verbs"
        elif args.synset == "n":
            pos_word = "nouns"
        elif args.synset == "a":
            pos_word = "adjectives"
        elif args.synset == "r":
            pos_word = "adverbs"
        else:
            pos_word = "words with an unknown pos tag"

        header_text = "\nTotal number of {} that begin sentences: \n{}\n".format(pos_word, dist.N())
        results_text = "\nWords that have a {} sense that begin sentences and their word count:\n".format(pos_word)

    elif args.tagger:
        header_text = "\nTotal number of {} words that begin sentences: \n{}\n".format(args.tagger, dist.N())
        results_text = "\nWords tagged {} that begin sentences and their word count:\n".format(args.tagger)

    else:
        header_text = "\nTotal number of words that begin sentences: \n{}\n".format(dist.N())
        results_text = "\nWords tagged that begin sentences and their word count:\n"

    output = args.output
    output.write(header_text)
    output.write("\n")
    output.write(results_text)
    output.write("\n")
    for x in dist.most_common():
        output.write(str(x[0]) + '  ' + str(x[1]))
        output.write("\n")
    output.write("\n")

def makedist(word_list):
    # Converts word_list into Frequency Distribution
    dist = FreqDist()
    for l in word_list:
        dist.update(l)
    return dist

def first_word(fname):
    # Returns list of first words of every sentence
    f = open(fname, "r")
    sentences = f.readlines()
    first_words = []
    for sent in sentences:
        first_words += [sent.split()[0]]   
        
    return first_words

def first_word_filter(fname, tag):
    # Returns list of first words of every sentence if the predicted pos tag is tag
    tag_list = read_one_tagger(fname)
    filtered_word_list = [sent[0][0] for sent in tag_list if sent[0][1] == tag]
    return filtered_word_list

def first_word_pos(fname, pos):
    # Returns list of first words of every sentence if the word has a pos sense
    first_word_list = first_word(fname)
    first_word_pos_list = [w for w in first_word_list if pos_check(w, pos)]
    return first_word_pos_list

def pos_check(word, pos):
    # Checks if word has pos sense in synset
    pos_bool = False
    word_morphy = wordnet.morphy(word.lower())
    if word_morphy:
        synsets = wordnet.synsets(word_morphy)
        for syn in synsets:
            if syn.pos() == pos:
                pos_bool = True
                break
    return pos_bool

def main(args):
    if args.synset:
        func = first_word_pos
        if args.file:
            arg_file = [args.file, args.synset]
        else:
            arg_list = zip(args.list, repeat(args.synset),)
        
    elif args.tagger:
        func = first_word_filter
        if args.file:
            arg_file = [args.file, args.tagger]
        else:
            arg_list = zip(args.list, repeat(args.tagger),)

    else:
        func = first_word
        if args.file:
            arg_file = args.file
        else:
            arg_list = zip(args.list)

    if args.file:
        dist = makedist([func(*arg_file)])
        
    else:
        with Pool(processes=args.cores) as p:          
                    word_list = p.starmap(
                            func,
                            arg_list,
                        1
                    )
                    dist = makedist(word_list)
    if args.output:
        results(args, dist)
    else:
        print(dist.N())
        print(dist.most_common())

if __name__ == '__main__':
    nicer.make_nice()
    parser = argparse.ArgumentParser()

    parser.add_argument("--file", "-f",
                            help="txt file to read proof from")

    parser.add_argument("--list", "-l", nargs='*',
                            help="list of txt files to read proof from")
    
    parser.add_argument("--output", "-o", type=argparse.FileType('w'),
                            help="txt file to write results to")

    parser.add_argument( "--cores", "-c",
                            help="Number of cores to use", type=int, default=4)

    parser.add_argument("--tagger", "-t", default=None,
                            help="specifies pos tag (given by off the shelf tagger) to filter")
    
    parser.add_argument("--synset", "-s", default=None,
                            help="specifies pos tag to find based on synset")
    
    args = parser.parse_args()

    main(args)
    args.output.close()
    



