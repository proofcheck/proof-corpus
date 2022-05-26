#!/usr/bin/env python

from nltk.tokenize.destructive import NLTKWordTokenizer
from nltk.tag import pos_tag_sents

word_tokenizer = NLTKWordTokenizer()

def read_one_tagger(fname):
    f = open(fname, "r")
    sentences = f.readlines()
    tokenized = [word_tokenizer.tokenize(s.split('\t')[-1]) for s in sentences]
    f.close()
    tagged = pos_tag_sents(tokenized)
    return tagged