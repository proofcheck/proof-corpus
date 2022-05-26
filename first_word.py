#!/usr/bin/env python

import argparse
import nicer
from multiprocessing import Pool
from itertools import repeat

from nltk.tokenize.destructive import NLTKWordTokenizer
from nltk.probability import FreqDist
from nltk_tagger import read_one_tagger
from nltk.corpus import wordnet

word_tokenizer = NLTKWordTokenizer()

def results(args, dist):
    if args.verbs:
        header_text = "\nTotal number of verbs that begin sentences: \n{}\n".format(dist.N())
        results_text = "\nVerbs tagged that begin sentences with their word count:\n"

    elif args.tag:
        header_text = "\nTotal number of {} words that begin sentences: \n{}\n".format(args.tag, dist.N())
        results_text = "\nWords tagged {} that begin sentences with their word count:\n".format(args.tag)

    else:
        header_text = "\nTotal number of words that begin sentences: \n{}\n".format(dist.N())
        results_text = "\nWords tagged that begin sentences with their word count:\n"

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
        first_words += [word_tokenizer.tokenize(sent)[0]]   
        
    return first_words

def first_word_filter(fname, tag):
    # Returns list of first words of every sentence if the pos tag is tag
    tag_list = read_one_tagger(fname)
    first_word_list = [sent[0] for sent in tag_list]
    filtered_word_list = [w for w,t in first_word_list if t == tag]

    #first_word_tag_list = []

    """
    first_word_tag_list = [w for sent in tag_list
    w,t in sent[0] if t == tag for sent in tag_list]
    """

    # for sent in tag_list:
    #     first_word = sent[0][0]
    #     first_word_tag = sent[0][1]
    #     if first_word_tag == tag:         
    #         first_word_tag_list += [first_word]
    #return first_word_tag_list
    return filtered_word_list

def first_word_verbs(fname):
    # Returns list of first words of every sentence if the word has a verb sense
    first_word_list = first_word(fname)
    first_word_verb_list = [w for w in first_word_list if verb_check(w)]
    return first_word_verb_list
    
def verb_check(word):
    # Checks if word has verb sense
    verb_bool = False
    word_morphy = wordnet.morphy(word.lower())
    if word_morphy:
        synsets = wordnet.synsets(word_morphy)
        for syn in synsets:
            if syn.pos() == "v":
                verb_bool = True
                break

    return verb_bool

def main(args):
    if args.verbs:
        func = first_word_verbs
        arg_file = args.file
        arg_list = zip(args.list)
        
    elif args.tag:
        func = first_word_filter
        arg_file = [args.file, args.tag]
        arg_list = zip(args.list, repeat(args.tag),)

    else:
        func = first_word
        arg_file = args.file
        arg_list = zip(args.list)

    if args.file:
        dist = makedist([func(*arg_file)])
        # dist = makedist([first_word(args.file)])
        # dist_v = makedist([first_word_verbs(args.file)])
        # dist_nnp = makedist([first_word_filter(args.file, "NNP")])
        
    else:
        with Pool(processes=args.cores) as p:          
                    word_list = p.starmap(
                            func,
                            arg_list,
                        1
                    )
                    dist = makedist(word_list)

    results(args, dist)

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

    parser.add_argument("--tag", "-t", default=None,
                            help="specifies pos tag (given by off the shelf tagger) to filter")
    
    parser.add_argument("--verbs", "-v", default=None,
                            help="specifies pos tag (given by off the shelf tagger) to filter")
    


    args = parser.parse_args()

    main(args)

