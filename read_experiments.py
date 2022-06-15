#!/usr/bin/env python

import argparse
import nicer
import numpy as np

def read_one_result(fname):
    with open(fname, "r") as fd:
        results_from_file = fd.read().splitlines()
    trial_results = np.array([[float(num) for num in trial.split("\t")[:-1]] for trial in results_from_file ])
    averages = np.mean(trial_results, axis=0)
    standard_deviations = np.std(trial_results, axis=0)
    summary = np.column_stack((averages, standard_deviations))
    return summary

def main(args):
    for f in args.results_files:
        conditions = f.split("_")
        condition = "_".join(conditions[1:4])
        summary_list = read_one_result(f).tolist()
        summary_strings_list = [[str(num) for num in metric] for metric in summary_list ]
        summary_joined_list = []
        for metric in summary_strings_list:
            summary_joined_list += [metric[0] + "," + metric[1]]
        summary_single_string = condition + "\t" + "\t".join(summary_joined_list) + "\n"
        args.output.write(summary_single_string)
    args.output.close()

if __name__ == '__main__':
    nicer.make_nice()
    parser = argparse.ArgumentParser()

    parser.add_argument("--results_files", "-f", nargs='*', 
                            help="txt file to read experiment results")
                            
    parser.add_argument("--output", "-o",type=argparse.FileType('w'),
                            help="txt file to write to")

    args = parser.parse_args()

    main(args)