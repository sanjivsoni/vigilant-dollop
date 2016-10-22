from ..BackEndClasses import *
from ..libraries import *
from ..helperFunctions import *

verifyUser = Authentication()
recoverUser = UserRecovery()
loginMsgs = 0
sendOTP = 0
choice = -1
attempt = 0
generatedOTP = 0

class SudoPasswordScreen(Screen):
    
    def __init__(self, **kwargs):

        super(SudoPasswordScreen, self).__init__(**kwargs)
        # Initialize Screen Elements
        self.layout = BoxLayout(orientation = 'vertical', pos_hint = {'center_y': .5, 'center_x': .5}, spacing = 25, size_hint = (0.25, 0.25))
        self.sudoPassword = TextInput(hint_text = 'sudo password', password = True, multiline = False)
        self.submitButton = Button(text = 'Submit')
        self.label = Label(text = 'Please Enter your sudo password.')

        # Add elements to screen
        self.submitButton.bind(on_press = self.checkSudoPassword)
        self.layout.add_widget(self.label)
        self.layout.add_widget(self.sudoPassword)
        self.layout.add_widget(self.submitButton)
        self.add_widget(self.layout)

    def checkSudoPassword(self, callback):
        # If valid Password then move to sign up form
        if checkSudoPwd(self.sudoPassword.text) == 1:
            App.get_running_app().root.current = 'signupScreen'

class UsernameScreen(Screen):

    def __init__(self, **kwargs):
        super(UsernameScreen, self).__init__(**kwargs)

        self.layout = BoxLayout(orientation = 'vertical', size_hint = (0.25,0.40), pos_hint = {'center_x': .5, 'center_y': .5}, spacing = 15)

        self.usernameField = TextInput(hint_text = 'username', multiline = False)
        self.nextButton  = Button(text = 'next', pos_hint = {'center_x': .5, 'center_y': .5}, spacing = 25)
        self.recoverUserNameButton = Button( text = 'forgot Username', size = (20, 10))
        self.statusLabel = Label(text = ' ')

        self.captcha = Image(source = 'src/images/captcha.jpg', allow_strech = True, size = (100,100))
        self.captchaTextInput = TextInput( multiline = False)
        self.captchaTextInput.pos_hint = {'center_x': .5, 'center_y': .5}
        self.captchaLayout = BoxLayout(orientation = 'horizontal', size_hint=(1,1))
        self.regenerateCaptchaButton = Button(size = (32,32), size_hint = (None, None))

        self.recoverPasswordButton = Button( text = 'forget password', size = (20, 10))
        self.moveToLevelTwoButton  = Button(text = 'next',
                            pos_hint = {'center_x': .5, 'center_y': .5}, spacing = 25)
        
        self.attempts = 0
        self.timeout = 0
        self.passwordAttempts = 0

        self.captchaCorrectText = ''
        self.captchaCorrectText = createCaptcha()
        self.captcha = Image(source = 'src/images/captcha.jpg')

        self.recoverUserNameButton.bind(on_release = self.recoverUsernameEvent)
        self.usernameField.bind(on_text = self.checkEmptyUserName)
        self.nextButton.bind( on_release = self.enterPassword )

        self.layout.add_widget(self.statusLabel)
        self.layout.add_widget(self.usernameField)

        self.regenerateCaptchaButton.background_normal = 'src/images/reset.png'
        self.regenerateCaptchaButton.pos_hint = {'center_x': .5, 'center_y': .5}
        self.regenerateCaptchaButton.bind( on_press = self.regenerateCaptcha )

        self.captchaLayout.add_widget(self.captcha)
        self.captchaLayout.add_widget(self.regenerateCaptchaButton)

        self.layout.add_widget(self.captchaLayout)
        self.layout.add_widget(self.captchaTextInput)

        self.nextButton.spacing = 50

        self.layout.add_widget(self.nextButton)
        self.layout.add_widget(self.recoverUserNameButton)

        self.add_widget(self.layout)
        self.usernameField.text = 'bhatshubhs'

        self.recoverPasswordButton.bind(on_release = partial(self.recoverPasswordEvent))
        self.moveToLevelTwoButton.bind(on_release = partial(self.verifyPasswordEvent))

    def regenerateCaptcha(self, callback):
        self.layout.children[3].remove_widget(self.captcha)
        self.captcha = Image(source = 'src/images/captcha.jpg')
        self.layout.children[3].add_widget(self.captcha)
        self.captchaCorrectText = createCaptcha()
        self.captchaTextInput.text = ''

    # Check if username is empty or not
    def checkEmptyUserName(self, callback):
        if self.usernameField == "":
            self.nextButton.disabled = True
        else:
            self.nextButton.disabled = False

    def enterPassword(self, callback):
        global verifyUser
        global userId
        global attempt
        global sendOTP
        global loginMsgs

        userExists = verifyUser.checkIfUserExists(self.usernameField.text)

        if self.captchaTextInput.text == self.captchaCorrectText:
            if userExists :
                sendOTP = OTP(verifyUser.returnUserID())
                loginMsgs = LoginMessages(verifyUser.returnUserID())
                self.usernameField.password = True
                self.usernameField.text = ''
                self.usernameField.hint_text = 'Password'

                self.usernameField.text = 'Qwe@1234'

                self.statusLabel.text = ' '
                self.layout.remove_widget(self.captchaLayout)
                self.layout.remove_widget(self.captchaTextInput)

                self.layout.size_hint = (0.25,0.27)

                self.children[0].remove_widget(self.recoverUserNameButton)
                self.children[0].remove_widget(self.nextButton)

                self.children[0].add_widget(self.moveToLevelTwoButton)
                self.children[0].add_widget(self.recoverPasswordButton)
            else:
                popup = Popup(title='Error',
                content=Label(text='Incorrect Username'),
                size_hint=(None, None), size=(180, 100))
                popup.open()

        else:
            # Unsuccessful match for Username
            popup = Popup(title='Error',
            content=Label(text='Incorrect Captcha Text'),
            size_hint=(None, None), size=(180, 100))
            popup.open()

    def verifyPasswordEvent(self, callback):
        global verifyUser
        passwordMatch = verifyUser.checkUserLevel1(self.usernameField.text)

        if passwordMatch:
            self.statusLabel.text = 'Password Matched'

            App.get_running_app().root.current = 'levelTwoScreen'
            App.get_running_app().root.get_screen('levelTwoScreen').startTimerIfOtp()
        else:
            # Unsuccessful match for Password
            print self.passwordAttempts
            self.passwordAttempts = self.passwordAttempts + 1
            popup = Popup(title='Error',
            content=Label(text='Incorrect Password'),
            size_hint=(None, None), size=(180, 100))
            popup.open()
            if(self.passwordAttempts > 3):
                loginMsgs.failedLogin()



    def recoverUsernameEvent(self, callback):
        root = App.get_running_app().root
        root.current = 'recoverScreen'
        root.get_screen('recoverScreen').updateLabel(1)
        root.get_screen('recoverScreen').usernameOrPasswordFlag = 1

    def recoverPasswordEvent(self, callback):
        root = App.get_running_app().root
        root.current = 'recoverScreen'
        root.get_screen('recoverScreen').updateLabel(2)
        root.get_screen('recoverScreen').usernameOrPasswordFlag = 0

class LevelTwoScreen(Screen):
    _total_seconds = 60
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
                pos_hint = {'center_x': .5, 'center_y': .5}, spacing = 25, multiline = False)

    otpTextSecond = TextInput(size_hint = (0.3, 0.2),
                pos_hint = {'center_x': .5, 'center_y': .5}, spacing = 25, multiline = False)
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
        randomLevel =1
        # OTP
        if randomLevel == 0:
            self.otpOnLevelTwoFlag = 1
            self.otpLevelOne()

        # Security Question
        else:
            self.securityQuestionLevelOne()

    def startTimerIfOtp(self):
        global choice
        choice = randint(0,1)
        print choice
        if self.otpOnLevelTwoFlag == 1:
            self.startTimer()
            self.otpSentLabel.text = self.returnOTPEvent()

        else:
            self.securityQuestionLabel.text = verifyUser.fetchUserSecurityQuestion(choice)


    def startTimer(self):
        self.timerLabel.text = "00:00"

        self._seconds = self._total_seconds
        self._minutes = self._total_minutes

        self._time_event = Clock.schedule_interval(partial(self.updateTimer), 1)

    def returnOTPEvent(self):
        otpQueue = Queue.Queue()
        global sendOTP
        global generatedOTP
        msg = ""
        choice = randint(0, 5)
        #choice  = 0
        if choice == 0:
            msg = "Please Enter the OTP sent to your registered Email"
            sendOTP.sendOTPforAuth_email(6,otpQueue)
            generatedOTP = otpQueue.get()


        elif choice == 1:
            msg = "Please Enter the OTP sent to your registered Mobile"
            sendOTP.sendOTPforAuth_mobile(6,otpQueue)
            generatedOTP = otpQueue.get()

        elif choice == 2:
            msg = "Enter the OTP sent on your registered mobile followed by birth year"
            sendOTP.sendOTPforAuth_mobile(2,otpQueue)
            generatedOTP = otpQueue.get() + verifyUser.fetchDOBforAuth(1)

        elif choice == 3:
            msg = "Enter the OTP sent on your registered mobile followed by birth year"
            sendOTP.sendOTPforAuth_mobile(2,otpQueue)
            generatedOTP = otpQueue.get() + verifyUser.fetchDOBforAuth(1)

        elif choice == 4:
            msg = "Enter the OTP sent on your registered email followed by birth date"
            sendOTP.sendOTPforAuth_email(4,otpQueue)
            generatedOTP = otpQueue.get() + verifyUser.fetchDOBforAuth(2)

        elif choice == 5:
            msg = "Enter the OTP sent on your registered email followed by birth date"
            sendOTP.sendOTPforAuth_email(4,otpQueue)
            generatedOTP = otpQueue.get() + verifyUser.fetchDOBforAuth(2)


        print generatedOTP

        return msg

    def otpLevelOne(self):
        self.otpText.bind(text = self.securityQuestionLevelTwo)

    def otpLevelTwo(self, callback):
        global choice

        if self.otpText.text == verifyUser.checkSecurityQuesAnswer(choice):
            self.midLayout.remove_widget(self.submitButton)
            self.headingLabel.text = 'Authentication Step 3'

            self.securityQuestionLabel.text = ' '

            self.otpSentLabel.text = self.returnOTPEvent()

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
        global verifyUser
        self.submitButton.bind( on_press = partial(self.otpLevelTwo))
        self.midLayout.add_widget(self.submitButton)
        pass

    def securityQuestionLevelTwo(self, instance, value):
        global verifyUser
        choice = randint(0,1)
        global generatedOTP
        if value == generatedOTP:
            Clock.unschedule(self._time_event)
            self.timerLabel.text = ' '
            self.otpSentLabel.text = ' '

            self.midLayout.remove_widget(self.otpText)
            self.otpText = self.otpTextSecond
            self.midLayout.add_widget(self.otpText)

            self.securityQuestionLabel.text = verifyUser.fetchUserSecurityQuestion(choice)

            self.submitButton.bind( on_press = partial(self.accessGrantedAfterSecurityQuestionLevelThree,choice) )
            self.midLayout.add_widget(self.submitButton)

    def sendLoginMessages(self,dt):
        global loginMsgs
        t1 = Thread(target=loginMsgs.loggedIn())
        t1.start()

    def accessGrantedAfterOtpLevelThree(self, callback, value):
        global generatedOTP
        global sendOTP
        global loginMsgs
        my_queue = Queue.Queue()
        if value == generatedOTP:
            print 'access granted'
            root = App.get_running_app().root
            root.current = 'HomeScreen'
            root.get_screen('HomeScreen').addFilesOnLogin()
            t1 = Thread(target=loginMsgs.loggedIn())
            t1.start()


    def accessGrantedAfterSecurityQuestionLevelThree(self, callback):
        global choice
        global loginMsgs
        if self.otpText.text == verifyUser.checkSecurityQuesAnswer(choice):
            print 'access granted'
            root = App.get_running_app().root
            root.current = 'HomeScreen'
            root.get_screen('HomeScreen').addFilesOnLogin()
            t1 = Thread(target=loginMsgs.loggedIn())
            t1.start()


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

    layout = BoxLayout(orientation = 'vertical', size_hint = (0.40,0.20),
                pos_hint = {'center_x': .5, 'center_y': .5}, spacing = 15)

    recoverLabel = Label( text = 'Recover by Email or phone')

    textInput = TextInput(hint_text = 'email or Mobile No.',multiline = False)
    submitButton = Button( text = 'Submit' )
    usernameOrPasswordFlag = 0
    mobileOrEmailFlag = 0

    def __init__(self, **kwargs):
        super(RecoverScreen, self).__init__(**kwargs)
        self.layout.add_widget(self.recoverLabel)
        self.layout.add_widget(self.textInput)
        self.layout.add_widget(self.submitButton)
        self.add_widget(self.layout)
        # Stub
        self.textInput.text = '+919810158269'


    def recoverByEmail(self, contact, my_queue):
        global recoverUser
        thread1 = Thread(target = recoverUser.recoverUserLevel1, args = (2,contact.text,my_queue,))
        thread1.start()

    def recoverByMobile(self, contact, my_queue):
        global recoverUser
        thread1 = Thread(target = recoverUser.recoverUserLevel1, args = (1,contact.text,my_queue,))
        thread1.start()

    def recoverStepTwoEvent(self, callback):
        global generatedOTP
        my_queue = Queue.Queue()
        contact = self.textInput

        if re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", contact.text):
            self.recoverByEmail(contact,my_queue)
        else:
            self.recoverByMobile(contact,my_queue)


        generatedOTP = my_queue.get()
        print generatedOTP
        if generatedOTP == -1:
            print "Recovery Id doesn't exists"
        else:
            self.enterOtp()

    def enterOtp(self):
        self.textInput.hint_text = 'Enter OTP'

        self.layout.remove_widget(self.submitButton)
        self.submitButton = Button( text = 'submit')
        self.layout.add_widget(self.submitButton)

        self.submitButton.bind( on_press = self.recoverStepTwoSsn )
        self.textInput.text = ''
        self.recoverLabel.text = 'Enter OTP'

    def recoverStepTwoSsn(self, callback):
        global generatedOTP
        global recoverUser
        if generatedOTP  == self.textInput.text:
            self.recoverLabel.text = recoverUser.fetchSSNType()
            self.textInput.hint_text = 'SSN Number'

            self.layout.remove_widget(self.submitButton)
            self.submitButton = Button( text = 'submit')
            self.layout.add_widget(self.submitButton)

            self.submitButton.bind( on_press = self.checkSSN )
            self.textInput.text = ''

    def checkSSN(self, callback):
        # Check valid SSN
        global choice
        choice = randint(0,1)
        global recoverUser
        if recoverUser.recoverUserLeveL2(self.textInput.text):
            self.recoverLabel.text = recoverUser.fetchUserSecurityQuestion(choice)
            self.textInput.hint_text = 'Answer'

            self.layout.remove_widget(self.submitButton)
            self.submitButton = Button( text = 'submit')
            self.layout.add_widget(self.submitButton)

            self.submitButton.bind( on_press = self.checkSecurityQuesAnswer )
            self.textInput.text = ''

    def checkSecurityQuesAnswer(self, callback):
        global choice
        global recoverUser
        if self.textInput.text == recoverUser.recoverUserLeveL3(choice):
            if self.usernameOrPasswordFlag == 1:
                self.recoverUserName()
            else:
                self.recoverPassword()

    def recoverUserName(self):
        print 'Recover USer NAme'
        self.textInput.text  = ''
        self.textInput.hint_text = 'USername'
        self.recoverLabel.text = "Enter Your new Username"

        self.layout.remove_widget(self.submitButton)
        self.submitButton = Button( text = 'submit')
        self.layout.add_widget(self.submitButton)
        self.submitButton.bind( on_press = self.updateUserName )

    def updateUserName(self, callback):
        global recoverUser
        recoverUser.updateUserID(self.textInput.text)

    def recoverPassword(self):
        print 'Recover PAsssword)'
        self.layout.size_hint = (0.4,0.25)
        self.textInput.text  = ''
        self.textInput.hint_text = 'Password'
        self.textInput.password = True
        self.recoverLabel.text = "Enter Your new Password"

        self.layout.remove_widget(self.submitButton)

        confirmPasswordField =TextInput(hint_text = 'Confirm Password')
        confirmPasswordField.password = True

        self.layout.add_widget(confirmPasswordField)
        self.submitButton = Button( text = 'submit')
        self.layout.add_widget(self.submitButton)
        self.submitButton.bind( on_press = self.updatePassword )

    def updatePassword(self, callback):
        global recoverUser
        recoverUser.updateUserPassword(self.textInput.text)

    def updateLabel(self, choice):
        if choice == 1:
            self.choice = 1
            self.recoverLabel.text = 'Recover Username by email or phone number'
            self.submitButton.bind(on_press = self.recoverStepTwoEvent)

        else:
            self.choice = 0
            self.recoverLabel.text = 'Recover Password by email or phone number'
            self.submitButton.bind(on_press = self.recoverStepTwoEvent)

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


    def addFilesOnLogin(self):
        grid = self.children[0].children[0].children[0].children[0]
        results = verifyUser.fetchLockedFiles()
        for i in results:
            fileName = aesDecrypt(i[1])
            filePath = aesDecrypt(i[0])
            fileButton = Button(text=' ', size=(40, 40),
                             size_hint=(None, None), id = str(fileName))

            fileButton.bind(on_press = partial(self.unlockFile, fileName, filePath))
            fileLabel = Label(text = str(fileName), width = 70, halign = 'left',valign = 'middle', id="label"+str(fileName), font_size='15sp')
            fileLabel.bind(size=fileLabel.setter('text_size'))

            grid.add_widget(fileButton)
            grid.add_widget(fileLabel)


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

        self.cancel()
        status = verifyUser.lockItem(args[0].path, completeFilePath[0])
        if status:
            self.lockFile(args[0].path, completeFilePath[0])
        else:
            popup = Popup(title='Error',
            content=Label(text='File already secured'),
            size_hint=(None, None), size=(180, 100))
            popup.open()



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

    def unlockFile(self, fileName, filePath, callback):

        grid = self.children[0].children[0].children[0].children[0]
        complete_file_name = str(filePath + '/' + fileName)
        file_name = fileName
        midLayout = self.children[0].children[1]

        label = Label(text = complete_file_name, size_hint = (0.9,0.5))
        button = Button(text = 'remove', size_hint = (0.1,0.5))
        button.bind(on_press = partial(self.removeFile, grid, file_name,label, button))
        verifyUser.unlockItem(filePath, fileName)
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
