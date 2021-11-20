"""
=================================================
Authors:        Drew Rinker, Henry Knehans
Date:           09/28/21
User Storys:    US-02

This file gets the user's single response or csv
    file of responses via the command line.
=================================================
"""

# TODO organize imports in separate files
import csv
import os
from datetime import datetime
from analysis.Response import Response

#===================================================================================
# Global Variables
#===================================================================================
response_objs = []

#===================================================================================
# Single Reponse Functions
#===================================================================================
"""
===================================================================
Description:
    Opens a command line to recieve and limits the text area to max_len words
Paramaters:
    max_len: the max word length a response can be
Returns:
    an array of the one response from the user
===================================================================
"""
def response_option(max_len):
    valid_response = False
    while not valid_response:
        response_value = str(input("Enter in a response (max {} words): ".format(max_len)))
        # TODO len(response_value) returns the number or characters. We need to change this condition to check for word length instead
        if len(response_value) > max_len:
            print("That was longer than {} words!".format(max_len))
        else:
            valid_response = True
    response_array = []
    response_array.append(response_value)
    return response_array


#===================================================================================
# csv File Functions
#===================================================================================
"""
===================================================================
Description:
    Gets rid of the 3 bom characters in the beginning if present
Paramaters:
    filename: the csv file of records to be validated
    default: the default encoding that would be returned
Returns:
    the encoding detected in the csv file
===================================================================
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
===================================================================
Description:
    Makes a copy of the input csv
Paramaters:
    path: the path of the csv file
Returns:
    N/A
===================================================================
"""
def csv_write(path):
    now = datetime.now()
    now_format = now.strftime("%d/%m/%Y-%H.%M")
    write_file = "new-" + path


"""
===================================================================
Description:
    Reads the csv file and makes sure it is formatted correctly
Paramaters:
    path: the path of the csv file
    encodingX: the encoding found by bom_validation()
Returns:
    an array of responses from the csv file
===================================================================
"""
def csv_read(path, encodingX):
    responses = []
    with open(path, newline='', encoding= encodingX) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter='|')
        for row in csv_reader:
            # # Validate that there is only one element in each record.
            # if len(row) != 1:
            #     print("***Invalid .csv file. The file must only contain one element per row***")
            #     break
            # else:
            #     current_resp = row[0]
            #     if len(current_resp) > max_len:
            #         print("Length was: " + str(len(current_resp)))
            #         current_resp = current_resp[0:max_len] 

            #     print("Length: " + str(len(current_resp)))

            #     data.append(current_resp)
            try:
                responses.append(row[0])
                # Create new response object and appends to list
                response_objs.append(Response(row[0]))
            except:
                pass
    return responses


"""
===================================================================
Description:
    This function is essentially the driver code for the .csv option.
    Asks the user for a path and then validates the path is valid.
Paramaters:
    N/A
Returns:
    data to then pass in to be tokenized and then analyzed by model
===================================================================
"""
def csv_option():
    valid_path = False
    while not valid_path:
        # TODO the user will have to enter full path or browse
        entered_file = str(input("Enter name of the data set (with the extention): "))
        entered_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data_sets', entered_file)
        if os.path.exists(entered_path):
            valid_path = True
        else:
            print("That was not a valid path or file.")
    endcoding = bom_validation(entered_path)
    responses = csv_read(entered_path, endcoding)
    return responses


#===================================================================================
# Main prompting function
#===================================================================================
"""
===================================================================
Description:
    This function prompts the user via command line for either a 
    single response or csv file of responses. An array of the response(s)
    is returned to then pass in and be analyzed by the model.
Paramaters:
    max_len: the max word length a response can be
Returns:
    the array of response(s)
===================================================================
"""
def get_input(max_len):

    valid_entry = False
    valid_entries = ['r','R','c','C']

    while not valid_entry:

        print("What would you like to like to do? \nImport a .csv file? Or enter in a response? \n ")
        option = str(input("Press 'c' for .csv. Press 'r' for response: "))
        
        if option in valid_entries:
            valid_entry = True
        else:
            print("\n" + "=" * 50)
            print("Enter a vaild response.")
            print("=" * 50)

    return response_option(max_len) if (option == 'r' or option == 'R') else csv_option()
