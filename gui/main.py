from logging import root
import kivy
from kivy.clock import Clock
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.togglebutton import ToggleButton
from kivy.app import App
from kivy.graphics import Color
from kivy.core.window import Window
from joblib import dump, load
from nltk.corpus import stopwords
from nltk.probability import FreqDist
from textblob import Word
from textblob import TextBlob
from sklearn.feature_extraction.text import TfidfVectorizer
from subprocess import Popen
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.lang import Builder
# from analysis.Sentiment_Analysis import Sentiment_Analysis
# from user_input.input import *
from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg
import matplotlib.pyplot as plt
from sklearn.decomposition import NMF
from wordcloud import WordCloud
from wordcloud import STOPWORDS

import os
import nltk
# import AnalysisReportApp
import config
nltk.download('stopwords')
kivy.require('2.0.0')

MAXLEN = 250


class FratForLife(Screen):
    #csv_txt_input = ObjectProperty(None)

    def main(self):
        # C:/Users/Brentlee/Downloads/demoData.csv <- Example file location input
        # get user input and clean the file data
        # if input_method is c, read from csv, otherwise; read from text input.
        csv_file_path = self.ids.csv_txt_input.text
        if(config.input_method == 'c'):
            data = getData(csv_file_path)
            cleanData = getCleanData(data)
        else:
            data = ['string']
            data[0] = str(self.ids.typed_txt_input.text)
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
        # thematic_model = load('thematic_model')
        # thematic_model.fit_transform(vectorData)

        config.thematic_model = NMF(
            n_components=1, init='random', random_state=0)
        config.thematic_model.fit_transform(vectorData)

        # get the feature names and print the topics from the model
        config.featureNames = vectorizer.get_feature_names()
        getTopics(config.thematic_model.components_, config.featureNames)

        # AnalysisReportApp.AnalysisReportApp.topics(topics)

        # topic_one = str(topics[0])
        # self.ids.topic_text.text = topic_one
        # open_close(self)

    def toggle_disable_inputs(self):
        if(self.ids.csv_txt_input.disabled is True):
            self.ids.csv_txt_input.disabled = False
            self.ids.typed_txt_input.disabled = True
            config.input_method = 'c'
        else:
            self.ids.csv_txt_input.disabled = True
            self.ids.typed_txt_input.disabled = False
            config.input_method = 'r'

    def dismiss_popup(self):
        self._popup.dismiss()

    def show_load(self):
        content = LoadDialog(load=self.load, cancel=self.dismiss_popup)
        self._popup = Popup(title="Load file", content=content,
                            size_hint=(0.9, 0.9))
        self._popup.open()

    # def show_save(self):
    #     content = SaveDialog(save=self.save, cancel=self.dismiss_popup)
    #     self._popup = Popup(title="Save file", content=content,
    #                         size_hint=(0.9, 0.9))
    #     self._popup.open()

    def load(self, path, filename):

        # with open(os.path.join(path, filename[0])) as stream:
        #     self.text_input.text = stream.read()

        # self.dismiss_popup()
        self.ids.csv_txt_input.text = os.path.join(path, filename[0])
        #true_file_name = os.path.join(path, filename[0])
        self.dismiss_popup()

    """
    ===================================================================
    Description: topic plots the thematic topic data on the result page
    Param(s): self
    Returns: nothing
    ===================================================================
    """

    def topic(self):
        # self.manager.get_screen("second").ids.topic_one.text = ', '.join(
        #     config.topic_list[0])
        # self.manager.get_screen("second").ids.topic_two.text = ', '.join(
        #     config.topic_list[1])

        for idx, topic in enumerate(config.thematic_model.components_):
            if idx == 0:
                topic_x = [(config.featureNames[i], topic[i].round(2))
                           for i in topic.argsort()[:-1000 - 1:-1]]
                topic_x = {i[0]: i[1] for i in topic_x}

        wordcloud = WordCloud(width=3000, height=3000, stopwords=STOPWORDS,
                              background_color="white", min_font_size=30)
        wordcloud = wordcloud.generate_from_frequencies(topic_x)

        # build figure (plot)
        fig = plt.figure(figsize=(50, 50))
        plot_one = fig.add_subplot(1, 2, 1)
        plot_two = fig.add_subplot(1, 2, 2)
        plot_one.axis("off", figure=fig)
        plot_one.imshow(wordcloud, interpolation="bilinear", figure=fig)
        plot_two.bar(config.top_five_topics, config.top_five_sentiments)
        fig.get_tight_layout()

        # print(config.top_five_topics[0])
        # print("\n")
        # print(config.top_five_sentiments[0])

        # put figure on results page at id topic_one
        self.manager.get_screen("second").ids.topic_one.clear_widgets()
        self.manager.get_screen("second").ids.topic_one.add_widget(
            FigureCanvasKivyAgg(fig))

        # clear figure
        fig = plt.figure()


class AnalysisReportApp(Screen):
    def clearTopics(self):
        config.topic_list.clear()


class WindowManager(ScreenManager):
    pass


class LoadDialog(FloatLayout):
    load = ObjectProperty(None)
    cancel = ObjectProperty(None)


'''
def __init__(self, **kwargs):
    super(FratForLife, self).__init__(**kwargs)
    with self.canvas.before:
        Color(0, 1, 0)
'''

"""
===================================================================
Description: getData returns the data located at the fileName param
Param(s): fileName path for data.
Returns: dataset as list of one element (entire dataset as one elem)
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
Param(s): data list (from getData())
Returns: A list of text, for example:

['great', 'great presentation', 'great presentation clear',...]

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
            if w not in stop_words and len(w) > 3:
                cleanD.append(w)
            if len(cleanD) != 0:
                cleanData.append(' '.join(cleanD))
    return cleanData


"""
=================================================================================
Description: getTopics prints the the repective topics and their components
Param(s): model components, feature names, and n = the number of words per topic.
Returns: Nothing, appends to config topic list and top five topics.
=================================================================================
"""


def getTopics(components, feature_names, n=50):
    counter = 0
    config.init()
    for idx, topic in enumerate(components):
        # config.topic_list.append([(feature_names[i]) for i in topic.argsort()[:-n - 1:-1]])
        config.topic_list.append(
            [(feature_names[i], topic[i].round(2)) for i in topic.argsort()[:-n - 1:-1]])
        if(counter < 5):
            config.top_five_topics.append(
                [(feature_names[i]) for i in topic.argsort()[:-n - 1:-1]])
            config.top_five_sentiments.append(
                [(topic[i].round(2)) for i in topic.argsort()[:-n - 1:-1]])
            counter += 1
    counter = 0
    # if(config.top_five_topics[] > 5 and config.top_five_sentiments > 5):
    top_five_topics = str(config.top_five_topics[0]).replace(
        '"', '').replace('\'', '').replace(' ', '').split("[")
    top_five_sentiments = str(config.top_five_sentiments[0]).replace(
        '"', '').replace('\'', '').replace(' ', '').split("[")
    top_five_topics = str(top_five_topics[1].split("]").pop(0)).split(',')
    top_five_sentiments = str(
        top_five_sentiments[1].split("]").pop(0)).split(',')
    temp_sentiment_list = []
    temp_topic_list = []
    # if(len(top_five_topics) > 5 and len(top_five_sentiments) > 5):
    for i in range(5):
        temp_topic_list.append(top_five_topics[i])
        temp_sentiment_list.append(top_five_sentiments[i])
    config.top_five_sentiments = temp_sentiment_list
    config.top_five_topics = temp_topic_list


class FratApp(App):
    def build(self):
        Window.size = (1920, 1080)


if __name__ == '__main__':
    FratApp().run()
