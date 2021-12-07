from analysis.Analysis import Analysis
import nltk # TODO this can be removed when nltk.download('stopwords') is saved and loaded in
from nltk.corpus import stopwords
from textblob import Word, TextBlob
from sklearn.decomposition import NMF
from sklearn.feature_extraction.text import TfidfVectorizer

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
    # TODO make sure this method truncates responses to max_len,
    #                            removes end of sentence punctuations
    #                            lematizes
    #                            returns a 2D array of strings so Top_Words_Analysis.find_top_words() can use it
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
