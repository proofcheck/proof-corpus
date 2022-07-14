#!/usr/bin/env python

import argparse
import nicer

from multiprocessing import Pool
from itertools import repeat

from sent_tools import *
from bigram_analysis import clean_sent

PATH = "merged_sents/"

def replace_collocations(line, collocations_dict, merge_collocations=False, print_status=False):
    sent = clean_sent(line, True)
    # total = len(collocations_dict.keys())
    # i = 0

    # for i, (colloc, joined) in enumerate(collocations_dict.items()):
    
    for colloc, joined in collocations_dict.items():
        if print_status and i % 100 == 0:
            print("{}% done".format(round(i/total*100, 2)))
            i += 1

        spaced = " ".join(colloc)
       
        if merge_collocations:
            sent = sent.replace(" " + spaced + " ", " " + joined + " ")
            sent = sent.replace("_" + spaced + " ", "_" + joined + " ")
            sent = sent.replace(" " + spaced + "_", " " + joined + "_")
            sent = sent.replace("_" + spaced + "_", "_" + joined + "_")
            sent = sent.replace("\t" + spaced + " ", "\t" + joined + " ")
            sent = sent.replace("\t" + spaced + "_", "\t" + joined + "_")

        else:
            sent = sent.replace(" " + spaced + " ", " " + joined + " ")
            sent = sent.replace("\t" + spaced + " ", "\t" + joined + " ")
    
    return sent

def get_collocations_dict(collocations_file):
    lines = collocations_file.read().splitlines()
    lines.sort(key = lambda x: float(x.split("\t")[2]), reverse=True)

    collocations = [ tuple(colloc for colloc in line.split("\t")[0].split()) for line in lines ]
    #collocations_string = [line.split("\t")[0] for line in lines]
    collocations_dict = { colloc : "_".join(colloc) for colloc in collocations}
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

def main(args):
    if args.test:
        for fd in args.test:
            print(fd)
            test_collocation_file(fd)
            print()
            fd.close()
        return

    collocations_dict = get_collocations_dict(args.collocation_file)
    args.collocation_file.close()

    if args.by_sentence:
        for fd in args.files:
            with Pool(processes=args.cores) as p:
                joined_lines = p.starmap(
                    replace_collocations,
                        zip(
                            fd.readlines(),
                            repeat(collocations_dict),
                            repeat(args.merge_collocations)
                            ),
                        50
                    )

                if args.merge_collocations:
                    fname = PATH + "merged_collocations/" + fd.name.split("/")[-1].split(".")[0] + "_" + args.extension + ".txt"
                else:
                    fname = PATH + fd.name.split("/")[-1].split(".")[0] + "_" + args.extension + ".txt"

                with open(fname, "w") as o:
                    lines = "\n".join(joined_lines)
                    o.write(lines)

            print("done", fd)
            fd.close()
    
    else:
        for fd in args.files:
            #_, sents = read_one(fd)
            #sents_string = "\n".join(sents)

            joined_lines = replace_collocations(
                                                    #sents_string, 
                                                    fd.read(),
                                                    collocations_dict,
                                                    args.merge_collocations,
                                                    
                                                )

            if args.merge_collocations:
                fname = PATH + "merged_collocations/" + fd.name.split("/")[-1].split(".")[0] + "_" + args.extension + ".txt"
            
            else:
                fname = PATH + fd.name.split("/")[-1].split(".")[0] + "_" + args.extension + ".txt"

            with open(fname, "w") as o:
                o.write(joined_lines)

            print("done", fd)
            fd.close()

if __name__ == "__main__":
    nicer.make_nice()
    parser = argparse.ArgumentParser()

    parser.add_argument("--files", "-f", nargs="*", type=argparse.FileType("r"),
                        help="txt file to read sents from")

    parser.add_argument("--cores", "-c", type=int, default=4,
                        help="number of cores")

    parser.add_argument("--collocation_file", "-cf", type=argparse.FileType("r"),
                        help="file to read collocations")

    parser.add_argument("--merge_collocations", "-m", action="store_true",
                        help="merge collocations too?")

    parser.add_argument("--test", "-t", nargs="*", type=argparse.FileType("r"),
                        help="test output")

    parser.add_argument("--by_sentence", "-S", action="store_true",
                        help="replace collocations by sentence")

    parser.add_argument("--extension", "-e",
                            help="file extension")

    args = parser.parse_args()

    main(args)


"""
c_f = "bigram_analysis/bigram_analysis_all_500.txt"
c = open(c_f, "r")
c_dict = get_collocations_dict(c)
c.close()
sent = "As a MATH-module this algebra can be written as MATH ."
sent1 = "Now there is a positive real-analytic function MATH such that a weighted configuration MATH is in MATH provided that MATH ."
replace_collocations(sent1, c_dict)
"""

"""
import re
"""
"""
spaced = spaced.replace("*", "\*")
joined = joined.replace("*", "\*")
"""
"""
sent = re.sub(r" " + spaced + r" ", r" " + joined + r" ", sent)
sent = re.sub(r"_" + spaced + r" ", r"_" + joined + r" ", sent)
sent = re.sub(r" " + spaced + r"_", r" " + joined + r"_", sent)
sent = re.sub(r"_" + spaced + r"_", r"_" + joined + r"_", sent)
"""
"""
sent = re.sub(r" " + spaced + r" ",  r" " + joined + r" ", sent)
"""