"""
=================================================
Author: Drew Rinker
Date:   09/29/21

Purpose: This is the Response object class file.
         It will define what a response is and 
         contain variables to hold result info
         related to each response.

         *There will be more information added
         to this class. I just don't know what 
         that information is yet.
=================================================
"""


class Response(object):
    """Represents a response and related result information"""

    number_of_responses = 0
    list_of_sentiment_scores = []

    def __init__(self, record):
        """Contructor takes in the actual record response."""
        Response.number_of_responses += 1
        self.record = record
        self.record_number = Response.number_of_responses
        self.sequences = [[]]
        self.sentiment_score
        self.themes = []

    def get_record(self):
        return self.record

    def set_record(self, record):
        self.record = record

    def get_sequence(self):
        return self.sequences

    def set_sequence(self, sequences):
        self.sequences = sequences

    def get_sentiment_score(self):
        return self.sentiment_score

    def set_sentiment_score(self, score):
        self.sentiment_score = score
        Response.list_of_sentiment_scores.append(score)

    def __len__(self):
        return len(self.record)

    def __str__(self):
        """String representation of a Response object."""
        return "Record Number: " + str(self.record_number) + "\n" + self.record

    def __eq__(self, other):
        return self.record == other.record

    def __neq__(self, other):
        return self.record != other.record

    def __add__(self, other):
        """This will combine two records and aggregate the result information."""
        # TODO
        # when result info is decided, need to implement aggregation of results here.

        # this is aggregating the sequences together.
        new_sequence = self.sequences + other.sequence
        new_response = Response(None, None)
        new_response.set_sequence(new_sequence)
        return new_sequence
