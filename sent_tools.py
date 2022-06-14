#!/usr/bin/env python

from multiprocessing import Pool
import nicer

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

def read_one(fn):
    # Input: file of sentences/proofs
    # Returns list of ids and sentences
    f = open(fn, "r")
    lines = f.readlines()
    ids, sents = split_sentences_ids(lines)
    f.close()
    return ids, sents

def read_one_tokenized(fn):
    # Input: file of sentences/proofs
    # Returns list of ids and tokenized sentences
    ids, sents = read_one(fn)
    tokenized = tokenize_sentences(sents)
    return ids, tokenized

def read_files(files, cores):
    nicer.make_nice()
    ids = []
    sents = []
    for fd in files:
        print(fd)
        with Pool(processes=cores) as p:
            for id_sent in p.imap(
                    split_sentence_id,
                    fd.readlines(),
                    250
                ):
                ids += id_sent[0]
                sents += id_sent[1]
        fd.close()
    return ids, sents

def read_files_tokenized(files, cores):
    nicer.make_nice()
    ids = []
    sents = []
    for fd in files:
        print(fd)
        with Pool(processes=cores) as p:
            for id_sent in p.imap(
                    split_sentence_id_tokenized,
                    fd.readlines(),
                    250
                ):
                ids += id_sent[0]
                sents += id_sent[1]
        fd.close()
    return ids, sents
