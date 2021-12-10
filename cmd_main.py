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
        processed_responses, raw_responses = get_input(MAXLEN)

        # Sentiment Analysis
        padded_sequences = Sentiment_Analysis.pre_process(processed_responses)
        sentiments = Sentiment_Analysis.analyze(padded_sequences)
        sentiment_analysis_results = Sentiment_Analysis.format_results(sentiments)
        featured_responses = Sentiment_Analysis.get_featured_responses(
            raw_responses, sentiments, sentiment_analysis_results["average"][1])
        
        # Thematic Analysis
        # clean_responses = Thematic_Analysis.pre_process(processed_responses, MAXLEN)
        # feature_names = Thematic_Analysis.analyze(clean_responses)
        # themes = Thematic_Analysis.format_results(feature_names)
        
        # Top Words Analysis
        word_dict = Top_Words_Analysis.pre_process(processed_responses)
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