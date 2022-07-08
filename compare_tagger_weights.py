#!/usr/bin/env python

import argparse
import nicer
import sys

from nltk.tag.perceptron import *

from sent_tools import *
from load_ontonotes_pos import *
from find_disagreeing_sents import get_taggers_from_ids, get_tagger_ids_from_list

START = ["-START-", "-START2-"]
END = ["-END-", "-END2-"]

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

def get_key(name, *args):
    return " ".join((name,) + tuple(args))

def find_significant_weights(tagger, sent_with_best_worst):
    best, worst, sent = sent_with_best_worst
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
    
    significant_weights = {key : get_weights(key, weight_dict, best, worst) for key in keys}

    return significant_weights

def get_weights(key, weight_dict, best, worst):
    try:
        feature_dict = weight_dict[key]
        return {best : feature_dict[best], worst : feature_dict[worst]}
    
    except KeyError:
        pass


def main(args):
    best_tagger_ids = get_tagger_ids_from_list(args.best_tagger)
    worst_tagger_ids = get_tagger_ids_from_list(args.worst_tagger, args.use_default)

    best_taggers = get_taggers_from_ids(best_tagger_ids)
    worst_taggers = get_taggers_from_ids(worst_tagger_ids, args.use_default)

    if args.use_default:
        worst_tagger_ids += ["default"]

    with open(args.file, "r") as f:
        lines = f.read().splitlines()
    sents_with_best_worst = [tuple(line.split("\t")) for line in lines] 

    result_string = ""
    for sent_with_best_worst in sents_with_best_worst:
        best_tagger_significant_weights = [(best_tagger_ids[tagger_ind], find_significant_weights(tagger, sent_with_best_worst)) 
                                            for tagger_ind, tagger in enumerate(best_taggers)]
        worst_tagger_significant_weights = [(worst_tagger_ids[tagger_ind], find_significant_weights(tagger, sent_with_best_worst)) 
                                            for tagger_ind, tagger in enumerate(worst_taggers)]

        keys = best_tagger_significant_weights[0][1].keys()
        best_feature_dict = {key : [(tagger_id, weights[key]) for tagger_id, weights in best_tagger_significant_weights] for key in keys}
        worst_feature_dict = {key : [(tagger_id, weights[key]) for tagger_id, weights in worst_tagger_significant_weights] for key in keys}
        
        result_string += sent_with_best_worst[-1] + "\n"
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
                            help="txt file to read sentences from")

    parser.add_argument("--best_tagger", "-b", default="41,9",
                            help="trial number of best taggers")

    parser.add_argument("--worst_tagger", "-te", default="38,22",
                            help="trial number of worst taggers")

    parser.add_argument("--use_default", "-d", action='store_true',
                            help="use default tagger?")

    parser.add_argument( "--output", "-o", type=argparse.FileType("w", encoding='UTF-8'),  
                            default=sys.stdout,
                            help="txt file to write results to")

    args = parser.parse_args()

    main(args)