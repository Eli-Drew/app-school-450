"""
=================================================
Author: Drew Rinker

=================================================
"""

import kivy
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.gridlayout import GridLayout

kivy.require('2.0.0')

class PongGame(Widget):
    pass

class PongSlap(GridLayout):
    pass

class PongApp(App):
    def build(self):
        return PongGame()

if __name__ == "__main__":
    PongApp().run()