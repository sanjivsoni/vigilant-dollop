from libraries import *

class User:

    def __init__(self,userDetails):
        self.userID = (userDetails).split()[0]
        self.userDetails = userDetails

    def createUser(self):

        establishConnection()
        sql = "INSERT INTO user(userid,password,email,mobile,sudoPwd) VALUES" + insertQueryHelper(self.userDetails)

        try:
            config.statement.execute(sql)
            config.conn.commit()
            flag = 1
        except Exception, e:
            print repr(e)
            config.conn.rollback()
            flag = 0
        closeConnection()

    def addPersonalDetails(self,info):

        establishConnection()
        sql = "INSERT INTO user(userid,first_name,last_name,mobile,dob,ssnid,ssn_type,address,pincode,country) VALUES" + info
        try:
            config.statement.execute(sql)
            config.conn.commit()
            flag = 1
        except Exception, e:
            print repr(e)
            config.conn.rollback()
            flag = 0

        closeConnection()

    def verifyMobile(self,case,sendTo):

        if case == 1:
            generatedOTP = generateOTP()
            establishConnection()
            sql = "UPDATE user SET mobileOTP = '" + hashEncrypt(generatedOTP) + "'" + "WHERE userid = " + "'" + self.userID + "'"

            try:
                config.statement.execute(sql)
                config.conn.commit()
                flag = 1
            except Exception, e:
                print repr(e)
                config.conn.rollback()
                flag = 0
            closeConnection()

            client = TwilioRestClient(config.account_sid, config.auth_token)
            message = client.messages.create(to = sendTo, from_ = config.from_number, body = config.mobile_msg + generatedOTP)

    def verifyEmail(self,case,sendTo):
        if case == 1:
            generatedOTP = generateOTP()
            establishConnection()
            sql = "UPDATE user SET emailOTP = '" + hashEncrypt(generatedOTP) + "'" + "WHERE userid = " + "'" + self.userID + "'"

            try:
                config.statement.execute(sql)
                config.conn.commit()
                flag = 1
            except Exception, e:
                print repr(e)
                config.conn.rollback()
                flag = 0
            closeConnection()

            msg = MIMEMultipart()
            msg['From'] = config.emailid
            msg['To'] = sendTo
            msg['Subject'] = config.email_subject
            body = config.email_msg + generatedOTP
            msg.attach(MIMEText(body, 'plain'))

            server = smtplib.SMTP(config.smtp_domain,config.smtp_port)
            server.starttls()
            server.login(config.emailid, config.email_pass)
            text = msg.as_string()
            server.sendmail(config.emailid, sendTo, text)
            server.quit()
