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
from textblob import Word, TextBlob
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
from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg
import matplotlib.pyplot as plt
from sklearn.decomposition import NMF
from kivy.factory import Factory
from analysis.Sentiment_Analysis import Sentiment_Analysis
import user_input.input
from analysis.Top_Words_Analysis import Top_Words_Analysis
from analysis.Thematic_Anlaysis import Thematic_Analysis

import os
import nltk
from gui import config


nltk.download('stopwords')
kivy.require('2.0.0')

MAXLEN = 250

class FratForLife(Screen):
    #csv_txt_input = ObjectProperty(None)

    def main(self):
        # C:/Users/Brentlee/Downloads/demoData.csv <- Example file location input
        # get user input and clean the file data
        # if input_method is c, read from csv; otherwise, read from text input.
        csv_file_path = self.ids.csv_txt_input.text
        if(config.input_method == 'c'):
            responses = user_input.input.csv_option(csv_file_path, MAXLEN)
            # TODO get validation in gui if path exists or not
                # will have to do this just for manually entered path
                # because browsed file is obviously there
        else:
            response = []
            response.append(str(self.ids.typed_txt_input.text))
            responses = user_input.input.response_option(response, MAXLEN)

        # Sentiment Analysis
        padded_sequences = Sentiment_Analysis.pre_process(responses, MAXLEN)
        sentiments = Sentiment_Analysis.analyze(padded_sequences)
        sentiment_analysis_results = Sentiment_Analysis.format_results(sentiments)
        featured_responses = Sentiment_Analysis.get_featured_responses(
            responses, sentiments, sentiment_analysis_results["average"][1])
        average_sentiment = sentiment_analysis_results.pop("average")
        
        # Thematic Analysis
        clean_responses = Thematic_Analysis.pre_process(responses, MAXLEN)
        Thematic_Analysis.analyze(clean_responses)
        Thematic_Analysis.format_results()
        
        # Top Words Analysis
        word_dict = Top_Words_Analysis.pre_process(responses, MAXLEN)
        top_words_dict = Top_Words_Analysis.analyze(word_dict)
        sorted_top_words_dict = Top_Words_Analysis.format_results(top_words_dict)

        """Analysis Summary Chart"""
        # TODO
        thematic_themes = config.topic_list[0]
        negative_sentiment = sentiment_analysis_results['percent_negative']
        postive_sentiment = sentiment_analysis_results['percent_positive']
        neutral_sentiment = sentiment_analysis_results['percent_neutral']
        self.manager.get_screen("second").ids.average_sentiment.text = "{} | {}".format(str(average_sentiment[0]),average_sentiment[1])
        self.manager.get_screen("second").ids.featured_response_title.text ="Featured {} Responses".format(average_sentiment[1])
        self.manager.get_screen("second").ids.featured_response_1.text = "\"{}\"".format(featured_responses[0])
        self.manager.get_screen("second").ids.featured_response_2.text = "\"{}\"".format(featured_responses[1])
        self.manager.get_screen("second").ids.featured_response_3.text = "\"{}\"".format(featured_responses[2])
        top_topics_dict = {}

        topic_one = thematic_themes[0][0].capitalize()
        topic_two = thematic_themes[1][0].capitalize()
        topic_three = thematic_themes[2][0].capitalize()
        topic_four = thematic_themes[3][0].capitalize()
        topic_five = thematic_themes[4][0].capitalize()
        top_topics_dict[topic_one] = thematic_themes[0][1]
        top_topics_dict[topic_two] = thematic_themes[1][1]
        top_topics_dict[topic_three] = thematic_themes[2][1]
        top_topics_dict[topic_four] = thematic_themes[3][1]
        top_topics_dict[topic_five] = thematic_themes[4][1]
        self.manager.get_screen("second").ids.theme_1.text = "{} | {}".format(topic_one, str(top_topics_dict[topic_one]))
        self.manager.get_screen("second").ids.theme_2.text = "{} | {}".format(topic_two, str(top_topics_dict[topic_two]))
        self.manager.get_screen("second").ids.theme_3.text = "{} | {}".format(topic_three, str(top_topics_dict[topic_three]))
        self.manager.get_screen("second").ids.theme_4.text = "{} | {}".format(topic_four, str(top_topics_dict[topic_four]))
        self.manager.get_screen("second").ids.theme_5.text = "{} | {}".format(topic_five, str(top_topics_dict[topic_five]))

        """Sentiment Analysis Pie Chart"""
        # pie_chart_labels = 'Negative', 'Positive', 'Neutral'
        pie_chart_labels = []
        pie_chart_percentages = []
        for key in sentiment_analysis_results:
            if sentiment_analysis_results[key] == 0:
                continue
            else:
                pie_chart_percentages.append(sentiment_analysis_results[key] / 100)
                pie_chart_labels.append(key.split('_')[1].capitalize())

        pie_chart_figure, pie_chart_ax = plt.subplots()
        pie_chart_ax.pie(pie_chart_percentages, labels=pie_chart_labels, autopct='%1.0f%%',
                                startangle=90, wedgeprops={'linewidth': 3.0, 'edgecolor': 'white'},textprops={'color': 'white'})
        # pie_chart_ax.axis('equal')
        pie_chart_figure.set_facecolor('none')
        self.manager.get_screen("second").ids.sentiment_chart.add_widget(FigureCanvasKivyAgg(pie_chart_figure))


        """Top Tokens Chart"""
        # top tokens bar graph. 
        # TODO make graph look better and add labels
        top_token_bar = plt.figure()
        top_token_plot = top_token_bar.add_subplot(1, 2, 2)
        # top_token_ax = top_token_bar.add_axes([0,0,1,1])
        words = []
        word_count = []
        for token_key in sorted_top_words_dict:
            words.append(token_key)
            word_count.append(sorted_top_words_dict[token_key])
        top_token_plot.bar(words, word_count)
        top_token_plot.set_facecolor('none')
        top_token_plot.set_ylabel('Number of Occurrences')
        top_token_plot.set_xlabel('Top Words')
        # plt.show()
        self.manager.get_screen("second").ids.top_token_bar_chart.add_widget(FigureCanvasKivyAgg(top_token_bar))

        """Top Topics and Their Sentiment chart"""
        # TODO
        sorted_top_topics_dict = {}
        max_sentiment_topic = ""
        max_sentiemnt = 0

        for i in range(len(top_topics_dict)):

            for topic, sentiment in top_topics_dict.items():
                if topic in sorted_top_topics_dict.keys():
                    continue
                elif sentiment > max_sentiemnt:
                    max_sentiemnt = sentiment
                    max_sentiment_topic = topic

            sorted_top_topics_dict[max_sentiment_topic] = max_sentiemnt
            max_sentiment_topic = ""
            max_sentiemnt = 0

        top_topic_bar = plt.figure()
        top_topic_plot = top_topic_bar.add_subplot(1, 2, 2)
        topic_words = []
        topic_sentiment = []
        for topic_key in top_topics_dict:
            topic_words.append(topic_key)
            topic_sentiment.append(sorted_top_topics_dict[topic_key])
        top_topic_plot.bar(topic_words, topic_sentiment)
        # top_token_bar.set_facecolor('none')
        top_topic_plot.set_ylabel('Sentiment Rating')
        top_topic_plot.set_xlabel('Top Topics')
        self.manager.get_screen("second").ids.top_topic_theme_bar.add_widget(FigureCanvasKivyAgg(top_topic_bar))

        # self.ids.topic_text.text = topic_one
        # open_close(self)

    def toggle_disable_inputs(self):
        if(self.ids.csv_txt_input.disabled is True):
            self.ids.csv_txt_input.disabled = False
            self.ids.typed_txt_input.disabled = True
            config.input_method = 'c'
            self.ids.browse_btn.disabled = False
        else:
            self.ids.csv_txt_input.disabled = True
            self.ids.typed_txt_input.disabled = False
            config.input_method = 'r'
            self.ids.browse_btn.disabled = True

    def dismiss_popup(self):
        self._popup.dismiss()

    def show_load(self):
        content = LoadDialog(load=self.load, cancel=self.dismiss_popup)
        self._popup = Popup(title="Load file", content=content,
                            size_hint=(0.9, 0.9))
        self._popup.open()

    # def show_analysis_in_process(self):
    # TODO
    # not sure how this is going to work
    #     self.analysis_animation = Factory.AnalysisPopup()
    #     self.analysis_animation.update_pop_up_text("Running Analysis")
    #     self.analysis_animation.open()

    def load(self, path, filename):

        # with open(os.path.join(path, filename[0])) as stream:
        #     self.text_input.text = stream.read()

        # self.dismiss_popup()
        self.ids.csv_txt_input.text = os.path.join(path, filename[0])
        #true_file_name = os.path.join(path, filename[0])
        self.dismiss_popup()



       

class AnalysisReportApp(Screen):
    def clearTopics(self):
        config.topic_list.clear()

    def clear_widgets(self, children=None):
        return super().clear_widgets(children=children)


class WindowManager(ScreenManager):
    pass


class AnalysisPopup(Popup):
    pop_up_text = ObjectProperty()

    def update_pop_up_text(self, p_message):
        self.pop_up_text.text = p_message


class LoadDialog(FloatLayout):
    load = ObjectProperty(None)
    cancel = ObjectProperty(None)


class FratApp(App):
    def build(self):
        Window.size = (1920, 1080)



if __name__ == '__main__':
    FratApp().run()
