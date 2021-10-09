"""
=================================================
Author: Drew Rinker
Date:   09/28/21

This file takes care of us-02.

I believe we will need to train and then test 
the data. I'm not sure how to do that yet. 
=================================================
"""
import csv
import os.path
from os import path
from typing import Sequence
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from keras.models import Sequential
from tensorflow.keras.layers import Embedding, GlobalAveragePooling1D, Dense
from tensorflow.python.keras.layers.core import Flatten
from datetime import datetime
import numpy as np

#===================================================================================
# Global Variables
#===================================================================================
max_response_length = 500
vocab_size = max_response_length
test_data = "some test data"
training_size = len(test_data) / 2
vector_size = 10 # (?) not sure what a good vector size would be

#===================================================================================
# Semantic Analysis Functions
#===================================================================================
"""
Creates a tokenizer and generates the training and testing sequences
Paramaters:
    test_data: the data to create and train/test the model
        (I'm guessing this test_data will come in as a large csv file)
Returns:
    void
"""
def generate_training_testing_seq(test_data):
    # First grab the responses and given sentiments
    dummy_responses = test_data['response']

    # Split data into training and testing
    global training_responses
    global testing_responses
    training_responses = dummy_responses[0:training_size]
    testing_responses = dummy_responses[training_size:]
    
    # Create a global tokenizer and word_index (this tokenizer needs to be used for the actual analysis)
    global tokenizer
    tokenizer = Tokenizer(num_words = vocab_size, oov_token="<OOV>")
    tokenizer.fit_on_texts(training_responses)
    word_index = tokenizer.word_index

    global training_padded
    training_sequences = tokenizer.texts_to_sequences(training_responses)
    training_padded = pad_sequences(training_sequences, maxlen=max_response_length)

    global testing_padded
    testing_sequences = tokenizer.texts_to_sequences(testing_responses)
    testing_padded = pad_sequences(testing_sequences, maxlen=max_response_length)

"""
This function builds the model with training and testing data
Paramaters:
    training_padded: the training set of responses padded
    training_responses: the training set of responses padded
    testing_padded: the testing set of responses padded
    testing_responses: the training set of responses padded
Returns:
    model: the model that has been trainined
"""
def build_model():
    model = Sequential()
    model.add(Embedding(vocab_size, vector_size, input_length=max_response_length, name="embedding"))
    model.add(GlobalAveragePooling1D())
    model.add(Flatten())
    model.add(Dense(1, activation="sigmoid"))
    model.compile(optimizer="adam", loss="binary_crossentropy", metrics=["accuracy"])

    # train the model
    num_epochs = 30
    model.fit(training_padded, training_responses, epochs=num_epochs,
                validation_data=(testing_padded, testing_responses), verbose=2)

    return model

"""
This function feeds in and predicts the sentiments of the responses based off of the model
Paramaters:
    padded_sequences: the data which to predict/determine the sentiment
        (must be tokenized with same tokenizer as the tokenizer for training set )
    model: the trained model to run the padded_sequences against for analysis
Returns:
    sentiments: an array or the estimated sentiments
"""
def feed_tokens_to_graph(padded_sequences, model):
    sentiments = model.predict(padded_sequences)
    return sentiments

"""
Tokenizes an array of strings into sequences and adds padding if necessary
Paramaters:
    data: the response(s) to be processed for analysis
Returns:
    void
"""
def pre_process(data):
    generate_training_testing_seq(test_data)
    # the global tokenizer created from generate_training_testing_seq(test_data) needs to be used
    sequences = tokenizer.texts_to_sequences(data)
    padded_sequences = pad_sequences(sequences, maxlen = max_response_length)

    model = build_model()

    sentiments = feed_tokens_to_graph(padded_sequences, model)
    print(sentiments)

#===================================================================================
# Single Reponse Functions
#===================================================================================
"""
This function will open a command line editor and limit the text area to 500 characters.
Paramaters:
    N/A
Returns:
    void
"""
def response_option():
    valid_response = False
    while not valid_response:
        response_value = str(input("Enter in a response (max 500 characters): "))
        if len(response_value) > 500:
            print("That was longer than 500 characters!")
        else:
            valid_response = True
    response_array = []
    response_array.append(response_value)

    pre_process(response_array)

#===================================================================================
# csv File Functions
#===================================================================================
"""
This function will get rid of the 3 bom characters in the beginning if present
Paramaters:
    filename: the csv file of records to be validated
Returns:
    the record after validation
"""
def bom_validation(filename, default='utf-8'):
    msboms = dict((bom['sig'], bom) for bom in (
        {'name': 'UTF-8', 'sig': b'\xEF\xBB\xBF', 'encoding': 'utf-8'},
        {'name': 'UTF-16 big-endian', 'sig': b'\xFE\xFF', 'encoding':
            'utf-16-be'},
        {'name': 'UTF-16 little-endian', 'sig': b'\xFF\xFE', 'encoding':
            'utf-16-le'},
        {'name': 'UTF-32 big-endian', 'sig': b'\x00\x00\xFE\xFF', 'encoding':
            'utf-32-be'},
        {'name': 'UTF-32 little-endian', 'sig': b'\xFF\xFE\x00\x00',
            'encoding': 'utf-32-le'}))

    with open(filename, 'rb') as f:
        sig = f.read(4)
        for sl in range(3, 0, -1):
            if sig[0:sl] in msboms:
                return msboms[sig[0:sl]]['encoding']
        return default

"""
This makes a copy of the input csv with responses truncated to 500 chars
Paramaters:
    path: the path of the csv file
Returns:
    N/A
"""
def csv_write(path):
    now = datetime.now()
    now_format = now.strftime("%d/%m/%Y-%H.%M")

    write_file = "new-" + path

"""
This function reads the csv file and makes sure it is formatted correctly. 
Paramaters:
    path: the path of the csv file
    encodingX:
Returns:
    data: response data from the csv file
"""
def csv_read(path, encodingX):
    # need to reorder some validation

    data = []
    
    count = 1
    with open(path, newline='', encoding= encodingX) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter='|')
        for row in csv_reader:

            current_row = row[0]

            # validate that there is only one element is each record.
            if len(row) != 1:
                print("***Invalid .csv file***")
                break
            else:
                if len(row[0]) > max_response_length:
                    print(current_row + "\n" + "Length was: " + str(len(current_row)))
                    current_row = current_row[0:max_response_length] 

                print(current_row + "\n" + "Length: " + str(len(current_row)))
                count += 1

                data.append(current_row)

    return data

"""
This function is essentially the driver code for the .csv option
This function asks user for a path and then validates the path is valid
Don't change the name to csv(). or it will cause errors
Paramaters:
    N/A
Returns:
    N/A
"""
def csv_option(): 
    valid_path = False
    while not valid_path:
        # TODO the user will have to enter full path or browse
        entered_file = str(input("Enter name of the data set (with the extention): "))
        entered_path = path.join(os.getcwd(), 'data-sets', entered_file) # this is dynamic and doesn't require us to change to our own path
        print(entered_path)
        path_exists = path.exists(entered_path)
        if path_exists:
            valid_path = True
            print("This is a valid path.")
        else:
            # continue just continues the loop. the else isn't nessecary but its good practice.
            print("That was not a valid path or file.")
    endcoding = bom_validation(entered_path)
    new_data = csv_read(entered_path, endcoding)

    # tokenize
    pre_process(new_data)
    
#===================================================================================
# Driver Code
#===================================================================================

def main():
    valid_entry = False
    valid_entries = ['r','R','c','C']

    while (not valid_entry):

        print("What would you like to like to do? \nImport a .csv file? Or enter in a response? \n ")
        option = str(input("Press 'c' for .csv. Press 'r' for response: "))
        
        if option in valid_entries:
            valid_entry = True
        
        else:
            print("\n" + "=" * 50)
            print("Enter a vaild response.")
            print("=" * 50)

    response_option() if (option == 'r' or option == 'R') else csv_option()
    

if __name__ == "__main__":
    main()