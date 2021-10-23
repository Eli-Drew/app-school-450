"""
=================================================
Author: Brent Anderson
Date created:   10/16/2021
Description: Thematic analysis model 
=================================================
"""

from nltk.corpus import stopwords
from textblob import Word
from textblob import TextBlob
from sklearn.decomposition import NMF
from sklearn.feature_extraction.text import TfidfVectorizer
import nltk
nltk.download('stopwords')


"""
============================================================================
Description: getTopics prints the the repective topics and their components
============================================================================
"""


def getTopics(components, feature_names, n=50):
    for idx, topic in enumerate(components):
        print("\nTopic %d: " % (
            idx+1), [(feature_names[i], topic[i].round(2)) for i in topic.argsort()[:-n - 1:-1]])


"""
===================================================================
Description: getData returns the data located at the fileName param
===================================================================
"""


def getData(fileName):
    # open file
    data = open(fileName, "r", encoding='UTF8')
    # split the file data
    splitData = data.read().replace('"', ' ').replace('’', '\'').split('\n\n')
    # convert all text to lowercase and replace all newlines with a space
    realData = [x.lower().replace('\n', ' ')
                for x in splitData if len(x) > 500]
    return realData


"""
===============================================================
Description: getCleanData returns its data param after cleaning
===============================================================
"""


def getCleanData(data):
    cleanData = []
    # stop words are words that lack context meaning but occur frequently in natural language
    stop_words = set(stopwords.words('english'))
    for d in data:
        tokens = ' '.join(TextBlob(d).noun_phrases).split()
        cleanD = []
        for w in tokens:
            # convert words to their base form, like plural to singular
            w = Word(w).lemmatize()
            if w not in stop_words and len(w) > 4:
                cleanD.append(w)
            if len(cleanD) != 0:
                cleanData.append(' '.join(cleanD))
    return cleanData


def main():
    isValid = True
    while (isValid):

        print("Enter q to quit, or the path of a file to perform thematic analysis on:")
        userInput = str(input())

        if userInput == "q" or userInput == "Q":
            isValid = False
            break

        else:
            print("Loading, please wait...")

            # C:/Users/Brentlee/Downloads/demoData.csv <- Example file location input
            # get user input and clean the file data
            data = getData(userInput)
            cleanData = getCleanData(data)

            # tokenize and vectorize the data
            # TFIDF = (occurences of word in document / total number of words in document) * (log[total # of documents in corpus / number of documents containing word])
            vectorizer = TfidfVectorizer(max_features=1000)
            vectorData = vectorizer.fit_transform(cleanData)

            # Non-Negative Matrix Factorization model...
            '''
            Given a matrix M x N, where M = Total number of documents and N = total number of words,
            NMF is the matrix decompostition that generates the Features with M rows and K columns,
            where K = total number of topics and the Components matrix is the matrix of K by N.
            The Product of the Features and Components matricies results in the approximation of the TF-IDF.
            '''

            nmf_model = NMF(n_components=5, init='random', random_state=0)
            nmf_model.fit_transform(vectorData)

            # get the feature names and print the topics from the model
            featureNames = vectorizer.get_feature_names()
            getTopics(nmf_model.components_, featureNames)


if __name__ == "__main__":
    main()
