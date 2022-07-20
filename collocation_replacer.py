#!/usr/bin/env python

"""Merges collocations based on bigram_analysis output."""

import argparse
import nicer
import time
import re

from multiprocessing import Pool
from itertools import repeat

from sent_tools import *

"""
Typical usage:
    python3 collocation_replacer.py -f merged_sents/sent00/sent00_5.txt -cf bigram_analysis/sent00/bigram_analysis_sent00_5.txt -o sent00/sent00_6.txt

Merge aggressively:
    python3 collocation_replacer.py -m -f preprocessed_sents/sent00.txt -cf bigram_analysis/sent00/non-aggressive/bigram_analysis_sent00.txt -o sent00/sent00_1.txt

Print time:
    python3 collocation_replacer.py -p -m -f preprocessed_sents/sent00.txt -cf bigram_analysis/sent00/non-aggressive/bigram_analysis_sent00.txt -o sent00/sent00_1.txt

Use regex:
    python3 collocation_replacer.py -r -p -m -f preprocessed_sents/sent00.txt -cf bigram_analysis/sent00/non-aggressive/bigram_analysis_sent00.txt -o sent00/sent00_1.txt

Merge by sentence:
    python3 collocation_replacer.py -S -f merged_sents/sent00/sent00_5.txt -cf bigram_analysis/sent00/bigram_analysis_sent00_5.txt -o sent00/sent00_6.txt

Test non-aggressively merged sents:
    python3 collocation_replacer.py -t -f merged_sents/sent00/sent00_6.txt
"""

PATH = "merged_sents/"

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

def replace_collocations(line, collocations_dict, merge_collocations=False, print_status=False, use_regex=False, search=None):
    # Use regex for replacements
    if use_regex:
        # Merge n > 2 grams (aggressive merging)
        if merge_collocations:
            if print_status:
                print("making regex", flush=True)
                start = time.clock_gettime(time.CLOCK_MONOTONIC)

            if not search:
                search = [colloc if not_star(colloc) else unstar(colloc) for colloc in reversed(collocations_dict.keys())]
                
                """
                # (\bwe\s(?=\bhave\b)|\bhave\s(?=\bMATH\b))
                search = [f"\\b{colloc[0]}\\s(?=\\b{colloc[1]}\\b)" for colloc in search]
                # negative lookhead for colloc[1]-
                search = [f"(?<!-)\\b{colloc[0]}\\s(?=\\b{colloc[1]}\\b)(?!\\b{colloc[1]}-)" for colloc in search]
                """

                # (?<!-)\\b
                search = [f"(?<!-)\\b{colloc[0]}\\s(?=\\b{colloc[1]}\\b[^-])" for colloc in search]
                search = "|".join(search)
                search = (f"({search})")

                if print_status:
                    end = time.clock_gettime(time.CLOCK_MONOTONIC)
                    print(end - start, "seconds to make regex", flush=True)
                    print("starting replacement", flush=True)
                    start = time.clock_gettime(time.CLOCK_MONOTONIC)

            line = re.sub(search, get_joined_aggressive, line)

            if print_status:
                end = time.clock_gettime(time.CLOCK_MONOTONIC)
                print(end-start, "seconds to replace", flush=True)

        # Only merge bigrams (non-aggressive merging)  
        else:
            if print_status:
                print("making regex", flush=True)
                start = time.clock_gettime(time.CLOCK_MONOTONIC)

            search = [colloc if not_star(colloc) else unstar(colloc) for colloc in collocations_dict.keys()]
            search = ["\\s" + " ".join(colloc) + "\\s" for colloc in search]
            search = "|".join(search)
            search = (f"({search})")

            if print_status:
                end = time.clock_gettime(time.CLOCK_MONOTONIC)
                print(end - start, "seconds to make regex", flush=True)
                print("starting replacement", flush=True)
                start = time.clock_gettime(time.CLOCK_MONOTONIC)

            line = re.sub(search, get_joined, line)

            if print_status:
                end = time.clock_gettime(time.CLOCK_MONOTONIC)
                print(end-start, "seconds to replace", flush=True)

    # Use python replace (not re.sub)
    else:
        total = len(collocations_dict.keys())
        for i, (colloc, joined) in enumerate(collocations_dict.items()):
            if print_status and i % 20 == 0:
                print("{}% of collocations done".format(round(i/total*100, 2)), flush=True)

            spaced = " ".join(colloc)

            # Merge n > 2 grams (aggressive merging)
            if merge_collocations:
                if print_status:
                    #print("replacing", flush=True)
                    start = time.clock_gettime(time.CLOCK_MONOTONIC)
                line = line.replace(" " + spaced + " ", " " + joined + " ")
                line = line.replace("_" + spaced + " ", "_" + joined + " ")
                line = line.replace(" " + spaced + "_", " " + joined + "_")
                line = line.replace("_" + spaced + "_", "_" + joined + "_")
                
                if print_status:
                    end = time.clock_gettime(time.CLOCK_MONOTONIC)
                    #print(end - start, "seconds to replace", flush=True)
                    
            # Only merge bigrams (non-aggressive merging)    
            else:
                if print_status:
                    print("replacing", flush=True)
                    start = time.clock_gettime(time.CLOCK_MONOTONIC)
                
                line = line.replace(" " + spaced + " ", " " + joined + " ")

                if print_status:
                    end = time.clock_gettime(time.CLOCK_MONOTONIC)
                    # if end - start < 0.5 or end - start > 0.7:
                    print(end - start, "seconds to replace", flush=True)
    
    return line

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

def replace_collocations_by_file(fd, collocations_dict, merge_collocations, print_time=False, use_regex=False):
    if args.print_time:
        print("start")
        start = time.clock_gettime(time.CLOCK_MONOTONIC)
    
    sents = fd.read()

    if args.print_time:
        end = time.clock_gettime(time.CLOCK_MONOTONIC)
        print("replace", end - start)
        start = end
        
    joined_lines = replace_collocations(
                                            sents,
                                            collocations_dict,
                                            merge_collocations,
                                            print_time,
                                            use_regex
                                        )

    # Output filename management
    if args.merge_collocations:
        if args.output:
            fname = PATH + "merged_collocations/" + args.output
        else:
            fname = PATH + "merged_collocations/" + fd.name.split("/")[-1].split(".")[0] + "_" + args.extension + ".txt"
    else:
        if args.output:
            fname = PATH + args.output
        else:
            fname = PATH + fd.name.split("/")[-1].split(".")[0] + "_" + args.extension + ".txt"
    
    # Write results
    if args.print_time:
        print("write", time.clock_gettime(time.CLOCK_MONOTONIC))
    with open(fname, "w") as o:
        o.write(joined_lines)

    print("done", fd, flush=True)
    fd.close()

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

    # Read and process by file
    if not args.by_sentence:
        """
        with Pool(processes=4) as p:
            p.starmap(
                replace_collocations_by_file,
                    zip(
                        args.files,
                        repeat(collocations_dict),
                        repeat(args.merge_collocations),
                        repeat(False),
                        repeat(args.use_regex)
                        ),
                    1
                )
        """
        print("start")

        for fd in args.files:            
            if args.print_time:
                start = time.clock_gettime(time.CLOCK_MONOTONIC)
            
            sents = fd.read()

            if args.print_time:
                end = time.clock_gettime(time.CLOCK_MONOTONIC)
                print("replace", end - start)
                start = end
            
            joined_lines = replace_collocations(
                                                    sents,
                                                    collocations_dict,
                                                    args.merge_collocations,
                                                    args.print_time,
                                                    args.use_regex
                                                )

        
            # Output filename management
            if args.merge_collocations:
                if args.output:
                    fname = PATH + "merged_collocations/" + args.output
                else:
                    fname = PATH + "merged_collocations/" + fd.name.split("/")[-1].split(".")[0] + "_" + args.extension + ".txt"
            else:
                if args.output:
                    fname = PATH + args.output
                else:
                    fname = PATH + fd.name.split("/")[-1].split(".")[0] + "_" + args.extension + ".txt"
            
            # Write results
            if args.print_time:
                print("write", time.clock_gettime(time.CLOCK_MONOTONIC))
            with open(fname, "w") as o:
                o.write(joined_lines)

            print("done", fd, flush=True)
            fd.close()
    
    # Read and process by sentence
    else:
        if args.use_regex and args.merge_collocations:
            search = [colloc if not_star(colloc) else unstar(colloc) for colloc in reversed(collocations_dict.keys())]
            
            """
            # (\bwe\s(?=\bhave\b)|\bhave\s(?=\bMATH\b))
            search = [f"\\b{colloc[0]}\\s(?=\\b{colloc[1]}\\b)" for colloc in search]
            # negative lookhead for colloc[1]-
            search = [f"(?<!-)\\b{colloc[0]}\\s(?=\\b{colloc[1]}\\b)(?!\\b{colloc[1]}-)" for colloc in search]
            """

            # (?<!-)\\b
            search = [f"(?<!-)\\b{colloc[0]}\\s(?=\\b{colloc[1]}\\b[^-])" for colloc in search]
            search = "|".join(search)
            search = (f"({search})")

            search = re.compile(search)

        else:
            search = None

        for fd in args.files:
            with Pool(processes=args.cores) as p:
                joined_lines = p.starmap(
                    replace_collocations,
                        zip(
                            fd.read().splitlines(),
                            repeat(collocations_dict),
                            repeat(args.merge_collocations),
                            repeat(False),
                            repeat(args.use_regex),
                            repeat(search)
                            ),
                        250
                    )

                if args.merge_collocations:
                    if args.extension:
                        fname = PATH + "merged_collocations/" + fd.name.split("/")[-1].split(".")[0] + "_" + args.extension + ".txt"
                    else:
                        fname = PATH + "merged_collocations/" + fd.name.split("/")[-1].split(".")[0] + ".txt"
                else:
                    if args.extension:
                        fname = PATH + fd.name.split("/")[-1].split(".")[0] + "_" + args.extension + ".txt"
                    else:
                        fname = PATH + fd.name.split("/")[-1].split(".")[0] + ".txt"

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

    parser.add_argument("--cores", "-c", type=int, default=4,
                        help="number of cores")

    parser.add_argument("--collocation_file", "-cf", type=argparse.FileType("r"),
                        help="file to read collocations")

    parser.add_argument("--merge_collocations", "-m", action="store_true",
                        help="merge collocations too?")

    parser.add_argument("--underscore_test", "-t", action="store_true",
                        help="test output")

    parser.add_argument("--print_time", "-p", action="store_true",
                        help="print time")

    parser.add_argument("--output", "-o",
                        help="output file")

    parser.add_argument("--extension", "-e",
                        help="extension")

    parser.add_argument("--by_sentence", "-S", action="store_true",
                        help="replace collocations by sentence")

    parser.add_argument("--use_regex", "-r", action="store_true",
                        help="use regex")

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
