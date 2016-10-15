from helperFunctions import *
from LoginDetailsClass import *

class Authentication:

    def __init__(self,userDetails):
        self.userID = (userDetails).split()[0]
        self.userPwd = (userDetails).split()[1]
        self.userDetails = userDetails
        self.userVerifiedLevel1 = False
        self.userVerifiedLevel2 = False
        self.userVerifiedLevel3 = False
        #self.authenticationComplete = self.userVerifiedLevel1 and self.userVerifiedLevel2 and self.userVerifiedLevel3
        self.authenticationComplete = True

    def checkUserLevel1(self):
        correctPassword = ""

        establishConnection()
        sql = "SELECT * FROM user WHERE userid =" + "'" + self.userID + "'"

        try:
            config.statement.execute(sql)
            results = config.statement.fetchall()
            for row in results:
                correctPassword = row[1]

        except Exception, e:
            print repr(e)
            config.conn.rollback()
            flag = 0
        if (correctPassword == self.userPwd):
            self.userVerifiedLevel1 = True

        closeConnection()

    def lockItem(self,path):
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

            status = lock(path,self.userPwd,encryptedSudoPwd)
            closeConnection()

    def unlockItem(self,path):
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

            status = unlock(path,self.userPwd,encryptedSudoPwd)
            closeConnection()


class OTP:
    def __init__(self,userID = ""):
        self.userID = userID

    def sendOTPforAuth_mobile(self):
        login_stats = LoginDetails(self.userID)
        userMobile = ""
        establishConnection()
        sql = "SELECT mobile FROM user WHERE userid =" + "'" + self.userID + "'"
        #print sql
        try:
            config.statement.execute(sql)
            results = config.statement.fetchall()
            for row in results:
                userMobile = aesDecrypt(config.key,row[0])

        except Exception, e:
            print repr(e)
            config.conn.rollback()
            flag = 0

        generatedOTP = generateOTP()
        client = TwilioRestClient(config.account_sid, config.auth_token)
        message = client.messages.create(to = userMobile, from_ = config.from_number, body = config.mobile_msg + generatedOTP)

        return generatedOTP

    def sendOTPforAuth_email(self):
        userEmail = ""
        establishConnection()
        sql = "SELECT email FROM user WHERE userid =" + "'" + self.userID + "'"
        try:
            config.statement.execute(sql)
            results = config.statement.fetchall()
            for row in results:
                userEmail = aesDecrypt(config.key,row[0])

        except Exception, e:
            print repr(e)
            config.conn.rollback()
            print "error"

        generatedOTP = generateOTP()
        msg = MIMEMultipart()
        msg['From'] = config.emailid
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
        return generatedOTP

    def sendOTPforRecovery_mobile(self,sendToMobile):

        generatedOTP = generateOTP()
        client = TwilioRestClient(config.account_sid, config.auth_token)
        message = client.messages.create(to = sendToMobile, from_ = config.from_number, body = config.mobile_msg + generatedOTP)
        return generatedOTP

    def sendOTPforRecovery_email(self,sendToEmail):

        generatedOTP = generateOTP()
        msg = MIMEMultipart()
        msg['From'] = config.emailid
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

        return generatedOTP