#!/usr/bin/env python

"""Finds common n-word sentences from sorted.txt"""

import argparse
import nicer
from multiprocessing import Pool
from itertools import repeat
import sys
from collections import Counter

from sent_tools import *
# SORTED_PATH = "/research/proofcheck/noda/proof-corpus/sorted_small.txt"
WC_PATH = "/research/proofcheck/noda/proof-corpus/sorted_small_wc.txt"
SORTED_PATH = "/research/proofcheck/2023-01-04/sorted.txt"

def check_alias(word, alias_list):
    # Check if word contains an alias
    for alias in alias_list:
        if alias in word:
            return True
    
    return False

def clean_word(word, alias_list):
    # Clean word (find indices of aliases, then lower)
    lower_list = list(word.lower())
    indices = []
    for alias in alias_list:
        current = word
        i = current.find(alias)
        while i != -1:
            indices += [(alias, i)]
            if i + len(alias) >= len(word):
                break
            i = word.find(alias, i+1) 

    for alias, ind in indices:
        lower_list[ind:ind+len(alias)] = list(alias)
    
    return "".join(lower_list)

def clean_sent(line, keep_punct=False, add_spacing=False):
    # Lower everything but aliases
    _, sent = split_sentence_id(line)
    alias_list = list(ALIASES)

    if keep_punct:
        tokens = [w.lower() if not check_alias(w, alias_list) else clean_word(w, alias_list) for w in tokenize(sent)]
    
    else:
        tokens = [w.lower() if not check_alias(w, alias_list) else clean_word(w, alias_list) for w in tokenize(sent) if w not in PUNCTUATION]

    if add_spacing:
        tokens = [""] + tokens + [""]

    return " ".join(tokens)

def count_words(sent):
    return len(sent.split())

def split_num_sent(line):
    line = line.strip()
    temp = line.split(" ")
    num = int(temp[0])
    sent = " ".join(temp[1:])
    return num, sent

def make_tuple_from_sorted(line):
    num_count, sent = split_num_sent(line)
    sent = clean_sent(sent)
    word_count = count_words(sent)
    return (num_count, sent, word_count)

def make_tuple_from_word_count(line):
    line = line.strip()
    num_count, sent, word_count = line.split("\t")
    return int(num_count), sent, int(word_count)

def read_sorted(filename=SORTED_PATH, cores=4):
    with Pool(processes=cores) as p:
        with open(WC_PATH, "w") as o:
            with open(filename, "r") as fd:
                # sent_tuples = []
                sent_counter = Counter()
                for sent_tuple in p.imap(
                    make_tuple_from_sorted,
                            fd.readlines(),
                        50
                        ) :
                            num_count, sent, word_count = sent_tuple
                            # if sent in sent_counter.keys():
                            sent_counter.update({sent : num_count})
                            # else:
                            # sent_counter.update({ sent : num_count })
                            
    return sent_counter

def read_word_count_file(fd, cores):
    with Pool(processes=cores) as p:
        sent_tuples = []
        sent_tuples += p.imap(
            make_tuple_from_word_count,
                    fd.readlines(),
                50
                )
    return sent_tuples

def write_results(sent_counter, output):
    # sent_list = [ [str(x) for x in sent] for sent in sent_list]
    for sent, num_count in sent_counter.items():
        sent_formatted = num_count + "\t" + sent + "\t" + count_words(sent) + "\n"
        output.write(sent_formatted)

def filter_by_word_count(sent_tuple, word_count):
    if sent_tuple[2] == word_count:
        return sent_tuple

def main(args):
    if args.file:
        sent_tuples = read_word_count_file(args.file, args.cores)
    else:
        sent_tuples = read_sorted(cores=args.cores)
    
    with Pool(processes=args.cores) as p:
        common_n = p.starmap(
                        filter_by_word_count,
                            zip(
                                sent_tuples,
                                repeat(args.word_count),
                            ),
                            50,
                        )
    common_n = list(filter(lambda x: x is not None, common_n))
    common_n = common_n[:args.n_common]

    # for sent in sent_tuples:
    #     if sent[2] == args.word_count:
    #         print(sent)
    #         common_n += [sent]
    #     else:
    #         continue
    #     if len(common_n) == args.n_common:
    #         break
    
    write_results(common_n, args.output)
    
if __name__ == "__main__":
    nicer.make_nice()
    parser = argparse.ArgumentParser()

    parser.add_argument("--file", "-f", type=argparse.FileType("r"),
                        help="tsv file to read sentences with word counts from")

    parser.add_argument("--cores", "-p", type=int, default=4,
                        help="number of cores")

    parser.add_argument("--output", "-o", type=argparse.FileType("w"), default=sys.stdout,
                        help="output file")
    
    parser.add_argument("--n_common", "-n", type=int, default=10,
                        help="number of common sentences to find")

    parser.add_argument("--word_count", "-wc", type=int, default=5,
                        help="number of words in sentence")
    
    args = parser.parse_args()

    main(args)