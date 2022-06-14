#!/usr/bin/env python


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

def tokenizer(sent):
    tokenized = sent.split(" ")
    return tokenized

def tokenize_sentences(sents):
    tokenized_sents = [tokenizer(sent) for sent in sents]
    return tokenized_sents

