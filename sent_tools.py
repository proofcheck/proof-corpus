#!/usr/bin/env python

"""Tools for corpus. (Mostly used by importing)"""

ALIASES = {"CASE", "CITE", "MATH", "NAME", "REF", "VERBATIM"}
PUNCTUATION = {
    ".",
    ",",
    ":",
    ";",
    "'",
    '"',
    "-",
    "?",
    "!",
    "(",
    ")",
    "{",
    "}",
    "[",
    "]",
    "`",
    "–",
    "''",
    '""',
    "``",
    "...",
    "…",
    "="
}

LEFT_BRACKET = {"(", "[", "{",}
RIGHT_BRACKET = {")", "]", "}",}

def split_sentence_id(line):
    line = line.strip()
    if "\t" in line:
        sent_id = line.split("\t")[0]
        sent = line.split("\t")[1]
    
    else:
        sent_id = ""
        sent = line
    return sent_id, sent

def split_sentences_ids(lines):
    # splits ids and text
    # input: lines
    # output: ids, text
    ids = []
    sents = []
    for line in lines:
        sent_id, sent = split_sentence_id(line)
        ids += sent_id
        sents += sent

    return ids, sents

def tokenize(sent):
    tokenized = sent.split(" ")
    return tokenized

def tokenize_sentences(sents):
    tokenized_sents = [tokenize(sent) for sent in sents]
    return tokenized_sents

def split_sentence_id_tokenized(line):
    sent_id, sent = split_sentence_id(line)
    tokenized = tokenize(sent)
    return sent_id, tokenized

def read_one(f):
    # Input: file of sentences/proofs
    # Returns list of ids and sentences
    lines = f.readlines()
    ids, sents = split_sentences_ids(lines)
    return ids, sents

def read_one_tokenized(fn):
    # Input: file of sentences/proofs
    # Returns list of ids and tokenized sentences
    ids, sents = read_one(fn)
    tokenized = tokenize_sentences(sents)
    return ids, tokenized
