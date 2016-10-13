from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.screenmanager import FadeTransition
from kivy.uix.textinput import TextInput
from kivy.properties import ObjectProperty


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

from random import randint

Builder.load_file("authentication.kv")

sm = ScreenManager(transition=FadeTransition())

class MenuScreen(Screen):
    pass

class UsernameScreen(Screen):
    username = ObjectProperty(None)
    message = ObjectProperty(None)
    
    def usernameEvent(self):
        # Stub
        self.username.text = "elliot"

        # Successful match for Username 
        if( self.username.text == "elliot"):
            App.get_running_app().root.current = 'password_screen'
        
        # Unsuccessful match for Username
        else:
            self.message.text = 'Invalid Username'

    def recoverUsernameEvent:
        pass

class PasswordScreen(Screen):
    password = ObjectProperty(None)
    message = ObjectProperty(None)
    
    def loginEvent(self):
        # Stub
        self.password.text = "elliot"

        # Successful match for Password 
        if( self.username.text == "elliot"):
            App.get_running_app().root.current = 'otp_screen'
        
        # Unsuccessful match for Password
        else:
            self.message.text = 'Invalid Password'

    pass

class LevelTwoScreen(Screen):
    pass

class LevelThreeScreen(Screen):
    pass

class RecoverUsernameScreen(Screen):
    pass

class RecoverPasswordScreen(Screen):
    pass

class HomeScreen(Screen):
    pass

class LoginScreen(Screen):
    username = ObjectProperty(None)
    password = ObjectProperty(None)
    message = ObjectProperty(None)
    loginButton = ObjectProperty(None)
    recoverButton = ObjectProperty(None)

    def loginEvent(self):
        self.username.text = "elliot"
        self.password.text = "elliot"


        # Successful Login
        if( self.username.text == "elliot" and self.password.text == "elliot"):
            self.message.text = 'login Successful'

            choice = randint(0,1)
            otp_label = ''

            if choice == 1:
                otp_label = "Enter OTP sent to your registered Email address"
                print 'Email'
                App.get_running_app().root.current = 'otp'
                App.get_running_app().root.get_screen('otp').update_otp_label(otp_label)
                
            else:
                otp_label = "Enter OTP sent to your registered Mobile Number"
                print 'Mobile'
                App.get_running_app().root.current = 'otp'
                App.get_running_app().root.get_screen('otp').update_otp_label(otp_label)
                
                
        # Failed Login
        else:
            self.message.text = 'login Unsuccessful'


class OtpScreen(Screen):
    otp_label = ObjectProperty(None)

    def update_otp_label(self, updated_text):
        self.otp_label.text = updated_text


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


#s
sm.add_widget(MenuScreen(name='username_screen'))
class TestApp(App):

    def build(self):
        return sm

if __name__ == '__main__':
    TestApp().run()
