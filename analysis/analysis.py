"""
=================================================
Authors:        Drew Rinker, Henry Knehans
Date:           10/23/21
User Storys:    US-03, US-04, US-05

This file will perform semantic, sentiment, and thematic analysis.
=================================================
"""

import os
from keras.models import Sequential
import tensorflow as tf
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
import numpy as np

"""
Tokenizes an array of strings (the user's response(s)) into sequences and pads/truncates if necessary

Paramaters:
    tokenizer: the tokenizer that was used for the model training/testing data
    data: the response(s) as an array of strings to be pre-processed for analysis
Returns:
    padded_sequences: the padded sequences to be analyzed by the model
"""
def pre_process(tokenizer:Tokenizer, data, max_word_len):
    sequences = tokenizer.texts_to_sequences(data)
    padded_sequences = pad_sequences(sequences, maxlen = max_word_len, padding = 'post', truncating = 'post')
    return padded_sequences

"""
Feeds in and predicts the sentiments of the user's response(s) based off of the model

Paramaters:
    padded_sequences: the user's response(s) as padded sequences which to predict/determine the sentiment
        (must be tokenized with same tokenizer as the tokenizer for the training/testing set)
    model: the trained model to run the padded_sequences against for analysis
Returns:
    sentiments: an array of the estimated sentiments
"""
def feed_tokens_to_graph(padded_sequences, model:Sequential):
    sentiments = model.predict(padded_sequences)
    return sentiments
