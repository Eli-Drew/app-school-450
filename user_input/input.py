import csv, os

"""
===================================================================
Description:
    Receives and limits the text area to max_len words
Paramaters:
    response: the string resonse passed in if running from the GUI
        or None if passed in for command line
    max_len: the max word length the response can be
Returns:
    an array of response from the user
===================================================================
"""
def response_option(response, max_len):
    
    # True when runnning application from command line
    if response == None:
        response = str(input("Enter in a response with no more than {} words: ".format(max_len)))

    if len(response.split()) > max_len:
        response =  ' '.join(response.split()[0:max_len])

    return [response]


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
            if sig[0:sl] in msboms:
                return msboms[sig[0:sl]]['encoding']
        return default


"""
===================================================================
Description:
    Reads the csv file and makes sure it is formatted correctly
Paramaters:
    csv_file_path: the string path of the csv file
    encodingX: the encoding found by bom_validation()
    max_len: the max word length a response can be
Returns:
    an array of string responses from the csv file
===================================================================
"""
def csv_read(csv_file_path, encodingX, max_len):
    
    responses = []

    with open(csv_file_path, newline='', encoding=encodingX) as csv_file:    
        csv_reader = csv.reader(csv_file, delimiter='|')
        for row in csv_reader:
            try:
                response = row[0]
                if len(response.split()) > max_len:
                    response =  ' '.join(response.split()[0:max_len])
                responses.append(response)
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
        the GUI or None if passed in for command line
    max_len: the max word length a response can be
Returns:
    an array of string responses
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
    return csv_read(csv_file_path, endcoding, max_len)


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

    return response_option(None, max_len) if (option == 'r' or option == 'R') else csv_option(None, max_len)
