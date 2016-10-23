from ..BackEndClasses import *
from ..libraries import *


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
    SQ1 = 0
    SQ2 = 0
    ssnType = 0



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

    def populateSecurityQuestionPart1Spinner(self):
        my_list = []
        for i in range(1,5):
            my_list.append(config.securityQuestionsPart1[i])
        self.ids.Y.values = my_list


    def populateSecurityQuestionPart2Spinner(self):
        my_list = []
        for i in range(5,9):
            my_list.append(config.securityQuestionsPart2[i])
        self.ids.X.values = my_list

    def populateSSN_Spinner(self):
        my_list = []
        for i in range(1,5):
            my_list.append(config.ssnTypes[i])
        self.ids['10'].values = my_list

    def getIntValueForSecurityQues1(self):
        for key in config.securityQuestionsPart1:
            if config.securityQuestionsPart1[key] == self.ids.Y.text:
                self.SQ1 = key

    def getIntValueForSecurityQues2(self):
        for key in config.securityQuestionsPart2:
            if config.securityQuestionsPart2[key] == self.ids.X.text:
                self.SQ2 = key

    def getIntValueForSSNtype(self):
        for key in config.ssnTypes:
            if config.ssnTypes[key] == self.ids['10'].text:
                self.ssnType = key


    # def secQues1(self):
    #     ID = self.ids['Y']
    #     ID2 = self.ids['LY']
    #     if not(ID.text == "Security Question"):
    #         ID2.color = [0,1,0,1]
    #     else:
    #         ID2.color = [1,1,1,1]
    def buttonAction(self):
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

        if not(self.SQ1 == 0) and not(self.SQ2 == 0) and not(self.ssnType == 0) and not(label[14].text == "Country Code"):
            if self.flag5 and self.flag3 and self.flag11 and self.flag1 and self.flag10 and self.flag4 and self.flag9 and self.flag8 and self.flag6 and self.flag2 and self.flag12:

                phoneNo = label[14].text+label[5].text
                userCredentials = label[1].text + " " + label[2].text
                userContactDetails = label[4].text + " " +phoneNo +  " " +"sudoPwd"
                userPersonalDetails = label[7].text + " " +label[8].text + " " +label[6].text + " " + str(self.ssnType) + " " +label[11].text.replace(" ", "#")
                userSecurityQues = str(self.SQ1) + " " + str(self.SQ2) +  " " +label[12].text.replace(" ", "#") + " " +label[13].text.replace(" ", "#")

                newUser = User(userCredentials)
                loginDetails = LoginDetails(hashEncrypt(label[1].text))
                newUser.createUser(userContactDetails)
                newUser.addPersonalDetails(userPersonalDetails)
                newUser.addSecurityQuestions(userSecurityQues)
                loginDetails.userCreated()

                App.get_running_app().root.current = 'usernameScreen'

        else:
            print "No"
