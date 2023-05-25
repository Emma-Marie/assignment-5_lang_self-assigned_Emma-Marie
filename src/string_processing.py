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
    # merge data and meta data on document IDs
    full_data = data.merge(meta, left_on="id", right_on="ID-dok")# corpus is a pandas series (1D array)
    # Create empty Series for male and female corpora
    male_corpus_series = pd.Series()
    female_corpus_series = pd.Series()

    for index, row in full_data.iterrows():
        if row["køn"] == 1:
            male_corpus_series[index] = row["content"]
        elif row["køn"] == 2:
            female_corpus_series[index] = row["content"]

    print(f"Length of male corpus is {len(male_corpus_series)}")
    print(f"Length of female corpus is {len(female_corpus_series)}")
    print(f"Length of full corpus is {len(full_data)}")

    # get sermon content
    #corpus = full_data["content"] 

    return male_corpus_series, female_corpus_series

def clean_data(corpus_series, corpus_name):
    # cleaning text using regex
    corpus_str = corpus_series.to_string(index=False)
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
    # Assign name to the clean tokens based on the corpus name
    clean_tokens_name = f"clean_tokens_{corpus_name}"
    globals()[clean_tokens_name] = clean_tokens

    return clean_tokens

def keyword_context(corpus_str, clean_tokens, args):
    keyword = args.keyword
    # count how many times a chosen word appears
    count = 0
    for idx, token in enumerate(clean_tokens):
        if token == keyword:
            count += 1
    print(f"{keyword} appear {count} times in corpus")
    
    # get context by finding the five tokens before and after the keyword
    context_data = []
    for idx, token in enumerate(clean_tokens):
        if token == keyword:
            before = ' '.join(clean_tokens[idx-5:idx])
            after = ' '.join(clean_tokens[idx+1:idx+6])
            full = [before, token, after]
            #print("{:50} {:20} {:50}".format(*full))
            context_data.append(full)
    context_path = os.path.join("out", f"context_{keyword}.csv")
    # Write the context data to the file
    with open(context_path, "w") as file:
        for context in context_data:
            file.write("{:50} {:20} {:50}\n".format(*context))
    print(f"The context of {keyword} is saved")

    # find sentences in which the chosen word appears
    keyword_sentences = []
    sentences = re.split(r'[.?!]\s*', corpus_str) # split corpus into sentences by periods, questionmarks and excalmation marks
    for idx, sentence in enumerate(sentences): # track index for each sentence
        if keyword in sentence: # print sentence, if the keyword is in it. 
            keyword_sentences.append((idx, sentence))
            #print(idx, "\t", sentence)
    # save sentences with keyword in csv file
    sentences_df = pd.DataFrame(keyword_sentences, columns=['sentence number', 'sentence'])
    df_path = os.path.join("out", f"sentences_{keyword}.csv")
    sentences_df.to_csv(df_path)
    print(f"Sentences with {keyword} is saved")

    return keyword

def coocurring_tokens(clean_tokens, args, keyword):
    # Remove stopwords
    with open("danish_stopwords.txt", "r") as file:
    #with open("stopord.txt", "r") as file:
        stopwords = [line.strip() for line in file]
    tokens_no_stopwords = [token for token in clean_tokens if token not in stopwords]
    # choose the number of co-occurrence
    num_cooccurring = args.cooccurring 
    # create a counter for co-occurring tokens
    cooccurring_counter = Counter()
    # iterate over the tokens
    for idx, token in enumerate(tokens_no_stopwords):
        if token == keyword:
            # find the five tokens before and five tokens after keyword
            cooccurring = tokens_no_stopwords[idx-5:idx] + tokens_no_stopwords[idx+1:idx+6]
            # add co-occuring tokens to list
            cooccurring_counter.update(cooccurring)
    # get the argpersed number of most common co-occurring tokens
    most_common_cooccurring = cooccurring_counter.most_common(num_cooccurring)
    # Create dataframe from most common co-occurring tokens
    cooccurring_df = pd.DataFrame(most_common_cooccurring, columns=['Token', 'Count'])
    df_path = os.path.join("out", f"cooccuring_words_{keyword}.csv")
    cooccurring_df.to_csv(df_path)
    #print(most_common_cooccurring)
    print(f"{num_cooccurring} most co-occuring words to {keyword} is saved")

    return most_common_cooccurring

def main():
    args = input_parse()
    # load and process data
    male_corpus_series, female_corpus_series = get_data()
    # tokneize and clean data
    clean_tokens_male = clean_data(male_corpus_series, "male")
    clean_tokens_female = clean_data(female_corpus_series, "female")
    # find sentences in which keyword appears
    #keyword = keyword_context(corpus_str, clean_tokens, args)
    # find and count tokens co-occurring with keyword
    #coocurring_tokens(clean_tokens, args, keyword)

if __name__ == "__main__":
    main()
