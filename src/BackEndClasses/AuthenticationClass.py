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

    def lockItem(self,filePath,fileName):
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

            status = lock(filePath + "/" +  fileName ,encryptedSudoPwd)
            if status == 1 :
                encryptedData = aesEncrypt(filePath + " " + fileName)
                sql = "INSERT INTO lockedFiles(userid,filepath,filename) VALUES " + insertQueryHelper(self.userID + " " + encryptedData)
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

    def unlockItem(self,filePath,fileName):
        if(self.authenticationComplete):
            encryptedSudoPwd = ""
            establishConnection()
            sql = "SELECT sudoPwd FROM user WHERE userid =" + "'" + self.userID + "'"
            print sql

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
                sql = "DELETE FROM lockedFiles WHERE filepath = '" + filePath + "' AND filename = '" + fileName + "'"
                try:
                    config.statement.execute(sql)

                except Exception, e:
                    print repr(e)
                    config.conn.rollback()
                    flag = 0

                return 1

            closeConnection()

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
        client = TwilioRestClient(config.account_sid, config.auth_token)
        message = client.messages.create(to = userMobile, from_ = config.from_number, body = config.mobile_msg + generatedOTP)

    def sendOTPforAuth_email(self,length,out_queue,):
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
        msg = MIMEMultipart()
        msg['From'] = "Team Vigilant Dollop"
        msg['To'] = userEmail
        msg['Subject'] = config.email_subject
        body = config.email_msg + generatedOTP
        msg.attach(MIMEText(body, 'plain'))

        server = smtplib.SMTP(config.smtp_domain,config.smtp_port)
        server.starttls()
        server.login(config.emailid, config.email_pass)
        text = msg.as_string()
        server.sendmail(config.emailid, userEmail, text)
        server.quit()

    def sendOTPforRecovery_mobile(self,sendToMobile,out_queue):

        generatedOTP = generateOTP(6)
        out_queue.put(generatedOTP)
        client = TwilioRestClient(config.account_sid, config.auth_token)
        message = client.messages.create(to = sendToMobile, from_ = config.from_number, body = config.mobile_msg + generatedOTP)

    def sendOTPforRecovery_email(self,sendToEmail,out_queue):

        generatedOTP = generateOTP(6)
        out_queue.put(generatedOTP)
        msg = MIMEMultipart()
        msg['From'] = "Team Vigilant Dollop"
        msg['To'] = sendToEmail
        msg['Subject'] = config.email_subject
        body = config.email_msg + generatedOTP
        msg.attach(MIMEText(body, 'plain'))

        server = smtplib.SMTP(config.smtp_domain,config.smtp_port)
        server.starttls()
        server.login(config.emailid, config.email_pass)
        text = msg.as_string()
        server.sendmail(config.emailid, sendToEmail, text)
        server.quit()
