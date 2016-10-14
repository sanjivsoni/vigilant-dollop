# Kivy Imports
from kivy.app import App
from kivy.app import Builder
from kivy.uix.screenmanager import FadeTransition, ScreenManager, Screen
from kivy.properties import ObjectProperty

from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.core.window import Window


from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.progressbar import ProgressBar
from kivy.uix.dropdown import DropDown

from kivy.uix.image import Image

from kivy.clock import Clock

# Python Imports
from random import randint
import re
from functools import partial

# Load Kivy file
Builder.load_file("authentication.kv")

Window.size = (700, 700)

# Classes for seperate screens
class UsernameScreen(Screen):
    username = ObjectProperty(None)
    message = ObjectProperty(None)
    
    # Validate User input Event
    def usernameEvent(self):
        # Stub
        self.username.text = "elliot"

        # Successful match for Username 
        if( self.username.text == "elliot"):
            # Change present screen to password screen.
            App.get_running_app().root.current = 'passwordScreen'
        
        # Unsuccessful match for Username
        else:
            self.message.text = 'Invalid Username'

    # Recover User name Event
    def recoverUsernameEvent(self):
        pass

class PasswordScreen(Screen):
    password = ObjectProperty(None)
    message = ObjectProperty(None)
    
    # Validate User Password input Event
    def passwordEvent(self):
        # Stub
        self.password.text = "elliot"

        # Successful match for Password 
        if( self.password.text == "elliot"):
            # Change present screen to password screen.
            App.get_running_app().root.current = 'levelTwoScreen'
        
        # Unsuccessful match for Username
        else:
            self.message.text = 'Invalid Username'

    # Recover User name Event
    def recoverUsernameEvent(self):
        pass

class LevelTwoScreen(Screen):
    
    otp = ObjectProperty(None)
    send = ObjectProperty(None)
    minutes = ObjectProperty(None)
    seconds = ObjectProperty(None)
    # 5 minutes timer
    _total_seconds = 30
    _total_minutes = 0
    _minutes = _total_seconds
    _seconds = _total_minutes
    _otp_expired = 0

    _time_event = 0

    def sendOtp(self):
        pass

    # Update Timer after One Second
    def updateTimer(self, dt):
        if self._minutes >= 0 and self._seconds > 0:
            self._seconds = self._seconds - 1
            if self._minutes > 0 and self._seconds == 0: 
                self._seconds = 60
                self._minutes = self._minutes - 1

            elif self._minutes == 0 and self._seconds == 0:
                Clock.unschedule(self._time_event)
                self.ids.send.disabled = False
                # Resend OTP after Timeout
                sentOtp()

            if self._minutes > 9:
                self.minutes.text = str(self._minutes) + ':'
            else:
                self.minutes.text = '0' + str(self._minutes) + ':'
                
            if self._seconds > 9:
                self.seconds.text = str(self._seconds)
            else:
                self.seconds.text = '0' + str(self._seconds)
    
    def endTimer(self):
        pass

    # Save OTP to database incase of app crash
    def saveTimer(self):
        pass
	
    def validOtpEvent(self):
        # Stub
        self.otp.text = "1"
        validOtp = "1"
        self._seconds = self._total_seconds
        self._minutes = self._total_minutes

        self._time_event = Clock.schedule_interval(partial(self.updateTimer), 1)
        self.ids.send.disabled = True

        # If valid OTP
        if validOtp == self.otp.text:
           # App.get_running_app().root.current = 'levelThreeScreen'
            pass            
        # Invalid OTP



# Screen Manager
screenManager = ScreenManager( transition = FadeTransition() )

# Add all screens to screen manager
screenManager.add_widget( UsernameScreen( name = 'usernameScreen' ) )
screenManager.add_widget( PasswordScreen( name = 'passwordScreen' ) )
screenManager.add_widget( LevelTwoScreen( name = 'levelTwoScreen' ) )
screenManager.add_widget( LevelTwoScreen( name = 'levelThreeScreen' ) )


class ThreeLevelAuthApp(App):
	def build(self):
		return screenManager

if __name__ == '__main__':
	ThreeLevelAuthApp().run()


