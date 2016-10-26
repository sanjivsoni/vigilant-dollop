from libraries import *

def aesEncrypt(plaintextArray):

    plaintexts = plaintextArray.split()
    totalWords = len(plaintexts)
    encrypted = ""

    blockSize = config.BLOCK_SIZE
    PADDING = '{'

    pad = lambda s: s + (blockSize - len(s) % blockSize) * PADDING

    EncryptAES = lambda c, s: base64.b64encode(c.encrypt(pad(s)))

    cipher = AES.new(config.key[0:16])

    for i in plaintexts:
        encrypted = encrypted + " " + EncryptAES(cipher,i)

    return encrypted.strip()

def aesDecrypt(encryptedText):
    blockSize = config.BLOCK_SIZE
    PADDING = '{'

    DecryptAES = lambda c, e: c.decrypt(base64.b64decode(e)).rstrip(PADDING)

    cipher = AES.new(config.key[0:16])

    decrypted = DecryptAES(cipher, encryptedText)
    return decrypted

def establishConnection():
    config.conn = MySQLdb.connect(config.db_hostip, config.db_user, config.db_pass, config.db_name)
    config.statement = config.conn.cursor()
    #print "connected"

def closeConnection():
    if config.conn.open:
        config.conn.close()
    #print "disconnected"

def createCaptcha():
    #Change the path of font on config file
    image = ImageCaptcha(fonts=[config.fontPath])
    captcha = ''.join(random.choice(string.digits) for j in range(4))
    print "captcha ", captcha
    image.write(captcha, 'src/images/captcha.jpg')
    return captcha

def checkSudoPwd(sudopwd):
    status = os.system("echo " + sudopwd + " | sudo -S -v")
    if status == 0:
        return 1
    else:
        return 0

def lock(path,encryptedSudoPwd):
    flag = 0
    sudoPwd = aesDecrypt(encryptedSudoPwd)
    path = path.replace(" ", "\ ")
    command1 = config.changeDirectory + sudoPwd + config.changeOwnerToRoot + path
    if os.system(command1) == 0:
        command2 = config.changeDirectory + sudoPwd + config.lockCommand + path
        if os.system(command2) == 0:
            flag = 1

    return flag

def unlock(path,encryptedSudoPwd):

    flag = 0
    sudoPwd = aesDecrypt(encryptedSudoPwd)
    path = path.replace(" ", "\ ")
    print path
    command1 = config.changeDirectory + sudoPwd + config.unlockCommand + path
    if os.system(command1) == 0:
        command2 = config.changeDirectory + sudoPwd + config.changeOwnerToUser + path
        if os.system(command2) == 0:
            flag = 1

    return flag

def currentUTC():
    return datetime.datetime.utcnow().strftime("%d-%m-%Y#%H:%M:%S")

def convertUTCToLocal(utcTime):

    if utcTime == "0":
        return "-" + " -"

    else:
        utcTimeZone = tz.tzutc()
        localTimezone = tz.tzlocal()

        utc = datetime.datetime.strptime(utcTime,'%d-%m-%Y %H:%M:%S')

        utc = utc.replace(tzinfo = utcTimeZone)
        localTime = utc.astimezone(localTimezone)

        return str(localTime.strftime("%d-%m-%Y %H:%M:%S"))

def hashEncrypt(plaintext):
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

def getUserIP():
    send_url = 'http://freegeoip.net/json'
    r = requests.get(send_url)
    j = json.loads(r.text)
    details =  j['ip']
    return details

def generateOTP(length):
    if length == 6:
        return ''.join(random.choice(string.ascii_lowercase + string.digits) for j in range(6))
    elif length == 2:
        return ''.join(random.choice(string.ascii_lowercase) for j in range(2))
    else:
        return ''.join(random.choice(string.ascii_lowercase + string.digits) for j in range(4))

def fetchLocation():
    send_url = 'http://freegeoip.net/json'
    r = requests.get(send_url)
    j = json.loads(r.text)
    details = "\nIP address: " + j['ip'] + "\n" + "Location: " + j['city'] + "," + j['region_name'] + "," + j['country_name']
    return details

def getUserName(userID):

    establishConnection()
    sql = "SELECT first_name FROM personal WHERE userid =" + "'" + userID + "'"
    #print sql
    try:
        config.statement.execute(sql)
        results = config.statement.fetchall()
        for row in results:
            userName = aesDecrypt(row[0])

    except Exception, e:
        print repr(e)
        config.conn.rollback()
        flag = 0

    closeConnection()
    return userName

def fetchSecurityQuestionPart1():
    securityQues = "["
    for i in range(1,5):
        securityQues = securityQues +  "'" + config.securityQuestionsPart1[i] + "'" + ","

    return securityQues[:-1] + "]"

def fetchSecurityQuestionPart2():
    securityQues = "["
    for i in range(5,9):
        securityQues = securityQues +  "'" + config.securityQuestionsPart2[i] + "'" + ","

    return securityQues[:-1] + "]"

def userDoesNotExists():
    print "Checking if user exists"
    establishConnection()
    sql = "SELECT COUNT(*) FROM user"
    flag = 1

    try:
        config.statement.execute(sql)
        results = config.statement.fetchall()
        for row in results:
            if row[0] == 1:
                flag = 0
                print "User Exists"
            else:
                print "User doesn't Exists"

    except Exception, e:
        print repr(e)
        config.conn.rollback()
        print "error"
    closeConnection()

    return flag


def runByThreadForEmail(*kargs):
    thread1 = Thread(target = kargs[0], args = (kargs[1],kargs[2],kargs[3],))
    thread1.start()

def runByThreadForMobile(*kargs):
    thread1 = Thread(target = kargs[0], args = (kargs[1],kargs[2],))
    thread1.start()

def sendTextMobile(sendTo,msg):
    client = TwilioRestClient(config.account_sid, config.auth_token)
    message = client.messages.create(to = sendTo, from_ = config.from_number, body = msg)
    print "Mobile OTP Sent"

def sendEmail(sendTo,message,subject):

    msg = MIMEMultipart()
    msg['From'] = "Team Vigilant Dollop"
    msg['To'] = sendTo
    msg['Subject'] = subject
    body = message
    msg.attach(MIMEText(body, 'plain'))

    server = smtplib.SMTP(config.smtp_domain,config.smtp_port)
    server.starttls()
    server.login(config.emailid, config.email_pass)
    text = msg.as_string()
    server.sendmail(config.emailid, sendTo, text)
    server.quit()
    print "Email OTP Sent"

def currentAttemptNo(updateLoginDetails):
    return updateLoginDetails.fetchAttemptNo()

def updateAttemptNo(updateLoginDetails,flag):
    updateLoginDetails.updateAttemptNo(flag)

def calculateRetryTime(updateLoginDetails):
    if updateLoginDetails.returnLastFailedLoginTime() == "- -":
        return -1
    else:
        lastFailedLoginDatetime = datetime.datetime.strptime(updateLoginDetails.returnLastFailedLoginTime(),'%d-%m-%Y %H:%M:%S')
        print lastFailedLoginDatetime
        currentDatetime = datetime.datetime.strptime(datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S"),"%d-%m-%Y %H:%M:%S")
        print currentDatetime

        timeDifference = currentDatetime - lastFailedLoginDatetime

        if(timeDifference.days > 0):
            return 0

        elif(timeDifference.seconds > 300):
            return 0

        else:
            return 300 - timeDifference.seconds

def checkAttemptsStatus(updateLoginDetails,loginMsgs):

    if currentAttemptNo(updateLoginDetails) < 3:
        # Unsuccessful match for Password
        updateAttemptNo(updateLoginDetails,1)
        status = -1 * int(currentAttemptNo(updateLoginDetails))
        print "currentAttemptNoA",currentAttemptNo(updateLoginDetails)
        thread1 = Thread(target = updateLoginDetails.updateFailedLoginTime)
        thread1.start()

    else:
        print "3 attempts over"
        #thread1 = Thread(target=loginMsgs.failedLogin)
        #thread1.start()
        print "currentAttemptNoB",currentAttemptNo(updateLoginDetails)
        status  = calculateRetryTime(updateLoginDetails)
        if status == 0:
            updateLoginDetails.updateFailedLoginTime()

    return status
