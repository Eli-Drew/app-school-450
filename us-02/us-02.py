"""
Author: Drew Rinker
Test File for user story 2

"""
import csv
import os.path
from os import path


#===================================================================================
# single reponse functions
#===================================================================================

def responseOption():
    # TODO
    # this function will open a command line editor and limit the text area to 500 characters.

    # this is easier than opening a command line editor
    responseValue = str(input("Enter in a response: "))
    if (len(responseValue) > 500):
        responseValue = responseValue[0:499]
        print("Response Length = " + str(len(responseValue)))
    else:
        print("Response Length = " + str(len(responseValue)))

#===================================================================================
# csv file functions
#===================================================================================

def csvRead(path):
    # TODO
    # this function reads the csv file and makes sure it is formatted correctly. 
    with open(path, newline='') as csvFile:
        csvReader = csv.reader(csvFile, delimiter=',')
        for row in csvReader:
            print(row)

def csvOption(): # dont change this to csv(). it will cause errors
    # TODO
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
            continue

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