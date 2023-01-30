#!/usr/bin/env python

"""Compares weights of trained taggers using output of find_disagreeing_sents.py"""

import argparse
import nicer
import sys

from nltk.tag.perceptron import *

from sent_tools import *
from load_ontonotes_pos import *
from find_disagreeing_sents import get_taggers_from_ids, get_tagger_ids_from_list

"""
Input :
    --file : file of sentences (in disagreeing_sents/, output of disagreeing_sents.py)
    --best_tagger : IDs of best taggers, split by commas (defaults to 41,9)
    --worst_tagger : IDs of worst taggers, split by commas (defaults to 38,22)
    (other arguments)

    Taggers are loaded from :
        TAGGER_PATH = "tagger/7_5/5sents_5iters_7_5_trial"

Output :
    --output : Writes output to file. If unspecified, prints results.
"""

"""
Typical usage :
    python3 compare_tagger_weights.py -f disagreeing_sents_7_8.txt

    Uses get_tagger_ids_from_ids and get_tagger_ids_from_list in find_disagreeing_sents.py to load taggers from 
        TAGGER_PATH = "tagger/7_5/5sents_5iters_7_5_trial"

To specify tagger ids :
    python3 compare_tagger_weights.py -f disagreeing_sents_7_8.txt -b 41,9 -w 38,22

To use the default tagger as a worst tagger :
    python3 compare_tagger_weights.py -f disagreeing_sents_7_8.txt -b 41,9 -w 38,22 -d
"""

# Start and end of sentence tags/words
START = ["-START-", "-START2-"]
END = ["-END-", "-END2-"]

def get_key(name, *args):
    # Get weight_dict key name from dictionary keys used to update weights
    return " ".join((name,) + tuple(args))

def find_significant_weights(tagger, sent_with_best_worst_tags):
    # Return only the weights that influence the first tag
    best_tag, worst_tag, sent = sent_with_best_worst_tags
    weight_dict = tagger.model.weights
    tokens = tokenize(sent)
    context = START + [tagger.normalize(w) for w in tokens] + END
    prev, prev2 = START
    word = tokens[0]
    i = 2

    keys = [get_key("bias"),
            get_key("i suffix", word[-3:]),
            get_key("i pref1", word[0] if word else ""),
            get_key("i-1 tag", prev),
            get_key("i-2 tag", prev2),
            get_key("i tag+i-2 tag", prev, prev2),
            get_key("i word", context[i]),
            get_key("i-1 tag+i word", prev, context[i]),
            get_key("i-1 word", context[i - 1]),
            get_key("i-1 suffix", context[i - 1][-3:]),
            get_key("i-2 word", context[i - 2]),
            get_key("i+1 word", context[i + 1]),
            get_key("i+1 suffix", context[i + 1][-3:]),
            get_key("i+2 word", context[i + 2])]
    
    significant_weights = {key : get_weights(key, weight_dict, best_tag, worst_tag) for key in keys}

    return significant_weights

def get_weights(key, weight_dict, best_tag, worst_tag):
    # Get weights for the key and turn them into a dict that maps taggers onto weights
    
    try:
        feature_dict = weight_dict[key]
        return {best_tag : feature_dict[best_tag], worst_tag : feature_dict[worst_tag]}
    
    except KeyError:
        pass


def main(args):
    # Get best/worst taggers
    best_tagger_ids = get_tagger_ids_from_list(args.best_tagger)
    worst_tagger_ids = get_tagger_ids_from_list(args.worst_tagger, args.use_default)

    best_taggers = get_taggers_from_ids(best_tagger_ids)
    worst_taggers = get_taggers_from_ids(worst_tagger_ids, args.use_default)

    if args.use_default:
        # Add default tagger to worst taggers
        worst_tagger_ids += ["default"]

    # Load best/worst tags and sentences
    with open(args.file, "r") as f:
        lines = f.read().splitlines()
    sents_with_best_worst_tags = [tuple(line.split("\t")) for line in lines] 

    result_string = ""
    
    # Loop through all the sentences in the testing file
    for sent_with_best_worst_tags in sents_with_best_worst_tags:
        # Create a list of (tagger_id, significant_weights_dict) for best/worst taggers
        best_tagger_significant_weights = [(best_tagger_ids[tagger_ind], find_significant_weights(tagger, sent_with_best_worst_tags)) 
                                            for tagger_ind, tagger in enumerate(best_taggers)]
        worst_tagger_significant_weights = [(worst_tagger_ids[tagger_ind], find_significant_weights(tagger, sent_with_best_worst_tags)) 
                                            for tagger_ind, tagger in enumerate(worst_taggers)]

        keys = best_tagger_significant_weights[0][1].keys()
        
        # Get a dictionary for best/worst taggers with the feature as the key and (id, weights) as the value
        best_feature_dict = {key : [(tagger_id, weights[key]) for tagger_id, weights in best_tagger_significant_weights] for key in keys}
        worst_feature_dict = {key : [(tagger_id, weights[key]) for tagger_id, weights in worst_tagger_significant_weights] for key in keys}
        
        result_string += sent_with_best_worst_tags[-1] + "\n"
        
        # For each feature, create a string of results combining best and worst taggers 
        for key in keys:
            result_string += key + "\n"
            tagger_results = [tagger_id + " " + str(tagger_dict) for tagger_id, tagger_dict in best_feature_dict[key]]
            result_string += "\t".join(tagger_results) + "\n"

            tagger_results = [tagger_id + " " + str(tagger_dict) for tagger_id, tagger_dict in worst_feature_dict[key]]
            result_string += "\t".join(tagger_results) + "\n"
        
        result_string += "\n"
    
    if args.output:
        args.output.write(result_string)
        args.output.close()      
    
if __name__ == '__main__':
    nicer.make_nice()
    parser = argparse.ArgumentParser()
    
    parser.add_argument("--file", "-f", 
                            help="txt file to read sentences and best/worst tags from (output of find_disagreeing_sents.py)")

    parser.add_argument("--best_tagger", "-b", default="41,9",
                            help="trial number of best taggers")

    parser.add_argument("--worst_tagger", "-w", default="38,22",
                            help="trial number of worst taggers")

    parser.add_argument("--use_default", "-d", action='store_true',
                            help="use default tagger?")

    parser.add_argument( "--output", "-o", type=argparse.FileType("w", encoding='UTF-8'),  
                            default=sys.stdout,
                            help="txt file to write results to")

    args = parser.parse_args()

    main(args)


"""
        add("bias")
        add("i suffix", word[-3:])
        add("i pref1", word[0] if word else "")
        add("i-1 tag", prev)
        add("i-2 tag", prev2)
        add("i tag+i-2 tag", prev, prev2)
        add("i word", context[i])
        add("i-1 tag+i word", prev, context[i])
        add("i-1 word", context[i - 1])
        add("i-1 suffix", context[i - 1][-3:])
        add("i-2 word", context[i - 2])
        add("i+1 word", context[i + 1])
        add("i+1 suffix", context[i + 1][-3:])
        add("i+2 word", context[i + 2])

 """