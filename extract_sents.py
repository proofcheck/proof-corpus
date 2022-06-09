#!/usr/bin/env python

import argparse
import nicer
from multiprocessing import Pool
from itertools import repeat

def results(args, ids, sentences):
    zipped = zip(ids, sentences)

    results_text = ["\t".join(results) for results in zipped]
    if args.output:
        output = args.output
        output.write("\n".join(results_text))
    
    else:
        print("\n".join(results_text))
    
def extract_sents(fn, wordlist):
    ids, sentences = read_one(fn)
    if ids != []:
        sentences_with_id = zip(ids, sentences)
        filtered_sents_with_id = [s for s in sentences_with_id if (s[1].split())[0] in wordlist]
        unzipped = zip(*filtered_sents_with_id)
        filtered_ids = list(unzipped[0])
        filtered_sents = list(unzipped[1])

    else:
        filtered_ids = []
        filtered_sents = [s for s in sentences if s.split()[0] in wordlist]
        
    return filtered_ids, filtered_sents

def read_one(fn):
    f = open(fn, "r")
    lines = f.readlines()
    ids = [l.split('\t')[0] for l in lines if "\t" in l]
    sents = [l.split('\t')[1]  if "\t" in l else l for l in lines]
    f.close()
    return ids, sents

def main(args):
    if args.word:
        wordlist = [args.word]
    else:
        wordlist = args.wordlist.read()
        wordlist = wordlist.split("\n")
        print(wordlist)

    if args.file:
        ids, sents = extract_sents(args.file, wordlist)
        
    else:
        with Pool(processes=args.cores) as p:          
                    return_list = p.starmap(
                            extract_sents,
                            zip(args.list,
                                repeat(wordlist)
                            ),
                        1
                    )
                    if len(return_list[0][0]) == 1:
                        ids = []
                        sents = [e for sub_l in return_list for e in sub_l]
                    else:
                        combined = list(zip(*return_list))
                        ids = [e for sub_l in combined[0] for e in sub_l]
                        sents = [e for sub_l in combined[1] for e in sub_l]

    results(args, ids, sents)

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

    
    parser.add_argument("--wordlist", "-wl", type=argparse.FileType('r'),
                            help="txt file to read word list from")
    
    parser.add_argument("--word", "-w", 
                            help="single word as word list")
    
    
    args = parser.parse_args()

    main(args)
    args.wordlist.close()
    args.output.close()
    





    
    
