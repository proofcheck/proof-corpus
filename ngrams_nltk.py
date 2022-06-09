import argparse
from collections import Counter
import os, re
from xmlrpc.client import Boolean

from nltk import util, lm, tokenize
from nltk.util import bigrams, everygrams, ngrams
from nltk.lm.preprocessing import flatten, padded_everygram_pipeline
from nltk.tokenize.destructive import NLTKWordTokenizer
from nltk.lm import MLE

from ngrams import get_ngrams, read_one
from nltk.tokenize.treebank import TreebankWordDetokenizer


def results(args):
    output = args.output
    text = args.file.readlines()
    tokenized = [NLTKWordTokenizer().tokenize(sent.strip()) for sent in text]
    
    for i in range(1, args.ngrams + 1):
        # words = ngrams(tokenized, i)
        cnt_ngrams = make_counter(tokenized, i)
        ngrams_text = "\nTop 10 most frequent {}-grams:\n"
        output.write(ngrams_text.format(i))
        for x in cnt_ngrams.most_common(10):
            output.write(str(x[0]) + '  ' + str(x[1]))
            output.write("\n")
        output.write("\n")


def make_counter(words, n):
    cnt = Counter()
    for sent in words:
        ngrams_list = ngrams(sent, n)
        cnt.update(ngrams_list)
    
    # for ngramlize_sent in words:
    #     if n == 3:
    #         print(list(ngramlize_sent))
    #     ngram_list = filter(lambda x: len(x) == n, list(ngramlize_sent))
    #     cnt.update(ngram_list)
    return cnt

def main(args): 
    # model_save(args)
   # model_experiment(args)
    results(args)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument("--file", "-f", type=argparse.FileType('r'),
                            help="txt file to read proof from")

    parser.add_argument("--ngrams", "-n", type=int, nargs='?', const=2,
                            help="specifies (n)grams")
    
    parser.add_argument("--output", "-o", type=argparse.FileType('w'),
                            help="txt file to write results to")

    args = parser.parse_args()

    main(args)
