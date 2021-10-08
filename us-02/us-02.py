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
from datetime import datetime
import numpy as np

#===================================================================================
# Global variables
#===================================================================================

maxResponseLength = 500

#===================================================================================
# semantic analysis functions
#===================================================================================

def tokenizeAndSequence(data):
    # tokenizes an array of strings

    tokenizer = Tokenizer(num_words = 100000, oov_token="<OOV>")
    tokenizer.fit_on_texts(data)
    word_index = tokenizer.word_index
    # print(word_index)

    sequences = tokenizer.texts_to_sequences(data)
    paddedSequences = pad_sequences(sequences, maxlen = 500)

    print("Word Index: ", word_index)
    # print("Sequences: ", sequences)
    print("Padded sequences: ", paddedSequences[0])
    print(paddedSequences.shape)

#===================================================================================
# single reponse functions
#===================================================================================

def responseOption():
    # this function will open a command line editor and limit the text area to 500 characters.
    validResponse = False
    while not validResponse:
        responseValue = str(input("Enter in a response (max 500 characters): "))
        if len(responseValue) > 500:
            print("That was longer than 500 characters!")
        else:
            validResponse = True
    responseArray = []
    responseArray.append(responseValue)

    tokenizeAndSequence(responseArray)

#===================================================================================
# csv file functions
#===================================================================================

def bomValidation(filename, default='utf-8'):
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

def csvWrite(path):
    # This makes a copy of the input csv with responses truncated to 500 chars
    now = datetime.now()
    nowFormat = now.strftime("%d/%m/%Y-%H.%M")

    writeFile = "new-" + path

def csvRead(path, encodingX):
    # this function reads the csv file and makes sure it is formatted correctly. 
    # need to reorder some validation

    data = []
    
    count = 1
    with open(path, newline='', encoding= encodingX) as csvFile:
        csvReader = csv.reader(csvFile, delimiter='|')
        for row in csvReader:

            currentRow = row[0]

            # validate that there is only one element is each record.
            if len(row) != 1:
                print("***Invalid .csv file***")
                break
            else:
                if len(row[0]) > maxResponseLength:
                    print(currentRow + "\n" + "Length was: " + str(len(currentRow)))
                    currentRow = currentRow[0:maxResponseLength] 

                print(currentRow + "\n" + "Length: " + str(len(currentRow)))
                count += 1

                data.append(currentRow)

    return data


def csvOption(): # dont change this to csv(). it will cause errors
    # this function asks user for a path and then validates the path is valid. 
    # this function is essentially the driver code for the .csv option.
    validPath = False
    while not validPath:
        # TODO
        # this will need to change. the user will have to enter full path or browse. 
        # change entered path to the correct path on your computer
        enteredFile = str(input("Enter name of the data set (with the extention): "))
        enteredPath = "C:\\Users\\Drew\\Documents\\app-school-450\\data-sets\\" + enteredFile
        print(enteredPath)
        existingPath = path.exists(enteredPath)
        if existingPath:
            validPath = True
            print("This is a valid path.")
        else:
            # continue just continues the loop. the else isn't nessecary but its good practice.
            print("That was not a valid path or file.")
    endcoding = bomValidation(enteredPath)
    newData = csvRead(enteredPath, endcoding)

    # tokenize
    tokenizeAndSequence(newData)
    
#===================================================================================
# driver code
#===================================================================================

def main():
    validEntry = False
    validEntries = ['r','R','c','C']

    while (not validEntry):

        print("What would you like to like to do? \nImport a .csv file? Or enter in a response? \n ")
        option = str(input("Press 'c' for .csv. Press 'r' for response: "))
        
        if option in validEntries:
            validEntry = True

        else:
            print("\n" + "=" * 50)
            print("Enter a vaild response.")
            print("=" * 50)

    if (option == 'r' or option == 'R'):
        responseOption()
    else:
        csvOption()
    

if __name__ == "__main__":
    main()