import kivy
from kivy.app import App
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.graphics import Color
from subprocess import Popen
import config
import main

kivy.require('2.0.0')


class AnalysisReportApp(App):
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

    def close_open(self):
        AnalysisReportApp().stop()
        Popen(['python', 'main.py'])


if __name__ == '__main__':
    AnalysisReportApp().run()
