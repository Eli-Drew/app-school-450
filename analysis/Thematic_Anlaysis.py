# TODO organize imports in separate files
from analysis.Analysis import Analysis
from nltk.corpus import stopwords
from textblob import Word, TextBlob
from sklearn.decomposition import NMF
from sklearn.feature_extraction.text import TfidfVectorizer
import nltk

class Thematic_Analysis(Analysis):

    nltk.download('stopwords') # TODO this may need to be saved somewhere too so we can load it in locally without having to download it
    vectorizer = TfidfVectorizer(max_features=1000)
    nmf_model = NMF(n_components=5, init='random', random_state=0)

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
    @classmethod
    def pre_process(cls, responses, max_len):
        
        clean_responses = []
        responses = [resp.lower().replace('\n', ' ') for resp in responses if len(resp) > max_len]
        stop_words = set(stopwords.words('english'))

        for resp in responses:
            tokens = ' '.join(TextBlob(resp).noun_phrases).split()
            clean_resp = []
            for word in tokens:
                word = Word(word).lemmatize()
                if word not in stop_words and len(word) > 4:
                    clean_resp.append(word)
                if len(clean_resp) != 0:
                    clean_responses.append(' '.join(clean_resp))

        vectors = cls.vectorizer.fit_transform(clean_responses)
        return vectors


    """
    ===================================================================
    Description:
        To be written
    Paramaters:
        vectors: 
    Returns:
        To be written
    ===================================================================
    """
    @classmethod
    def analyze(cls, vectors):
        cls.nmf_model.fit_transform(vectors)
        feature_names = cls.vectorizer.get_feature_names()
        return feature_names
        

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
    def format_results(cls, feature_names):
        # TODO Add in formatting Brent implemented to get a list of the five themes
        themes = []
        # TODO would like to make this more readable if kept
        for idx, topic in enumerate(cls.nmf_model.components_):
            themes.append((idx+1), [(feature_names[i], topic[i].round(2)) for i in topic.argsort()[:-50 - 1:-1]])
        return themes


# Old comments for thematic analysis functions
"""
===================================================================
Description: getData returns the data located at the fileName param
Param(s): fileName path for data.
Returns: dataset as list of one element (entire dataset as one elem)
===================================================================
===============================================================
Description: getCleanData returns its data param after cleaning
Param(s): data list (from getData())
Returns: A list of text, for example:

['great', 'great presentation', 'great presentation clear',...]
===============================================================
=================================================================================
Description: getTopics prints the the repective topics and their components
Param(s): model components, feature names, and n = the number of words per topic.
Returns: Nothing, just prints topics (at least for now).
=================================================================================
"""