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

def closeConnection():
    config.conn.close()

def createCaptcha():
    #Change the path of font on config file
    image = ImageCaptcha(fonts=[config.fontPath])
    captcha = ''.join(random.choice(string.ascii_lowercase + string.digits) for j in range(6))
    data = image.generate(captcha)
    image.write(captcha, 'captcha.png')

def checkSudoPwd(sudopwd):
    if os.system("echo " + sudopwd + " | sudo -S -v") == 0:
        return 1
    else:
        return 0

def lock(path,encryptedSudoPwd):

    flag = 0
    sudoPwd = aesDecrypt(encryptedSudoPwd)

    command1 = config.changeDirectory + sudoPwd + config.changeOwnerToRoot + path

    if os.system(command1) == 0:
        command2 = config.changeDirectory + sudoPwd + config.lockCommand + path
        if os.system(command2) == 0:
            flag = 1

    return flag

def unlock(path,encryptedSudoPwd):

    flag = 0
    sudoPwd = aesDecrypt(encryptedSudoPwd)

    command1 = config.changeDirectory + sudoPwd + config.unlockCommand + path
    if os.system(command1) == 0:
        command2 = config.changeDirectory + sudoPwd + config.changeOwnerToUser + path
        if os.system(command2) == 0:
            flag = 1

    return flag

def currentUTC():
    return datetime.utcnow().strftime("%Y-%m-%d#%H:%M:%S")

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

def getUserDetails():
    return  "User:" + getpass.getuser() + "#MAC#Address#:#" + hex(get_mac())

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
    establishConnection()
    sql = "SELECT COUNT(*) FROM user"
    flag = 1

    try:
        config.statement.execute(sql)
        results = config.statement.fetchall()
        for row in results:
            if row[0] == 1:
                flag = 0

    except Exception, e:
        print repr(e)
        config.conn.rollback()
        print "error"

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
