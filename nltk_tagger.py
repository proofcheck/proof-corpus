#!/usr/bin/env python

from nltk.tokenize.destructive import NLTKWordTokenizer
from nltk.tag import pos_tag_sents
from nltk.tag.perceptron import PerceptronTagger

tagger = PerceptronTagger()

def read_one_tagger(fname):
    f = open(fname, "r")
    sentences = f.readlines()
    tokenized = [(s.split('\t')[-1]).split() for s in sentences]
    f.close()
    tagged = [tagger.tag(sent) for sent in tokenized]
    return tagged
    """
     [_pos_tag(sent, tagset, tagger, lang) for sent in sentences]
     tagger.tag(word_tokenize(sentence))
    """

def read_one(fn):
    f = open(fn, "r")
    lines = f.readlines()
    f.close()
    return lines