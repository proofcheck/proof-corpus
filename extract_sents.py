#!/usr/bin/env python

"""Creates word bins for optimal tagger experiment. 
    Specifically, it extracts sentences that begin with words in word_file from tagged sentences.""" 

import argparse
import nicer
from multiprocessing import Pool
from itertools import repeat

from load_tagged_sent import load_one_sent_tags
from sent_tools import *

"""
Input :
    --files : tagged sentences (in tagged_sents/, output of tagger.py)
    --word_file : txt file containing word list to make bins (eg. optimal_tagger_extra/word_bin_list.txt)
        or 
    --word : the word itself as a string (eg. Note)
    (other arguments)

    Note : The word must be capitalized for both --word and in --word_list
           If this script is being run in order to make training/testing sets using make_test_train.py, 
           add the -u flag as make_test_train.py uses unique sentences (sentences in word_bins/unique) by default.

Output :
    txt files of sentences starting with specified word (in word_bins/ or word_bins/unique/)

    Output is saved in word_bins/ or word_bins/unique/ depending on whether the -u flag is used.
    The file name is automatically formatted to be the word (by which we're creating the word bin).
        file_name = "word_bins/" + word + args.extension + ".txt"
        file_name_unique = "word_bins/unique/" + word + args.extension + ".txt"
"""

"""
Typical usage :
    nohup python3 extract_sents.py -f tagged_sents/tagged_sentences_6_13.txt -w Enumerate -p 20 -u
"""

def check_first_word(sent, word):
    # Input: sentence with tags (connected by _ ), word
    # Returns sentence if the first word of the sentence is word
    sent_id, sent_tags = load_one_sent_tags(sent)
    if sent_tags[0][0] == word:
        return sent

def make_bins(args):
    # Extract sentences that begin with specified word from tagged file
    # Input: tagged file, word/words (file)
    if args.word:
        word_list = args.word.split()

    elif args.word_file:
        word_list = args.word_file.read().splitlines()
        args.word_file.close()
    
    if not args.extension:
        args.extension = ""
    
    with open(args.file, "r") as fd:
        lines = fd.readlines()

    for word in word_list:
        print(word)
        file_name = "word_bins/" + word + args.extension + ".txt"
        
        # Only keep unique sentences
        if args.unique:
            file_name_unique = "word_bins/unique/" + word + args.extension + ".txt"
            unique_sents = set()
            unique_output = open(file_name_unique, "w")

        with open(file_name, "w") as output:  
            with Pool(processes=args.cores) as p:          
                for ind, line in enumerate(p.starmap(
                    check_first_word,
                    zip(
                        lines,
                        repeat(word),
                        ),
                            50,
                    )):
                        if ind % 100000 == 0:
                            print(round(ind / len(lines) * 100, 2), "% done", sep="")

                        if line:
                            sent = line.split("\t")[1]
                            output.write(sent)
                            if args.unique:
                                if sent not in unique_sents:
                                    unique_sents.add(sent)
                                    unique_output.write(sent) 
                            
                if args.unique:
                    unique_output.close()
        
def main(args):
    make_bins(args)

if __name__ == '__main__':
    nicer.make_nice()
    parser = argparse.ArgumentParser()

    parser.add_argument("--file", "-f", 
                            help="txt file to read tags from")
    
    parser.add_argument("--output", "-o",
                            help="txt file to write results to")

    parser.add_argument( "--cores", "-p",
                            help="number of cores to use", type=int, default=4)
    
    parser.add_argument("--word", "-w", 
                            help="single word as word list")
    
    parser.add_argument("--extension", "-e", 
                            help="custom extension for filename")
    
    parser.add_argument("--word_file", "-wf", type=argparse.FileType('r'),
                            help="txt file to read word list from")
    
    parser.add_argument("--unique", "-u", action="store_true",
                            help="store unique sentences")

                            
    args = parser.parse_args()

    main(args)
    





    
    
