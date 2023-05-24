# system tools
import os
import sys
sys.path.append(".") # necessary if I don't use utils?
# data processing tools
import string, os 
import pandas as pd
import numpy as np
np.random.seed(42)
# keras module for building LSTM 
import tensorflow as tf
tf.random.set_seed(42)
import tensorflow.keras.utils as ku 
from tensorflow.keras.models import Sequential
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.layers import Embedding, LSTM, Dense, Dropout
# surpress warnings
import warnings
warnings.filterwarnings("ignore")
warnings.simplefilter(action='ignore', category=FutureWarning)
# utils
import sys
sys.path.append(".")
import utils.requirement_functions as rf
# save tokenizer
from joblib import dump, load

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
    corpus = full_data["content"][1:10] # I chose a small sample of sermons to provide the run from being "killed". 
    print("corpus of sermons generated")

    return corpus

def sermons_tokenizer(corpus):
    # tokenization created by TensorFlow
    tokenizer = Tokenizer()
    tokenizer.fit_on_texts(corpus)
    total_words = len(tokenizer.word_index) + 1
    print("Tokenization done")
    # turn input (the sermon content) into numerical output
    inp_sequences = rf.get_sequence_of_tokens(tokenizer, corpus)
    # pad input (make sequences the same length)
    predictors, label, max_sequence_len = rf.generate_padded_sequences(inp_sequences, total_words)
    # save tokenizer
    tokenizer_path = os.path.join("models", "RNN_tokenizer.joblib")
    dump(tokenizer, tokenizer_path)

    return max_sequence_len, total_words, predictors, label

def rnn_model(max_sequence_len, total_words, predictors, label):
   #create model
    model = rf.create_model(max_sequence_len, total_words)
    print(model.summary())
    #Train model
    history = model.fit(predictors, 
                        label, 
                        epochs=1, # make higher? Before it was 100
                        batch_size=128,
                        verbose=1)
    # Save model
    modelpath = os.path.join("models", f"rnn-model_seq{max_sequence_len}.keras")
    tf.keras.models.save_model(model, modelpath, overwrite=False, save_format=None)
    print("Model saved!")

def main():
    # load and prepare dataset
    corpus = get_data()
    # tokenize data
    max_sequence_len, total_words, predictors, label = sermons_tokenizer(corpus)
    # train RNN model
    rnn_model(max_sequence_len, total_words, predictors, label)

if __name__ == "__main__":
    main()