import os
import csv
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from keras.models import Sequential
from tensorflow.keras.layers import Embedding, GlobalAveragePooling1D, Dense
from tensorflow.python.keras.layers.core import Flatten
import numpy as np

"""
This function should be broken up and only be in the Jupyter Notebook file 
but is here soley for testing purposes until we find a way to import the
trained/tested model from the .ipynb file.

This function builds a keras Sequential model and trains/tests it with test_data_file.
It then returns the model along with the tokenizer used to build it.

Paramaters:
    N/A
Returns:
    model: the trained and tested model
    tokenizer: the tokenizer that was used for the model and should be used
                for the pre-processing of the response data
"""

def create_model(max_word_len):

    print("\nCreating model...\n")

    # Read in the test_data_file and append to the responses and sentiments arrays
    path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'data_sets', 'henry_test_data.csv')
    with open(path, newline = '', encoding = 'utf-8') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter='|')
        responses = []
        sentiments = []
        for row in csv_reader:
            try:
                responses.append(row[0])
                sentiments.append(float(row[1]))
            except:
                pass
        global training_size
        training_size = len(responses) // 2
    
    # Split the responses and sentiments into training and testing sets
    training_responses = responses[0:training_size]
    testing_responses = responses[training_size:]
    training_sentiments = sentiments[0:training_size]
    testing_sentiments = sentiments[training_size:]

    vocab_size = 1000   # hovering over Embedding() shows that vocab_size should not be greater than 1000
    tokenizer = Tokenizer(num_words = vocab_size, oov_token="<OOV>")
    tokenizer.fit_on_texts(training_responses)

    training_sequences = tokenizer.texts_to_sequences(training_responses)
    training_padded = pad_sequences(training_sequences, maxlen = max_word_len, padding = 'post', truncating = 'post')
    testing_sequences = tokenizer.texts_to_sequences(testing_responses)
    testing_padded = pad_sequences(testing_sequences, maxlen = max_word_len, padding = 'post', truncating = 'post')

    # Convert to NumPy arrays. Necessary for model
    training_padded = np.array(training_padded)
    training_sentiments = np.array(training_sentiments)
    testing_padded = np.array(testing_padded)
    testing_sentiments = np.array(testing_sentiments)

    # Building the model
    model = Sequential()
    model.add(Embedding(vocab_size, 10, input_length=max_word_len))
    model.add(GlobalAveragePooling1D())
    # model.add(Flatten())  # The Flatten layer was used in one video I saw. May want to look further into for future model
    model.add(Dense(24, activation="relu"))
    model.add(Dense(1, activation="sigmoid"))
    model.compile(optimizer="adam", loss="binary_crossentropy", metrics=["accuracy"])

    # Train the model
    num_epochs = 15
    model.fit(training_padded, training_sentiments, epochs=num_epochs,
              validation_data=(testing_padded, testing_sentiments), verbose=2)

    print()

    return model, tokenizer
