# TODO organize imports in separate files
from analysis.Analysis import Analysis
from keras.datasets import imdb # TODO this can be removed once the word_index is saved and loaded in
from keras.preprocessing.text import text_to_word_sequence
from keras.preprocessing import sequence

class Sentiment_Analysis(Analysis):

    model = None # TODO load the saved sentiment model
    word_index = imdb.get_word_index() # TODO this may need to be saved and loaded in too

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
            token_seq = [cls.word_index[word] if word in cls.word_index else -1 for word in word_seq]
            token_sequences.append(token_seq)

        return sequence.pad_sequences(token_sequences, max_len)


    """
    ===================================================================
    Description:
        Predicts the sentiments of the sequences based off of the model
    Paramaters:
        padded_sequences: the padded sequences of integers returned by pre_process()
    Returns:
        the predicted sentiments as an array of floating points
    ===================================================================
    """
    @classmethod
    def analyze(cls, padded_sequences):
        sentiments = cls.model.predict(padded_sequences)
        return sentiments


    """
    ===================================================================
    Description:
        Format the sentiments returned from analyze() to prepare for GUI output
    Paramaters:
        sentiments: 
    Returns:
        To be written
    ===================================================================
    """
    @classmethod
    def format_results(cls, sentiments):
        pass
