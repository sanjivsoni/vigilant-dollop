from libraries import *

class PasswordRecovery:

    def __init__(self,userID):
        self.userID = userID
        self.Level1 = False
        self.Level2 = False
        self.Level3 = False
        self.userIdentified = self.Level1 and self.Level2 and self.Level3

    def recoverPasswordLeveL1(self,recoveryType,recoveryID):
        correctRecoveryID = ""
        generatedOTP = ""
        otpAuthentication = OTP.new(userID)
        establishConnection()

        if(recoveryType == 1):
            sql = "SELECT mobile FROM user WHERE userid =" + "'" + self.userID + "'"

        elif(recoveryType == 2):
            sql = "SELECT email FROM user WHERE userid =" + "'" + self.userID + "'"

        try:
            config.statement.execute(sql)
            results = config.statement.fetchall()
            for row in results:
                correctRecoveryID = row[0]

        except Exception, e:
            print repr(e)
            config.conn.rollback()
            flag = 0

        if (correctRecoveryID == aesEncrypt(config.key,recoveryID)):
            if(recoveryType == 1):
                generatedOTP = otpAuthentication.sendOTPforRecovery_mobile(recoveryID)

            elif(recoveryType == 2):
                generatedOTP = otpAuthentication.sendOTPforRecovery_email(recoveryID)

        return generatedOTP

    def recoverPasswordLeveL2(self,ssn_type,ssnid):
        establishConnection()

        sql = "SELECT ssnid,ssn_type FROM personal WHERE userid =" + "'" + self.userID + "'"

        try:
            config.statement.execute(sql)
            results = config.statement.fetchall()
            for row in results:
                correctSSnId = aesDecrypt(config.key,row[0])
                correctSSntype = aesDecrypt(config.key,row[1])

        except Exception, e:
            print repr(e)
            config.conn.rollback()
            flag = 0

        if((correctSSnId == ssnid) and (correctSSntype == ssn_type)):
            self.Level2 = True
            return 1
        else:
            return 0

    def recoverPasswordLeveL3(self,quesType, quesAnswer):

        establishConnection()
        if(quesType <= 4):
            sql = "SELECT ques1,ans1 FROM security_ques WHERE userid =" + "'" + self.userID + "'"

        elif(quesType > 4):
            sql = "SELECT ques2,ans2 FROM security_ques WHERE userid =" + "'" + self.userID + "'"

        try:
            config.statement.execute(sql)
            results = config.statement.fetchall()
            for row in results:
                correctQuesType = aesDecrypt(config.key,row[0])
                correctAnswer = aesDecrypt(config.key,row[1])

        except Exception, e:
            print repr(e)
            config.conn.rollback()
            flag = 0

        if((correctQuesType == quesType) and (correctAnswer == quesAnswer)):
            self.Level3 = True
            return 1
        else:
            return 0

    def fetchUpdatePassword(self,newPwd):
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


class UserRecovery:

    def __init__(self):
        self.userID = ""
        self.Level1 = False
        self.Level2 = False
        self.Level3 = False
        self.userIdentified = self.Level1 and self.Level2 and self.Level3

    def recoverUserLevel1(self,recoveryType,recoveryID):
        correctRecoveryID = ""
        generatedOTP = ""
        flag = False
        otpAuthentication = OTP.new(userID)
        establishConnection()

        if(recoveryType == 1):
            sql = "SELECT mobile FROM user WHERE mobile =" + "'" + aesEncrypt(config.key,recoveryID) + "'"

        elif(recoveryType == 2):
            sql = "SELECT email FROM user WHERE email =" + "'" + aesEncrypt(config.key,recoveryID) + "'"

        try:
            config.statement.execute(sql)
            results = config.statement.fetchall()
            for row in results:
                flag = True

        except Exception, e:
            print repr(e)
            config.conn.rollback()
            flag = 0

        if (flag):
            if(recoveryType == 1):
                generatedOTP = otpAuthentication.sendOTPforRecovery_mobile(recoveryID)
                sql = "SELECT userid FROM user WHERE mobile =" + "'" + aesEncrypt(config.key,recoveryID) + "'"

            elif(recoveryType == 2):
                generatedOTP = otpAuthentication.sendOTPforRecovery_email(recoveryID)
                "SELECT userid FROM user WHERE email =" + "'" + aesEncrypt(config.key,recoveryID) + "'"


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

        return generatedOTP

    def recoverPasswordLeveL2(self,ssn_type,ssnid):
        establishConnection()

        sql = "SELECT ssnid,ssn_type FROM personal WHERE userid =" + "'" + self.userID + "'"

        try:
            config.statement.execute(sql)
            results = config.statement.fetchall()
            for row in results:
                correctSSnId = aesDecrypt(config.key,row[0])
                correctSSntype = aesDecrypt(config.key,row[1])

        except Exception, e:
            print repr(e)
            config.conn.rollback()
            flag = 0

        if((correctSSnId == ssnid) and (correctSSntype == ssn_type)):
            self.Level2 = True
            return 1
        else:
            return 0

    def recoverPasswordLeveL3(self,quesType, quesAnswer):

        establishConnection()
        if(quesType <= 4):
            sql = "SELECT ques1,ans1 FROM security_ques WHERE userid =" + "'" + self.userID + "'"

        elif(quesType > 4):
            sql = "SELECT ques2,ans2 FROM security_ques WHERE userid =" + "'" + self.userID + "'"

        try:
            config.statement.execute(sql)
            results = config.statement.fetchall()
            for row in results:
                correctQuesType = aesDecrypt(config.key,row[0])
                correctAnswer = aesDecrypt(config.key,row[1])

        except Exception, e:
            print repr(e)
            config.conn.rollback()
            flag = 0

        if((correctQuesType == quesType) and (correctAnswer == quesAnswer)):
            self.Level3 = True
            return 1
        else:
            return 0
