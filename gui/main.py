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
import os
import nltk
import AnalysisReportApp
import config
nltk.download('stopwords')
kivy.require('2.0.0')


class FratForLife(Screen):
    #csv_txt_input = ObjectProperty(None)

    def main(self):

        # ======================================================
        # TODO clean code to fit final functionality of product!
        # ======================================================

        # C:/Users/Brentlee/Downloads/demoData.csv <- Example file location input
        # get user input and clean the file data

        pass

        # AnalysisReportApp.AnalysisReportApp.topics(topics)

        # topic_one = str(topics[0])
        # self.ids.topic_text.text = topic_one
        # open_close(self)

    def toggle_disable_inputs(self):
        if(self.ids.csv_txt_input.disabled is True):
            self.ids.csv_txt_input.disabled = False
            self.ids.typed_txt_input.disabled = True
        else:
            self.ids.csv_txt_input.disabled = True
            self.ids.typed_txt_input.disabled = False

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


class AnalysisReportApp(Screen):
    def build(self):

        #topics = main.topic_list

        Window.clearcolor = (0, 14/255, 52/255, 1)

        layout = BoxLayout(orientation='vertical')

        title = Label(text='Feedack Response Analysis Report',
                      size_hint_y=None, height=64, padding=(8, 8))

        content = BoxLayout(orientation='horizontal')

        sidebar = BoxLayout(orientation='vertical',
                            size_hint_x=None, width=200)

        tpc1_btn = Button(text='topic-1')
        # =============================================
        # TODO get topics into the widgets on this side
        # =============================================
        #tpc1_btn.text = topic_1
        sidebar.add_widget(tpc1_btn)
        sidebar.add_widget(Button(text='topic-2'))
        sidebar.add_widget(Button(text='topic-3'))
        sidebar.add_widget(Button(text='topic-4'))
        sidebar.add_widget(Button(text='topic-5'))
        sidebar.add_widget(Button(text='export'))
        again_btn = Button(text='again')
        again_btn.bind(on_release=AnalysisReportApp.close_open)
        sidebar.add_widget(again_btn)

        grid = GridLayout(cols=2)

        summary = BoxLayout(orientation='vertical')
        summary.add_widget(Label(text='summary'))
        summary.add_widget(Label(text='content', size_hint_y=None, height=32))

        chart = BoxLayout(orientation='vertical')
        chart.add_widget(Label(text='chart'))
        chart.add_widget(Label(text='content', size_hint_y=None, height=32))

        topic1 = config.topic_list[0]

        topics1 = BoxLayout(orientation='vertical')
        topics1.add_widget(Label(text='topics1' + topic1))
        topics1.add_widget(Label(text='content', size_hint_y=None, height=32))

        topics2 = BoxLayout(orientation='vertical')
        topics2.add_widget(Label(text='topics2'))
        topics2.add_widget(Label(text='content', size_hint_y=None, height=32))

        grid.add_widget(summary)
        grid.add_widget(chart)
        grid.add_widget(topics1)
        grid.add_widget(topics2)

        layout.add_widget(title)

        content.add_widget(sidebar)
        content.add_widget(grid)

        layout.add_widget(content)

        return layout


class WindowManager(ScreenManager):
    pass


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
            if w not in stop_words and len(w) > 4:
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
        config.topic_list.append([(feature_names[i], topic[i].round(2))
                                  for i in topic.argsort()[:-n - 1:-1]])


def open_close(self):
    Popen(['python', 'AnalysisReportApp.py'])
    FratApp().stop()


def close_open(self):
    AnalysisReportApp().stop()
    Popen(['python', 'main.py'])


class FratApp(App):
    def build(self):
        global root
        global csv_txt_input
        root = FratForLife()
        csv_txt_input = root.ids.csv_txt_input
        Window.size = (1920, 1080)
        return Builder.load_file("Frat.kv")


class LoadDialog(FloatLayout):
    load = ObjectProperty(None)
    cancel = ObjectProperty(None)


if __name__ == '__main__':
    FratApp().run()
