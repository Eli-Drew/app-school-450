from user_input.input import get_input
from analysis.Sentiment_Analysis import Sentiment_Analysis
from analysis.Thematic_Anlaysis import Thematic_Analysis
from analysis.Top_Words_Analysis import Top_Words_Analysis

MAXLEN = 250

def main():

    # Get user's responses
    responses = get_input(MAXLEN)
    # TODO figure out why characters aren't being removed from beginning of data_sets/responses.csv
    # print(responses) # notice the first few characters after inputting responses.csv

    # Sentiment Analysis
    padded_sequences = Sentiment_Analysis.pre_process(responses, MAXLEN)
    sentiments = Sentiment_Analysis.analyze(padded_sequences)
    sentiment_analysis_results = Sentiment_Analysis.format_results(sentiments)
    
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
    Sentiment_Analysis.print_sentiment_results(sentiment_analysis_results)
    # Thematic_Analysis.print_themes(themes)
    print("\nTop 5 Themes:\nTheme 1: 0.0\nTheme 2: 0.0\nTheme 3: 0.0\nTheme 4: 0.0\nTheme 5: 0.0")
    Top_Words_Analysis.print_top_words(sorted_top_words_dict)
    print("\n====================================================")

    # TODO add in option and functionality to run another analysis


if __name__ == "__main__":
    main()