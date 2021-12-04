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
import matplotlib.pyplot as plt
from kivy_garden.graph import Graph

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
        data = getData(csv_file_path)
        cleanData = getCleanData(data)

        # Sentiment Analysis
        # TODO 
        # endcoding = bom_validation(csv_file_path)
        # file = csv_read(csv_file_path, endcoding)
        # padded_sequences = Sentiment_Analysis.pre_process(responses, MAXLEN)
        # sentiments = Sentiment_Analysis.analyze(padded_sequences)
        # sentiment_analysis_results = Sentiment_Analysis.format_results(
        #     sentiments)

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
        # thematic_model = load('thematic_model') # looks like only a file name is given but no path.
        # thematic_model.fit_transform(vectorData)

        config.thematic_model = NMF(
            n_components=1, init='random', random_state=0)
        config.thematic_model.fit_transform(vectorData)

        # get the feature names and print the topics from the model
        # featureNames = vectorizer.get_feature_names()
        # getTopics(thematic_model.components_, featureNames)

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

    def topic(self):
        self.manager.get_screen("second").ids.topic_one.text = ', '.join(
            config.topic_list[0])
        # self.manager.get_screen("second").ids.topic_two.text = ', '.join(
        #     config.topic_list[1])
        plt.plot([1,23,2,4])
        plt.ylabel('some number')
        self.manager.get_screen("second").ids.topic_two.add_widget(FigureCanvasKivyAgg(plt.gcf()))

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
Returns: Nothing, just prints topics (at least for now).
=================================================================================
"""


def getTopics(components, feature_names, n=50):
    config.init()
    for idx, topic in enumerate(components):
        # config.topic_list.append([(feature_names[i]) for i in topic.argsort()[:-n - 1:-1]])
        config.topic_list.append(
            [(feature_names[i], topic[i].round(2)) for i in topic.argsort()[:-n - 1:-1]])


class FratApp(App):
    def build(self):
        Window.size = (1920, 1080)


if __name__ == '__main__':
    FratApp().run()
