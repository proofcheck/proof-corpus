
import argparse
from collections import Counter
from concurrent.futures import process
import os, re
from xmlrpc.client import Boolean

alias_list = ["CASE", "CITE", "MATH", "NAME", "REF"]
punctuation_list = [".", ",", ":", ";", "'", '"', "-", "?", "!", "(", ")", "{", "}", "[", "]", "`", "–"]

def read_one(fname, size=-1, remove_punctuation=False):
    # Reads a single txt file with one sentence of proof per line
    # Returns a list of all the words in the file 
    processed_elements = []

    # Testing purposes
    # Reads (size) lines of text file
    if size!=-1:
        elements = [next(fname) for x in range(size)]
    else:
        elements = fname.readlines()

    # Tokenizes and removes punctuation if specified
    for element in elements:
        processed_element = []
        element = tokenize(element)
        if remove_punctuation:
            element = filter_nonwords(element)
        processed_element += element
        processed_elements += [processed_element]
    return processed_elements

def tokenize(s):
    # Returns tokenized sentences
    s = s.strip()
    split_list = re.split(r'(\W)', s)
    filtered_list = filter(lambda x: (x != ""), split_list)
    tokenized_list = filter(lambda x: (x != " "), filtered_list)

    # Makes all tokens lowercase except tokens in alias_list
    #tokenized_list = [ x if x in alias_list else x.lower() for x in tokenized_list  ]
    return tokenized_list

def filter_nonwords(list_of_tokens):
    return [x for x in list_of_tokens if x not in punctuation_list ]
    # TODO is this the best way...?
    # filter(lambda x: (x.isalpha()), list_of_tokens)
    
def get_unigrams(list_of_elements):
    # Returns unigrams counter
    cnt = Counter()
    for e in list_of_elements:
        cnt.update(e)
    return cnt

def get_bigrams(list_of_elements):
    # Returns bigrams counter
    cnt = Counter()
    for e in list_of_elements:
        e = ['<s>'] + e + ['</s>']
        bigram_list = zip(e[:-1], e[1:])
        cnt.update(bigram_list)
    return cnt

def get_trigrams(list_of_elements):
    # Returns trigrams counter
    cnt = Counter()
    for e in list_of_elements:
        e = ['<ss>', '<s>'] + e + ['</s>', '</ss>']
        trigram_list = zip(e[:-2], e[1:-1], e[2:])
        cnt.update(trigram_list)
    return cnt

def get_ngrams(list_of_elements, n, head=False):
    # Reurns ngrams counter
    cnt = Counter()
    for e in list_of_elements:
        # Add sentence boundary markers if specified
        if head==False:
            # e = generate_startline_character(n-1) + e + generate_endline_character(n-1)
            e = ['<s>'] + e + ['</s>']
        zip_list = []
        # Create list of lists to zip for creating ngrams
        for i in range(n):
            if i == n-1:
                zip_list += [e[i:]]
            else:
                zip_list += [e[i:i-n+1]]
        n_gram_list = zip(*zip_list)
        cnt.update(n_gram_list)
    return cnt

def generate_startline_character(n):
    # Generates start character
    l = []
    for i in range(1, n+1):
        char = '<' + 's'*i +'>'
        l += [char]
    return l

def generate_endline_character(n):
    # Generates end character
    l = []
    for i in range(1, n+1):
        char = '</' + 's'*i +'>'
        l += [char]
    return l

def results(args):
    list_of_words = read_one(args.file, args.size, args.remove_punctuation)
    output = args.output
    for i in range(1, args.ngrams+1):
        cnt_ngrams = get_ngrams(list_of_words, i, args.remove_marker)
        ngrams_text = "\nTop 10 most frequent {}-grams:\n"
        output.write(ngrams_text.format(i))
        for x in cnt_ngrams.most_common(args.top_n):
            output.write(str(x[0]) + '  ' + str(x[1]))
            output.write("\n")
        output.write("\n")

def main(args): 
    if args.output != None:
        results(args)
    
    else:
        list_of_words = read_one(args.file, args.size, args.remove_punctuation)
    
        cnt_uni = get_unigrams(list_of_words)
        cnt_bi = get_bigrams(list_of_words)
        cnt_tri = get_trigrams(list_of_words)
        
        cnt_ngrams = get_ngrams(list_of_words, args.ngrams, args.remove_marker)

        print("Top 10 most frequent unigrams:")
        print(cnt_uni.most_common(args.top_n))
        print("\n")
        
        print("Top 10 most frequent bigrams:")
        print(cnt_bi.most_common(args.top_n))
        print("\n")

        print("Top 10 most frequent trigrams:")
        print(cnt_tri.most_common(args.top_n))
        print("\n")

        ngrams_text = "Top 10 most frequent {}-grams:"
        print(ngrams_text.format(args.ngrams))
        print(cnt_ngrams.most_common(args.top_n))
        print("\n")

        ngrams_text = "Top 10 most frequent {}-grams:"
        print(ngrams_text.format(args.ngrams))
        print(cnt_ngrams.most_common(args.top_n))
        print("\n")

if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument("--file", "-f", type=argparse.FileType('r'),
                            help="txt file to read proof from")

    parser.add_argument("--directory", "-d",
                            help="directory to extract files from")

    parser.add_argument("--size", "-s", type=int, nargs='?', const=1000, default=-1,
                            help="specifies first (s) sentences to extract")

    parser.add_argument("--top_n", "-t", type=int, nargs='?', const=10,
                            help="specifies top (n) most common _grams")

    parser.add_argument("--remove_punctuation", "-p", action='store_true',
                            help="remove punctuation")
    
    parser.add_argument("--remove_marker", "-m", action='store_true',
                            help="remove sentence boundary markers")

    parser.add_argument("--ngrams", "-n", type=int, nargs='?', const=4,
                            help="specifies (n)grams")

    parser.add_argument("--output", "-o", type=argparse.FileType('w'),
                            help="txt file to write results to")

    args = parser.parse_args()

    main(args)
