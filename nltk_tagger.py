#!/usr/bin/env python
import argparse
from nltk.tag import pos_tag_sents
from nltk.tag.perceptron import PerceptronTagger
import nicer
from multiprocessing import Pool
from itertools import repeat

tagger = PerceptronTagger()

def read_one_tagger(fname):
    f = open(fname, "r")
    sentences = f.readlines()
    tokenized = [(s.split('\t')[-1]).split() for s in sentences]
    f.close()
    tagged = [tagger.tag(sent) for sent in tokenized]
    return tagged

def read_one(fn):
    f = open(fn, "r")
    lines = f.readlines()
    f.close()
    return lines

def save_tag(fname):
    output = fname.split('/')[-1] 
    output = output.split('.')[0] + "_tag.txt"
    tagged = read_one_tagger(fname)
    o = open(output, "w")
    o.write(str(tagged))
    o.close()

def main(args):
    if args.file:
        save_tag(args.file)
        
    else:
        with Pool(processes=args.cores) as p:          
                    return_list = p.starmap(
                            save_tag,
                            zip(args.list
                            ),
                        1
                    )


if __name__ == '__main__':
    nicer.make_nice()
    parser = argparse.ArgumentParser()

    parser.add_argument("--file", "-f",
                            help="txt file to read proof from")

    parser.add_argument("--list", "-l", nargs='*',
                            help="list of txt files to read proof from")
    

    parser.add_argument( "--cores", "-c",
                            help="Number of cores to use", type=int, default=4)

    
    
    args = parser.parse_args()

    main(args)
    