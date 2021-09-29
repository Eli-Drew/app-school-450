"""
=================================================
Author: Drew Rinker
Date:   09/28/21

This file takes care of us-02
=================================================
"""
import csv
import os.path
from os import path

#===================================================================================
# Global variables
#===================================================================================

maxResponseLength = 500

#===================================================================================
# single reponse functions
#===================================================================================

def responseOption():
    # TODO
    # this function will open a command line editor and limit the text area to 500 characters.

    # this is easier than opening a command line editor
    responseValue = str(input("Enter in a response: "))
    if (len(responseValue) > maxResponseLength):
        responseValue = responseValue[0:maxResponseLength]
        print("Response Length = " + str(len(responseValue)))
    else:
        print("Response Length = " + str(len(responseValue)))

#===================================================================================
# csv file functions
#===================================================================================

def bomValidation(record):
    # TODO
    # this function will get rid of the 3 bom characters in the beginning if present

    bomDict = [
        {'name': 'UTF-8', 'sig': b'\xEF\xBB\xBF', 'encoding': 'utf-8'},
        {'name': 'UTF-16 big-endian', 'sig': b'\xFE\xFF', 'encoding': 'utf-16-be'},
        {'name': 'UTF-16 little-endian', 'sig': b'\xFF\xFE', 'encoding': 'utf-16-le'},
        {'name': 'UTF-32 big-endian', 'sig': b'\x00\x00\xFE\xFF', 'encoding': 'utf-32-be'},
        {'name': 'UTF-32 little-endian', 'sig': b'\xFF\xFE\x00\x00', 'encoding': 'utf-32-le'}]

    bomListOriginal = [b'\xEF\xBB\xBF', b'\xFE\xFF', b'\x00\x00\xFE\xFF', b'\xFF\xFE\x00\x00']

    # this list will have to be added to so we can do this for any time of bom encoding
    bomList = ['ï»¿']

    # test = record[:3]

    if record[:3] in bomList:
        record = record[3:]

    # print('record 1 = ' + str(record))
    
    return record

def csvRead(path):

    # this function reads the csv file and makes sure it is formatted correctly. 
    # need to reorder some validation
    count = 0
    with open(path, newline='') as csvFile:
        csvReader = csv.reader(csvFile, delimiter=',')
        for row in csvReader:

            currentRow = row[0]

            if count == 0:
                currentRow = bomValidation(currentRow)
                count += 1
 
            print("Record length is: " + str(len(row[0])))

            # validate that there is only one element is each record.
            if len(row) != 1:
                print("***Invalid .csv file***")
            else:
                if len(row[0]) > maxResponseLength:
                    currentRow = currentRow[0:maxResponseLength] 
                    print("Length now is: " + str(len(currentRow)))
                    

def csvOption(): # dont change this to csv(). it will cause errors

    # this function asks user for a path and then validates the path is valid. 
    validPath = False
    while not validPath:
        enteredPath = str(input("Enter path to the file: "))
        existingPath = path.exists(enteredPath)
        if existingPath:
            validPath = True
            print("This is a valid path.")
            csvRead(enteredPath)

        else:
            # continue just continues the loop. the else isn't nessecary but its good practice.
            print("That was not a valid path or file.")

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