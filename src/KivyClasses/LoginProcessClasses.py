from ..BackEndClasses import *
from ..libraries import *

verifyUser = Authentication()
choice = -1
userID = ""
attempt = 0
generatedOTP = 0

class UsernameScreen(Screen):
    usernameField = TextInput(hint_text = 'username')

    recoverUserNameButton = Button( text = 'forgot Username', size = (20, 10))

    nextButton  = Button(text = 'next', 
                pos_hint = {'center_x': .5, 'center_y': .5}, spacing = 25)

    statusLabel = Label(text = ' ')

    recoverPasswordButton = Button( text = 'forget password', size = (20, 10))
    moveToLevelTwoButton  = Button(text = 'next', 
                        pos_hint = {'center_x': .5, 'center_y': .5}, spacing = 25)

    attempts = 0
    timeout = 0


    def __init__(self, **kwargs):
        super(UsernameScreen, self).__init__(**kwargs)

        self.recoverUserNameButton.bind(on_release = self.recoverUsernameEvent)
        self.usernameField.bind(on_text = self.checkEmptyUserName) 
        self.nextButton.bind( on_release = self.nextEvent )

        layout = BoxLayout(orientation = 'vertical', size_hint = (0.25,0.27),
                pos_hint = {'center_x': .5, 'center_y': .5}, spacing = 15)
        layout.add_widget(self.statusLabel)

        layout.add_widget(self.usernameField)
        layout.add_widget(self.nextButton)
        layout.add_widget(self.recoverUserNameButton)

        self.add_widget(layout)
        self.usernameField.text = 'sonisanjiv'

        self.recoverPasswordButton.bind(on_release = partial(self.recoverPasswordEvent))
        self.moveToLevelTwoButton.bind(on_release = partial(self.verifyPasswordEvent))
    
    # Check if username is empty or not
    def checkEmptyUserName(self, callback):
        if self.usernameField == "":
            self.nextButton.disabled = True
        else:
            self.nextButton.disabled = False

    def nextEvent(self, callback):
        global verifyUser
        global userId
        global attempt

        userExists = verifyUser.checkIfUserExists(self.usernameField.text) 
        
        if userExists :
            userID = self.usernameField.text

            self.usernameField.password = True
            self.usernameField.text = ''
            self.usernameField.hint_text = 'Password'

            self.usernameField.text = 'Test@1234'
            
            self.statusLabel.text = ' '
            
            self.children[0].remove_widget(self.recoverUserNameButton)
            self.children[0].remove_widget(self.nextButton)

            self.children[0].add_widget(self.moveToLevelTwoButton)
            self.children[0].add_widget(self.recoverPasswordButton)

        else:
            # Unsuccessful match for Username
            popup = Popup(title='Error',
            content=Label(text='Incorrect Username'),
            size_hint=(None, None), size=(180, 100))
            popup.open()
    
    def verifyPasswordEvent(self, callback):
        global verifyUser
        global choice
        passwordMatch = verifyUser.checkUserLevel1(self.usernameField.text)

        if passwordMatch:
            self.statusLabel.text = 'Password Matched'

            choice = randint(0, 1)
            choice2 = randint(0, 7)
            App.get_running_app().root.current = 'levelTwoScreen'
            App.get_running_app().root.get_screen('levelTwoScreen').startTimerIfOtp()
        else:
            # Unsuccessful match for Password 
            popup = Popup(title='Error',
            content=Label(text='Incorrect Password'),
            size_hint=(None, None), size=(180, 100))
            popup.open()

    def recoverUsernameEvent(self, callback):
        root = App.get_running_app().root
        root.current = 'recoverScreen'
        root.get_screen('recoverScreen').updateLabel(1)

    def recoverPasswordEvent(self, callback):
        root = App.get_running_app().root
        root.current = 'recoverScreen'
        root.get_screen('recoverScreen').updateLabel(2)



class LevelTwoScreen(Screen):
    _total_seconds = 5
    _total_minutes = 0
    _minutes = _total_seconds
    _seconds = _total_minutes
    _otp_expired = 0

    _time_event = 0
    _otp_choice = 0
    correctOTP = ""

    otpOnLevelTwoFlag = 0

    headingLabel = Label( text = ' HEADING')
    securityQuestionLabel = Label ()
    otpSentLabel = Label ()
    timerLabel = Label()
    otpText = TextInput(size_hint = (0.3, 0.2),
                pos_hint = {'center_x': .5, 'center_y': .5}, spacing = 25)
    
    otpTextSecond = TextInput(size_hint = (0.3, 0.2),
                pos_hint = {'center_x': .5, 'center_y': .5}, spacing = 25)
    regenerateOtpButton = Button ( text = "Regenerate OTP", size=(120,40),size_hint=(1, None),
                pos_hint = {'center_x': .5, 'center_y': .5}, spacing = 30)

    layout = BoxLayout( orientation = 'vertical')

    
    submitButton = Button(text = 'Submit', size_hint = (0.3,0.2),
                pos_hint = {'center_x': .5, 'center_y': .5}, spacing = 25)
    
    topLayout = BoxLayout( orientation = 'vertical', size_hint = (1, 0.3))
    midLayout = BoxLayout( orientation = 'vertical', size_hint = (1, 0.3), spacing = 10)
    bottomLayout = BoxLayout( orientation = 'vertical', size_hint = (1, 0.3), spacing = 10, padding = 10)
    
    def __init__(self, **kwargs):
        super(LevelTwoScreen, self).__init__(**kwargs)

        self.topLayout.add_widget(self.headingLabel)
        self.topLayout.add_widget(self.otpSentLabel)
        
        self.midLayout.add_widget(self.securityQuestionLabel)
        self.midLayout.add_widget(self.otpText)

        self.bottomLayout.add_widget(self.timerLabel)
        
        self.layout.add_widget(self.topLayout)
        self.layout.add_widget(self.midLayout)
        self.layout.add_widget(self.bottomLayout)

        self.add_widget(self.layout)
        self.headingLabel.text = "Authentication Step 2"

        randomLevel = randint(0,1)

        # Stub
        #randomLevel = 1
        
        # OTP
        if randomLevel == 0:
            self.otpOnLevelTwoFlag = 1
            self.otpLevelOne()

        # Security Question
        else:
            self.securityQuestionLevelOne()

    def startTimerIfOtp(self):
        if self.otpOnLevelTwoFlag == 1:
            self.startTimer()

    def startTimer(self):
        self.timerLabel.text = "00:00"

        self._seconds = self._total_seconds
        self._minutes = self._total_minutes

        self._time_event = Clock.schedule_interval(partial(self.updateTimer), 1)

    def otpLevelOne(self):
        random = randint(0,1)
        # OTP on Email
        if random == 1:
            self.otpSentLabel.text = "OTP Sent to Email"
        # OTP on Mobile
        else:
            self.otpSentLabel.text = "OTP Sent to Mobile"

        self.otpText.bind(text = self.securityQuestionLevelTwo)

    def otpLevelTwo(self, callback):
        if self.otpText.text == 'iron':
            self.midLayout.remove_widget(self.submitButton)
            self.headingLabel.text = 'Authentication Step 3'

            self.securityQuestionLabel.text = ' '
            random = randint(0,1)
            # OTP on Email
            if random == 1:
                self.otpSentLabel.text = "OTP Sent to Email"
            # OTP on Mobile
            else:
                self.otpSentLabel.text = "OTP Sent to Mobile"

            self.timerLabel.text = "00:00"

            self._seconds = self._total_seconds
            self._minutes = self._total_minutes

            self.midLayout.remove_widget(self.otpText)
            self.otpText = self.otpTextSecond
            self.midLayout.add_widget(self.otpText)

            self.otpText.bind(text = self.accessGrantedAfterOtpLevelThree)

            self._time_event = Clock.schedule_interval(partial(self.updateTimer), 1)

        else:
            pass


    def securityQuestionLevelOne(self):
        self.securityQuestionLabel.text = "Who is you favourite super hero ? (answer is iron :) )"

        # Stub
        self.otpText.text='iron'

        self.submitButton.bind( on_press = self.otpLevelTwo )
        self.midLayout.add_widget(self.submitButton)
        pass

    def securityQuestionLevelTwo(self, instance, value):
        if value == '123456':
            Clock.unschedule(self._time_event)
            self.timerLabel.text = ' '
            self.otpSentLabel.text = ' '

            self.midLayout.remove_widget(self.otpText)
            self.otpText = self.otpTextSecond
            self.midLayout.add_widget(self.otpText)
            
            self.securityQuestionLabel.text = "Who is you favourite super hero ? (answer is iron :) )"

            self.submitButton.bind( on_press = self.accessGrantedAfterSecurityQuestionLevelThree )
            self.midLayout.add_widget(self.submitButton)

    def accessGrantedAfterOtpLevelThree(self, callback, value):
        if value == '123456':
            print 'access granted'
            App.get_running_app().root.current = 'HomeScreen'

    def accessGrantedAfterSecurityQuestionLevelThree(self, callback):
        if self.otpText.text == 'iron':
            print 'access granted'
            App.get_running_app().root.current = 'HomeScreen'


    def regenerateOtp(self, callback):
        self.startTimer()
        self.bottomLayout.remove_widget(self.regenerateOtpButton)
        self.otpText.disabled = False

    # Update Timer after One Second
    def updateTimer(self, dt):
        if self._minutes >= 0 and self._seconds > 0:
            self._seconds = self._seconds - 1
            if self._minutes > 0 and self._seconds == 0:
                self._seconds = 60
                self._minutes = self._minutes - 1

            elif self._minutes == 0 and self._seconds == 0:
                Clock.unschedule(self._time_event)
                self.timerLabel.text = ''
                self.bottomLayout.add_widget(self.regenerateOtpButton)
                self.regenerateOtpButton.bind(on_press = self.regenerateOtp)
                self.otpText.disabled = True
                return

                # Resend OTP after Timeout
            clockState = ""

            if self._minutes > 9:
                clockState = str(self._minutes) + ':'
            else:
                clockState = '0' + str(self._minutes) + ':'

            if self._seconds > 9:
                clockState =  clockState + str(self._seconds)
            else:
                clockState = clockState + '0' + str(self._seconds)

            self.timerLabel.text = clockState
        
class RecoverScreen(Screen):

    layout = BoxLayout(orientation = 'vertical', size_hint = (0.25,0.20),
                pos_hint = {'center_x': .5, 'center_y': .5}, spacing = 15)

    recoverLabel = Label( text = 'Recover by Email or phone')

    recoverMedium = TextInput(hint_text = 'email or Mobile No.')
    submitButton = Button( text = 'submit' )
    usernameOrPasswordFlag = 0
    mobileOrEmailFlag = 0

    def __init__(self, **kwargs):
        super(RecoverScreen, self).__init__(**kwargs)    
        self.layout.add_widget(self.recoverLabel)
        self.layout.add_widget(self.recoverMedium)
        self.layout.add_widget(self.submitButton)
        self.add_widget(self.layout)


    def recoverUsernameByEmail(self, callback):
        pass

    def recoverUsernameByMobile(self, callback):
        pass
    def recoverPasswordByEmail(self, callback):
        pass
    def recoverPasswordByMobile(self, callback):
        pass

    def recoverStepTwoEvent(self, callback):
        global generatedOTP
        my_queue = Queue.Queue()
        recoverUser = UserRecovery()
        contact = self.recoverMedium

        x = 0
        if re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", contact.text):
            print "Email"
            thread1 = Thread(target = recoverUser.recoverUserLevel1, args = (2,contact.text,my_queue,))
            thread1.start()
            App.get_running_app().root.current = 'recoverylevelTwoScreen'
            App.get_running_app().root.get_screen('recoverylevelTwoScreen').parameter(self.pathValue)
            x = 1

        else:
            print "Phone"
            thread1 = Thread(target = recoverUser.recoverUserLevel1, args = (1,contact.text,my_queue,))
            thread1.start()
            App.get_running_app().root.current = 'recoverylevelTwoScreen'
            App.get_running_app().root.get_screen('recoverylevelTwoScreen').parameter(self.pathValue)
            x = 2
        generatedOTP = my_queue.get()


    def updateLabel(self, choice):
        if choice == 1:
            self.choice = 1
            self.recoverLabel.text = 'Recover Username by email or phone number'
            self.submitButton.bind(on_press = self.recoverStepTwoEvent)

        else:
            self.choice = 0
            self.recoverLabel.text = 'Recover Password by email or phone number'    
            self.submitButton.bind(on_press = self.recoverStepTwoEvent)

class LevelTwoScreen2(Screen):

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

    def updateLabel(self, choice2):

        _instruction = self.ids['instruction']
        if choice2 == 0:
            _instruction.text = "Please Enter the OTP sent to your registered Email"
        elif choice2 == 1:
            _instruction.text = "Please Enter the OTP sent to your registered Mobile"
        elif choice2 == 2:
            _instruction.text = "Enter the OTP sent on your registered mobile followed by First Three Letters of your first Name"
        elif choice2 == 3:
            _instruction.text = "Enter the OTP sent on your registered mobile followed by First Three Letters of your first Name"
        elif choice2 == 4:
            _instruction.text = "Enter the OTP sent on your registered email followed by First Three Letters of your last Name"
        elif choice2 == 5:
            _instruction.text = "Enter the OTP sent on your registered email followed by First Three Letters of your last Name"
        elif choice2 == 6:
            _instruction.text = verifyUser.fetchUserSecurityQuestion(1)
        elif choice2 == 7:
            _instruction.text = verifyUser.fetchUserSecurityQuestion(2)



    def updateButtonLabel(self, choice):
        if choice == 1:
            self.ids.send.text = "Send OTP to Email"
        else:
            self.ids.send.text = "Send OTP to Mobile"

    def updateScreen(self, choice, choice2):
        self.updateButtonLabel(choice)
        self.updateLabel(choice2)

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
                App.get_running_app().root.current = 'levelThreeScreen'
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

    # def updateButtonLabel(self):
    #     global choice
    #     if choice == 1:
    #         self.ids.send.text = "Send OTP to Email"
    #     else:
    #         self.ids.send.text = "Send OTP to Mobile"

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

class LevelThreeScreen(Screen):

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

    elementCounter = 0
    first_time_add_button = 1

    def __init__(self, **kwargs):
        super(HomeScreen, self).__init__(**kwargs)

        layout = BoxLayout(orientation = 'vertical')

        topLayout = BoxLayout(orientation = 'horizontal', size_hint = (1, 0.05), height = 10)

        lockFileButton = Button(text = "Lock Files", id = 'lock_button')
	lockFileButton.bind(on_press = self.showLoadPopup)

        topLayout.add_widget(lockFileButton)
        midLayout = BoxLayout(orientation = 'horizontal', size_hint = (1,0.1))
        bottomLayout = BoxLayout(size_hint = (1, 0.9), padding = 20)

        grid = GridLayout(id = 'unlocked_files', cols = 6, padding = 5, spacing = 20,
                size_hint = (None, None), width = 650,  pos_hint = {'center_x': .5, 'center_y': .5})

        grid.bind(minimum_height=grid.setter('height'))


        # add button into that gridi from database
        '''
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

	bottomLayout.add_widget(scroll)

	layout.add_widget(topLayout)
	layout.add_widget(midLayout)
	layout.add_widget(bottomLayout)

        self.add_widget(layout)

        popupContent = BoxLayout(size = self.size, pos = self.pos, orientation = 'vertical')
        fileView = FileChooserListView(id = 'filechooser')

        popupManagerButtons = BoxLayout(size_hint_y = None, height = 20)

        cancelButton = Button(text = 'cancel')
        cancelButton.bind(on_press = self.cancel)

        loadButton = Button(text = 'load')
        loadButton.bind(on_press = partial(self.load,fileView))

        popupManagerButtons.add_widget(cancelButton)
        popupManagerButtons.add_widget(loadButton)

        popupContent.add_widget(fileView)
        popupContent.add_widget(popupManagerButtons)

        self._popup = Popup(title = "Select Files to lock", content = popupContent,
                            size_hint = (0.9, 0.9))

    def cancel(self, *args):
        self._popup.dismiss()

    def load(self, *args):
        #print args[0].path, args[0].selection[0]
        filePath = str(args[0].path).split('/')
        completeFilePath = str(args[0].selection[0]).split('/')

        for name in filePath:
            try:
                completeFilePath.remove(name)
            except ValueError:
                pass

        self.lockFile(args[0].path, completeFilePath[0])
        self.cancel()


    def lockFile(self, *args):
        buttonId = str(args[1])
        fileButton = Button(text=' ', size=(40, 40),
                         size_hint=(None, None), id = buttonId)

        fileButton.bind(on_press = partial(self.unlockFile, buttonId, args[0]))
        fileLabel = Label(text = buttonId  , width = 70, halign = 'left',valign = 'middle', id="label"+buttonId, font_size='15sp')
        fileLabel.bind(size=fileLabel.setter('text_size'))
        midLayout = self.children[0].children[1]

        if len(midLayout.children) > 0: 
            child_first = midLayout.children[0]
            child_second = midLayout.children[1]

            midLayout.remove_widget(child_first)
            midLayout.remove_widget(child_second)

            self.elementCounter = self.elementCounter - 1

        grid = self.children[0].children[0].children[0].children[0]
        grid.add_widget(fileButton)
        grid.add_widget(fileLabel)


    def removeFile(self, *args):
        grid = args[0]
        file_name = args[1]
        label_previous = args[2]
        button_previous = args[3]
        midLayout = self.children[0].children[1]

        grid = self.children[0].children[0].children[0].children[0]
#        print grid.children[int(args[0])]
        inValidWidget = []
        deleted = 1
        for child in grid.children:
            if child.id == file_name:
                for label in grid.children:
                    if label.id == "label"+ str(file_name) and deleted == 1:
                        deleted = 0
                        grid.remove_widget(child)
                        grid.remove_widget(label)
                        midLayout.remove_widget(button_previous)
                        midLayout.remove_widget(label_previous)

    def unlockFile(self, *args):

        grid = self.children[0].children[0].children[0].children[0]
        complete_file_name = str(args[1]+'/'+ args[0])
        file_name = args[0]
        midLayout = self.children[0].children[1]

        label = Label(text = complete_file_name, size_hint = (0.9,0.5))
        button = Button(text = 'remove', size_hint = (0.1,0.5))
        button.bind(on_press = partial(self.removeFile, grid, file_name,label, button))

        if  self.first_time_add_button == 1:
            self.first_time_add_button = 0

            midLayout.add_widget(label)
            midLayout.add_widget(button)
        else:
            if len(midLayout.children) > 0 :
                previous_label = midLayout.children[0]
                previous_button = midLayout.children[1]

                midLayout.remove_widget(previous_label)
                midLayout.remove_widget(previous_button)

                midLayout.add_widget(label)
                midLayout.add_widget(button)
            else:
                midLayout.add_widget(label)
                midLayout.add_widget(button)

    def showLoadPopup(self, *args):
        self._popup.open()


