# Kivy Imports
from kivy.app import App
from kivy.app import Builder
from kivy.uix.screenmanager import FadeTransition, ScreenManager, Screen
from kivy.properties import ObjectProperty

from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.core.window import Window

from kivy.uix.filechooser import FileChooserIconView
from kivy.uix.popup import Popup
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
            choice = randint(0, 1)
        
            App.get_running_app().root.get_screen('levelTwoScreen').updateButtonLabel(choice)
        
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
    _otp_choice = 0

    def sendOtp(self):
        pass

    def updateButtonLabel(self, choice):
        if choice == 1:
            self.ids.send.text = "Send OTP to Email"
        else:
            self.ids.send.text = "Send OTP to Mobile"

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

class LoadDialog(FloatLayout):
    load = ObjectProperty(None)
    cancel = ObjectProperty(None)

class HomeScreen(Screen):

    counter = 0
    second_counter = 0

    def __init__(self, **kwargs):
        super(HomeScreen, self).__init__(**kwargs)

        layout = BoxLayout(orientation = 'vertical')
        top_layout = BoxLayout(orientation= 'horizontal', size_hint=(1, 0.1))
        
        button = Button(text="Lock Files", id='lock_button')
        button.bind(on_press = partial(self.lockFile, 'file' ))

        button_unlock = Button(text="Unlock File", id='unlock_button')
        #button_unlock.bind(on_press = partial(self.unlockFile, 'file1'))

        top_layout.add_widget(button)
        top_layout.add_widget(button_unlock)
        bottom_layout = BoxLayout(size_hint = (1, 0.9))
        

        grid = GridLayout(id='unlocked_files', cols=6, padding=25, spacing=41,
                size_hint=(None, None), width=650,  pos_hint={'center_x': .5, 'center_y': .5})

        grid.bind(minimum_height=grid.setter('height'))


        # add button into that grid
        '''
        for i in range(8):
            btn = Button(text = "file" + str(i), size = (90, 90),
                         size_hint = (None, None), id = str(i))
            btn.bind(on_press = partial(self.unlockFile, str(i)))

            grid.add_widget(btn)
        '''
        # create a scroll view, with a size < size of the grid
        scroll = ScrollView(size_hint = (None, None), size = (650, 500),
                pos_hint = {'center_x': .5, 'center_y': .5}, do_scroll_x = False)	
	scroll.add_widget(grid)
	bottom_layout.add_widget(scroll)
	layout.add_widget(top_layout)
	layout.add_widget(bottom_layout)
        self.add_widget(layout)

    def lockFile(self, *args):
        self.counter = self.counter + 1
#        print args[0]
#        print ("button pressed <%s> " %args[0])
        button = Button(text=str(args[0]) + str(self.counter), size=(70, 70),
                         size_hint=(None, None), id = str(self.counter))

        button.bind(on_press = partial(self.unlockFile, str(self.counter)))
        #button.bind(on_press = partial(self.un
        self.children[0].children[0].children[0].children[0].add_widget(button)

    def unlockFile(self, *args):

        grid = self.children[0].children[0].children[0].children[0]
#        print grid.children[int(args[0])]
        inValidWidget = []
        
        for child in grid.children:
            if child.id == args[0]:
                grid.remove_widget(child)
    
#    def printFilePath(self):
#        print self.ids.icon_view_tab.path, self.ids.icon_view_tab.selection
    



# Screen Manager
screenManager = ScreenManager( transition = FadeTransition() )

# Add all screens to screen manager
#screenManager.add_widget( UsernameScreen( name = 'usernameScreen' ) )
#screenManager.add_widget( PasswordScreen( name = 'passwordScreen' ) )
#screenManager.add_widget( LevelTwoScreen( name = 'levelTwoScreen' ) )
#screenManager.add_widget( LevelTwoScreen( name = 'levelThreeScreen' ) )

screenManager.add_widget( HomeScreen( name = 'homeScreen' ) )

class ThreeLevelAuthApp(App):
	def build(self):
		return screenManager

if __name__ == '__main__':
	ThreeLevelAuthApp().run()


