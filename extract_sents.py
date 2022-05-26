#!/usr/bin/env python

import argparse
import nicer
from multiprocessing import Pool
from itertools import repeat

def results(args, results):
    results_text = "".join(results)
    if args.output:
        output = args.output
        output.write(results_text)
    
    else:
        print(results_text)
    
def extract_sents(fn, wordlist):
    ids, sentences = read_one(fn)
    if ids != []:
        sentences_with_id = zip(ids, sentences)
        filtered_sents = [s for s in sentences_with_id if (s[1].split())[0] in wordlist]
    else:
        filtered_sents = [s for s in sentences if s.split()[0] in wordlist]
    return filtered_sents

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
        wordlist = args.wordlist.readlines()

    if args.file:
        flat_result_list = extract_sents(args.file, wordlist)
        
    else:
        with Pool(processes=args.cores) as p:          
                    return_list = p.starmap(
                            extract_sents,
                            zip(args.list,
                                repeat(wordlist)
                            ),
                        1
                    )
                    flat_result_list = [e for sub_l in return_list for e in sub_l]
    if type(flat_result_list[0]) == str:
        results_text = flat_result_list
    else:
        flat_result_list.sort(key = lambda sentence_tup: sentence_tup[1])
        results_text = [s[0] + "\t" + s[1] for s in flat_result_list]
    results(args, results_text)

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

    





    
    
