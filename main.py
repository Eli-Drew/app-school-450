# TODO organize imports in separate files
from user_input.input import get_input
from analysis.Sentiment_Analysis import Sentiment_Analysis
from analysis.Thematic_Anlaysis import Thematic_Analysis

MAXLEN = 250

def main():

    # Get user's responses
    responses = get_input(MAXLEN)
    # TODO figure out why characters aren't being removed from beginning of data_sets/responses.csv
    # print(responses) # uncomment this line to see what is happening after inputting responses.csv

    # Sentiment Analysis
    padded_sequences = Sentiment_Analysis.pre_process(responses, MAXLEN)
    sentiments = Sentiment_Analysis.analyze(padded_sequences) # model needs to be loaded into Sentiment_Analysis.py first
    sentiments = Sentiment_Analysis.format_results(sentiments) # does nothing now
    print(sentiments)

    # Thematic Analysis
    vectors = Thematic_Analysis.pre_process(responses, MAXLEN)
    feature_names = Thematic_Analysis.analyze(vectors)
    themes = Thematic_Analysis.format_results(feature_names)
    print(themes)

    '''
    # Set sentminets to the corresponding response_obj
    for i in range(len(sentiments)):
        input.response_objs[i].set_sentiment_score(sentiments[i][0])

    # Display the response_objs
    for response_obj in input.response_objs:
        print(response_obj)
        print()
    '''

if __name__ == "__main__":
    main()