from libraries import *

#Databse Connection
conn = MySQLdb.connect(config.db_hostip, config.db_user, config.db_pass, config.db_name)
statement = conn.cursor()


def lock(path):
    command = config.lockCommand + path
    os.system(command)

def unlock(path):
    command = config.unlockCommand + path
    os.system(command)

def currentUTC():
    return datetime.utcnow().strftime("%Y-%m-%d#%H:%M:%S")

def encrypt(plaintext):
    encryptedText = SHA256.new(plaintext)
    return encryptedText.hexdigest()

def insertQueryHelper(raw):
    processed = "('"
    splitarray = raw.split()
    for i in splitarray:
        processed = processed + i +"','"
    processed = processed + "')"
    processed= processed.replace("','')","')")
    return processed


class User:

    def sendOTP_mobile(self,case,sendTo):
        if case == 1:
            client = TwilioRestClient(config.account_sid, config.auth_token)
            message = client.messages.create(to = sendTo, from_ = config.from_number, body = config.msg )

    def sendOTP_email(self,case,sendTo):
        if case == 1:
            msg = MIMEMultipart()
            msg['From'] = config.emailid
            msg['To'] = sendTo
            msg['Subject'] = config.email_subject
            body = config.email_msg
            msg.attach(MIMEText(body, 'plain'))

            server = smtplib.SMTP(config.smtp_domain,config.smtp_port)
            server.starttls()
            server.login(config.emailid, config.email_pass)
            text = msg.as_string()
            server.sendmail(config.emailid, sendTo, text)
            server.quit()


    def getCurrentUser(self):
        return getpass.getuser()

    def checkUser(self,userid,password):
        encryptedUserid = encrypt(userid)
        encryptedPassword = encrypt(password)
        correctPassword = "0"

        sql = "SELECT * FROM user WHERE userid =" + "'" + encryptedUserid + "'"
        print sql

        try:
            statement.execute(sql)
            results = statement.fetchall()
            for row in results:
                correctPassword = row[1]

        except Exception, e:
            print repr(e)
            conn.rollback()
            flag = 0
        if (correctPassword == encryptedPassword):
            print "yes"
        else:
            print "no"




    def user(self,userDetails):

        sql = "INSERT INTO user(userid,password,email) VALUES" + userDetails
        #print sql;

        try:
            statement.execute(sql)
            conn.commit()
            flag = 1
        except Exception, e:
            print repr(e)
            conn.rollback()
            flag = 0

    def personalDetails(self,info):

        sql = "INSERT INTO user(userid,first_name,last_name,mobile,dob,ssnid,ssn_type,address,pincode,country) VALUES" + info
        try:
            statement.execute(sql)
            conn.commit()
            flag = 1
        except Exception, e:
            print repr(e)
            conn.rollback()
            flag = 0

    def loginStats(self,info):

        sql = "INSERT INTO login_stats(userid,created_at,pwd_changed_at,failed_login_time,updated_at,logout_time,last_otp_time,system_details) VALUES" + info
        sql = sql.replace("#", " ")
        print sql
        try:
            statement.execute(sql)
            conn.commit()
            flag = 1
        except Exception, e:
            print repr(e)
            conn.rollback()
            flag = 0
