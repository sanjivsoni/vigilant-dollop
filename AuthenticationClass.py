from helperFunctions import *

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

    def checkUserLevel2(self,otpType,userOTP):

        correctOTP = ""
        establishConnection()
        if(otpType == 1):
            sql = "SELECT mobileOTP FROM user WHERE userid =" + "'" + self.userID + "'"

        elif(otpType == 2):
            sql = "SELECT emailOTP FROM user WHERE userid =" + "'" + self.userID + "'"

        try:
            config.statement.execute(sql)
            results = config.statement.fetchall()
            for row in results:
                correctOTP = row[0]

        except Exception, e:
            print repr(e)
            config.conn.rollback()
            flag = 0
        if (correctOTP == hashEncrypt(userOTP)):
            self.userVerifiedLevel2 = True

        closeConnection()

    def sendOTP_mobile(self,case):

        userMobile = ""
        establishConnection()
        sql = "SELECT mobile FROM user WHERE userid =" + "'" + self.userID + "'"
        #print sql
        try:
            config.statement.execute(sql)
            results = statement.fetchall()
            for row in results:
                userMobile = aesDecrypt(self.userID,row[0])

        except Exception, e:
            print repr(e)
            config.conn.rollback()
            flag = 0

        if case == 1:
            generatedOTP = generateOTP()
            client = TwilioRestClient(config.account_sid, config.auth_token)
            message = client.messages.create(to = userMobile, from_ = config.from_number, body = config.mobile_msg + generatedOTP)

    def sendOTP_email(self,case):
        userEmail = ""
        establishConnection()
        sql = "SELECT email FROM user WHERE userid =" + "'" + self.userID + "'"
        try:
            config.statement.execute(sql)
            results = config.statement.fetchall()
            for row in results:
                userEmail = aesDecrypt(self.userID,row[0])

        except Exception, e:
            print repr(e)
            config.conn.rollback()
            print "error"
        if (case == 1):
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
                statement.config.execute(sql)
                results = config.statement.fetchall()
                for row in results:
                    encryptedSudoPwd = row[0]

            except Exception, e:
                print repr(e)
                config.conn.rollback()
                flag = 0

            status = unlock(path,self.userPwd,encryptedSudoPwd)
            closeConnection()
