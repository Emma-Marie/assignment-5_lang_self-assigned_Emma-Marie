import os
import re
import string
from collections import Counter, OrderedDict
import pandas as pd
import argparse
import csv

# Data paths
DATA_path = os.path.join("..", "..", "768706", "data", "content.dat")
META_path = os.path.join("..", "..", "768706", "metadata", "Joined_Meta.xlsx")

def input_parse():
    #initialie the parser
    parser = argparse.ArgumentParser()
    # add argument
    parser.add_argument("--keyword", type=str) # keyword token
    parser.add_argument("--cooccurring", type=int, default=10) # the number of co-ocurring tokens
    # parse the arguments from command line
    args = parser.parse_args()
    return args

def get_data(data_path, meta_path):
    # load sermons data
    data = pd.read_csv(data_path, index_col=0) 
    # load metadata
    meta = pd.read_excel(meta_path)
    # merge data and metadata on document IDs
    full_data = data.merge(meta, left_on="id", right_on="ID-dok")
    return full_data
    
    # Create empty Series for male and female corpora
    #male_corpus_series = pd.Series()
    #female_corpus_series = pd.Series()

    #for index, row in full_data.iterrows():
    #    if row["køn"] == 1:
    #        male_corpus_series[index] = row["content"]
    #    elif row["køn"] == 2:
    #        female_corpus_series[index] = row["content"]

    #print(f"Length of male corpus is {len(male_corpus_series)}")
    #print(f"Length of female corpus is {len(female_corpus_series)}")

    #return male_corpus_series, female_corpus_series

def clean_data(corpus_series, corpus_name):
    # cleaning text using regex
    corpus_str = corpus_series.to_string(index=False)
    # cleaning text using regex
    corpus_str = corpus_str.replace("\\n", " ")
    corpus_str = corpus_str.replace("\\t", " ")
    # turn every token lowercase
    corpus_str = corpus_str.lower()
    # Remove special characters except hyphen
    corpus_str = re.sub(r'[^a-zA-Z0-9æøåÆØÅ ]', '', corpus_str)

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

def count_keyword(clean_tokens, keyword):
    count = clean_tokens.count(keyword)
    return count

def get_keyword_context(clean_tokens, keyword):
    # get context by finding the five tokens before and after the keyword
    context_data = []
    for idx, token in enumerate(clean_tokens):
        if token == keyword:
            before = ' '.join(clean_tokens[idx-5:idx])
            after = ' '.join(clean_tokens[idx+1:idx+6])
            full = [before, token, after]
            context_data.append(full)

    return context_data

def save_context_data(context_data, keyword, corpus_name):
    keyword_folder = os.path.join("out", keyword)
    os.makedirs(keyword_folder, exist_ok=True)  # Create the keyword subfolder if it doesn't exist
    context_path = os.path.join(keyword_folder, f"context_{keyword}_{corpus_name}.csv")

    with open(context_path, "w", newline='', encoding='utf-8') as file:
        for context in context_data:
            file.write("{:50} {:20} {:50}\n".format(*context))

    print(f"The context of {keyword} in {corpus_name} is saved")

def keyword_context(clean_tokens_male, clean_tokens_female, args):
    keyword = args.keyword
    context_data_male = get_keyword_context(clean_tokens_male, keyword)
    context_data_female = get_keyword_context(clean_tokens_female, keyword)
    save_context_data(context_data_male, keyword, "male")
    save_context_data(context_data_female, keyword, "female")

def get_cooccurring_tokens(clean_tokens, args, keyword, corpus_name):
    # Remove stopwords
    with open("danish_stopwords.txt", "r") as file:
        stopwords = [line.strip() for line in file]
    tokens_no_stopwords = [token for token in clean_tokens if token not in stopwords]
    # choose the number of co-occurrence
    num_cooccurring = args.cooccurring 
    # create a counter for co-occurring tokens
    cooccurring_counter = Counter()
    # iterate over the tokens
    for idx, token in enumerate(tokens_no_stopwords):
        if token == keyword:
            # find the five tokens before and five tokens after the keyword
            cooccurring = tokens_no_stopwords[idx-5:idx] + tokens_no_stopwords[idx+1:idx+6]
            # add co-occurring tokens to list
            cooccurring_counter.update(cooccurring)
    # get the parsed number of most common co-occurring tokens
    most_common_cooccurring = cooccurring_counter.most_common(num_cooccurring)
    # Create a dataframe from the most common co-occurring tokens
    cooccurring_df = pd.DataFrame(most_common_cooccurring, columns=['Token', 'Count'])
    df_path = os.path.join("out", keyword, f"cooccuring_words_{corpus_name}_{keyword}.csv")
    cooccurring_df.to_csv(df_path)
    print(f"{num_cooccurring} most co-occurring words to {keyword} in {corpus_name} are saved")

    return most_common_cooccurring

def main():
    args = input_parse()
    # load and process data
    full_data = get_data(DATA_path, META_path)
    
    # Split data into male and female corpora
    male_corpus_series = full_data.loc[full_data["køn"] == 1, "content"]
    female_corpus_series = full_data.loc[full_data["køn"] == 2, "content"]
    print(f"Length of male corpus is {len(male_corpus_series)}")
    print(f"Length of female corpus is {len(female_corpus_series)}")
    
    # tokenize and clean data
    clean_tokens_male = clean_data(male_corpus_series, "male")
    clean_tokens_female = clean_data(female_corpus_series, "female")
    # Count keyword occurrences
    count_male = count_keyword(clean_tokens_male, args.keyword)
    count_female = count_keyword(clean_tokens_female, args.keyword)
    print(f"{args.keyword} appears {count_male} times in the male corpus")
    print(f"{args.keyword} appears {count_female} times in the female corpus")
    # find sentences in which keyword appears
    keyword_context(clean_tokens_male, clean_tokens_female, args)
    # find and count tokens co-occurring with keyword
    cooccurring_tokens_male = get_cooccurring_tokens(clean_tokens_male, args, args.keyword, "male")
    cooccurring_tokens_female = get_cooccurring_tokens(clean_tokens_female, args, args.keyword, "female")

if __name__ == "__main__":
    main()
