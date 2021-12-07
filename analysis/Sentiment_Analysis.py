from analysis.Analysis import Analysis
# from Analysis import Analysis
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2' # suppresses tf info and warning logs
from tensorflow.keras.models import load_model
import tensorflow.python.keras.engine.base_layer_v1 # needed for compiling deliverable
from tensorflow.keras.datasets.imdb import get_word_index
from tensorflow.keras.preprocessing.text import text_to_word_sequence
from tensorflow.keras.preprocessing.sequence import pad_sequences

class Sentiment_Analysis(Analysis):
    
    # model_path = os.path.join(os.path.dirname(__file__), 'sentiment_model.tf')
    model_path = os.path.join(os.path.expanduser('~'), 'FRAT-models\\analysis\\sentiment_model.tf')
    # if os.path.exists(model_path):
    #     print("\n\n\n{} exists\n\n\n".format(model_path))
    # else:
    #     print("\n\n\n{} does not exist\n\n\n".format(model_path))
    model = load_model(model_path, compile=False)
    word_index = get_word_index()

    negative_range = [0.00, 0.44]
    neutral_range = [0.45, 0.55]
    positive_range = [0.56, 1.00]

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
            token_seq = [cls.word_index[word] if word in cls.word_index else 0 for word in word_seq]
            token_sequences.append(token_seq)

        return pad_sequences(token_sequences, max_len)


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
        dictionary containing the average sentiment and percentages of
        negative, neural, and positive sentiments throughout the responses
    ===================================================================
    """
    @classmethod
    def format_results(cls, sentiments):

        sentiment_analysis_results = {}
        average_sentiment = 0
        average_sentiment_type = ""
        negatives_count = neutrals_count = positives_count = 0

        sum = 0
        # Iterate through to get the counts of each sentiment type
        for sentiment in sentiments:
            sentiment = round(sentiment[0].item(), 2)
            sum += sentiment
            # Increment correct count
            if (cls.negative_range[0] <= sentiment <= cls.negative_range[1]):
                negatives_count += 1
            elif (cls.neutral_range[0] <= sentiment <= cls.neutral_range[1]):
                neutrals_count += 1
            elif (cls.positive_range[0] <= sentiment <= cls.positive_range[1]):
                positives_count += 1

        sentiment_analysis_results["percent_negative"] = round((negatives_count / len(sentiments)) * 100)
        sentiment_analysis_results["percent_neutral"] = round((neutrals_count / len(sentiments)) * 100)
        sentiment_analysis_results["percent_positive"] = round((positives_count / len(sentiments)) * 100)

        average_sentiment = round(sum / len(sentiments), 2)
        # Assign correct average sentiment type
        if (cls.negative_range[0] <= average_sentiment <= cls.negative_range[1]):
            average_sentiment_type = "negative"
        elif (cls.neutral_range[0] <= average_sentiment <= cls.neutral_range[1]):
            average_sentiment_type = "neutral"
        elif (cls.positive_range[0] <= average_sentiment <= cls.positive_range[1]):
            average_sentiment_type = "positive"

        sentiment_analysis_results["average"] = [average_sentiment, average_sentiment_type]

        # Ensure total of percents is equal to 100
        total_percent = sentiment_analysis_results["percent_negative"] \
                      + sentiment_analysis_results["percent_neutral"] \
                      + sentiment_analysis_results["percent_positive"]
        if total_percent != 100:
            difference = 100 - total_percent
            target_percent = "percent_" + average_sentiment_type
            sentiment_analysis_results[target_percent] += difference

        return sentiment_analysis_results


    """
    ===================================================================
    Description:
        Find up to 3 responses showcasing the average sentiment
    Paramaters:
        responses: an array of strings
        sentiments: the predicted sentiments as a 2D array of floating points
            returned by analyze()
        average_sentiment_type: the type of the average of sentiments
            (negative, neutral, positive)
    Returns:
        a list of 3 or less featured responses
    ===================================================================
    """
    @classmethod
    def get_featured_responses(cls, responses, sentiments, average_sentiment_type):
        
        # Determine the target_range and target_value
        target_range = []
        target_value = None
        if average_sentiment_type == "negative":
            target_range = cls.negative_range
            target_value = 0.0
        elif average_sentiment_type == "neutral":
            target_range = cls.neutral_range
        else:
            target_range = cls.positive_range
            target_value = 1.0

        # Get all sentiments/responses that are in the target_range
        targeted_sentiments_dict = {}
        response_num = 0
        for sentiment in sentiments:
            sentiment = round(sentiment[0].item(), 2)
            if target_range[0] <= sentiment <= target_range[1]:
                targeted_sentiments_dict[sentiment] = responses[response_num]
            response_num += 1

        return Sentiment_Analysis.sort_feautred_reponses(targeted_sentiments_dict, target_value)


    """
    ===================================================================
    Description:
        Sort and get up to 3 sentiment/response entries from
            a dict of sentiment keys and response values
    Paramaters:
        targeted_sentiments: the dict of sentiments and corresponding responses
        target_value: the targeted sentiment value to base sorting off of
    Returns:
        a list of 3 or less featured responses
    ===================================================================
    """
    @classmethod
    def sort_feautred_reponses(cls, targeted_sentiments_dict, target_value):
        
        featured_responses = []
        sorted_responses_dict = {}

        # Sort from least to greatest for negative responses
        if target_value == 0.0:

            min_sentiment_response = ""
            min_sentiment = 1.0
                
            for i in range(len(targeted_sentiments_dict)):

                for sentiment, response in targeted_sentiments_dict.items():
                    if response in sorted_responses_dict.values():
                        continue
                    elif sentiment < min_sentiment:
                        min_sentiment = sentiment
                        min_sentiment_response = response

                sorted_responses_dict[min_sentiment] = min_sentiment_response
                min_sentiment_response = ""
                min_sentiment = 1.0

        # Sort from greatest to least for positive responses
        elif target_value == 1.0:

            max_sentiment_response = ""
            max_sentiment = 0.0
                
            for i in range(len(targeted_sentiments_dict)):

                for sentiment, response in targeted_sentiments_dict.items():
                    if response in sorted_responses_dict.values():
                        continue
                    elif sentiment > max_sentiment:
                        max_sentiment = sentiment
                        max_sentiment_response = response

                sorted_responses_dict[max_sentiment] = max_sentiment_response
                max_sentiment_response = ""
                max_sentiment = 0.0

        # Append to featured_responses the response entries from correct dict
        if target_value != None:
            for response in sorted_responses_dict.values():
                featured_responses.append(response)
        else:
            for response in targeted_sentiments_dict.values():
                featured_responses.append(response)

        num_responses = 3 if (len(featured_responses) >= 3) else len(featured_responses)
        return featured_responses[0:num_responses]


    """
    ===================================================================
    Description:
        Print each entry from the dictionary returned by format_results()
        as well as the featured responses
    Paramaters:
        sentiment_analysis_results: dictionary containing the average
            sentiment and percentages of negative, neural, and positive
            sentiments throughout the responses
        featured_responses: a list of 3 or less string responses that
            showcase the average sentiment
    Returns:
        N/A
    ===================================================================
    """
    @classmethod
    def print_sentiment_results(cls, sentiment_analysis_results, featured_responses):

        print("\nAverage Sentiment: {} | {}".format(
            sentiment_analysis_results["average"][0], sentiment_analysis_results["average"][1].capitalize()))

        print("Percent Negative: {}%".format(sentiment_analysis_results["percent_negative"]))
        print("Percent Neutral: {}%".format(sentiment_analysis_results["percent_neutral"]))
        print("Percent Positive: {}%".format(sentiment_analysis_results["percent_positive"]))

        print("\nFeatured {} Responses: ".format(sentiment_analysis_results["average"][1].capitalize()))
        for response in featured_responses:
            print("\t\"{}\"".format(response))