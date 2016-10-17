from helperFunctions import *

class LoginDetails:

    def __init__(self,userID):
        self.userID = hashEncrypt(userID)

    def userCreated(self):
        aesEncryptedInfo = aesEncrypt(currentUTC() + " " + getUserDetails())
        establishConnection()
        sql = "INSERT INTO login_stats(userid,created_at,system_details) VALUES " + insertQueryHelper(self.userID + " " )
        sql = sql.replace("#", " ")
        try:
            config.statement.execute(sql)
            config.conn.commit()
            flag = 1
        except Exception, e:
            print repr(e)
            config.conn.rollback()
            flag = 0

        closeConnection()

    def passwordChanged(self):

        establishConnection()
        sql = "UPDATE login_stats SET pwd_changed_at = '" + aesEncrypt(currentUTC()) + "' " + ",system_details = '" + aesEncrypt(getUserDetails()) + "'"  + " WHERE userid = " + "'" + self.userID + "'"
        sql = sql.replace("#", " ")
        try:
            config.statement.execute(sql)
            config.conn.commit()
            print "success"
        except Exception, e:
            print repr(e)
            config.conn.rollback()
            flag = 0

        closeConnection()

    def recordUpdated(self):

        establishConnection()
        sql = "UPDATE login_stats SET updated_at = '" + aesEncrypt(currentUTC()) + " '" + ",system_details = '" + aesEncrypt(getUserDetails()) + "'"  + "WHERE userid = " + "'" + self.userID + "'"
        sql = sql.replace("#", " ")
        try:
            config.statement.execute(sql)
            config.conn.commit()
            print "success"
        except Exception, e:
            print repr(e)
            config.conn.rollback()
            flag = 0
        closeConnection()

    def updateFailedLoginTime(self):

        establishConnection()
        sql = "UPDATE login_stats SET failed_login_time = '" + aesEncrypt(currentUTC()) + " '" + ",system_details = '" + aesEncrypt(getUserDetails()) + "'"  + "WHERE userid = " + "'" + self.userID + "'"
        sql = sql.replace("#", " ")
        try:
            config.statement.execute(sql)
            config.conn.commit()
            print "success"
        except Exception, e:
            print repr(e)
            config.conn.rollback()
            flag = 0

        closeConnection()

    def updateLogoutTime(self):

        establishConnection()
        sql = "UPDATE login_stats SET logout_time = '" + aesEncrypt(currentUTC()) + " '" + ",system_details = '" + aesEncrypt(getUserDetails()) + "'"  + "WHERE userid = " + "'" + self.userID + "'"
        sql = sql.replace("#", " ")
        try:
            config.statement.execute(sql)
            config.conn.commit()
            print "success"
        except Exception, e:
            print repr(e)
            config.conn.rollback()
            flag = 0

        closeConnection()

class LoginDetailsMessages:
    def __init__(self,userID = ""):
        self.userID = hashEncrypt(userID)

    def succesfulLoginMessage(self):
        establishConnection()
        sql = "SELECT mobile,email FROM user WHERE userid =" + "'" + self.userID + "'"
        #print sql
        try:
            config.statement.execute(sql)
            results = config.statement.fetchall()
            for row in results:
                userMobile = "+91" + aesDecrypt(row[0])
                userEmail  = aesDecrypt(row[1])

        except Exception, e:
            print repr(e)
            config.conn.rollback()
            flag = 0
        closeConnection()


        #send text
        mobileText = "Dear " + getUserName(self.userID) + ",\n" + config.succesfulLoginMessageText + fetchLocation() + config.messageTextSignature
        client = TwilioRestClient(config.account_sid, config.auth_token)
        message = client.messages.create(to = userMobile, from_ = config.from_number, body = mobileText)

        #send email
        msg = MIMEMultipart()
        msg['From'] = "Team Vigilant Dollop"
        msg['To'] = userEmail
        msg['Subject'] = "Login from Device"
        body_ = "Dear " + getUserName(self.userID) + ",\n" + config.succesfulLoginMessageTextEmail_part1 + fetchLocation()
        body = body_ + config.succesfulLoginMessageTextEmail_part2 + config.succesfulLoginMessageTextEmail_part3 + config.messageTextSignature
        msg.attach(MIMEText(body, 'plain'))

        server = smtplib.SMTP(config.smtp_domain,config.smtp_port)
        server.starttls()
        server.login(config.emailid, config.email_pass)
        text = msg.as_string()
        server.sendmail(config.emailid, userEmail, text)
        server.quit()

    def failedLoginMessage(self):
        establishConnection()
        sql = "SELECT mobile,email FROM user WHERE userid =" + "'" + self.userID + "'"
        #print sql
        try:
            config.statement.execute(sql)
            results = config.statement.fetchall()
            for row in results:
                userMobile = "+91" + aesDecrypt(row[0])
                userEmail  = aesDecrypt(row[1])

        except Exception, e:
            print repr(e)
            config.conn.rollback()
            flag = 0
        closeConnection()

        #send text
        mobileText = "Dear " + getUserName(self.userID) + ",\n" + config.failedLoginMessageText + fetchLocation() + config.failedLoginMessageText_part2 + config.messageTextSignature
        client = TwilioRestClient(config.account_sid, config.auth_token)
        message = client.messages.create(to = userMobile, from_ = config.from_number, body = mobileText)

        #send email
        msg = MIMEMultipart()
        msg['From'] = "Team Vigilant Dollop"
        msg['To'] = userEmail
        msg['Subject'] = "Login from Device"
        body = "Dear " + getUserName(self.userID) + ",\n" + config.failedLoginMessageText +  fetchLocation() + config.failedLoginMessageText_part2 + config.messageTextSignature
        msg.attach(MIMEText(body, 'plain'))

        server = smtplib.SMTP(config.smtp_domain,config.smtp_port)
        server.starttls()
        server.login(config.emailid, config.email_pass)
        text = msg.as_string()
        server.sendmail(config.emailid, userEmail, text)
        server.quit()
