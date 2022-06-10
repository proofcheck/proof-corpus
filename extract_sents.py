#!/usr/bin/env python

import argparse
import nicer
from multiprocessing import Pool
from itertools import repeat

from load_tagged_sent import load_one_sent

def results(args, ids, sentences):
    zipped = zip(ids, sentences)

    results_text = ["\t".join(results) for results in zipped]
    if args.output:
        output = args.output
        output.write("\n".join(results_text))
    
    else:
        print("\n".join(results_text))
    
def extract_sents(fn, word):
    ids, sentences = read_one(fn)
    if ids != []:
        sentences_with_id = zip(ids, sentences)
        filtered_sents_with_id = [s for s in sentences_with_id if (s[1].split())[0] == word]
        unzipped = zip(*filtered_sents_with_id)
        filtered_ids = list(unzipped[0])
        filtered_sents = list(unzipped[1])

    else:
        filtered_ids = []
        filtered_sents = [s for s in sentences if s.split()[0] == word]
        
    return filtered_ids, filtered_sents


def read_one(fn):
    f = open(fn, "r")
    lines = f.readlines()
    ids = [l.split('\t')[0] for l in lines if "\t" in l]
    sents = [l.split('\t')[1]  if "\t" in l else l for l in lines]
    f.close()
    return ids, sents

def check_one_sent(sent, word):
    sent_id, sent_tags = load_one_sent(sent)
    if sent_tags[0][0] == word:
        return sent

def extract_sents_from_lines(args):
    if args.word:
        word_list = args.word.split()

    elif args.word_file:
        word_list = args.word_file.read().splitlines()
        args.word_file.close()
    
    if not args.extension:
        args.extension = ""

    for word in word_list:
        file_name = "word_bins/unique" + word + args.extension + ".txt"
        unique_sents = set()
        with open(args.file, "r") as fd:
            with open(file_name, "w") as output:
                with Pool(processes=args.cores) as p:          
                    for line in p.starmap(
                        check_one_sent,
                        zip(
                            fd.readlines(),
                            repeat(word),
                            ),
                                50,
                        ):
                            if line:
                                sent = line.split("\t")[1]
                                if sent not in unique_sents:
                                    unique_sents.add(sent)
                                    output.write(sent)

def previous_main(args):
    if args.word:
        word_list = [args.word]

    else:
        word_list = args.wordlist.read()
        word_list = args.wordlist.split("\n")
        print(word_list)
    if args.file:
        ids, sents = extract_sents(args.file, word_list)
        
    else:
        
        with Pool(processes=args.cores) as p:          
                            return_list = p.starmap(
                                    extract_sents,
                                    zip(args.list,
                                        repeat(word_list)
                                    ),
                                1000
                            )
                            if len(return_list[0][0]) == 1:
                                ids = []
                                sents = [e for sub_l in return_list for e in sub_l]
                            else:
                                combined = list(zip(*return_list))
                                ids = [e for sub_l in combined[0] for e in sub_l]
                                sents = [e for sub_l in combined[1] for e in sub_l]

    if args.output:
        args.output.close()
    if args.wordlist:
        args.wordlist.close()

def main(args):
    extract_sents_from_lines(args)

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
                            help="number of cores to use", type=int, default=4)
    
    parser.add_argument("--word", "-w", 
                            help="single word as word list")
    
    parser.add_argument("--extension", "-e", 
                            help="custom extension for filename")
    
    parser.add_argument("--word_file", "-wf", type=argparse.FileType('r'),
                            help="txt file to read word list from")
    
    
    args = parser.parse_args()

    main(args)
    





    
    
