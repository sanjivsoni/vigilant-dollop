from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.screenmanager import FadeTransition
from kivy.uix.textinput import TextInput

Builder.load_file("authentication.kv")
# Declare both screens
class LoginScreen(Screen):
    pass

class SignupScreen(Screen):
    pass

# Create the screen manager
sm = ScreenManager(transition=FadeTransition())
sm.add_widget(LoginScreen(name='login'))
sm.add_widget(SignupScreen(name='signup'))

class TestApp(App):

    def build(self):
        return sm

if __name__ == '__main__':
    TestApp().run()