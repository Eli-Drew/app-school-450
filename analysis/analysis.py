"""
=================================================
Authors:        Drew Rinker, Henry Knehans
Date:           10/23/21
User Storys:    US-03, US-04, US-05

This file will perform semantic, sentiment, and thematic analysis.
=================================================
"""


import os
from tensorflow.keras.models import Sequential
import tensorflow as tf
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
import numpy as np
from nltk.corpus import stopwords
from textblob import Word
from textblob import TextBlob
import nltk
nltk.download('stopwords')

"""
Tokenizes an array of strings (the user's response(s)) into sequences and pads/truncates if necessary

Paramaters:
    tokenizer: the tokenizer that was used for the model training/testing data
    data: the response(s) as an array of strings to be pre-processed for analysis
Returns:
    padded_sequences: the padded sequences to be analyzed by the model
"""


def pre_process(tokenizer: Tokenizer, data, max_word_len):
    sequences = tokenizer.texts_to_sequences(data)
    padded_sequences = pad_sequences(
        sequences, maxlen=max_word_len, padding='post', truncating='post')
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


def feed_tokens_to_graph(padded_sequences, model: Sequential):
    sentiments = model.predict(padded_sequences)
    return sentiments


"""
===================================================================
Description: getData returns the data located at the fileName param
Param(s): fileName path for data.
Returns: dataset as list of one element (entire dataset as one elem)
===================================================================
"""


def getData(fileName):
    # open file
    data = open(fileName, "r", encoding='UTF8')
    # split the file data
    splitData = data.read().replace('"', ' ').replace('’', '\'').split('\n\n')
    # convert all text to lowercase and replace all newlines with a space
    realData = [x.lower().replace('\n', ' ')
                for x in splitData if len(x) > 500]
    return realData


"""
===============================================================
Description: getCleanData returns its data param after cleaning
Param(s): data list (from getData())
Returns: A list of text, for example:

['great', 'great presentation', 'great presentation clear',...]

===============================================================
"""


def getCleanData(data):
    cleanData = []
    # stop words are words that lack context meaning but occur frequently in natural language
    stop_words = set(stopwords.words('english'))
    for d in data:
        tokens = ' '.join(TextBlob(d).noun_phrases).split()
        cleanD = []
        for w in tokens:
            # convert words to their base form, like plural to singular
            w = Word(w).lemmatize()
            if w not in stop_words and len(w) > 4:
                cleanD.append(w)
            if len(cleanD) != 0:
                cleanData.append(' '.join(cleanD))
    return cleanData


"""
=================================================================================
Description: getTopics prints the the repective topics and their components
Param(s): model components, feature names, and n = the number of words per topic.
Returns: Nothing, just prints topics (at least for now).
=================================================================================
"""


def getTopics(components, feature_names, n=50):
    for idx, topic in enumerate(components):
        print("\nTopic %d: " % (
            idx+1), [(feature_names[i], topic[i].round(2)) for i in topic.argsort()[:-n - 1:-1]])
