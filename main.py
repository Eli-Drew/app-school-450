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
# do not move the above two lines. they have to come before the rest of the imports
import os
import nltk
import kivy
from kivy.app import App
from kivy.core.window import Window
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg
import matplotlib.pyplot as plt
import user_input.input
from analysis.Sentiment_Analysis import Sentiment_Analysis
from analysis.Thematic_Anlaysis import Thematic_Analysis
from analysis.Top_Words_Analysis import Top_Words_Analysis
from gui import config
from kivy.uix.boxlayout import BoxLayout

nltk.download('stopwords')
kivy.require('2.0.0')

MAXLEN = 250

class FratForLife(Screen):
    #csv_txt_input = ObjectProperty(None)

    def main(self):

        if(config.input_method == 'c'):
            valid_path = False
            while not valid_path:
                csv_file_path = self.ids.csv_txt_input.text
                responses = user_input.input.csv_option(csv_file_path, MAXLEN)
                if not responses == "INVALID":
                    valid_path = True
                else:
                    # TODO replace this with a popup message that should have to be clicked to exit to be able re-enter another file
                    print("That was not a valid csv path or file. File must exist and end in a \'.csv\' extension.")
        else:
            response = self.ids.typed_txt_input.text
            responses = user_input.input.response_option(response, MAXLEN)

        # Sentiment Analysis
        padded_sequences = Sentiment_Analysis.pre_process(responses, MAXLEN)
        sentiments = Sentiment_Analysis.analyze(padded_sequences)
        sentiment_analysis_results = Sentiment_Analysis.format_results(sentiments)
        featured_responses = Sentiment_Analysis.get_featured_responses(
            responses, sentiments, sentiment_analysis_results["average"][1])
        
        # Thematic Analysis
        clean_responses = Thematic_Analysis.pre_process(responses, MAXLEN)
        Thematic_Analysis.analyze(clean_responses)
        Thematic_Analysis.format_results()
        sorted_top_topics_dict = self.get_topics_dict()

        # Top Words Analysis
        word_dict = Top_Words_Analysis.pre_process(responses, MAXLEN)
        top_words_dict = Top_Words_Analysis.analyze(word_dict)
        sorted_top_words_dict = Top_Words_Analysis.format_results(top_words_dict)

        # Populate GUI
        self.populate_summary_chart(sentiment_analysis_results, featured_responses, sorted_top_topics_dict)
        self.populate_pie_chart(sentiment_analysis_results)
        self.populate_topics_chart(sorted_top_topics_dict)
        self.populate_words_chart(sorted_top_words_dict)


        # self.ids.topic_text.text = topic_one
        # open_close(self)


    """Create dictionary of top topics and related sentiments sorted from greatest to least"""
    def get_topics_dict(self):

        top_topics_list = config.topic_list[0]
        top_topics_dict = {}

        # Create topics dicionary out of topics list
        for topic in top_topics_list:
            top_topics_dict[topic[0].capitalize()] = topic[1]

        # Sort top_topics_dict
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

        return sorted_top_topics_dict


    """Analysis Summary Chart"""
    def populate_summary_chart(self, sentiment_analysis_results, featured_responses, sorted_top_topics_dict):

        average_sentiment = sentiment_analysis_results.pop("average")

        # Add average sentiment results to summary chart
        self.manager.get_screen("second").ids.average_sentiment.text = "{} | {}".format(str(average_sentiment[0]), average_sentiment[1])
        self.manager.get_screen("second").ids.featured_response_title.text ="Featured {} Responses".format(average_sentiment[1])
        
        # Add featured responses to summary chart
        # TODO make the responses be populated on different GUI fields
        # for i in range(len(featured_responses)):
        #     self.manager.get_screen("second").ids.featured_response_1.text = "\"{}\"".format(featured_responses[i])
        self.manager.get_screen("second").ids.featured_response_1.text = "\"{}\"".format(featured_responses[0])
        self.manager.get_screen("second").ids.featured_response_2.text = "\"{}\"".format(featured_responses[1])
        self.manager.get_screen("second").ids.featured_response_3.text = "\"{}\"".format(featured_responses[2])

        # Add top topics to summary chart
        # TODO make the topics be populated on different GUI fields
        # for topic, sentiment in sorted_top_topics_dict.items():
        #     self.manager.get_screen("second").ids.theme_1.text = "{} | {}".format(topic, str(sentiment))
        self.manager.get_screen("second").ids.theme_1.text = "{} | {}".format("topic1", str(1.5))
        self.manager.get_screen("second").ids.theme_2.text = "{} | {}".format("topic2", str(1.5))
        self.manager.get_screen("second").ids.theme_3.text = "{} | {}".format("topic3", str(1.5))
        self.manager.get_screen("second").ids.theme_4.text = "{} | {}".format("topic4", str(1.5))
        self.manager.get_screen("second").ids.theme_5.text = "{} | {}".format("topic5", str(1.5))

    
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
        # pie_chart_ax.axis('equal')
        pie_chart_figure.set_facecolor('none')

        container_id = 'sentiment_chart_container'
        new_id = 'sentiment_chart'
        self.create_plot_box_layout(container_id, new_id)
        self.manager.get_screen("second").ids.sentiment_chart.add_widget(FigureCanvasKivyAgg(pie_chart_figure))


    """Top Topics/Sentiments Chart"""
    def populate_topics_chart(self, sorted_top_topics_dict):

        top_topic_bar = plt.figure()
        top_topic_plot = top_topic_bar.add_subplot(1, 2, 2)

        topics = []
        topic_sentiments = []

        for topic, topic_sentiment in sorted_top_topics_dict.items():
            topics.append(topic)
            topic_sentiments.append(topic_sentiment)

        top_topic_plot.bar(topics, topic_sentiments)
        # top_words_bar.set_facecolor('none')
        top_topic_plot.set_ylabel('Sentiment Rating')
        top_topic_plot.set_xlabel('Top Topics')

        container_id = 'top_topic_theme_bar_container'
        new_id = 'top_topic_theme_bar'
        self.create_plot_box_layout(container_id, new_id)
        self.manager.get_screen("second").ids.top_topic_theme_bar.add_widget(FigureCanvasKivyAgg(top_topic_bar))


    """Top Words Chart"""
    def populate_words_chart(self, sorted_top_words_dict):

        # TODO make graph look better and add labels
        top_words_bar = plt.figure()
        top_words_plot = top_words_bar.add_subplot(1, 2, 2)
        # top_token_ax = top_words_bar.add_axes([0,0,1,1])

        words = []
        word_counts = []

        for word, word_count in sorted_top_words_dict.items():
            words.append(word)
            word_counts.append(word_count)

        top_words_plot.bar(words, word_count)
        top_words_plot.set_facecolor('none')
        top_words_plot.set_ylabel('Number of Occurrences')
        top_words_plot.set_xlabel('Top Words')

        container_id = 'top_token_bar_chart_container'
        new_id = 'top_token_bar_chart'
        self.create_plot_box_layout(container_id, new_id)
        self.manager.get_screen("second").ids.top_token_bar_chart.add_widget(FigureCanvasKivyAgg(top_words_bar))


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

    def create_plot_box_layout(self, container_id, new_id):
    # TODO passing the id is odd
        container = self.manager.get_screen("second").ids[container_id]
        layout = BoxLayout(orientation='vertical')
        container.add_widget(layout)
        self.manager.get_screen("second").ids[new_id] = layout


class AnalysisReportApp(Screen):
    def clear_topics(self):
        config.topic_list.clear()

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
