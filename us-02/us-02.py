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
import os
import tensorflow as tf
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from datetime import datetime
import numpy as np

#===================================================================================
# Global Variables
#===================================================================================
max_response_length = 500

#===================================================================================
# Semantic Analysis Functions
#===================================================================================
"""
Tokenizes an array of strings (the user's response(s)) into sequences and adds padding if necessary
Paramaters:
    data: the response(s) as an array of strings to be pre-processed for analysis
Returns:
    padded_sequences: the padded sequences to be analyzed by the model
"""
def tokenize_and_sequence(data):
    # TODO change this tokenizer to be the same as the one used for the training/testing data
    tokenizer = Tokenizer(num_words = 100000, oov_token="<OOV>")
    tokenizer.fit_on_texts(data)

    sequences = tokenizer.texts_to_sequences(data)
    padded_sequences = pad_sequences(sequences, maxlen = max_response_length)

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
def feed_tokens_to_graph(padded_sequences, model):
    sentiments = model.predict(padded_sequences)
    return sentiments

#===================================================================================
# Single Reponse Functions
#===================================================================================
"""
Opens a command line editor and limits the text area to 500 characters
Paramaters:
    N/A
Returns:
    response_array: data to then pass in to be tokenized and then analyzed by the model
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

    return response_array

#===================================================================================
# csv File Functions
#===================================================================================
"""
Gets rid of the 3 bom characters in the beginning if present
Paramaters:
    filename: the csv file of records to be validated
    default: 
Returns:
    encoding
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
Makes a copy of the input csv with responses truncated to 500 chars
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
Reads the csv file and makes sure it is formatted correctly
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
                    print("Length was: " + str(len(current_row)))
                    current_row = current_row[0:max_response_length] 

                print("Length: " + str(len(current_row)))
                count += 1

                data.append(current_row)

    return data

"""
This function is essentially the driver code for the .csv option
Asks the user for a path and then validates the path is valid
Don't change the name to csv() or it will cause errors
Paramaters:
    N/A
Returns:
    new_data: data to then pass in to be tokenized and then analyzed by model
"""
def csv_option(): 
    valid_path = False
    while not valid_path:
        # TODO the user will have to enter full path or browse
        entered_file = str(input("Enter name of the data set (with the extention): "))
        entered_path = os.path.join(os.getcwd(), 'data-sets', entered_file)
        path_exists = os.path.exists(entered_path)
        if path_exists:
            valid_path = True
            # print("This is a valid path.")
        else:
            # continue just continues the loop. the else isn't nessecary but its good practice.
            print("That was not a valid path or file.")
    endcoding = bom_validation(entered_path)
    new_data = csv_read(entered_path, endcoding)

    return new_data
    
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

    data = response_option() if (option == 'r' or option == 'R') else csv_option()
    
    padded_sequences = tokenize_and_sequence(data)
    print(padded_sequences)
    # feed_tokens_to_graph(padded_sequences)

if __name__ == "__main__":
    main()