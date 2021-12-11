"""

Copyright 2021 Brent Anderson, Hannah Bolick, Kadidia Kantao, Henry Knhans and Drew Rinker

Permission is hereby granted, free of charge, to any person obtaining a copy of this software 
and associated documentation files (the "Software"), to deal in the Software without restriction, 
including without limitation the rights to use, copy, modify, merge, publish, distribute, 
sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is 
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or 
substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, 
INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A 
PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR 
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN 
AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION 
WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

"""


from analysis.Analysis import Analysis
from analysis.Thematic_Anlaysis import Thematic_Analysis

class Top_Words_Analysis(Analysis):

    """
    ===================================================================
    Description:
        Iterates through all words from the user's responses and creates
        a dictionary of the words seen and their count of occurrences
    Paramaters:
        responses: TBD based on implementation
            (responses needs to end up being a 2D array of strings before iterating through)
        max_len: the max word count that the responses can have
    Returns:
        Dictionary with all words and their count of occurrences
    ===================================================================
    """
    @classmethod
    def pre_process(cls, responses, max_len):
        # TODO uncomment line after first ensuring pre_process() is working correctly
        # TODO The pre-processed responses returned from Thematic_Analysis.pre_process() called in main
        #       should probably actually be passed in instead
        # responses = Thematic_Analysis.pre_process(responses, max_len)
        word_dict = {}
        for resp in responses:
            for word in resp.split():
                if word not in word_dict:
                    word_dict[word] = 1
                else:
                    word_dict[word] += 1
        return word_dict


    """
    ===================================================================
    Description:
        Takes the word_dict returned by created_word_dict() and finds the
        top 5 words with the highest counts
    Paramaters:
        word_dict: dictionary with all words and their count of occurrences
    Returns:
        Dictionary of the top 5 words and their counts
    ===================================================================
    """
    @classmethod
    def analyze(cls, word_dict):

        top_words_dict = {
            "word1" : 0,
            "word2" : 0,
            "word3" : 0,
            "word4" : 0,
            "word5" : 0
        }

        min_top_word = "word1"
        min_top_count = 0

        # Find the top 5 words with the highest counts
        for word, count in word_dict.items():

            if count > min_top_count:
                del top_words_dict[min_top_word]
                top_words_dict[word] = count
                min_top_word = word
                min_top_count = count

                # Find the current minimum word/count entry in top_words_dict
                for top_word, top_count in top_words_dict.items():
                    if top_count < min_top_count:
                        min_top_word = top_word
                        min_top_count = top_count

        # Find and remove any word from top_words_dict if any initial entry is still present
        # This is a very rare case
        remove_words = []
        for word, count in top_words_dict.items():
            if count == 0:
                remove_words.append(word)
        for word in remove_words:
            del top_words_dict[word]

        return top_words_dict


    """
    ===================================================================
    Description:
        Sorts top_words_dict based on value from greatest to least
    Paramaters:
        top_words_dict: Dictionary of the top 5 words and their counts
            returned by analyze()
    Returns:
        Dictionary of the top 5 words and their counts sorted from
        greatest to least
    ===================================================================
    """
    @classmethod
    def format_results(cls, top_words_dict):

        sorted_words_dict = {}
        max_count_word = ""
        max_count = 0
        
        for i in range(len(top_words_dict)):

            for word, count in top_words_dict.items():
                if word in sorted_words_dict.keys():
                    continue
                elif count > max_count:
                    max_count = count
                    max_count_word = word

            sorted_words_dict[max_count_word] = max_count
            max_count_word = ""
            max_count = 0

        return sorted_words_dict

    
    """
    ===================================================================
    Description:
        Prints the top 5 words and their count of occurrences
    Paramaters:
        sorted_words_dict: Dictionary of the top 5 words and their counts
            sorted from greatest to least
    Returns:
        N/A
    ===================================================================
    """
    @classmethod
    def print_top_words(cls, sorted_words_dict):
        print("\nTop {} Occurring Words:".format(len(sorted_words_dict)))
        for word, count in sorted_words_dict.items():
            print("{}: {}".format(word, count))
