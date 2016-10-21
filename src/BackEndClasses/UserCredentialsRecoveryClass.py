from ..helperFunctions import *
from AuthenticationClass import *

class PasswordRecovery:

    def __init__(self,userID):
        self.userID = hashEncrypt(userID)
        self.Level1 = False
        self.Level2 = False
        self.Level3 = False
        #self.userIdentified = self.Level1 and self.Level2 and self.Level3
        self.userIdentified = True

    def recoverPasswordLeveL1(self,recoveryType,out_queue):
        recoveryID = ""
        otpAuthentication = OTP(self.userID)
        flag = 0
        establishConnection()

        if(recoveryType == 1):
            sql = "SELECT mobile FROM user WHERE userid =" + "'" + self.userID + "'"

        elif(recoveryType == 2):
            sql = "SELECT email FROM user WHERE userid =" + "'" + self.userID + "'"

        try:
            config.statement.execute(sql)
            results = config.statement.fetchall()
            for row in results:
                recoveryID = row[0]

        except Exception, e:
            print repr(e)
            config.conn.rollback()
            flag = 0


        if(recoveryType == 1):
            otpAuthentication.sendOTPforAuth_mobile(out_queue)

        elif(recoveryType == 2):
            otpAuthentication.sendOTPforAuth_email(out_queue)

        if flag == 0 :
            return -1

    def recoverPasswordLeveL2(self,ssn_type,ssnid):
        establishConnection()

        sql = "SELECT ssnid,ssn_type FROM personal WHERE userid =" + "'" + self.userID + "'"

        try:
            config.statement.execute(sql)
            results = config.statement.fetchall()
            for row in results:
                correctSSnId = aesDecrypt(row[0])
                correctSSntype = aesDecrypt(row[1])

        except Exception, e:
            print repr(e)
            config.conn.rollback()
            flag = 0

        if((correctSSnId == ssnid) and (correctSSntype == ssn_type)):
            self.Level2 = True
            return 1
        else:
            return 0

    def recoverPasswordLeveL3(self,quesType,quesAnswer):

        establishConnection()
        if(quesType <= 4):
            sql = "SELECT ques1,ans1 FROM security_ques WHERE userid =" + "'" + self.userID + "'"

        elif(quesType > 4):
            sql = "SELECT ques2,ans2 FROM security_ques WHERE userid =" + "'" + self.userID + "'"

        try:
            config.statement.execute(sql)
            results = config.statement.fetchall()
            for row in results:
                correctQuesType = aesDecrypt(row[0])
                correctAnswer = aesDecrypt(row[1])

        except Exception, e:
            print repr(e)
            config.conn.rollback()
            flag = 0

        if((correctQuesType == quesType) and (correctAnswer == quesAnswer)):
            self.Level3 = True
            return 1
        else:
            return 0

    def addNewPassword(self,newPwd):
        if(self.userIdentified):
            establishConnection()
            sql = sql = "UPDATE user SET password = '" + hashEncrypt(newPwd) + " '" + "WHERE userid = " + "'" + self.userID + "'"

            try:
                config.statement.execute(sql)
                config.conn.commit()
                flag = 1
            except Exception, e:
                print repr(e)
                config.conn.rollback()
                flag = 0
            closeConnection()

            if(flag):
                return 1
            else:
                return 0

class UserRecovery:

    def __init__(self):
        self.userID = ""
        self.Level1 = False
        self.Level2 = False
        self.Level3 = False
        self.userIdentified = self.Level1 and self.Level2 and self.Level3

    def recoverUserLevel1(self,recoveryType,recoveryID,out_queue):
        correctRecoveryID = ""
        generatedOTP = ""
        otpAuthentication = Authentication()
        flag = 0
        establishConnection()

        if(recoveryType == 1):
            sql = "SELECT mobile FROM user WHERE mobile =" + "'" + aesEncrypt(recoveryID) + "'"

        elif(recoveryType == 2):
            sql = "SELECT email FROM user WHERE email =" + "'" + aesEncrypt(recoveryID) + "'"

        try:
            config.statement.execute(sql)
            results = config.statement.fetchall()
            for row in results:
                flag = 1

        except Exception, e:
            print repr(e)
            config.conn.rollback()
            flag = 0

        if (flag):
            if(recoveryType == 1):
                otpAuthentication.sendOTPforRecovery_mobile(recoveryID,out_queue)
                sql = "SELECT userid FROM user WHERE mobile =" + "'" + aesEncrypt(recoveryID) + "'"

            elif(recoveryType == 2):
                otpAuthentication.sendOTPforRecovery_email(recoveryID,out_queue)
                sql = "SELECT userid FROM user WHERE email =" + "'" + aesEncrypt(recoveryID) + "'"


            #Fetch userID
            try:
                config.statement.execute(sql)
                results = config.statement.fetchall()
                for row in results:
                    self.userID = row[0]

            except Exception, e:
                print repr(e)
                config.conn.rollback()
                flag = 0

            closeConnection()


        else:
            closeConnection()
            out_queue.put(-1)




    def recoverUserLeveL2(self,ssnid):
        establishConnection()

        sql = "SELECT ssnid FROM personal WHERE userid =" + "'" + self.userID + "'"
        print sql

        try:
            config.statement.execute(sql)
            results = config.statement.fetchall()
            for row in results:
                correctSSnId = aesDecrypt(row[0])

        except Exception, e:
            print repr(e)
            config.conn.rollback()
            flag = 0

        if(correctSSnId == ssnid):
            self.Level2 = True
            return 1
        else:
            return 0

    def recoverUserLeveL3(self,quesType, quesAnswer):

        establishConnection()
        if(int(quesType) <= 4):
            sql = "SELECT ques1,ans1 FROM security_ques WHERE userid =" + "'" + self.userID + "'"

        elif(int(quesType) > 4):
            sql = "SELECT ques2,ans2 FROM security_ques WHERE userid =" + "'" + self.userID + "'"

        try:
            config.statement.execute(sql)
            results = config.statement.fetchall()
            for row in results:
                correctQuesType = aesDecrypt(row[0])
                correctAnswer = aesDecrypt(row[1])

        except Exception, e:
            print repr(e)
            config.conn.rollback()
            flag = 0

        if((correctQuesType == quesType) and (correctAnswer == quesAnswer)):
            self.Level3 = True
            return 1
        else:
            return 0
