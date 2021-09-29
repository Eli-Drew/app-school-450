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

    numberOfResponses = 0
    listOfSentimentScores = []

    def __init__(self, record, recordNumber):
        """Contructor takes in the actual record response."""
        Response.numberOfResponses += 1
        self.record = record
        self.recordNumber = recordNumber
        self.sequences = [[]]
        self.sentimentScore
        self.themes = []

    def getRecord(self):
        return self.record

    def setRecord(self, record):
        self.record = record

    def getSequence(self):
        return self.sequences

    def setSequence(self, sequences):
        self.sequences = sequences
    
    def getSentimentScore(self):
        return self.sentimentScore

    def setSentimentScore(self, score):
        self.sentimentScore = score
        Response.listOfSentimentScores.append(score)

    def __len__(self):
        return len(self.record)

    def __str__(self):
        """String representation of a Response object."""
        return "Record Number: " + str(self.recordNumber) + "\n" + self.record

    def __eq__(self, other):
        return self.record == other.record

    def __neq__(self, other):
        return self.record != other.record

    def __add__(self, other):
        """This will combine two records and aggregate the result information."""
        # TODO
        # when result info is decided, need to implement aggregation of results here.

        # this is aggregating the sequences together.
        newSequence = self.sequences + other.sequence
        newResponse = Response(None, None)
        newResponse.setSequence(newSequence)
        return newResponse