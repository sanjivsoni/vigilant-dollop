from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.screenmanager import FadeTransition
from kivy.uix.textinput import TextInput

from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.progressbar import ProgressBar
from kivy.uix.scrollview import ScrollView
from kivy.uix.image import Image
from kivy.uix.popup import Popup
from kivy.uix.dropdown import DropDown
import re


Builder.load_file("authentication.kv")
# Declare both screens


class MenuScreen(Screen):
    pass

class LoginScreen(Screen):
    pass

class OtpScreen(Screen):
    pass

class SignupScreen(Screen):
    def val_change(self):
        label = ['bar','1','2','3','4','5','6','7','8','9','10','11','12','13']
        label_b = self.ids['bar']


        set_val = 0
        for num in range(1,14):
        	label[num] = self.ids[str(num)]
        	if not(label[num].text == ''):
        		set_val+=100

        label_b.value =  set_val

    def mail_valid():
        mail_e = self.ids['4']
        _valid = self.ids['MSG3']
        if re.match(r'[\w.-]+@[\w.-]+', mail_e.text):
            _valid.text= ""
        else:
            _valid.text= "Not The Correct Format"
    def conf_valid(self):
        pass_w = self.ids['2']
        pass_c = self.ids['3']
        _valid = self.ids['MSG2']
        if pass_w.text != pass_c.text:
            _suggest = " Password Doesn't Match. "
        else:
            _suggest = " "
        
        _valid.text = _suggest
        
    def pass_valid(self):
        pass_w = self.ids['2']
        uCase = 0
        lCase = 0
        num = 0
        splChar = 0
        lent = 0
        VAL = pass_w.text
        _suggest = ""
        _valid = self.ids['MSG']
        if len(VAL)<8 or len(VAL)>16:
            lent = 0
        else:
            lent = 1
        for i in range (0,len(VAL)):
           if VAL[i].isupper():
               uCase = 1
           if VAL[i].islower():
               lCase = 1
           if VAL[i].isdigit():
               num = 1
           if (not(VAL[i].isupper()) and not(VAL[i].islower()) and not(VAL[i].isdigit())):
               splChar = 1      
        if not(uCase):
            _suggest = _suggest + "\n Password Must Have One Upper Case Char."
        else :
            _suggest = _suggest + " "
        if not(lCase):
            _suggest = _suggest + "\n Password Must Have One Lower Case Char."
        if not(num):
            _suggest = _suggest + "\n Password Must Have One Digit."
        if not(splChar):
            _suggest = _suggest + "\n Password Must Have One Special Char."
        if not(lent):
            _suggest = _suggest + "\n Password Must Be Between 8 and 16 characters long\n"
           
        _valid.text = _suggest

    def mail_work(self):
        self.val_change()
        self.mail_valid()
    def conf_work(self):
        self.val_change()
        self.conf_valid()
    def pass_work(self):
        self.val_change()
        self.pass_valid()

# Create the screen manager
sm = ScreenManager(transition=FadeTransition())

#s
sm.add_widget(MenuScreen(name='main'))
sm.add_widget(SignupScreen(name='signup'))
sm.add_widget(LoginScreen(name='login'))
sm.add_widget(OtpScreen(name='otp'))
class TestApp(App):

    def build(self):
        return sm

if __name__ == '__main__':
    TestApp().run()
