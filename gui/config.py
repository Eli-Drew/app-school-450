from nltk.util import tokenwrap
from sklearn.decomposition import NMF

topic_list = ["0"]

thematic_model = NMF(n_components=1, init='random', random_state=0)

featureNames = []

input_method = 'c'

top_five_topics = []

top_five_sentiments = []


def init():
    global topic_list
    topic_list = []
