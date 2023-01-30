#!/usr/bin/env python

"""Rewrites preprocessed sents with merged collocations based on bigram_analysis output (or \n separated list of collocations)."""

import argparse
import nicer
import time
import re

from multiprocessing import Pool
from itertools import repeat

from sent_tools import *

"""
Input :
    --files : files to read sentences from (in merged_sents/ or preprocessed_sents/)
    --collocation_file : file to read collocations from (in bigram_analysis/, usually output of bigram_analysis.py)
    (other arguments)

Output :
    txt file of merged sentences 
    
    The file is saved in merged_sents/aggressive or merged_sents/non-aggressive depending on whether -m is used, (unless path is specified using -fp).
    Filenames are taken automatically from the input file.
    If -fp is used, the output is saved to that path with the automatically formatted file name.
"""

"""
Typical usage :
    nohup time python3 collocation_replacer.py -f preprocessed_sents/sent1*.txt -cf bigram_analysis/bigram_analysis_all_500_7_14.txt -fp merged_sents/non-aggressive/time -p 50

Merge aggressively :
    nohup time python3 collocation_replacer.py -m -f preprocessed_sents/sent1*.txt -cf bigram_analysis/bigram_analysis_all_500_7_14.txt -m -fp merged_sents/aggressive/time -p 50

Print time :
    python3 collocation_replacer.py -P -f preprocessed_sents/sent00.txt -cf bigram_analysis/bigram_analysis_all_500_7_14.txt -fp merged_sents/non-aggressive/time -p 50

Test non-aggressively merged sents :
    python3 collocation_replacer.py -t -f merged_sents/sent00/aggressive/sent00_6.txt
"""

PATH = "merged_sents/"

def replace_collocations(line, collocations_dict, merge_collocations=False, print_time=False, use_regex=False, search=None):
    # Use python replace (not re.sub)
    if print_time:
        num_colloc = len(collocations_dict.keys())

    for i, (colloc, joined) in enumerate(collocations_dict.items()):
        if print_time and i % 20 == 0:
            print("{}% of collocations done".format(round(i/num_colloc*100, 2)), flush=True)

        spaced = " ".join(colloc)

        # Merge n > 2 grams (aggressive merging)
        if merge_collocations:
            if print_time:
                start = time.clock_gettime(time.CLOCK_MONOTONIC)

            line = line.replace(" " + spaced + " ", " " + joined + " ")
            line = line.replace("_" + spaced + " ", "_" + joined + " ")
            line = line.replace(" " + spaced + "_", " " + joined + "_")
            line = line.replace("_" + spaced + "_", "_" + joined + "_")
            
            if print_time:
                end = time.clock_gettime(time.CLOCK_MONOTONIC)
                print(end - start, "seconds to replace", flush=True)
                
        # Only merge bigrams (non-aggressive merging)    
        else:
            if print_time:
                start = time.clock_gettime(time.CLOCK_MONOTONIC)
            
            line = line.replace(" " + spaced + " ", " " + joined + " ")

            if print_time:
                end = time.clock_gettime(time.CLOCK_MONOTONIC)
                print(end - start, "seconds to replace", flush=True)

    return line

def get_collocations_dict(collocations_file):
    lines = collocations_file.read().splitlines()
    lines.sort(key = lambda x: float(x.split("\t")[2]), reverse=True)
    collocations = [ tuple(colloc for colloc in line.split("\t")[0].split()) for line in lines ]
    collocations_dict = { colloc : "_".join(colloc) for colloc in collocations }
    return collocations_dict

def test_collocation_file(f):
    lines = f.read().splitlines()

    for line in lines:
        for token in tokenize(line):
            num = 0
            for c in token:
                if c == "_":
                    num += 1
            if num > 1:
                print(token)

"""Helper functions for re.sub"""
def not_star(collocation):
    # True if collocation does not contain *
    if collocation[0] == "*" or collocation[1] == "*":
        return False
    else:
        return True

def unstar(collocation):
    # Escape * (for re.sub)
    new_collocation = list(collocation)

    if collocation[0] == "*":
        new_collocation[0] = "\*"
    if collocation[1] == "*":
        new_collocation[1] = "\*"

    return tuple(new_collocation)

def get_joined(match):
    # Get joined colloc for non-aggressive merging using re.sub
    colloc = match.group(0)
    joined = "_".join(colloc.split())
    return " " + joined + " "

def get_joined_aggressive(match):
    # Get joined colloc for aggressive merging using re.sub
    colloc = match.group(0)
    return colloc.strip() + "_"

def main(args):
    # Testing for non-aggressive replacements
    # Prints words with multiple underscores
    if args.underscore_test:
        for fd in args.files:
            print(fd)
            test_collocation_file(fd)
            print()
            fd.close()
        return

    collocations_dict = get_collocations_dict(args.collocation_file)
    args.collocation_file.close()

    # Read and process by sentence
    for fd in args.files:
        with Pool(processes=args.cores) as p:
            joined_lines = p.starmap(
                replace_collocations,
                    zip(
                        fd.read().splitlines(),
                        repeat(collocations_dict),
                        repeat(args.merge_collocations),
                        repeat(args.print_time)
                        ),
                    250
                )

            if args.merge_collocations:
                if args.extension:
                    fname = PATH + "aggressive/" + fd.name.split("/")[-1].split(".")[0] + "_" + args.extension + ".txt"
                
                elif args.path:
                    fname = args.path + "/" + fd.name.split("/")[-1].split(".")[0] + ".txt"

                else:
                    fname = PATH + "aggressive/" + fd.name.split("/")[-1].split(".")[0] + ".txt"
            else:
                if args.extension:
                    fname = PATH + "non-aggressive/" + fd.name.split("/")[-1].split(".")[0] + "_" + args.extension + ".txt"
                
                elif args.path:
                    fname = args.path + "/" +  fd.name.split("/")[-1].split(".")[0] + ".txt"

                else:
                    fname = PATH + "non-aggressive/" + fd.name.split("/")[-1].split(".")[0] + ".txt"

            with open(fname, "w") as o:
                lines = "\n".join(joined_lines)
                o.write(lines)

        print("done", fd, flush=True)
        fd.close()
            
if __name__ == "__main__":
    nicer.make_nice()
    parser = argparse.ArgumentParser()

    parser.add_argument("--files", "-f", nargs="*", type=argparse.FileType("r"),
                        help="txt file to read sents from")

    parser.add_argument("--cores", "-p", type=int, default=4,
                        help="number of cores")

    parser.add_argument("--collocation_file", "-cf", type=argparse.FileType("r"),
                        help="file to read collocations")

    parser.add_argument("--merge_collocations", "-m", action="store_true",
                        help="merge collocations too?")

    parser.add_argument("--underscore_test", "-t", action="store_true",
                        help="test output")

    parser.add_argument("--print_time", "-P", action="store_true",
                        help="print time")

    parser.add_argument("--path", "-fp",
                        help="output file path")

    parser.add_argument("--extension", "-e",
                        help="extension")

    args = parser.parse_args()

    main(args)

"""
c_f = "bigram_analysis/bigram_analysis_all_500_7_14.txt"
c = open(c_f, "r")
c_dict = get_collocations_dict(c)
c.close()
sent = "integrating REF with respect to MATH it follows that we have to bound the integral over MATH of the four terms on the right hand side"
sent = "As a MATH-module this algebra can be written as MATH ."
sent1 = "Now there is a positive real-analytic function MATH such that a weighted configuration MATH is in MATH provided that MATH ."
replace_collocations(sent1, c_dict)
"""
