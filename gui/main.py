
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.togglebutton import ToggleButton
from kivy.app import App
from kivy.graphics import Color
from kivy.core.window import Window
import kivy
kivy.require('2.0.0')


class FratForLife(Widget):
    '''
    def __init__(self, **kwargs):
        super(FratForLife, self).__init__(**kwargs)
        with self.canvas.before:
            Color(0, 1, 0)
    '''
    pass


class FratApp(App):
    def build(self):
        Window.size = (1920, 1080)
        return FratForLife()


if __name__ == '__main__':
    FratApp().run()


'''
class FratForLife(Widget):
    pass


class FratApp(App):
    def build(self):
        Window.size = (1920, 1080)
        layout = GridLayout(cols=1, rows=5)
        layout.add_widget(Label(text='Feedback Response Analysis Tool'))
        layout.add_widget(TextInput(text='Sample input text'))
        layout.add_widget(ToggleButton(text='Toggle'))
        csvLayout = GridLayout(cols=2, rows=2)
        csvLayout.add_widget(TextInput(text='CSV Location on your pc'))
        csvLayout.add_widget(Button(text='Browse Local Files'))
        csvLayout.add_widget(
            TextInput(text='Enable toggle to type in a single response'))
        csvLayout.add_widget(Button(text='Analyze'))
        layout.add_widget(csvLayout)
        return layout


if __name__ == '__main__':
    FratApp().run()
'''
