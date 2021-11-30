import csv, os

"""
===================================================================
Description:
    Receives and limits the text area to max_len words
Paramaters:
    max_len: the max word length the response can be
Returns:
    an array of response from the user
===================================================================
"""
def response_option(max_len):
    valid_response = False
    while not valid_response:
        response = str(input("Enter in a response with no more than {} words: ".format(max_len)))
        if len(response.split()) > max_len:
            print("That was longer than {} words!".format(max_len))
        else:
            valid_response = True
    return [response]


"""
===================================================================
Description:
    Gets rid of the 3 bom characters in the beginning if present
Paramaters:
    filename: the csv file of records to be validated
    default: the default encoding to be returned
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
    Reads the csv file and makes sure it is formatted correctly
Paramaters:
    path: the path of the csv file
    encodingX: the encoding found by bom_validation()
Returns:
    an array of string responses from the csv file
===================================================================
"""
def csv_read(path, encodingX):
    responses = []
    with open(path, newline='', encoding=encodingX) as csv_file:
        csv_reader = csv.reader(csv_file)
        for row in csv_reader:
            # TODO Cleanup if/else and try/except
            # Validate that there is only one element in each record.
            try:
                responses.append(row[0])
            except:
                print("***Invalid csv file. The file must only contain one element per row***")
    return responses


"""
===================================================================
Description:
    Prompts the user for a csv file, validates, and then returns
    the file as an array of responses
Paramaters:
    N/A
Returns:
    an array of string responses
===================================================================
"""
def csv_option():
    valid_path = False
    while not valid_path:
        entered_file = str(input("Enter name of csv file with extension: "))
        entered_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data_sets', entered_file)
        if os.path.exists(entered_path):
            valid_path = True
        else:
            print("That was not a valid path or file.")
    endcoding = bom_validation(entered_path)
    return csv_read(entered_path, endcoding)


"""
===================================================================
Description:
    This function prompts the user via command line for either a 
    single response or csv file of responses. An array of the response(s)
    is returned to then go through analysis.
Paramaters:
    max_len: the max word length a response can be
Returns:
    an array of string responses
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

    return response_option(max_len) if (option == 'r' or option == 'R') else csv_option()
