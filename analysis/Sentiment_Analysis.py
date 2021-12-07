from analysis.Analysis import Analysis
import os
import tensorflow.keras
# TODO this can be removed once the word_index is saved and loaded in
from tensorflow.keras.datasets import imdb
from tensorflow.keras.preprocessing.text import text_to_word_sequence
from tensorflow.keras.preprocessing import sequence


class Sentiment_Analysis(Analysis):

    model_path = os.path.join(os.path.dirname(__file__), 'sentiment_model.tf')
    # model_path = "C:\\Users\\Drew\\FRAT-models\\analysis\\sentiment_model.tf"
    model = tensorflow.keras.models.load_model(model_path)
    # TODO this may need to be saved and loaded in too
    word_index = imdb.get_word_index()

    """
    ===================================================================
    Description:
        Tokenizes an array of strings into sequences of integers
        and does any padding or truncating if necessary
    Paramaters:
        responses: an array of strings to be pre-processed
        max_len: the max word length a response can be
    Returns:
        the padded sequences as a 2D array of integers
    ===================================================================
    """
    @classmethod
    def pre_process(cls, responses, max_len):

        token_sequences = []
        for response in responses:
            word_seq = text_to_word_sequence(response)
            # TODO fix the error being thrown when analyzing a response with the oov character
            token_seq = [cls.word_index[word]
                         if word in cls.word_index else 0 for word in word_seq]
            token_sequences.append(token_seq)

        return sequence.pad_sequences(token_sequences, max_len)

    """
    ===================================================================
    Description:
        Predicts the sentiments of the sequences based off of the model
    Paramaters:
        padded_sequences: the padded sequences of integers returned by pre_process()
    Returns:
        the predicted sentiments as 2D array of floating points
    ===================================================================
    """
    @classmethod
    def analyze(cls, padded_sequences):
        sentiments = cls.model.predict(padded_sequences)
        return sentiments

    """
    ===================================================================
    Description:
        Iterate through the sentiments returned by analyze() to get the 
        overall sentiment as well as the percentages of negative, neural,
        and positive sentiments
    Paramaters:
        sentiments: the predicted sentiments as a 2D array of floating points
    Returns:
        dictionary containing the overall sentiment and percentages of
        negative, neural, and positive sentiments throughout the responses
    ===================================================================
    """
    @classmethod
    def format_results(cls, sentiments):

        sentiment_analysis_results = {}

        sum = 0
        negative_range = [0.00, 0.44]
        neutral_range = [0.45, 0.55]
        positive_range = [0.56, 1.00]
        negatives_count = neutrals_count = positives_count = 0

        # Iterate through to get sentiment sum and the counts of each sentiment type
        for sentiment in sentiments:
            sentiment_value = round(sentiment[0].item(), 2)
            sum += sentiment_value
            # Increment correct count
            if (negative_range[0] <= sentiment_value <= negative_range[1]):
                negatives_count += 1
            elif (neutral_range[0] <= sentiment_value <= neutral_range[1]):
                neutrals_count += 1
            elif (positive_range[0] <= sentiment_value <= positive_range[1]):
                positives_count += 1

        sentiment_analysis_results["overall"] = round(sum / len(sentiments), 2)
        sentiment_analysis_results["percent_negative"] = round((negatives_count / len(sentiments)) * 100, 2)
        sentiment_analysis_results["percent_neutral"] = round((neutrals_count / len(sentiments)) * 100, 2)
        sentiment_analysis_results["percent_positive"] = round((positives_count / len(sentiments)) * 100, 2)

        return sentiment_analysis_results

    """
    ===================================================================
    Description:
        Print each entry from the dictionary returned by format_results()
    Paramaters:
        sentiment_analysis_results: dictionary containing the overall
            sentiment and percentages of negative, neural, and positive
            sentiments throughout the responses
    Returns:
        N/A
    ===================================================================
    """
    @classmethod
    def print_sentiment_results(cls, sentiment_analysis_results):
        print("\nOverall Sentiment: {}".format(
            sentiment_analysis_results["overall"]))
        print("Percent Negative: {}%".format(
            sentiment_analysis_results["percent_negative"]))
        print("Percent Neutral: {}%".format(
            sentiment_analysis_results["percent_neutral"]))
        print("Percent Positive: {}%".format(
            sentiment_analysis_results["percent_positive"]))
