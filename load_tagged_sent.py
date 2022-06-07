#!/usr/bin/env python

import argparse
import nicer
from multiprocessing import Pool
from itertools import repeat

from nltk.probability import FreqDist

from nltk_tagger import proof_pos_tagger, write_tags

def results(args, dist):
    header_text = "\nTotal number of {} words that begin sentences: \n{}\n".format(args.tagger, dist.N())
    results_text = "\nWords tagged {} that begin sentences and their word count:\n".format(args.tagger)

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

def dist_output(dist, output):
    for x in dist.most_common():
        output.write(str(x[0]) + '  ' + str(x[1]))
        output.write("\n")
    output.write("\n")


def first_word_filter(fname, cores, tag, make_tag=False):
    # Returns list of first words of every sentence if the predicted pos tag is tag
    if make_tag:
        ids, tag_list = proof_pos_tagger(fname)
    else:
        ids, tag_list = load_tags(fname, cores)

    with Pool(processes=cores) as p:
            return_list = p.starmap(
                check_one_sent,
                zip(ids, 
                tag_list, 
                repeat(tag),
                ),
                1000,
            )
            print(return_list)
            all_tags = list(zip(*return_list))
            ids = all_tags[0]
            sents = all_tags[1]
            words = all_tags[2]
    
    word_dist = makedist(words)
    return ids, sents, word_dist

def check_one_sent(this_id, this_sent, tag):
    if this_sent[0][1] == tag:
        return this_id, this_sent, this_sent[0][1]


def load_one_sent(line):
    line = line.strip()
    if "\t" in line:
        this_id = line.split('\t')[0]
        sentence = line.split('\t')[1]
    else:
        this_id = ""
        sentence = line
    
    tags = [tuple(word.split('_')) for word in sentence.split(" ") ]

    # for word in tags:
    #     if "—" in word[0]:
    #         print(this_id)
    #         print(sentence)

    return this_id, tags

def load_tags(tagfile, cores=5):
    all_tags = []
    with Pool(processes=cores) as p:
            tags = p.imap(
                load_one_sent,
                tagfile.readlines(),
                1000,
            )
            all_tags = list(zip(*tags))
            ids = all_tags[0]
            sents = all_tags[1]
    tagfile.close()
    return ids, sents

def find_proof_tags(search_id, ids, tags):
    index_id = [ind for ind, this_id in enumerate(ids) if this_id == search_id]
    proof_tags = [tags[i] for i in index_id]
    return proof_tags

def main(args):
    # ids, sents = load_tags(args.file, args.cores)
    # this_id = "9203/alg-geom9203002"
    # tags = find_proof_tags(this_id, ids, sents)

    ids, sents, word_dist = first_word_filter(args.file, args.cores, args.tag)
    write_tags(ids, sents, args.output_sentences)
    args.output_wordlist.write("Words that begin sentences with the tag {}\n".format(args.tag))
    dist_output(word_dist, args.output_wordlist)

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
    
    
    args = parser.parse_args()

    main(args)
    args.file.close()




