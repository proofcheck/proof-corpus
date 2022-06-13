#!/usr/bin/env python

import argparse
import nicer
from multiprocessing import Pool
from itertools import repeat

from nltk.probability import FreqDist
from first_word import make_dist

def dist_output(dist, output):
    # Writes distribution to output depending in order of frequency
    # Input : distribution, output file
    for x in dist.most_common():
        output.write(str(x[0]) + '  ' + str(x[1]))
        output.write("\n")
    output.write("\n")

def nnp_dist(tagfile, cores):
    # Creates distribution of words that begin sentenes and are taggged NNP
    ids, sents, dist = first_word_filter(tagfile, cores, "NNP")
    return dist

def first_word_filter(fname, cores, tag):
    # Returns list of first words of every sentence if the predicted pos tag is tag
    ids, tag_list = load_tags(fname, cores)

    with Pool(processes=cores) as p:
            return_list = p.starmap(
                check_one_sent_tag,
                zip(ids, 
                tag_list, 
                repeat(tag),
                ),
                1000,
            )
            all_tags = list(zip(*return_list))
            ids = all_tags[0]
            sents = all_tags[1]
            words = all_tags[2]
    
    word_dist = make_dist(words)
    return ids, sents, word_dist

def check_one_sent_tag(this_id, this_sent, tag):
    # Checks if first word of the sentence is tagged tag
    if this_sent[0][1] == tag:
        return this_id, this_sent, this_sent[0][1]

def load_one_sent_tags(line):
    # Loads one sentence of tags
    line = line.strip()
    if "\t" in line:
        this_id = line.split('\t')[0]
        sentence = line.split('\t')[1]
    else:
        this_id = ""
        sentence = line
    
    tags = [tuple(word.split('_')) for word in sentence.split(" ") ]
    return this_id, tags
    

def load_tags(tagfile, cores=5):
    # Loads tags from file of tagged sentences
    all_tags = []
    with Pool(processes=cores) as p:
            tags = p.imap(
                load_one_sent_tags,
                tagfile.readlines(),
                250,
            )
            all_tags = list(zip(*tags))
            ids = all_tags[0]
            sents = all_tags[1]
    tagfile.close()
    
    return ids, sents

def is_sent(sent):
    # Checks if the list (sentence) is actually a sentence
    for word in sent:
        if type(word) is not tuple or len(word) != 2:
            return False
    
    return True


def main(args):
    dist = nnp_dist(args.file, args.cores)
    dist_output(args, dist)
    

if __name__ == '__main__':
    nicer.make_nice()
    parser = argparse.ArgumentParser()

    parser.add_argument("--file", "-f",type=argparse.FileType("r"),
                            help="txt file to read proof/tags from")

    parser.add_argument("--output_sentences", "-os", type=argparse.FileType('w'),
                            help="txt file to write tagged sentences to")
    
    parser.add_argument("--output_wordlist", "-ow", type=argparse.FileType('w'),
                            help="txt file to write wordlist to")

    parser.add_argument( "--cores", "-c",
                            help="Number of cores to use", type=int, default=4)

    parser.add_argument("--tag", "-t", default=None,
                            help="specifies pos tag (given by off the shelf tagger) to filter")
    
    parser.add_argument("--output", "-o", type=argparse.FileType('w'),
                            help="txt file to write to")

    
    args = parser.parse_args()

    main(args)
    args.file.close()




