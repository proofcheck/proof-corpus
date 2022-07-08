#!/usr/bin/env python

import argparse
import nicer
import pickle

from nltk.tag.perceptron import normalize

from sent_tools import *
from load_ontonotes_pos import *
from train_tagger import DEFAULT_TAGGER
from tagger import untag_sent_to_tokens, write_tags
from load_tagged_sent import untag_line_to_tokens
from find_disagreeing_sents import get_taggers_from_trial

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

def find_significant_weights(tagger, sent):
    weight_dict = tagger.model.weights()
    tokens = tokenize(sent)
    context = START + [normalize(w) for w in tokens] + END
    prev, prev2 = START
    word = tokens[0]
    i = 0

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
    
    significant_weights = {key : weight_dict[key] for key in keys}

    return significant_weights


def main(args):
    best_tagger_ids = [int(num) for num in args.best_tagger.split(",")]
    worst_tagger_ids = [int(num) for num in args.worst_tagger.split(",")]

    best_taggers = get_taggers_from_trial(best_tagger_ids)
    worst_taggers = get_taggers_from_trial(worst_tagger_ids, args.use_default)

    with open(args.file, "r") as f:
        sentences = f.read().splitlines()
    
    for sent in sentences:
        best_tagger_significant_weights = [(best_tagger_ids[ind], find_significant_weights(tagger, sent)) 
                                            for ind, tagger in enumerate(best_taggers)]
        worst_tagger_significant_weights = [(worst_tagger_ids[ind], find_significant_weights(tagger, sent)) 
                                            for ind, tagger in enumerate(worst_taggers)]

        print(sent)
        keys = best_tagger_significant_weights[0][1].keys()
        best_feature_dict = {key : (tagger_id, weights[key]) for tagger_id, weights in best_tagger_significant_weights for key in keys}
        worst_feature_dict = {key : (tagger_id, weights[key]) for tagger_id, weights in worst_tagger_significant_weights for key in keys}
        
        for key in keys:
            print(key)
            print(best_feature_dict[key])
            print(worst_feature_dict[key])
        


        
        

    

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

    args = parser.parse_args()

    main(args)