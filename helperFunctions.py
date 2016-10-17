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

def lock(path,encryptedSudoPwd):

    sudoPwd = aesDecrypt(config.key,encryptedSudoPwd)

    command = config.changeDirectory + sudoPwd + config.changeOwnerToRoot + path
    print command
    os.system(command)
    command = config.changeDirectory + sudoPwd + config.lockCommand + path
    print command
    os.system(command)

def unlock(path,encryptedSudoPwd):
    sudoPwd = aesDecrypt(config.key,encryptedSudoPwd)

    command = config.changeDirectory + sudoPwd + config.unlockCommand + path
    os.system(command)
    command = config.changeDirectory + sudoPwd + config.changeOwnerToUser + path
    os.system(command)

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

def generateOTP():
    return ''.join(random.choice(string.digits) for j in range(6))

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
