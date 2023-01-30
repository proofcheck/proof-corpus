#!/usr/bin/env python

"""Summarizes results from main_experiment.py or dumped_main_experiment.py by taking averages and standard deviations from multiple trials."""

import argparse
import nicer
import numpy as np
import os
os.environ['OPENBLAS_NUM_THREADS'] = '1'

"""
Input :
    --files : txt files to read experiment results from
            
    Files should be outputs of main_experiment.py or dumped_main_experiment.py

Output :
    --output : txt file of results, summarized 
    
    Example output in experiments/summary

How to look at results :
    Takes the results of n trials of an experiment (done under the same condition) in one txt file, and writes the average and standard deviation for each metric.
    Formatted :
        file_name\taverage_of_first_metric,standard_deviation_of_first_metric\taverage_of_second_metric,standard_deviation_of_second_metric\t...\n
"""

"""
Typical usage :
    python3 read_experiment_results.py -f experiments/*find3.txt experiments/*identify3.txt experiments/experiment_default_tagger_main3.txt experiments/experiment_100sents_5iters_main3.txt -o experiments/summary_all_find_identify3.txt
"""

def read_one_result(fname):
    # Reads in one result file (result of multiple trials under the same condition) and return average/standard deviation of all the metrics
    with open(fname, "r") as fd:
        results_str_list = fd.read().splitlines()
    
    trial_results = [[item for item in trial.split("\t")] for trial in results_str_list]
    
    # Check if results has trial name
    if is_float(trial_results[0][0]) is False:
        trial_names = [item[0] for item in trial_results]
        trial_results = [item[1:] for item in trial_results]

    floated_results = np.array([[float(item) for item in trial] for trial in trial_results])
    averages = np.mean(floated_results, axis=0)
    standard_deviations = np.std(floated_results, axis=0)
    summary = np.column_stack((averages, standard_deviations))
    
    return summary

def is_float(item):
    try:
        if float(item):
            return True

    except ValueError:
        return False


def main(args):
    file_list = list(filter(lambda x: os.path.getsize(x)>1, args.files))
    # For each condition (file)
    for f in file_list:
        # Get condition from file name
        conditions = f.split("_")
        condition = "_".join(conditions[1:4])
        summary_list = read_one_result(f).tolist()
        summary_strings_list = [[str(num) for num in metric] for metric in summary_list]
        summary_joined_list = []
        for metric in summary_strings_list:
            summary_joined_list += [metric[0] + "," + metric[1]]
        # Write average,standard deviation for each metric
        summary_single_string = condition + "\t" + "\t".join(summary_joined_list) + "\n"
        args.output.write(summary_single_string)
    args.output.close()

if __name__ == '__main__':
    nicer.make_nice()
    parser = argparse.ArgumentParser()

    parser.add_argument("--files", "-f", nargs='*', 
                            help="txt file to read experiment results")
                            
    parser.add_argument("--output", "-o",type=argparse.FileType('w'),
                            help="txt file to write to")

    args = parser.parse_args()

    main(args)