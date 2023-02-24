#!/usr/bin/env python

import argparse
import nicer 
import re

from multiprocessing import Pool
from itertools import repeat

from sent_tools import *

"""
[document identifier]<tab>[label]<tab>[document text]<newline> 
"""

"""
'([a-z]|-)+'
cond-mat
cs
gr-qc
hep-lat
hep-ph
hep-th
math
math-ph
nlin
physics
quant-ph
"""

def unique_sentences(fd):
    lines = fd.readlines()
    fd.close()
    return unique_sent_id(lines)

def unique_sent_id(lines):
    unique_id_lines = []
    previous_proof_id = ""
    previous_sent_num = 1
    for line in lines:
        current_proof_id, sent = split_sentence_id(line)
        if current_proof_id == previous_proof_id:
            current_proof_id = previous_proof_id + "_" + str(previous_sent_num + 1)
            previous_sent_num += 1
        else:
            previous_proof_id = current_proof_id
            previous_sent_num = 1
        unique_id_lines += ["\t".join([current_proof_id, sent])]
    return unique_id_lines

def clean_sent(line):
    # only works for sent files up to sent07.tsv
    sent_id, sent = split_sentence_id(line)
    topic = re.search("([a-z]|-)+", sent_id)
    if not topic:
        topic = ""
    else:
        topic = topic.group()
    csv_line = sent_id + "\t" + topic + "\t" + sent + "\n"
    return csv_line

def main(args):
    lines = []
    for fd in args.files:
        lines += unique_sentences(fd)
        print(fd, "done", flush=True)
    #print(lines)

    with Pool(processes=args.cores) as p:
        with open(args.output, "w") as o:
            for line in p.starmap(
                clean_sent,
                    zip(
                        lines
                        ),
                    50
                ):
                    

                # if args.extension:
                #     fname = PATH + fd.name.split("/")[-1].split(".")[0] + "_" + args.extension + ".csv"
                # else:
                #     fname = PATH + fd.name.split("/")[-1].split(".")[0] + ".csv"

                    o.write(line)

if __name__ == "__main__":
    nicer.make_nice()
    parser = argparse.ArgumentParser()

    parser.add_argument("--files", "-f", 
                        nargs="*", 
                        type=argparse.FileType("r"),
                        help="tsv file to read sents from")

    parser.add_argument("--cores", "-p", type=int, default=4,
                        help="number of cores")

    parser.add_argument("--output", "-o", 
                        # type=argparse.FileType("w"),
                        help="txt file to write sents to")

    args = parser.parse_args()

    main(args)

