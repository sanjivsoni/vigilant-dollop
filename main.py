from helperFunctions import*

#for classes
from UserClass import*
from LoginDetailsClass import*
from AuthenticationClass import*
from UserCredentialsRecoveryClass import *

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
from kivy.core.image import Image as CoreImage
import datetime

# Load Kivy file
Builder.load_file("authentication.kv")

Window.size = (700, 700)
verifyUser = Authentication()
choice = -1
userID = ""
attempt = 0
generatedOTP = 0
# Classes for seperate screens
class SignupScreen(Screen):
    flag = 0
    flag1 =0
    flag2 = 0
    flag3 = 0
    flag4 = 0
    flag5 = 0
    flag6 = 0
    flag7 = 0
    flag8 = 0
    flag9 = 0
    flag10 = 0
    flag11 = 0
    flag12 = 0


    def val_change(self):
        label = ['bar','1','2','3','4','5','6','7','8','9','10','11','12','13', '14']
        label_b = self.ids['bar']
        label[1] = self.ids['1']
        label[2] = self.ids['2']
        label[3] = self.ids['3']
        label[4] = self.ids['4']
        label[5] = self.ids['5']
        label[6] = self.ids['6']
        label[7] = self.ids['7']
        label[8] = self.ids['8']
        label[10] = self.ids['10']
        label[11] = self.ids['11']
        label[12] = self.ids['12']
        label[13] = self.ids['13']
        label[14] = self.ids['14']
        set_val = 0

        if not(label[1].text == ''):
            set_val+=100
        if not(label[2].text == ''):
            set_val+=100
        if not(label[3].text == ''):
            set_val+=100
        if not(label[4].text == ''):
             set_val+=100
        if not(label[5].text == ''):
             set_val+=100
        if not(label[6].text == ''):
             set_val+=100
        if not(label[7].text == ''):
             set_val+=100
        if not(label[8].text == ''):
             set_val+=100
        if not(label[11].text == ''):
             set_val+=100
        if not(label[12].text == ''):
             set_val+=100
        if not(label[13].text == ''):
             set_val+=100
        label_b.value =  set_val

    def valiDate(self):
        dob = self.ids['6']
        L7 = self.ids['L6']
        now = datetime.datetime.now()
        flag = 0
        self.flag3=0
        if dob.text == "":
            L7.color = [1,1,1,1]
            flag +=1
        if re.match(r"(\b\d{2}[/]\d{2}[/]\d{4}\b)", dob.text):
            X = dob.text.split('/')
            if int(X[1])>0 and int(X[0])>0:
                if int(X[2]) <now.year and int(X[2]) >=1900:
                    L7.color = [0,1,0,1]
                    flag +=1
                    self.flag3+=1
                if int(X[2]) == now.year and int(X[1]) < now.month:
                    L7.color = [0,1,0,1]
                    flag +=1
                    self.flag3+=1
                if int(X[2]) == now.year and int(X[1]) == now.month and int(X[0]) <=now.day:
                    L7.color = [0,1,0,1]
                    flag +=1
                    self.flag3+=1
        if not(flag):
            L7.color = [1,0,0,1]

    def mail_valid(self):
        mail_e = self.ids['4']
        L7 = self.ids['L4']
        self.flag11 = 0
        if re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", mail_e.text):
            L7.color = [0,1,0,1]
            self.flag11+=1
        elif mail_e.text == "":
            L7.color = [1,1,1,1]
        else:
            L7.color = [1,0,0,1]
    def conf_valid(self):
        self.flag1 = 0
        pass_w = self.ids['2']
        pass_c = self.ids['3']
        L7 = self.ids['L3']
        _valid = self.ids['MSG2']
        if pass_w.text != pass_c.text or pass_w.text=="" :
             if pass_c.text == "":
                L7.color = [1,1,1,1]
                _suggest = ""
             else:
                L7.color = [1,0,0,1]
                _suggest = "Password Doesn't Match"
        else:
            L7.color = [0,1,0,1]
            _suggest = " "
            self.flag1+=1
        _valid.text = _suggest

    def pass_valid(self):
        pass_w = self.ids['2']
        L7 = self.ids['L2']
        uCase = 0
        lCase = 0
        num = 0
        splChar = 0
        lent = 0
        flag = 0
        self.flag10 = 0
        VAL = pass_w.text
        _suggest = "\n"
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
            _suggest = _suggest + "Must Have One Upper Case Char.\n"
            flag +=1
        else :
            _suggest = _suggest + ""
        if not(lCase):
            _suggest = _suggest + "Must Have One Lower Case Char.\n"
            flag +=1
        if not(num):
            _suggest = _suggest + "Must Have One Digit.\n"
            flag += 1
        if not(splChar):
            _suggest = _suggest + "Must Have One Special Char.\n"
            flag += 1
        if not(lent):
            _suggest = _suggest + "Must Be Between 8 and 16 characters long.\n"
            flag += 1
        if(not(len(VAL))):
            flag +=1
            _suggest =  "\n"

        if(flag):
            if pass_w.text == "":
                L7.color = [1,1,1,1]
            else:
                L7.color = [1,0,0,1]
        else:
            L7.color = [0,1,0,1]
            self.flag10 += 1
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
    def name_work(self):
         L7 = self.ids['L7']
         name = self.ids['7']
         self.val_change()
         self.flag4 = 0
         if(not(name.text.isalpha())):
            if name.text == "":
                L7.color = [1,1,1,1]
            else:
                L7.color = [1,0,0,1]
         else:
            L7.color = [0,1,0,1]
            self.flag4 += 1
    def Lname_work(self):
         L7 = self.ids['L8']
         name = self.ids['8']
         self.val_change()
         self.flag9 = 0
         if(not(name.text.isalpha())):
            if name.text == "":
                L7.color = [1,1,1,1]
            else:
                L7.color = [1,0,0,1]
         else:
            L7.color = [0,1,0,1]
            self.flag9 += 1
    def uid_work(self):
         L7 = self.ids['L1']
         name = self.ids['1']
         self.val_change()
         flag = 0
         self.flag8 = 0
         if len(name.text) >=8 and len(name.text) <=16:
            for i in range (0,len(name.text)):
                if name.text[i].isalnum() or name.text[i]=="_":
                    continue
                else:
                    flag+=1
                    break
         else:
             flag += 1

         if flag:
             if name.text == "":
                 L7.color = [1,1,1,1]
             else:
                 L7.color = [1,0,0,1]
         else:
             if name.text == "":
                 L7.color = [1,1,1,1]
             elif name.text[0].isdigit():
                 L7.color = [1,0,0,1]
             else:
                L7.color = [0,1,0,1]
                self.flag8 += 1

    def cont_work(self):
         L7 = self.ids['L5']
         name = self.ids['5']
         self.flag6 = 0
         self.val_change()
         if(not(name.text.isdigit()) or len(name.text)!=10):
            if name.text == "":
                L7.color = [1,1,1,1]
            else:
                L7.color = [1,0,0,1]
         else:
            if (name.text[0] == "7") or (name.text[0] == "8") or (name.text[0] == "9"):
                L7.color = [0,1,0,1]
                self.flag6 += 1
            else:
                L7.color = [1,0,0,1]
    def ssn(self):
         L7 = self.ids['11']
         name = self.ids['L11']
         self.flag5 = 0
         self.val_change()
         name.color = [1,1,1,1]
         if not(L7.text==""):
             self.flag5+=1
             name.color = [0,1,0,1]
    def ans1(self):
         L7 = self.ids['12']
         name = self.ids['L12']
         self.flag2 = 0
         self.val_change()
         name.color = [1,1,1,1]
         if not(L7.text==""):
             self.flag2+=1
             name.color = [0,1,0,1]
    def ans2(self):
         L7 = self.ids['13']
         name = self.ids['L13']
         self.flag12 = 0
         self.val_change()
         name.color = [1,1,1,1]
         if not(L7.text==""):
             self.flag12+=1
             name.color = [0,1,0,1]

    # def secQues1(self):
    #     ID = self.ids['Y']
    #     ID2 = self.ids['LY']
    #     if not(ID.text == "Security Question"):
    #         ID2.color = [0,1,0,1]
    #     else:
    #         ID2.color = [1,1,1,1]
    def buttonAction(self):
        ID = self.ids['X']
        ID2 = self.ids['Y']
        ID3 = self.ids['10']
        label = ['bar','1','2','3','4','5','6','7','8','9','10','11','12','13','14']
        label_b = self.ids['bar']
        label[1] = self.ids['1']
        label[2] = self.ids['2']
        label[3] = self.ids['3']
        label[4] = self.ids['4']
        label[5] = self.ids['5']
        label[6] = self.ids['6']
        label[7] = self.ids['7']
        label[8] = self.ids['8']
        label[10] = self.ids['10']
        label[11] = self.ids['11']
        label[12] = self.ids['12']
        label[13] = self.ids['13']
        label[14] = self.ids['14']


        Q1 = 0
        Q2 = 0
        _SSN = 0
        if not(ID.text == "Security Question") and not(ID2.text == "Security Question") and not(ID3.text == "SSN Type") and not(label[14].text == "Country Code"):
            if self.flag5 and self.flag3 and self.flag11 and self.flag1 and self.flag10 and self.flag4 and self.flag9 and self.flag8 and self.flag6 and self.flag2 and self.flag12:
                if ID.text == "Your Childhood Hero?":
                    Q2 = 5
                elif ID.text == "Time Of The Day Were You Born ?":
                    Q2 = 6
                elif ID.text == "The steet you grew up in?":
                    Q2 = 7
                elif ID.text == "Your Childhood Nickname?":
                    Q2 = 8
                else:
                    Q2 = 0
                if ID2.text == "Mother's Maiden Name ?":
                    Q1 = 1
                elif ID2.text == "Pet's Name ?":
                    Q1 = 2
                elif ID2.text ==  "First Teacher's Name ?":
                    Q1 = 3
                elif ID2.text == "Favourite Holiday Destination?":
                    Q1 = 4
                else:
                    Q1 = 0
                if ID3.text ==  "Voter ID":
                    _SSN = 1
                elif ID3.text == "PAN Card":
                    _SSN = 2
                elif ID3.text ==  "Aadhaar Card":
                    _SSN = 3
                elif ID3.text == "Driver's License":
                    _SSN = 4
                else:
                    _SSN = 0
                
                
                phoneNo = label[14].text+label[5].text
                userCredentials = label[1].text + " " + label[2].text
                userContactDetails = label[4].text + " " +phoneNo +  " " +"sudoPwd"
                userPersonalDetails = label[7].text + " " +label[8].text + " " +label[6].text + " " + str(_SSN) + " " +label[11].text
                userSecurityQues = str(Q1) + " " +label[12].text + " " + str(Q2) + " " +label[13].text
                print phoneNo
                newUser = User(userCredentials)
                newUser.createUser(userContactDetails)
                newUser.addPersonalDetails(userPersonalDetails)
                newUser.addSecurityQuestions(userSecurityQues)
                App.get_running_app().root.current = 'usernameScreen'

                #print Q1
                #print Q2
                #print _SSN
        else:
            print "No"



class PasswordReset(Screen):
    def check_validity(self):
        pass_w = self.ids['pass_reset']
        L7 = self.ids['Message']
        uCase = 0
        lCase = 0
        num = 0
        splChar = 0
        lent = 0
        flag = 0
        self.flag10 = 0
        VAL = pass_w.text
        _suggest = "\n"
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
            _suggest = _suggest + "Must Have One Upper Case Char.\n"
            flag +=1
        else :
            _suggest = _suggest + ""
        if not(lCase):
            _suggest = _suggest + "Must Have One Lower Case Char.\n"
            flag +=1
        if not(num):
            _suggest = _suggest + "Must Have One Digit.\n"
            flag += 1
        if not(splChar):
            _suggest = _suggest + "Must Have One Special Char.\n"
            flag += 1
        if not(lent):
            _suggest = _suggest + "Must Be Between 8 and 16 characters long.\n"
            flag += 1
        if(not(len(VAL))):
            flag +=1
            _suggest =  "\n"
        L7.text = _suggest
    # if(flag):
    #     if pass_w.text == "":
    #         L7.color = [1,1,1,1]
    #     else:
    #         L7.color = [1,0,0,1]
    #else:
  #      L7.color = [0,1,0,1]
   #     self.flag10 += 1
        

class UsernameScreen(Screen):
    username = ObjectProperty(None)
    message = ObjectProperty(None)
    attempt = 0
    invalidTime = 0
    
    def check_username(self):
        if self.ids['username'].text ==  "":
            self.ids['loginButton'].disabled = True
        else:
            self.ids['loginButton'].disabled = False
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

    def check_password(self):
        if self.ids['password'].text ==  "":
            self.ids['passwordButton'].disabled = True
        else:
            self.ids['passwordButton'].disabled = False
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
            x = 1

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
    
    def reRender(self,dt):
        App.get_running_app().root.current = 'usernameScreen'
    def parameter(self, x):
        self.pathValue = x
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
                pass # Case where no answer or wrong answer has been entered
        else:
            pass

        if self.pathValue == 2:
            App.get_running_app().root.current = 'passwordReset'
            self.ids['recoverMessage'].text = ""
        else:
            self.ids['recoverMessage'].text = "Username Has Been Mailed To You On Your Registered Mail ID" 
            Clock.schedule_once(self.reRender, 2)
    def parameter(self,x):
        self.pathValue = x
class UserRecoveryLevelThreeScreen(Screen):

    pathValue = 0
    contactValue = 0

    def parameter(self,x,y):
        self.pathValue = x
        self.contactValue = y
    def renderSecurityQues(self):
        ssn = self.ids['ssn_Value']
        # Stub
        if ssn.text == "":#compare SSN with Database Value. SSN Value entered by user while recovery is stored in ssn.text
            App.get_running_app().root.current = 'recoverysecQuestion'
            App.get_running_app().root.get_screen('recoverysecQuestion').parameter(self.pathValue)
        else: #Case where no value or wrong value has been eneterd
            pass
        # Invalid OTP

class PasswordRecoveryLevelThreeScreen(Screen):

    pathValue = 0
    contactValue = 0

    def parameter(self,x,y):
        self.pathValue = x
        self.contactValue = y
    def renderSecurityQues(self):
        ssn = self.ids['ssn_Value']
        # Stub
        if ssn.text == "":#compare SSN with Database Value. SSN Value entered by user while recovery is stored in ssn.text
            App.get_running_app().root.current = 'recoverysecQuestion'
            App.get_running_app().root.get_screen('recoverysecQuestion').parameter(self.pathValue)
        else: #Case where no value or wrong value has been eneterd
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
                
                if self.pathValue == 1:
                    print "1"
                    App.get_running_app().root.current = 'userrecoverylevelThreeScreen'
                    App.get_running_app().root.get_screen('userrecoverylevelThreeScreen').parameter(self.pathValue,3)
                elif self.pathValue == 2:
                    print "2"
                    App.get_running_app().root.current = 'passwordrecoverylevelThreeScreen'
                    App.get_running_app().root.get_screen('passwordrecoverylevelThreeScreen').parameter(self.pathValue,3)

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

    def updateLabel(self, choice2):
        _instruction = self.ids['instruction'] 
        if choice2 == 0:
            _instruction.text = "OTP to Email"
        elif choice2 == 1:
            _instruction.text = "OTP to Mobile"
        elif choice2 == 2:
            _instruction.text = "OTP + First Name"
        elif choice2 == 3:
            _instruction.text = "OTP + Last Name"
        elif choice2 == 4:
            _instruction.text = "OTP + Random Number"
        elif choice2 == 5:
            _instruction.text = "Security Question 1"
        else:
            _instruction.text = "Security Question 2"

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

    counter = 0
    second_counter = 0


    def __init__(self, **kwargs):
        super(HomeScreen, self).__init__(**kwargs)

        layout = BoxLayout(orientation = 'vertical')
        top_layout = BoxLayout(orientation= 'horizontal', size_hint=(1, 0.1), height = 10 )

        button = Button(text="Lock Files", id='lock_button')
	button.bind(on_press = self.show_load)
        #button.bind(on_press = partial(self.lockFile, 'file' ))

        button_unlock = Button(text="Unlock File", id='unlock_button')
        #button_unlock.bind(on_press = partial(self.unlockFile, 'file1'))

        top_layout.add_widget(button)
        top_layout.add_widget(button_unlock)
        bottom_layout = BoxLayout(size_hint = (1, 0.9), padding = 20)

        grid = GridLayout(id='unlocked_files', cols=4, padding=5, spacing=5,
                size_hint=(None, None), width=600,  pos_hint={'center_x': .5, 'center_y': .5})

        grid.bind(minimum_height=grid.setter('height'))


        # add button into that grid

        for i in range(8):
            btn = Button(text = "file" + str(i), size = (30, 30),
                         size_hint = (None, None), id = str(i))
            btn.bind(on_press = partial(self.unlockFile, str(i)))
            label = Label(text = "file" + str(i), width=70, halign = 'left',valign = 'middle')
            label.bind(size=label.setter('text_size'))

            grid.add_widget(btn)
            grid.add_widget(label)

        # create a scroll view, with a size < size of the grid
        scroll = ScrollView(size_hint = (None, None), size = (600, 500),
                pos_hint = {'center_x': .5, 'center_y': .5}, do_scroll_x = False)
	scroll.add_widget(grid)
	bottom_layout.add_widget(scroll)
	layout.add_widget(top_layout)
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
        print args[0].path, args[0].selection
        self.lockFile(args[0].path,args[0].selection)
        self.cancel()


    def lockFile(self, *args):
        self.counter = self.counter + 1
#        print args[0]
#        print ("button pressed <%s> " %args[0])
        button_id = str(args[1])
        button = Button(text=button_id, size=(30, 30),
                         size_hint=(None, None), id = button_id)

        button.bind(on_press = partial(self.unlockFile, button_id))
        #button.bind(on_press = partial(self.un
        self.children[0].children[0].children[0].children[0].add_widget(button)

    def unlockFile(self, *args):

        grid = self.children[0].children[0].children[0].children[0]
#        print grid.children[int(args[0])]
        inValidWidget = []

        for child in grid.children:
            if child.id == args[0]:
                grid.remove_widget(child)


    def show_load(self, *args):

        self._popup.open()


# Screen Manager
screenManager = ScreenManager( transition = FadeTransition() )

# Add all screens to screen manager
x = 2
# Check For Comparison Here If A USer Exists Or Not 
if x== 1:  #Case Where User Does Not Exist
    screenManager.add_widget( SignupScreen( name = 'signupScreen' ) )
else:      #Case Where User Does Exists
    screenManager.add_widget( UsernameScreen( name = 'usernameScreen' ) )
screenManager.add_widget( UsernameScreen( name = 'usernameScreen' ) )
screenManager.add_widget( PasswordScreen( name = 'passwordScreen' ) )
screenManager.add_widget( LevelTwoScreen( name = 'levelTwoScreen' ) )
screenManager.add_widget( LevelThreeScreen( name = 'levelThreeScreen' ) )
screenManager.add_widget( RecoveryLevelTwoScreen( name = 'recoverylevelTwoScreen' ) )
screenManager.add_widget( UsernameRecover( name = 'usernameRecoverScreen' ) )
screenManager.add_widget( PasswordRecover( name = 'passwordRecoverScreen' ) )
screenManager.add_widget( UserRecoveryLevelThreeScreen( name = 'userrecoverylevelThreeScreen' ) )
screenManager.add_widget( PasswordRecoveryLevelThreeScreen( name = 'passwordrecoverylevelThreeScreen' ) )
screenManager.add_widget( RecoverySecQuestion( name = 'recoverysecQuestion' ) )
screenManager.add_widget( PasswordReset( name = 'passwordReset' ) )

screenManager.add_widget( HomeScreen( name = 'homeScreen' ) )

class ThreeLevelAuthApp(App):
	def build(self):
		return screenManager

if __name__ == '__main__':
	ThreeLevelAuthApp().run()
