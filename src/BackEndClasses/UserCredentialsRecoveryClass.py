from ..helperFunctions import *
from AuthenticationClass import *

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
                sql = "SELECT userid FROM user WHERE mobile =" + "'" + aesEncrypt(recoveryID) + "'"

            elif(recoveryType == 2):
                sql = "SELECT userid FROM user WHERE email =" + "'" + aesEncrypt(recoveryID) + "'"

            #Fetch userID
            try:
                config.statement.execute(sql)
                results = config.statement.fetchall()
                for row in results:
                    self.userID = row[0]
                    otpAuthentication = OTP(self.userID)

            except Exception, e:
                print repr(e)
                config.conn.rollback()
                flag = 0

            closeConnection()
            if(recoveryType == 1):
                otpAuthentication.sendOTPforRecovery_mobile(recoveryID,out_queue)

            elif(recoveryType == 2):
                otpAuthentication.sendOTPforRecovery_email(recoveryID,out_queue)

        else:
            closeConnection()
            out_queue.put(-1)

    def fetchSSNType(self):

        ssn = ""
        establishConnection()

        sql = "SELECT ssn_type FROM personal WHERE userid =" + "'" + self.userID + "'"

        try:
            config.statement.execute(sql)
            results = config.statement.fetchall()
            for row in results:
                ssn = aesDecrypt(row[0])

        except Exception, e:
            print repr(e)
            config.conn.rollback()

        closeConnection()
        return config.ssnTypes[int(ssn)]

    def recoverUserLeveL2(self,ssnid):
        establishConnection()
        sql = "SELECT ssnid FROM personal WHERE userid =" + "'" + self.userID + "'"

        try:
            config.statement.execute(sql)
            results = config.statement.fetchall()
            for row in results:
                correctSSnId = aesDecrypt(row[0]).replace("#", " ")

        except Exception, e:
            print repr(e)
            config.conn.rollback()
            flag = 0

        if(correctSSnId == ssnid):
            self.Level2 = True
            return 1
        else:
            return 0

    def fetchUserSecurityQuestion(self,questionNo):

        ques = ""
        establishConnection()

        if questionNo == 1:
            sql = "SELECT ques1 FROM security_ques WHERE userid =" + "'" + self.userID + "'"
        else:
            sql = "SELECT ques2 FROM security_ques WHERE userid =" + "'" + self.userID + "'"

        try:
            config.statement.execute(sql)
            results = config.statement.fetchall()
            for row in results:
                ques = row[0]

        except Exception, e:
            print repr(e)
            config.conn.rollback()

        closeConnection()

        if questionNo == 1:
            return config.securityQuestionsPart1[int(aesDecrypt(ques))]

        else:
            return config.securityQuestionsPart2[int(aesDecrypt(ques))]

    def recoverUserLeveL3(self,questionNo):


        ans = ""
        establishConnection()

        if questionNo == 1:
            sql = "SELECT ans1 FROM security_ques WHERE userid =" + "'" + self.userID + "'"
        else:
            sql = "SELECT ans2 FROM security_ques WHERE userid =" + "'" + self.userID + "'"

        try:
            config.statement.execute(sql)
            results = config.statement.fetchall()
            for row in results:
                ans = aesDecrypt(row[0]).replace("#", " ")

        except Exception, e:
            print repr(e)
            config.conn.rollback()

        closeConnection()

        return ans

    def updateUserID(self,newUserID):
        establishConnection()
        userTableSql = "UPDATE user SET userid = '" + hashEncrypt(newUserID) + "' " + " WHERE userid = " + "'" + self.userID + "'"
        personalTableSql = "UPDATE personal SET userid = '" + hashEncrypt(newUserID) + "' " + " WHERE userid = " + "'" + self.userID + "'"
        SQTableSql = "UPDATE security_ques SET userid = '" + hashEncrypt(newUserID) + "' " + " WHERE userid = " + "'" + self.userID + "'"
        lockedFilesTableSQL = "UPDATE lockedFiles SET userid = '" + hashEncrypt(newUserID) + "' " + " WHERE userid = " + "'" + self.userID + "'"
        try:
            config.statement.execute(userTableSql)
            config.conn.commit()
            config.statement.execute(personalTableSql)
            config.conn.commit()
            config.statement.execute(SQTableSql)
            config.conn.commit()
            config.statement.execute(lockedFilesTableSQL)
            config.conn.commit()

        except Exception, e:
            print repr(e)
            config.conn.rollback()
            flag = 0

        closeConnection()

    def updateUserPassword(self,newPassword):
        establishConnection()
        sql = "UPDATE user SET password = '" + hashEncrypt(newPassword) + "' " + " WHERE userid = " + "'" + self.userID + "'"
        print sql
        try:
            config.statement.execute(sql)
            config.conn.commit()
            print "success"
        except Exception, e:
            print repr(e)
            config.conn.rollback()
            flag = 0

        closeConnection()
