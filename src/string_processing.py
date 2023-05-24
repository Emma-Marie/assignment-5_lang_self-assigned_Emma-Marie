import os
import re
import string
from collections import Counter, OrderedDict
import pandas as pd
import argparse

def input_parse():
    #initialie the parser
    parser = argparse.ArgumentParser()
    # add argument
    parser.add_argument("--keyword", type=str) # keyword token
    parser.add_argument("--cooccurring", type=int, default=10) # the number of co-ocurring tokens
    # parse the arguments from command line
    args = parser.parse_args()
    return args

def get_data():
    # load sermons data
    sermon_path = os.path.join("..", "..", "768706", "data", "content.dat")
    data = pd.read_csv(sermon_path, index_col=0) 
    # load metadata
    meta_path = os.path.join("..", "..", "768706", "metadata", "Joined_Meta.xlsx")
    meta = pd.read_excel(meta_path)
    # merge on document IDs
    full_data = data.merge(meta, left_on="id", right_on="ID-dok")
    # get sermon content
    corpus = full_data["content"]# [1:100] ## I chose a small sample of sermons to provide the run from being "killed".
    # turn into string
    corpus_str = corpus.to_string(index=False)
    # cleaning text using regex
    corpus_str = corpus_str.replace("\\n", " ")
    # turn every token lowercase
    corpus_str = corpus_str.lower()
    # split tokens
    tokens = corpus_str.split()
    # clean tokens by removing punctuation etc. 
    clean_tokens = []
    for token in tokens:
        stripped = token.strip(string.punctuation)
        if not stripped == "":
            clean_tokens.append(stripped)
    
    # Remove stopwords
    stopwords_file = "danish_stopwords.txt"
    with open(stopwords_file, 'r') as file:
        stopwords = [line.strip() for line in file]
    clean_tokens = [token for token in clean_tokens if token not in stopwords]

    print("Data is ready!")

    return corpus_str, tokens

def examine_token(corpus_str, clean_tokens, args):
    keyword = args.keyword
    # count how many times a chosen word appears
    count = 0
    for idx, token in enumerate(clean_tokens):
        if token == keyword:
            count += 1
    print(count)
    # find sentences in which the chosen word appears
    #sentences = re.split(r'[.?!]\s*', corpus_str)
    #for idx, sentence in enumerate(sentences):
    #    if keyword in sentence:
    #        print(idx, "\t", sentence)

    # get context by finding the five tokens before and after the keyword
    for idx, token in enumerate(clean_tokens):
        if token == keyword:
            before = ' '.join(clean_tokens[idx-5:idx])
            after = ' '.join(clean_tokens[idx+1:idx+6])
            full = [before, token, after]
            print("{:50} {:20} {:50}".format(*full))

    # choose the number of co-occurrence
    num_cooccurring = args.cooccurring 
    # create a counter for co-occurring tokens
    cooccurring_counter = Counter()
    # iterate over the tokens
    for idx, token in enumerate(clean_tokens):
        if token == keyword:
            cooccurring = clean_tokens[idx-5:idx] + clean_tokens[idx+1:idx+6]
            cooccurring_counter.update(cooccurring)
    # get the most common co-occurring tokens
    most_common_cooccurring = cooccurring_counter.most_common(num_cooccurring)

    print(most_common_cooccurring)

    return most_common_cooccurring

def main():
    args = input_parse()
    # load and process data
    corpus_str, tokens = get_data()
    # examin self-chosen token
    examine_token(corpus_str, tokens, args)

if __name__ == "__main__":
    main()
