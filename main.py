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
===============================================
Class SDD reference: Section(s) 4.0, 4.1, 4.1.1
===============================================
"""

from kivy.config import Config
Config.set('input', 'mouse', 'mouse,multitouch_on_demand')
# Do not move the above two lines. They must to come first.
import os
import kivy
from kivy.app import App
from kivy.core.window import Window
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty
from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg
import matplotlib.pyplot as plt
import user_input.input
from analysis.Sentiment_Analysis import Sentiment_Analysis
from analysis.Thematic_Anlaysis import Thematic_Analysis
from analysis.Top_Words_Analysis import Top_Words_Analysis
import gui_config

kivy.require('2.0.0')

MAXLEN = 250

class FratForLife(Screen):

    def main(self):

        if(gui_config.input_method == 'c'):
            csv_file_path = self.ids.csv_txt_input.text
            processed_responses, raw_responses = user_input.input.csv_option(csv_file_path, MAXLEN)
            csv_file_path = self.ids.csv_txt_input.text
            responses = user_input.input.csv_option(csv_file_path, MAXLEN)
            if not responses == "INVALID":
                valid_path = True
            else:

                print("That was not a valid csv path or file. File must exist and end in a \'.csv\' extension.")
                return
        else:
            response = self.ids.typed_txt_input.text
            processed_responses, raw_responses = user_input.input.response_option(response, MAXLEN)

        # Sentiment Analysis
        padded_sequences = Sentiment_Analysis.pre_process(processed_responses)
        sentiments = Sentiment_Analysis.analyze(padded_sequences)
        sentiment_analysis_results = Sentiment_Analysis.format_results(sentiments)
        featured_responses = Sentiment_Analysis.get_featured_responses(
            raw_responses, sentiments, sentiment_analysis_results["average"][1])
        
        # Thematic Analysis
        topics_dict = Thematic_Analysis.pre_process(processed_responses)
        top_topics_dict = Thematic_Analysis.analyze(topics_dict)
        sorted_top_topics_dict = Thematic_Analysis.format_results(top_topics_dict)
        
        # Top Words Analysis
        word_dict = Top_Words_Analysis.pre_process(processed_responses)
        top_words_dict = Top_Words_Analysis.analyze(word_dict)
        sorted_top_words_dict = Top_Words_Analysis.format_results(top_words_dict)

        # Populate GUI
        self.populate_summary_chart(sentiment_analysis_results, featured_responses)
        self.populate_pie_chart(sentiment_analysis_results)
        self.populate_topics_chart(sorted_top_topics_dict)
        self.populate_words_chart(sorted_top_words_dict)


    """Analysis Summary Chart"""
    def populate_summary_chart(self, sentiment_analysis_results, featured_responses):

        average_sentiment = sentiment_analysis_results.pop("average")

        # Add average sentiment results to summary chart
        self.manager.get_screen("second").ids.average_sentiment.text = "{} | {}".format(str(average_sentiment[0]), average_sentiment[1].capitalize())
        self.manager.get_screen("second").ids.featured_response_title.text = "Featured {} Responses".format(average_sentiment[1].capitalize())

        # Add featured responses to summary chart
        featured_response_ids = [featured_response_id for featured_response_id in self.manager.get_screen("second").ids.featured_response_layout.children]
        for index in range(len(featured_responses)):
            featured_response_ids[index].text = "\"{}\"".format(featured_responses[index])
    

    """Sentiment Analysis Pie Chart"""
    def populate_pie_chart(self, sentiment_analysis_results):
        
        pie_chart_labels = []
        pie_chart_percentages = []

        for sentiment_type, percent in sentiment_analysis_results.items():
            if percent == 0:
                continue
            else:
                pie_chart_labels.append(sentiment_type.split('_')[1].capitalize())
                pie_chart_percentages.append(percent / 100)

        pie_chart_figure, pie_chart_ax = plt.subplots()
        pie_chart_ax.pie(pie_chart_percentages, labels=pie_chart_labels, autopct='%1.0f%%',
                                startangle=90, wedgeprops={'linewidth': 3.0, 'edgecolor': 'white'},textprops={'color': 'white'})

        pie_chart_figure.set_facecolor('none')

        container_id = 'sentiment_chart_container'
        new_id = 'sentiment_chart'
        self.create_plot_box_layout(container_id, new_id)
        self.manager.get_screen("second").ids.sentiment_chart.add_widget(FigureCanvasKivyAgg(pie_chart_figure))


    """Top Topics Chart"""
    def populate_topics_chart(self, sorted_top_topics_dict):

        top_topic_bar = plt.figure()
        top_topic_plot = top_topic_bar.add_subplot(1, 2, 2)

        topics = []
        topic_count = []

        for topic, count in sorted_top_topics_dict.items():
            topics.append(topic)
            topic_count.append(count)

        top_topic_plot.bar(topics, topic_count)
        top_topic_plot.set_ylabel('Number of Occurrences')
        top_topic_bar.set_facecolor('none')
        top_topic_plot.yaxis.label.set_color('white')
        top_topic_plot.xaxis.label.set_color('white')
        top_topic_plot.set_xlabel('Top Topics')

        container_id = 'top_topic_theme_bar_container'
        new_id = 'top_topic_theme_bar'
        self.create_plot_box_layout(container_id, new_id)
        self.manager.get_screen("second").ids.top_topic_theme_bar.add_widget(FigureCanvasKivyAgg(top_topic_bar))


    """Top Words Chart"""
    def populate_words_chart(self, sorted_top_words_dict):

        top_words_bar = plt.figure()
        top_words_plot = top_words_bar.add_subplot(1, 2, 2)

        words = []
        word_counts = []

        for word, word_count in sorted_top_words_dict.items():
            words.append(word)
            word_counts.append(word_count)

        top_words_plot.bar(words, word_count)
        top_words_bar.set_facecolor('none')
        top_words_plot.set_ylabel('Number of Occurrences')
        top_words_plot.set_xlabel('Top Words')

        top_words_plot.xaxis.label.set_color('white')
        top_words_plot.yaxis.label.set_color('white')

        container_id = 'top_token_bar_chart_container'
        new_id = 'top_token_bar_chart'
        self.create_plot_box_layout(container_id, new_id)
        self.manager.get_screen("second").ids.top_token_bar_chart.add_widget(FigureCanvasKivyAgg(top_words_bar))


    def toggle_disable_inputs(self):
        if(self.ids.csv_txt_input.disabled is True):
            self.ids.csv_txt_input.disabled = False
            self.ids.typed_txt_input.disabled = True
            self.ids.browse_btn.disabled = False
            gui_config.input_method = 'c'
        else:
            self.ids.csv_txt_input.disabled = True
            self.ids.typed_txt_input.disabled = False
            self.ids.browse_btn.disabled = True
            gui_config.input_method = 'r'


    def dismiss_popup(self):
        self._popup.dismiss()


    def show_load(self):
        content = LoadDialog(load=self.load, cancel=self.dismiss_popup)
        self._popup = Popup(title="Load file", content=content,
                            size_hint=(0.9, 0.9))
        self._popup.open()


    def load(self, path, filename):

        self.ids.csv_txt_input.text = os.path.join(path, filename[0])
        self.dismiss_popup()


    def create_plot_box_layout(self, container_id, new_id):

        container = self.manager.get_screen("second").ids[container_id]
        layout = BoxLayout(orientation='vertical')
        container.add_widget(layout)
        self.manager.get_screen("second").ids[new_id] = layout


class AnalysisReportApp(Screen):
    
    def remove_plot_graphs(self):
        pie_chart_container = self.ids.sentiment_chart_container
        pie_chart = self.ids.sentiment_chart
        pie_chart_container.remove_widget(pie_chart)

        top_topics_chart_container = self.ids.top_topic_theme_bar_container
        top_topic_chart = self.ids.top_topic_theme_bar
        top_topics_chart_container.remove_widget(top_topic_chart)

        top_words_chart_container = self.ids.top_token_bar_chart_container
        top_words_chart = self.ids.top_token_bar_chart
        top_words_chart_container.remove_widget(top_words_chart)


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
