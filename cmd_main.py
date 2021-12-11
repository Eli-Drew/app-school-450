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


print("Welcome to the Feedback Response Analysis Tool")
print("Please wait for startup...")

from user_input.input import get_input
from analysis.Sentiment_Analysis import Sentiment_Analysis
from analysis.Thematic_Anlaysis import Thematic_Analysis
from analysis.Top_Words_Analysis import Top_Words_Analysis

MAXLEN = 250

def main():

    flag = True
    while flag:

        # Get user's responses
        responses = get_input(MAXLEN)

        # Sentiment Analysis
        padded_sequences = Sentiment_Analysis.pre_process(responses, MAXLEN)
        sentiments = Sentiment_Analysis.analyze(padded_sequences)
        sentiment_analysis_results = Sentiment_Analysis.format_results(sentiments)
        featured_responses = Sentiment_Analysis.get_featured_responses(
            responses, sentiments, sentiment_analysis_results["average"][1])
        
        # Thematic Analysis
        # clean_responses = Thematic_Analysis.pre_process(responses, MAXLEN)
        # feature_names = Thematic_Analysis.analyze(clean_responses)
        # themes = Thematic_Analysis.format_results(feature_names)
        
        # Top Words Analysis
        word_dict = Top_Words_Analysis.pre_process(responses, MAXLEN)
        top_words_dict = Top_Words_Analysis.analyze(word_dict)
        sorted_top_words_dict = Top_Words_Analysis.format_results(top_words_dict)

        # Print Analysis Results
        print("\n=================Analysis Results=================")
        Sentiment_Analysis.print_sentiment_results(sentiment_analysis_results, featured_responses)
        # Thematic_Analysis.print_themes(themes)
        print("\nTop 5 Themes:\nTheme 1: 0.0\nTheme 2: 0.0\nTheme 3: 0.0\nTheme 4: 0.0\nTheme 5: 0.0")
        Top_Words_Analysis.print_top_words(sorted_top_words_dict)
        print("\n==================================================")

        # Prompt to run another analysis
        valid_input = False
        while not valid_input:
            run_again = str(input("\nRun another analysis? [y/n]: "))
            if run_again == 'y':
                flag = True
                valid_input = True
            elif run_again == 'n':
                flag = False
                valid_input = True
            else:
                print("Invalid input. Must enter 'y' for yes or 'n' for no.")

if __name__ == "__main__":
    main()
