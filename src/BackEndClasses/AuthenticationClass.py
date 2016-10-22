from ..helperFunctions import *
from LoginDetailsClass import *

class Authentication:

    def __init__(self):
        self.userID = ""
        self.userDetails = ""
        self.userVerifiedLevel1 = False
        self.userVerifiedLevel2 = False
        self.userVerifiedLevel3 = False
        #self.authenticationComplete = self.userVerifiedLevel1 and self.userVerifiedLevel2 and self.userVerifiedLevel3
        self.authenticationComplete = True

    def checkIfUserExists(self,userID):
        flag = 0
        establishConnection()
        sql = "SELECT userid FROM user WHERE userid =" + "'" + hashEncrypt(userID) + "'"

        try:
            config.statement.execute(sql)
            results = config.statement.fetchall()
            for row in results:
                self.userID = row[0]
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

    def checkUserLevel1(self,userEnteredPwd):
        correctPassword = ""

        establishConnection()
        sql = "SELECT password FROM user WHERE userid =" + "'" + self.userID + "'"
        #print sql

        try:
            config.statement.execute(sql)
            results = config.statement.fetchall()
            for row in results:
                self.userPwd = row[0]
                correctPassword = row[0]

        except Exception, e:
            print repr(e)
            config.conn.rollback()
            flag = 0
        closeConnection()
        if (correctPassword == hashEncrypt(userEnteredPwd)):
            self.userVerifiedLevel1 = True
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

    def checkSecurityQuesAnswer(self,questionNo):

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
                ans = aesDecrypt(row[0])

        except Exception, e:
            print repr(e)
            config.conn.rollback()

        closeConnection()

        return ans

    def fetchDOBforAuth(self,dobType):
        ques = ""
        establishConnection()

        sql = "SELECT dob FROM personal WHERE userid =" + "'" + self.userID + "'"

        try:
            config.statement.execute(sql)
            results = config.statement.fetchall()
            for row in results:
                dob = row[0]

        except Exception, e:
            print repr(e)
            config.conn.rollback()

        closeConnection()

        birthDate = aesDecrypt(dob).split("/")[0]
        birthYear = aesDecrypt(dob).split("/")[2]

        if(dobType == 1):
            return birthYear
        else:
            return birthDate

    def returnUserID(self):
        return self.userID

    def lockItem(self,filePath,fileName):
        if(self.authenticationComplete):
            flag = -1
            encryptedSudoPwd = ""
            establishConnection()
            sql = "SELECT sudoPwd FROM user WHERE userid =" + "'" + self.userID + "'"

            try:
                config.statement.execute(sql)
                results = config.statement.fetchall()
                for row in results:
                    encryptedSudoPwd = row[0]

            except Exception, e:
                print repr(e)
                config.conn.rollback()
                flag = 0

            status = lock(filePath + "/" +  fileName ,encryptedSudoPwd)
            if status == 1 :
                encryptedData = aesEncrypt(filePath + " " + fileName)
                sql = "INSERT INTO lockedFiles(userid,filepath,filename) VALUES " + insertQueryHelper(self.userID + " " + encryptedData)

                try:
                    config.statement.execute(sql)
                    config.conn.commit()
                    flag = 1

                except Exception, e:
                    config.conn.rollback()
                    flag = 0

            closeConnection()
            if flag:
                return 1
            else:
                return 0

    def unlockItem(self,filePath,fileName):
        if(self.authenticationComplete):
            encryptedSudoPwd = ""
            establishConnection()
            sql = "SELECT sudoPwd FROM user WHERE userid =" + "'" + self.userID + "'"

            try:
                config.statement.execute(sql)
                results = config.statement.fetchall()
                for row in results:
                    encryptedSudoPwd = row[0]

            except Exception, e:
                print repr(e)
                config.conn.rollback()
                flag = 0

            status = unlock(filePath + "/" +  fileName,encryptedSudoPwd)

            if status == 1:
                sql = "DELETE FROM lockedFiles WHERE filepath = '" + aesEncrypt(filePath) + "' AND filename = '" + aesEncrypt(fileName) + "'"
                print sql
                try:
                    config.statement.execute(sql)
                    config.conn.commit()
                except Exception, e:
                    print repr(e)
                    config.conn.rollback()
                    flag = 0

                return 1

            closeConnection()

    def fetchLockedFiles(self):

        establishConnection()

        sql = "SELECT filepath,filename FROM lockedFiles WHERE userid =" + "'" + self.userID + "'"

        try:
            config.statement.execute(sql)
            results = config.statement.fetchall()
            for row in results:
                print aesDecrypt(row[0])
                print aesDecrypt(row[1])

        except Exception, e:
            print repr(e)
            config.conn.rollback()
            flag = 0

        return results

class OTP:

    def __init__(self,userID = ""):
        self.userID = userID

    def sendOTPforAuth_mobile(self,length,out_queue):
        #login_stats = LoginDetails(self.userID)
        userMobile = ""
        establishConnection()
        sql = "SELECT mobile FROM user WHERE userid =" + "'" + self.userID + "'"
        #print sql
        try:
            config.statement.execute(sql)
            results = config.statement.fetchall()
            for row in results:
                userMobile = aesDecrypt(row[0])

        except Exception, e:
            print repr(e)
            config.conn.rollback()
            flag = 0

        generatedOTP = generateOTP(length)
        out_queue.put(generatedOTP)
        runByThreadForMobile(sendTextMobile,userMobile,config.mobile_msg + generatedOTP)

    def sendOTPforAuth_email(self,length,out_queue):
        userEmail = ""
        establishConnection()
        sql = "SELECT email FROM user WHERE userid =" + "'" + self.userID + "'"
        #print sql
        try:
            config.statement.execute(sql)
            results = config.statement.fetchall()
            for row in results:
                userEmail = aesDecrypt(row[0])
                #print userEmail

        except Exception, e:
            print repr(e)
            config.conn.rollback()
            print "error"


        generatedOTP = generateOTP(length)
        out_queue.put(generatedOTP)
        runByThreadForEmail(sendEmail,userEmail,config.email_msg + generatedOTP,config.emailOtpSubject)
        #return generatedOTP

    def sendOTPforRecovery_mobile(self,sendToMobile,out_queue):
        generatedOTP = generateOTP(6)
        out_queue.put(generatedOTP)
        runByThreadForMobile(sendTextMobile,userMobile,config.mobile_msg + generatedOTP)

    def sendOTPforRecovery_email(self,sendToEmail,out_queue):

        generatedOTP = generateOTP(6)
        out_queue.put(generatedOTP)
        runByThreadForEmail(sendEmail,userEmail,config.email_msg + generatedOTP,config.emailOtpSubject)

class LoginMessages:
    def __init__(self,userID = ""):
        self.userID = userID

    def loggedIn(self):
        userMobile = ""
        userEmail = ""
        establishConnection()
        sql = "SELECT mobile FROM user WHERE userid =" + "'" + self.userID + "'"
        #print sql

        try:
            config.statement.execute(sql)
            results = config.statement.fetchall()

            for row in results:
                userMobile = aesDecrypt(row[0])

        except Exception, e:
            print repr(e)
            config.conn.rollback()
            flag = 0


        sql = "SELECT email FROM user WHERE userid =" + "'" + self.userID + "'"
        try:
            config.statement.execute(sql)
            results = config.statement.fetchall()

            for row in results:
                userEmail = aesDecrypt(row[0])

        except Exception, e:
            print repr(e)
            config.conn.rollback()
            flag = 0


        sendTextMobile(userMobile,config.succesfulLoginMessageText + fetchLocation())
        sendEmail(userEmail,config.succesfulLoginMessageTextEmail_part1 + fetchLocation() + config.succesfulLoginMessageTextEmail_part2 + config.succesfulLoginMessageTextEmail_part3+config.messageTextSignature,config.emailSuccesfulLoginSubject)

    def failedLogin(self):

        userMobile = ""
        userEmail = ""
        establishConnection()
        sql = "SELECT mobile FROM user WHERE userid =" + "'" + self.userID + "'"
        #print sql

        try:
            config.statement.execute(sql)
            results = config.statement.fetchall()

            for row in results:
                userMobile = aesDecrypt(row[0])

        except Exception, e:
            print repr(e)
            config.conn.rollback()
            flag = 0


        sql = "SELECT email FROM user WHERE userid =" + "'" + self.userID + "'"
        try:
            config.statement.execute(sql)
            results = config.statement.fetchall()

            for row in results:
                userEmail = aesDecrypt(row[0])

        except Exception, e:
            print repr(e)
            config.conn.rollback()
            flag = 0

        sendTextMobile(userMobile,config.succesfulLoginMessageText + fetchLocation())
        sendEmail(userEmail,config.succesfulLoginMessageTextEmail_part1 + fetchLocation() + config.succesfulLoginMessageTextEmail_part2 + config.succesfulLoginMessageTextEmail_part3+config.messageTextSignature,config.emailSuccesfulLoginSubject)
