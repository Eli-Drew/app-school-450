"""
===================================================================================================
Copyright 2021 Brent Anderson, Hannah Bolick, Kadidia Kantao, Henry Knehans, Drew Rinker
Permission is hereby granted, free of charge, to any person obtaining a copy of this software 
and associated documentation files (the 'Software'), to deal in the Software without restriction, 
including without limitation the rights to use, copy, modify, merge, publish, distribute, 
sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is 
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or 
substantial portions of the Software.

THE SOFTWARE IS PROVIDED 'AS IS', WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, 
INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A 
PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR 
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN 
AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION 
WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
===================================================================================================
"""
"""
=========================================================
Class SDD reference: Section 3.2.3.3, 3.2.2.3.5, 3.2.4.3.
=========================================================
"""

from analysis.Analysis import Analysis
import nltk # TODO this can be removed when nltk.download('stopwords') is saved and loaded in
from nltk.corpus import stopwords
from textblob import Word, TextBlob
from sklearn.decomposition import NMF
from sklearn.feature_extraction.text import TfidfVectorizer
from wordcloud import WordCloud
from wordcloud import STOPWORDS
from gui import config

class Thematic_Analysis(Analysis):

    nltk.download('stopwords') # TODO this may need to be saved somewhere too so we can load it in locally without having to download it
    vectorizer = TfidfVectorizer(max_features=1000)
    config.thematic_model = NMF(n_components=1, init='random', random_state=0)

    """
    ===================================================================
    Description:
        To be written
    Paramaters:
        responses: an array of strings(?) to be pre-processed
        max_len: the max word length a response can be
    Returns:
        To be written
    ===================================================================
    """
    # TODO make sure this method truncates responses to max_len,
    #                            removes end of sentence punctuations
    #                            lematizes
    #                            returns a 2D array of strings so Top_Words_Analysis.find_top_words() can use it
    @classmethod
    def pre_process(cls, responses, max_len):
        
        clean_responses = []
        # split_responses = responses.read().replace('"', ' ').replace('’', '\'').split('\n\n')
        responses = [resp.lower().replace('\n', ' ') for resp in responses if len(resp) > max_len]
        stop_words = set(stopwords.words('english'))

        for resp in responses:
            tokens = ' '.join(TextBlob(resp).noun_phrases).split()
            clean_resp = []
            for word in tokens:
                word = Word(word).lemmatize()
                if word not in stop_words:
                    clean_resp.append(word)
                if len(clean_resp) != 0:
                    clean_responses.append(' '.join(clean_resp))

        return clean_responses


    """
    ===================================================================
    Description:
        To be written
    Paramaters:
        clean_responses: 
    Returns:
        To be written
    ===================================================================
    """
    @classmethod
    def analyze(cls, clean_responses):
        vectors = cls.vectorizer.fit_transform(clean_responses)
        config.thematic_model.fit_transform(vectors)
        config.feature_names = cls.vectorizer.get_feature_names()
        

    """
    ===================================================================
    Description:
        Format the themes returned from analyze() to prepare for GUI output
    Paramaters:
        feature_names: 
    Returns:
        To be written
    ===================================================================
    """
    @classmethod
    def format_results(cls):

        '''
        Given a matrix M x N, where M = Total number of documents and N = total number of words,
        NMF is the matrix decompostition that generates the Features with M rows and K columns,
        where K = total number of topics and the Components matrix is the matrix of K by N.
        The Product of the Features and Components matricies results in the approximation of the TF-IDF.
        '''
        ## we think this is for the word cloud picture
        # for idx, topic in enumerate(config.thematic_model.components_):
        #     if idx == 0:
        #         topic_x_list = []
        #         for i in topic.argsort()[:-1000 - 1:-1]:
        #             topic_x_list.append((config.feature_names[i], topic[i].round(2)))

        #         topic_x_dict = {}
        #         for i in topic_x_list:
        #             topic_x_dict[i[0]] = i[1]

        # wordcloud = WordCloud(width=3000, height=3000, stopwords=STOPWORDS,
        #                       background_color="white", min_font_size=30)
        # wordcloud = wordcloud.generate_from_frequencies(topic_x_dict) # topic_x_dict must have string key and float value
        config.init()
        for idx, topic in enumerate(config.thematic_model.components_):
            config.topic_list.append(
                [(config.feature_names[i], topic[i].round(2)) for i in topic.argsort()[:-5 - 1:-1]])



    """
    ===================================================================
    Description:
        Prints the top themes returned by format_results()
    Paramaters:
        themes: the array of themes to be printed
    Returns:
        N/A
    ===================================================================
    """
    @classmethod
    def print_themes(cls, themes):
        print("\nTop {} Themes:".format(len(themes)))
        # TODO change this to print out the sentiment with each theme
        for theme in themes:
            print("{}: 0.0".format(theme))
