#!/usr/bin/env python

import argparse
from nltk.tag.perceptron import PerceptronTagger
import nicer
from multiprocessing import Pool
from sentize2 import sentize_proof
import sys

tagger = PerceptronTagger()

def sent_tagger(line):
    sent_id, sent = split_sentence_id(line)
    tokenized = [sent.split() for sent in sent]
    tagged = tagger.tag(tokenized)
    return sent_id, tagged

def proof_pos_tagger(line):
    # input: one line from proofs**.txt (one proof)
    # returns: ids, tagged sentence
    lines = sentize_proof(line)
    ids, sents = split_sentence_id(lines)
    tokenized = [sent.split() for sent in sents]
    lengths = [len(sent) for sent in tokenized]
    flat_tokenized = [e for sub_l in tokenized for e in sub_l]
    tagged = tagger.tag(flat_tokenized)
    tagged_sent = []
    now_sent = []
    count = 0
    for length in lengths:
        if tagged == []:
            break
        else:
            now_sent = tagged[:length]
            tagged_sent += [now_sent]
            tagged = tagged[length:]
    return ids, tagged_sent
    
def split_sentence_id(lines):
    # splits ids and rest of text
    # input: list of lines
    # output: ids, text
    ids = [line.split("\t")[0] for line in lines if "\t" in line]
    sents = [line.split("\t")[1] if "\t" in line else line for line in lines ]
    return ids, sents

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
    # input must be proof.tsv
    for fd in args.files:
        print(fd)
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
    
