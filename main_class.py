from libraries import *


def encryptSudo(key,sudoPwd):

    blockSize = config.BLOCK_SIZE
    PADDING = '{'

    pad = lambda s: s + (blockSize - len(s) % blockSize) * PADDING

    EncryptAES = lambda c, s: base64.b64encode(c.encrypt(pad(s)))

    cipher = AES.new(key[0:16])

    encrypted = EncryptAES(cipher, sudoPwd)
    return encrypted

def decryptSudo(key,encryptedSudoPwd):
    blockSize = config.BLOCK_SIZE
    PADDING = '{'

    DecryptAES = lambda c, e: c.decrypt(base64.b64decode(e)).rstrip(PADDING)

    cipher = AES.new(key[0:16])

    decrypted = DecryptAES(cipher, encryptedSudoPwd)
    return decrypted

def establishConnection():
    global conn
    conn = MySQLdb.connect(config.db_hostip, config.db_user, config.db_pass, config.db_name)
    global statement
    statement = conn.cursor()

def closeConnection():
    global conn
    conn.close()

def createCaptcha():
    #Change the path of font on config file
    image = ImageCaptcha(fonts=[config.fontPath])
    captcha = ''.join(random.choice(string.ascii_lowercase + string.digits) for j in range(6))
    data = image.generate(captcha)
    image.write(captcha, 'captcha.png')

def lock(path,key,encryptedSudoPwd):

    sudoPwd = decryptSudo(key,encryptedSudoPwd)

    command = config.changeDirectory + sudoPwd + config.changeOwnerToRoot + path
    print command
    os.system(command)
    command = config.changeDirectory + sudoPwd + config.lockCommand + path
    print command
    os.system(command)

def unlock(path,key,encryptedSudoPwd):
    sudoPwd = decryptSudo(key,encryptedSudoPwd)

    command = config.changeDirectory + sudoPwd + config.changeOwnerToRoot + path
    os.system(command)
    command = config.changeDirectory + sudoPwd + config.unlockCommand + path
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

def getUserDetails():
    return  "User:" + getpass.getuser() + "#MAC#Address#:#" + hex(get_mac())

def generateOTP():
    return ''.join(random.choice(string.ascii_lowercase + string.digits) for j in range(6))

class User:

    def __init__(self,userDetails):
        self.userID = (userDetails).split()[0]
        self.userDetails = userDetails

    def createUser(self):

        establishConnection()
        sql = "INSERT INTO user(userid,password,email,sudoPwd) VALUES" + insertQueryHelper(self.userDetails)

        try:
            statement.execute(sql)
            conn.commit()
            flag = 1
        except Exception, e:
            print repr(e)
            conn.rollback()
            flag = 0
        closeConnection()

    def addPersonalDetails(self,info):

        establishConnection()
        sql = "INSERT INTO user(userid,first_name,last_name,mobile,dob,ssnid,ssn_type,address,pincode,country) VALUES" + info
        try:
            statement.execute(sql)
            conn.commit()
            flag = 1
        except Exception, e:
            print repr(e)
            conn.rollback()
            flag = 0

        closeConnection()

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

    def checkUser(self):
        correctPassword = ""

        establishConnection()
        sql = "SELECT * FROM user WHERE userid =" + "'" + self.userID + "'"
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
        if (correctPassword == self.userPwd):
            self.userVerifiedLevel1 = True

        closeConnection()

    def sendOTP_mobile(self,case,sendTo):

        if case == 1:
            client = TwilioRestClient(config.account_sid, config.auth_token)
            message = client.messages.create(to = sendTo, from_ = config.from_number, body = config.msg + generateOTP() )

    def sendOTP_email(self,case,sendTo):
        if case == 1:
            msg = MIMEMultipart()
            msg['From'] = config.emailid
            msg['To'] = sendTo
            msg['Subject'] = config.email_subject
            body = config.email_msg + generateOTP()
            msg.attach(MIMEText(body, 'plain'))

            server = smtplib.SMTP(config.smtp_domain,config.smtp_port)
            server.starttls()
            server.login(config.emailid, config.email_pass)
            text = msg.as_string()
            server.sendmail(config.emailid, sendTo, text)
            server.quit()

    def lockItem(self,path):
        if(self.authenticationComplete):
            encryptedSudoPwd = ""
            establishConnection()
            sql = "SELECT sudoPwd FROM user WHERE userid =" + "'" + self.userID + "'"

            try:
                statement.execute(sql)
                results = statement.fetchall()
                for row in results:
                    encryptedSudoPwd = row[0]

            except Exception, e:
                print repr(e)
                conn.rollback()
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
                statement.execute(sql)
                results = statement.fetchall()
                for row in results:
                    encryptedSudoPwd = row[0]

            except Exception, e:
                print repr(e)
                conn.rollback()
                flag = 0

            status = unlock(path,self.userPwd,encryptedSudoPwd)
            closeConnection()



class LoginDetails(User):

    def userCreated(self):
        details = self.userID + " " + currentUTC() + " " + getUserDetails()

        establishConnection()
        sql = "INSERT INTO login_stats(userid,created_at,system_details) VALUES " + insertQueryHelper(details)
        sql = sql.replace("#", " ")
        try:
            statement.execute(sql)
            conn.commit()
            flag = 1
        except Exception, e:
            print repr(e)
            conn.rollback()
            flag = 0

        closeConnection()

    def passwordChanged(self):

        establishConnection()
        sql = "UPDATE login_stats SET pwd_changed_at = '" + currentUTC() + "' " + ",system_details = '" + getUserDetails() + "'"  + " WHERE userid = " + "'" + self.userID + "'"
        sql = sql.replace("#", " ")
        try:
            statement.execute(sql)
            conn.commit()
            print "success"
        except Exception, e:
            print repr(e)
            conn.rollback()
            flag = 0

        closeConnection()

    def recordUpdated(self):

        establishConnection()
        sql = "UPDATE login_stats SET updated_at = '" + currentUTC() + " '" + ",system_details = '" + getUserDetails() + "'"  + "WHERE userid = " + "'" + self.userID + "'"
        sql = sql.replace("#", " ")
        try:
            statement.execute(sql)
            conn.commit()
            print "success"
        except Exception, e:
            print repr(e)
            conn.rollback()
            flag = 0
        closeConnection()

    def updateFailedLoginTime(self):

        establishConnection()
        sql = "UPDATE login_stats SET failed_login_time = '" + currentUTC() + " '" + ",system_details = '" + getUserDetails() + "'"  + "WHERE userid = " + "'" + self.userID + "'"
        sql = sql.replace("#", " ")
        try:
            statement.execute(sql)
            conn.commit()
            print "success"
        except Exception, e:
            print repr(e)
            conn.rollback()
            flag = 0

        closeConnection()

    def updateLogoutTime(self):

        establishConnection()
        sql = "UPDATE login_stats SET logout_time = '" + currentUTC() + " '" + ",system_details = '" + getUserDetails() + "'"  + "WHERE userid = " + "'" + self.userID + "'"
        sql = sql.replace("#", " ")
        try:
            statement.execute(sql)
            conn.commit()
            print "success"
        except Exception, e:
            print repr(e)
            conn.rollback()
            flag = 0

        closeConnection()

    def updateLastOTPtime(self):

        establishConnection()
        sql = "UPDATE login_stats SET last_otp_time = '" + currentUTC() + " '" + ",system_details = '" + getUserDetails() + "'"  + "WHERE userid = " + "'" + self.userID + "'"
        sql = sql.replace("#", " ")
        try:
            statement.execute(sql)
            conn.commit()
            print "success"
        except Exception, e:
            print repr(e)
            conn.rollback()
            flag = 0

        closeConnection()
