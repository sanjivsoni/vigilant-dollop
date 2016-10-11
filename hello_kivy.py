import kivy

from kivy.app import App
from kivy.app import ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmamager import ScreenManager, Screen

class LoginScreen(Screen):
    pass

class SignUpScreen(Screen):
    pass

class MainScreen(BoxLayout):
    pass

class MyScreenManager(ScreenManager):
    pass

class AuthenticationApp(App):
    def build(self):
        return MyScreenManager()

if __name__ == '__main__':
    AuthenticationApp().run()

