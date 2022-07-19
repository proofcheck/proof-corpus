#!/usr/bin/env python

"""Find sentences such that 
    - the best taggers agree on the tag (best tag)
    - the worst taggers agree on the tag (worst tag)
    - best tag and worst tag are not the same

    and write it out in the following format:
    best_tag\tworst_tag\tsent
    """

import argparse
import nicer
import pickle
import sys

from sent_tools import *
from load_ontonotes_pos import *
from train_tagger import DEFAULT_TAGGER
from tagger import untag_sent_to_tokens, write_tags
from load_tagged_sent import untag_line_to_tokens

"""
Typical usage:
    python3 find_disagreeing_sents.py -f testing_set/4verbs_handtagged.txt -o disagreeing_sents_7_8.txt
"""

TAGGER_PATH = "tagger/7_5/5sents_5iters_7_5_trial"

def mismatch_finder(sent, best_taggers, worst_taggers):
    # Return sent, best_tags, worst_tags if 
    #   len(best_tags) == len(worst_tags) == 1 AND
    #   best_tags != worst_tags
    tokenized = untag_line_to_tokens(sent)
    best_tagger_answers = list(set([tagger.tag(tokenized)[0][1] for tagger in best_taggers]))
    worst_tagger_answers = list(set([tagger.tag(tokenized)[0][1] for tagger in worst_taggers]))

    if (len(best_tagger_answers) == 1 and len(worst_tagger_answers) == 1 
        and worst_tagger_answers != best_tagger_answers):
            return tokenized, best_tagger_answers, worst_tagger_answers
    
    else:
        return None, None, None

def get_taggers_from_ids(tagger_num_list, use_default=False):
    # Get pickled taggers from id number
    taggers = []
    if use_default:
        tagger_num_list = tagger_num_list[:-1]
        
    for num in tagger_num_list:
        tagger_file = TAGGER_PATH + num + ".pk"
        with open(tagger_file, "rb") as resource:
            taggers += [pickle.load(resource)]

    if use_default:
        taggers += [DEFAULT_TAGGER]
    
    return taggers

def get_tagger_ids_from_list(id_list, use_default=False):
    # Get tagger_id from list of ids
    tagger_ids = [num for num in id_list.split(",")]
    if use_default:
        tagger_ids += ["default"]
    return tagger_ids

def main(args):
    best_tagger_ids = get_tagger_ids_from_list(args.best_tagger)
    worst_tagger_ids = get_tagger_ids_from_list(args.worst_tagger, args.use_default)

    best_taggers = get_taggers_from_ids(best_tagger_ids)
    worst_taggers = get_taggers_from_ids(worst_tagger_ids, args.use_default)

    with open(args.file, "r") as f:
        lines = f.read().splitlines()

    for line in lines:
        tokenized, best_tagger_answers, worst_tagger_answers = mismatch_finder(line, best_taggers, worst_taggers)
        # If there are disagreeing sents,
        if tokenized and args.output:
            sentence = " ".join(tokenized)
            args.output.write(best_tagger_answers[0] + "\t" + worst_tagger_answers[0] + "\t" + sentence + "\n")

    if args.write_tags:
        # Tag sentences using every tagger (best and worst) and write the tags out
        all_taggers = best_taggers + worst_taggers
        all_taggers_ids = best_tagger_ids + worst_tagger_ids

        for ind, tagger in enumerate(all_taggers):
            tags = [tagger.tag(untag_line_to_tokens(line)) for line in lines]
            with open("trial" + all_taggers_ids[ind] + ".txt", "w") as f:
                write_tags([], tags, f)

    if args.output:
        args.output.close()

if __name__ == '__main__':
    nicer.make_nice()
    parser = argparse.ArgumentParser()
    
    parser.add_argument("--file", "-f",
                            help="txt file to read (testing set)")

    parser.add_argument("--best_tagger", "-b", default="41,9",
                            help="trial number of best taggers")

    parser.add_argument("--worst_tagger", "-te", default="38,22",
                            help="trial number of worst taggers")

    parser.add_argument("--use_default", "-d", action='store_true',
                            help="use default tagger?")

    parser.add_argument("--write_tags", "-w", action='store_true',
                            help="write tags?")

    parser.add_argument("--output", "-o", type=argparse.FileType('w'), 
                            default=sys.stdout,
                            help="file to write sentences to")

    args = parser.parse_args()

    main(args)


# TESTING_F = "testing_set/4verbs_handtagged.txt"

# use_default_tagger = False

# TRIAL41 = "tagger/7_5/5sents_5iters_7_5_trial41.pk"
# TRIAL9 = "tagger/7_5/5sents_5iters_7_5_trial9.pk"

# TRIAL38 = "tagger/7_5/5sents_5iters_7_5_trial38.pk"
# TRIAL22 = "tagger/7_5/5sents_5iters_7_5_trial22.pk"

# BEST_TAGGER_FILES = [TRIAL41, TRIAL9]
# WORST_TAGGERS_FILES = [TRIAL38, TRIAL22]

# BEST_TAGGERS = []
# for tagger_file in BEST_TAGGER_FILES:
#     with open(tagger_file, "rb") as resource:
#         BEST_TAGGERS += [pickle.load(resource)]

# WORST_TAGGERS = []
# for tagger_file in WORST_TAGGERS_FILES:
#     with open(tagger_file, "rb") as resource:
#         WORST_TAGGERS += [pickle.load(resource)]