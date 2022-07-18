#!/usr/bin/env python

"""Creates word bins for optimal tagger experiment. (Extracts sentences and tags that begin with words in word_file from tagged sentences.)""" 

import argparse
import nicer
from multiprocessing import Pool
from itertools import repeat

from load_tagged_sent import load_one_sent_tags
from sent_tools import *

"""
Typical usage:
    nohup python3 extract_sents.py -f tagged_sentences/tagged_sentences_6_13.txt -w Enumerate -c 20 -u

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
    
    parser.add_argument("--output", "-o", type=argparse.FileType('w'),
                            help="txt file to write results to")

    parser.add_argument( "--cores", "-c",
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
    





    
    
