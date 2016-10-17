from helperFunctions import*

#for classes
from UserClass import*
from LoginDetailsClass import*
from AuthenticationClass import*
from UserCredentialsRecoveryClass import *

# Load Kivy file
Builder.load_file("authentication.kv")

Window.size = (700, 700)
verifyUser = Authentication()
choice = -1
userID = ""
attempt = 0
generatedOTP = 0
# Classes for seperate screens
class ChangePassword(Screen):
    pass

class UsernameScreen(Screen):
    username = ObjectProperty(None)
    message = ObjectProperty(None)
    attempt = 0
    invalidTime = 0
    # Validate User input Event
    def usernameEvent(self):
        # Stub
        self.username.text  = "bhatshubhs"
        global attempt
        global verifyUser
        global userID

        userExists = verifyUser.checkIfUserExists(self.username.text)
        # Successful match for Username
        if(self.username.text  == "bhatshubhs"):
            # Change present screen to password screen.
            App.get_running_app().root.current = 'passwordScreen'
            userID = self.username.text

        # Unsuccessful match for Username
        else:
            self.message.text = 'Invalid Username'

    # Recover User name Event
    def recoverUsernameEvent(self):
        App.get_running_app().root.current = 'usernameRecoverScreen'
        App.get_running_app().root.get_screen('usernameRecoverScreen').parameter(1)

class PasswordScreen(Screen):
    password = ObjectProperty(None)
    message = ObjectProperty(None)

    # Validate User Password input Event
    def passwordEvent(self):
        # Stub
        self.password.text = "123456"
        global verifyUser
        global choice
        passwordMatched = verifyUser.checkUserLevel1(self.password.text)
        # Successful match for Password
        if(passwordMatched):
            # Change present screen to password screen.
            App.get_running_app().root.current = 'levelTwoScreen'
            choice = randint(0, 1)
            choice2 = randint(0, 6)
            App.get_running_app().root.get_screen('levelTwoScreen').updateScreen(choice, choice2)

        else:
            # Unsuccessful match for Username
            self.message.text = 'Invalid Password'

    # Recover User name Event
    def recoverPasswordEvent(self):
        App.get_running_app().root.current = 'passwordRecoverScreen'
        App.get_running_app().root.get_screen('passwordRecoverScreen').parameter(2)

class UsernameRecover(Screen):
    username = ObjectProperty(None)
    message = ObjectProperty(None)
    recoverlink = ObjectProperty(None)
    attempt = 0
    invalidTime = 0
    pathValue = 0
    # Validate User input Event
    #self.ids['loginButton'].disabled = True
    def nextUserEvent(self):
        # Stub
        global generatedOTP
        my_queue = Queue.Queue()
        recoverUser = UserRecovery()
        contact = self.ids.recoverlink
        x = 0
        if re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", contact.text):
            print "Email"
            thread1 = Thread(target = recoverUser.recoverUserLevel1, args = (2,contact.text,my_queue,))
            thread1.start()
            App.get_running_app().root.current = 'recoverylevelTwoScreen'
            App.get_running_app().root.get_screen('recoverylevelTwoScreen').parameter(self.pathValue)
            x =1

        else:
            print "Phone"
            thread1 = Thread(target = recoverUser.recoverUserLevel1, args = (1,contact.text,my_queue,))
            thread1.start()
            App.get_running_app().root.current = 'recoverylevelTwoScreen'
            App.get_running_app().root.get_screen('recoverylevelTwoScreen').parameter(self.pathValue)
            x = 2
        generatedOTP = my_queue.get()




    def parameter(self,x):
        self.pathValue = x
    # Recover User name Event
    def recoverUsernameEvent(self):
        pass

class PasswordRecover(Screen):
    username = ObjectProperty(None)
    message = ObjectProperty(None)
    attempt = 0
    invalidTime = 0
    pathValue = 0
    # Validate User input Event
    #self.ids['loginButton'].disabled = True
    def nextPassEvent(self, buttonValue):
        global userID
        recoverPassword = PasswordRecovery(userID)
        my_queue = Queue.Queue()

        # Stub
        if buttonValue == 1:
            thread1 = Thread(target = recoverPassword.recoverPasswordLeveL1, args = (2,my_queue,))
            thread1.start()

        elif buttonValue == 2:
            thread1 = Thread(target = recoverPassword.recoverPasswordLeveL1, args = (1,my_queue,))
            thread1.start()

        global generatedOTP
        generatedOTP = my_queue.get()
        print generatedOTP
        
        App.get_running_app().root.current = 'recoverylevelTwoScreen'
        App.get_running_app().root.get_screen('recoverylevelTwoScreen').parameter(self.pathValue)

        #else:
         #  pass
    def parameter(self,x):
        self.pathValue = x
    # Recover User name Event
    def recoverUsernameEvent(self):
        pass
class RecoverySecQuestion(Screen):
    pathValue = 0
    
    def questionEvent(self):
        QValue = -1
        Question = self.ids['recoveryQuestion']
        Answer = self.ids['recoveryAnswer']
        if Question.text == "Your Childhood Hero?":
            QValue = 5
        elif Question.text == "Time Of The Day Were You Born ?":
            QValue = 6
        elif Question.text == "The steet you grew up in?":
            QValue = 7
        elif Question.text == "Your Childhood Nickname?":
            QValue = 8
        elif Question.text == "Mother's Maiden Name ?":
            QValue = 1
        elif Question.text == "Pet's Name ?":
            QValue = 2
        elif Question.text ==  "First Teacher's Name ?":
            QValue = 3
        elif Question.text == "Favourite Holiday Destination?":
            QValue = 4
        else:
            QValue = -1
        if QValue == "": #Comparison for Question 
            if Answer.text == "":#Comparison for Answer
                pass
            else:
                pass
        else:
            pass
    def parameter(self,x):
        self.pathValue = x
class RecoveryLevelThreeScreen(Screen):

    pathValue = 0
    contactValue = 0

    def parameter(self,x,y):
        self.pathValue = x
        self.contactValue = y
    def renderSecurityQues(self):
        ssn = self.ids['ssn_Value']
        ssnType = 0
        message = "Please Enter Your" + str(ssnType) + "Number"
        # Stub
        if 1:#compare SSN with Database Value
            App.get_running_app().root.current = 'recoverysecQuestion'
            App.get_running_app().root.get_screen('recoverysecQuestion').parameter(self.pathValue)
        else:
            pass
        # Invalid OTP

class RecoveryLevelTwoScreen(Screen):

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
    pathValue = 0
    choiceValue = 0
    _time_event = 0
    _otp_choice = 0

    def parameter(self,x):
        self.pathValue = x


    def sendOtp(self):
        pass

    def color_white(self,dt):
        label= []
        label.append(self.ids['otp'])
        label.append(self.ids['otp_2'])
        label.append(self.ids['otp_3'])
        label.append(self.ids['otp_4'])
        label.append(self.ids['otp_5'])
        label.append(self.ids['otp_6'])

        for i in range(0,6):
            label[i].background_color = [1,1,1,1]
            label[i].text = ""
    def compareOTP(self):
        global generatedOTP
        label= []
        label.append(self.ids['otp'])
        label.append(self.ids['otp_2'])
        label.append(self.ids['otp_3'])
        label.append(self.ids['otp_4'])
        label.append(self.ids['otp_5'])
        label.append(self.ids['otp_6'])
        global otpCompareValue
        otpCompareValue = 0
        tempPass = ""
        for i in range(0,6):
            tempPass += label[i].text

        otpFlag = 0

        for i in range(0,6):
            if not(label[i].text ==""):
                continue
            else:
                otpFlag = 1
                break
        if otpFlag == 0:
            if tempPass == generatedOTP:
                for i in range(0,6):
                    label[i].background_color = [0,1,0,1]
                    App.get_running_app().root.current = 'recoverylevelThreeScreen'
                    App.get_running_app().root.get_screen('recoverylevelThreeScreen').parameter(self.pathValue,x)

            else:
                for i in range(0,6):
                    label[i].background_color = [1,0,0,1]
                    otpCompareValue = 0
                Clock.schedule_once(self.color_white, 1)
                label[0].focus = True

    def check1_otp(self):
        otp = self.ids['otp']
        otp2 = self.ids['otp_2']
        otp3 = self.ids['otp_3']
        otp4 = self.ids['otp_4']
        otp5 = self.ids['otp_5']
        otp6 = self.ids['otp_6']
        if not(otp.text == ""):
            if not(otp.text.isdigit()):
                otp.text = ""
            else:
                self.compareOTP()
                otp.focus = False
                otp2.focus = True
    def check2_otp(self):
        otp = self.ids['otp']
        otp2 = self.ids['otp_2']
        otp3 = self.ids['otp_3']
        otp4 = self.ids['otp_4']
        otp5 = self.ids['otp_5']
        otp6 = self.ids['otp_6']
        if not(otp2.text == ""):
            if not(otp2.text.isdigit()):
                otp.text = ""
            else:
                self.compareOTP()
                otp2.focus = False
                otp3.focus = True
    def check3_otp(self):
        otp = self.ids['otp']
        otp2 = self.ids['otp_2']
        otp3 = self.ids['otp_3']
        otp4 = self.ids['otp_4']
        otp5 = self.ids['otp_5']
        otp6 = self.ids['otp_6']
        if not(otp3.text == ""):
            if not(otp3.text.isdigit()):
                otp3.text = ""
            else:
                self.compareOTP()
                otp3.focus = False
                otp4.focus = True
    def check4_otp(self):
        otp = self.ids['otp']
        otp2 = self.ids['otp_2']
        otp3 = self.ids['otp_3']
        otp4 = self.ids['otp_4']
        otp5 = self.ids['otp_5']
        otp6 = self.ids['otp_6']
        if not(otp4.text == ""):
            if not(otp4.text.isdigit()):
                otp4.text = ""
            else:
                self.compareOTP()
                otp4.focus = False
                otp5.focus = True
    def check5_otp(self):
        otp = self.ids['otp']
        otp2 = self.ids['otp_2']
        otp3 = self.ids['otp_3']
        otp4 = self.ids['otp_4']
        otp5 = self.ids['otp_5']
        otp6 = self.ids['otp_6']
        if not(otp5.text == ""):
            if not(otp5.text.isdigit()):
                otp5.text = ""
            else:
                self.compareOTP()
                otp5.focus = False
                otp6.focus = True
    def check6_otp(self):
        otp = self.ids['otp']
        otp2 = self.ids['otp_2']
        otp3 = self.ids['otp_3']
        otp4 = self.ids['otp_4']
        otp5 = self.ids['otp_5']
        otp6 = self.ids['otp_6']

        if not(otp6.text == ""):
            if not(otp6.text.isdigit()):
                otp6.text = ""
            else:
                self.compareOTP()
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
        validOtp = ""
        self._seconds = self._total_seconds
        self._minutes = self._total_minutes

        self._time_event = Clock.schedule_interval(partial(self.updateTimer), 1)
        self.ids.send.disabled = True

        # If valid OTP

           # App.get_running_app().root.current = 'levelThreeScreen'
        # Invalid OTP

class LevelTwoScreen(Screen):

    otp = ObjectProperty(None)
    send = ObjectProperty(None)
    minutes = ObjectProperty(None)
    seconds = ObjectProperty(None)
    # 5 minutes timer
    _total_seconds = 60
    _total_minutes = 0
    _minutes = _total_seconds
    _seconds = _total_minutes
    _otp_expired = 0

    _time_event = 0
    _otp_choice = 0
    correctOTP = ""


    def color_white(self,dt):
        label= []
        label.append(self.ids['otp'])
        label.append(self.ids['otp_2'])
        label.append(self.ids['otp_3'])
        label.append(self.ids['otp_4'])
        label.append(self.ids['otp_5'])
        label.append(self.ids['otp_6'])

        for i in range(0,6):
            label[i].background_color = [1,1,1,1]
            label[i].text = ""
    def compareOTP(self):
        label= []
        label.append(self.ids['otp'])
        label.append(self.ids['otp_2'])
        label.append(self.ids['otp_3'])
        label.append(self.ids['otp_4'])
        label.append(self.ids['otp_5'])
        label.append(self.ids['otp_6'])

        tempPass = ""
        for i in range(0,6):
            tempPass += label[i].text

        otpFlag = 0

        for i in range(0,6):
            if not(label[i].text ==""):
                continue
            else:
                otpFlag = 1
                break
        if otpFlag == 0:
            if tempPass == self.correctOTP:
                for i in range(0,6):
                    label[i].background_color = [0,1,0,1]
            else:
                for i in range(0,6):
                    label[i].background_color = [1,0,0,1]

                Clock.schedule_once(self.color_white, 1)
                label[0].focus = True

    def check1_otp(self):
        otp = self.ids['otp']
        otp2 = self.ids['otp_2']
        otp3 = self.ids['otp_3']
        otp4 = self.ids['otp_4']
        otp5 = self.ids['otp_5']
        otp6 = self.ids['otp_6']
        if not(otp.text == ""):
            if not(otp.text.isdigit()):
                otp.text = ""
            else:
                self.compareOTP()
                otp.focus = False
                otp2.focus = True
    def check2_otp(self):
        otp = self.ids['otp']
        otp2 = self.ids['otp_2']
        otp3 = self.ids['otp_3']
        otp4 = self.ids['otp_4']
        otp5 = self.ids['otp_5']
        otp6 = self.ids['otp_6']
        if not(otp2.text == ""):
            if not(otp2.text.isdigit()):
                otp.text = ""
            else:
                self.compareOTP()
                otp2.focus = False
                otp3.focus = True
    def check3_otp(self):
        otp = self.ids['otp']
        otp2 = self.ids['otp_2']
        otp3 = self.ids['otp_3']
        otp4 = self.ids['otp_4']
        otp5 = self.ids['otp_5']
        otp6 = self.ids['otp_6']
        if not(otp3.text == ""):
            if not(otp3.text.isdigit()):
                otp3.text = ""
            else:
                self.compareOTP()
                otp3.focus = False
                otp4.focus = True
    def check4_otp(self):
        otp = self.ids['otp']
        otp2 = self.ids['otp_2']
        otp3 = self.ids['otp_3']
        otp4 = self.ids['otp_4']
        otp5 = self.ids['otp_5']
        otp6 = self.ids['otp_6']
        if not(otp4.text == ""):
            if not(otp4.text.isdigit()):
                otp4.text = ""
            else:
                self.compareOTP()
                otp4.focus = False
                otp5.focus = True
    def check5_otp(self):
        otp = self.ids['otp']
        otp2 = self.ids['otp_2']
        otp3 = self.ids['otp_3']
        otp4 = self.ids['otp_4']
        otp5 = self.ids['otp_5']
        otp6 = self.ids['otp_6']
        if not(otp5.text == ""):
            if not(otp5.text.isdigit()):
                otp5.text = ""
            else:
                self.compareOTP()
                otp5.focus = False
                otp6.focus = True
    def check6_otp(self):
        otp = self.ids['otp']
        otp2 = self.ids['otp_2']
        otp3 = self.ids['otp_3']
        otp4 = self.ids['otp_4']
        otp5 = self.ids['otp_5']
        otp6 = self.ids['otp_6']

        if not(otp6.text == ""):
            if not(otp6.text.isdigit()):
                otp6.text = ""
            else:
                self.compareOTP()

    def sendOtp(self):
        pass

    def updateButtonLabel(self):
        global choice
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
        validOtp = ""
        global choice
        global userID
        my_queue = Queue.Queue()
        sendOTP = OTP(hashEncrypt(userID))

        self._seconds = self._total_seconds
        self._minutes = self._total_minutes

        self._time_event = Clock.schedule_interval(partial(self.updateTimer), 1)
        self.ids.send.disabled = True

        if(choice == 1):
            print "email"
            thread1 = Thread(target = sendOTP.sendOTPforAuth_email, args = (my_queue,))
            thread1.start()
        else:
            print "mobile"
            thread1 = Thread(target = sendOTP.sendOTPforAuth_mobile, args = (my_queue,))
            thread1.start()

        self.correctOTP = my_queue.get()

class HomeScreen(Screen):

    counter = 0
    second_counter = 0


    def __init__(self, **kwargs):
        super(HomeScreen, self).__init__(**kwargs)

        layout = BoxLayout(orientation = 'vertical')
        
        top_layout = BoxLayout(orientation= 'horizontal', size_hint=(1, 0.1), height = 10 )

        button = Button(text="Lock Files", id='lock_button')
	button.bind(on_press = self.show_load)

        
        top_layout.add_widget(button)
        mid_layout = BoxLayout(orientation = 'horizontal', size_hint = (1,0.1))
        bottom_layout = BoxLayout(size_hint = (1, 0.9), padding = 20)

        grid = GridLayout(id='unlocked_files', cols=6, padding=5, spacing=20,
                size_hint=(None, None), width=650,  pos_hint={'center_x': .5, 'center_y': .5})

        grid.bind(minimum_height=grid.setter('height'))


        # add button into that grid
        '''
>>>>>>> e494b1ccd9b5c149407f11f94db0549fdc02fb0a
        for i in range(8):
            btn = Button(text = "file" + str(i), size = (30, 30),
                         size_hint = (None, None), id = str(i))
            btn.bind(on_press = partial(self.unlockFile, str(i)))
            label = Label(text = "file" + str(i), width=90, halign = 'left',valign = 'middle', id="label"+str(i))
            label.bind(size=label.setter('text_size'))

            grid.add_widget(btn)
            grid.add_widget(label)
        '''
        # create a scroll view, with a size < size of the grid
        scroll = ScrollView(size_hint = (None, None), size = (650, 500),
                pos_hint = {'center_x': .5, 'center_y': .5}, do_scroll_x = False)	
	scroll.add_widget(grid)
	bottom_layout.add_widget(scroll)
	layout.add_widget(top_layout)
	layout.add_widget(mid_layout)
	layout.add_widget(bottom_layout)
        self.add_widget(layout)

        content = BoxLayout(size = self.size, pos = self.pos, orientation = 'vertical')
        fileView = FileChooserListView(id = 'filechooser')

        buttons = BoxLayout(size_hint_y = None, height = 20)

        cancel_button = Button(text = 'cancel')
        cancel_button.bind(on_press = self.cancel)

        load_button = Button(text = 'load')
        load_button.bind(on_press = partial(self.load,fileView))

        buttons.add_widget(cancel_button)
        buttons.add_widget(load_button)
        content.add_widget(fileView)
        content.add_widget(buttons)

        self._popup = Popup(title="Select Files to lock", content=content,
                            size_hint=(0.9, 0.9))
    def cancel(self, *args):
        self._popup.dismiss()

    def load(self, *args):
        print args[0].path, args[0].selection[0]
        path = str(args[0].path).split('/')
#        print path
        complete_path = str(args[0].selection[0]).split('/')
#        print complete_path

        for name in path:
            try:
                complete_path.remove(name)
            except ValueError:
                pass

        self.lockFile(args[0].path, complete_path[0])
        self.cancel()


    def lockFile(self, *args):
        self.counter = self.counter + 1
#        print args[0]
#        print ("button pressed <%s> " %args[0])
        button_id = str(args[1])
        button = Button(text=' ', size=(40, 40),
                         size_hint=(None, None), id = button_id)

        button.bind(on_press = partial(self.unlockFile, button_id, args[0]))
        label = Label(text = button_id  , width = 70, halign = 'left',valign = 'middle', id="label"+button_id, font_size='15sp')
        label.bind(size=label.setter('text_size'))
        
        
        grid = self.children[0].children[0].children[0].children[0]
        grid.add_widget(button)
        grid.add_widget(label)

    previous_remove_button_label = ''
    first_time_add_button = 1

    def removeFile(self, *args):
        grid = args[0]
        file_name = args[1]
        label_previous = args[2]
        button_previous = args[3]
        mid_layout = self.children[0].children[1]

        grid = self.children[0].children[0].children[0].children[0]
#        print grid.children[int(args[0])]
        inValidWidget = []

        for child in grid.children:
            if child.id == file_name:
                grid.remove_widget(child)
                for label in grid.children:
                    if label.id == "label"+ str(file_name):
                        grid.remove_widget(label)
                        mid_layout.remove_widget(button_previous)
                        mid_layout.remove_widget(label_previous)
                        self.counter_element = self.counter_element - 1
        
        
    counter_element = 0

    def unlockFile(self, *args):

        grid = self.children[0].children[0].children[0].children[0]
        complete_file_name = str(args[1]+'/'+ args[0])
        file_name = args[0]
        mid_layout = self.children[0].children[1]

        if  self.first_time_add_button == 1:
            self.first_time_add_button = 0
            label = Label(text = complete_file_name, size_hint = (0.5,1))
            button = Button(text = 'remove', size_hint = (0.5,1))
            button.bind(on_press = partial(self.removeFile, grid, file_name,label, button)) 
            mid_layout.add_widget(label)
            mid_layout.add_widget(button)
            self.counter_element = self.counter_element + 1
            print 'A',self.counter_element
        else:
            if self.counter_element > 0:
                previous_label = mid_layout.children[0]
                previous_button = mid_layout.children[1]

                mid_layout.remove_widget(previous_label)
                mid_layout.remove_widget(previous_button)
            else: 
                label = Label(text = complete_file_name, size_hint = (0.5,1))
                button = Button(text = 'remove', size_hint = (0.5,1))
                button.bind(on_press = partial(self.removeFile, grid, file_name, label, button)) 
                
                mid_layout.add_widget(label)
                mid_layout.add_widget(button)
                self.counter_element = self.counter_element + 1
                print 'B',self.counter_element

    def show_load(self, *args):
        self._popup.open()


# Screen Manager
screenManager = ScreenManager( transition = FadeTransition() )

# Add all screens to screen manager

screenManager.add_widget( UsernameScreen( name = 'usernameScreen' ) )
screenManager.add_widget( PasswordScreen( name = 'passwordScreen' ) )
screenManager.add_widget( LevelTwoScreen( name = 'levelTwoScreen' ) )
screenManager.add_widget( LevelTwoScreen( name = 'levelThreeScreen' ) )
screenManager.add_widget( RecoveryLevelTwoScreen( name = 'recoverylevelTwoScreen' ) )
screenManager.add_widget( UsernameRecover( name = 'usernameRecoverScreen' ) )
screenManager.add_widget( PasswordRecover( name = 'passwordRecoverScreen' ) )
screenManager.add_widget( RecoveryLevelThreeScreen( name = 'recoverylevelThreeScreen' ) )
screenManager.add_widget( RecoverySecQuestion( name = 'recoverysecQuestion' ) )

screenManager.add_widget( HomeScreen( name = 'homeScreen' ) )

class ThreeLevelAuthApp(App):
	def build(self):
		return screenManager

if __name__ == '__main__':
	ThreeLevelAuthApp().run()
