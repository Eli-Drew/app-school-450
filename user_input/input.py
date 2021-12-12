"""
===================================================================================================
Copyright 2021 Brent Anderson, Hannah Bolick, Kadidia Kantao, Henry Knehans, Drew Rinker
Permission is hereby granted, free of charge, to any person obtaining a copy of this software 
and associated documentation files (the 'Software'), to deal in the Software without restriction, 
including without limitation the rights to use, copy, modify, merge, publish, distribute, 
sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is 
furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in all copies or 
substantial portions of the Software.
THE SOFTWARE IS PROVIDED 'AS IS', WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, 
INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A 
PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR 
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN 
AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION 
WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
===================================================================================================
"""

"""
======================================
Class SDD reference: Section 3.2.2.3.5
======================================
"""

import os, csv
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2' # suppresses tf info and warning logs
from tensorflow.keras.preprocessing.text import text_to_word_sequence
from nltk.corpus import stopwords
from textblob import Word

"""
===================================================================
Description:
    Receives and limits the text area to max_len words
Paramaters:
    response: the string resonse passed in if running from the GUI
        or None if passed in for command line
    max_len: the max word length a response will be truncated to
Returns:
    a list of one string response pre-processed;
    a list of one string response without any pre-processing
===================================================================
"""
def response_option(response, max_len):
    
    # True when runnning application from command line
    if response == None:
        response = str(input("Enter in a response with no more than {} words: ".format(max_len)))

    return pre_process([response], max_len), [response]


"""
===================================================================
Description:
    Finds the encoding of the csv file being read
Paramaters:
    csv_file_path: the string csv file path of records to be validated
    default: the default encoding to be returned
Returns:
    the encoding detected in the csv file
===================================================================
"""
def bom_validation(csv_file_path, default='utf-8'):

    msboms = dict((bom['sig'], bom) for bom in (
        {'name': 'UTF-8', 'sig': b'\xEF\xBB\xBF', 'encoding': 'utf-8'},
        {'name': 'UTF-16 big-endian', 'sig': b'\xFE\xFF', 'encoding':
            'utf-16-be'},
        {'name': 'UTF-16 little-endian', 'sig': b'\xFF\xFE', 'encoding':
            'utf-16-le'},
        {'name': 'UTF-32 big-endian', 'sig': b'\x00\x00\xFE\xFF', 'encoding':
            'utf-32-be'},
        {'name': 'UTF-32 little-endian', 'sig': b'\xFF\xFE\x00\x00',
            'encoding': 'utf-32-le'},
        {'name': 'UTF-8-SIG', 'sig': b'\xef\xbb\xbf', 'encoding': 'utf-8-sig'}))

    with open(csv_file_path, 'rb') as csv_file:
        sig = csv_file.read(4)
        for sl in range(3, 0, -1):
            if sig[:sl] in msboms:
                return msboms[sig[:sl]]['encoding']
        return default


"""
===================================================================
Description:
    Reads the csv file and makes sure it is formatted correctly
Paramaters:
    csv_file_path: the string path of the csv file
    encodingX: the encoding found by bom_validation()
Returns:
    a list of string responses from the csv file
===================================================================
"""
def csv_read(csv_file_path, encodingX):
    
    responses = []

    with open(csv_file_path, newline='', encoding=encodingX) as csv_file:    
        csv_reader = csv.reader(csv_file, delimiter='|')
        for row in csv_reader:
            try:
                responses.append(row[0])
            except:
                print("***Invalid row. The file must only contain one element per row***")

    return responses


"""
===================================================================
Description:
    If called from get_input() for app to be ran via command line,
    prompts the user for a csv file. If not, uses the path retrieved
    from the GUI. Validates and then returns the file as an array
    of responses
Paramaters:
    csv_file_path: the string path of the csv file if running from
        the GUI or None if passed for command line
    max_len: the max word length a response will be truncated to
Returns:
    a list of string responses pre-processed;
    a list of string responses without any pre-processing
===================================================================
"""

def csv_option(csv_file_path, max_len):

    # True when runnning application from command line
    if csv_file_path == None:

        valid_path = False
        while not valid_path:
            
            csv_file_path = str(input("Enter full path name of csv file with extension: "))
            if not (os.path.exists(csv_file_path) and csv_file_path[-4:] == '.csv'):
                print("That was not a valid csv path or file. File must exist and end in a \'.csv\' extension.")
            else:
                valid_path = True
    
    # When runnning application from GUI
    else:
        if not (os.path.exists(csv_file_path) and csv_file_path[-4:] == '.csv'):
            return "INVALID"

    endcoding = bom_validation(csv_file_path)
    responses = csv_read(csv_file_path, endcoding)
    return pre_process(responses, max_len), responses


"""
===================================================================
Description:
    General pre-processing of user input for all analyses which
    removes non-alphanumeric characters, truncates to max_len
    words, removes stop words, and lemmatizes words
Paramaters:
    responses: a list of strings from user input
    max_len: the max word length a response will be truncated to
Returns:
    a list of pre-processed strings
===================================================================
"""
def pre_process(responses, max_len):
    
    stop_words = set(stopwords.words('english'))

    clean_responses = []
    for response in responses:

        # Filter out non-alphanumeric characters and truncate to max_len
        response = text_to_word_sequence(response)
        if len(response) > max_len:
            response = response[:max_len]
        
        # Remove stop words and lemmatize words from response
        clean_response = []
        for word in response:
            if word not in stop_words:
                clean_response.append(Word(word).lemmatize())
        clean_responses.append(' '.join(clean_response))

    return clean_responses

"""
===================================================================
Description:
    This function prompts the user via command line for either a 
    single response or csv file of responses. An array of the response(s)
    is returned to then go through analysis.
Paramaters:
    max_len: the max word length a response can be
Returns:
    a list of string responses
===================================================================
"""
def get_input(max_len):

    valid_entry = False
    valid_entries = ['r','R','c','C']

    while not valid_entry:

        print("\nImport a csv file or type a response?")
        option = str(input("Press 'c' for csv. Press 'r' for response: "))
        
        if option in valid_entries:
            valid_entry = True
        else:
            print("\n" + "=" * 50)
            print("Enter a vaild response.")
            print("=" * 50)

    if (option == 'r' or option == 'R'):
        return response_option(None, max_len)
    else:
        return csv_option(None, max_len)
