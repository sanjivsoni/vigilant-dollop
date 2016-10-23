from ..helperFunctions import *

class LoginDetails:

    def __init__(self,userID):
        self.userID = userID

    def userCreated(self):
        aesEncryptedInfo = aesEncrypt(currentUTC() + " " + str(0))
        establishConnection()
        sql = "INSERT INTO login_stats(userid,created_at,loginAttempts) VALUES " + insertQueryHelper(self.userID + " " + aesEncryptedInfo)
        try:
            config.statement.execute(sql)
            config.conn.commit()
            flag = 1
        except Exception, e:
            print repr(e)
            config.conn.rollback()
            flag = 0

        closeConnection()

    def returnLastFailedLoginTime(self):
        establishConnection()
        time = ""
        sql = "SELECT failed_login_time FROM login_stats WHERE userid = " + "'" + self.userID + "'"
        try:
            config.statement.execute(sql)
            results = config.statement.fetchall()
            for row in results:
                time = aesDecrypt(row[0]).replace("#"," ")

        except Exception, e:
            print repr(e)
            config.conn.rollback()
            flag = 0

        closeConnection()

        return convertUTCToLocal(time)

    def fetchAttemptNo(self):
        establishConnection()
        attemptNo = ""

        sql = "SELECT loginAttempts FROM login_stats WHERE userid = " + "'" + self.userID + "'"
        #print sql
        try:
            config.statement.execute(sql)
            results = config.statement.fetchall()
            for row in results:
                attemptNo = int(aesDecrypt(row[0]))

        except Exception, e:
            print repr(e)
            config.conn.rollback()
            flag = 0

        closeConnection()
        return attemptNo

    def updateAttemptNo(self,flag):

        if flag == 1:
            currentAttemptNo = self.fetchAttemptNo()
            newAttemptNo = str(currentAttemptNo + 1)
        else:
            newAttemptNo = str(0)
        establishConnection()
        sql = "UPDATE login_stats SET loginAttempts = '" + aesEncrypt(newAttemptNo) + "'" + "WHERE userid = " + "'" + self.userID + "'"
        try:
            config.statement.execute(sql)
            config.conn.commit()
        except Exception, e:
            print repr(e)
            config.conn.rollback()
            flag = 0
        closeConnection()



    def passwordChanged(self):

        establishConnection()
        sql = "UPDATE login_stats SET pwd_changed_at = '" + aesEncrypt(currentUTC()) + "'" + " WHERE userid = " + "'" + self.userID + "'"
        try:
            config.statement.execute(sql)
            config.conn.commit()
        except Exception, e:
            print repr(e)
            config.conn.rollback()
            flag = 0

        closeConnection()

    def recordUpdated(self):

        establishConnection()
        sql = "UPDATE login_stats SET updated_at = '" + aesEncrypt(currentUTC()) + "'" + "WHERE userid = " + "'" + self.userID + "'"
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
        sql = "UPDATE login_stats SET failed_login_time = '" + aesEncrypt(currentUTC()) + "'" + ",failedLogin_ip = '" + aesEncrypt(getUserIP()) + "'"  + "WHERE userid = " + "'" + self.userID + "'"
        try:
            config.statement.execute(sql)
            config.conn.commit()
        except Exception, e:
            print repr(e)
            config.conn.rollback()
            flag = 0

        closeConnection()

    def updateLoginTime(self):
        establishConnection()
        sql = "UPDATE login_stats SET login_time = '" + aesEncrypt(currentUTC()) + "'" + ",login_ip = '" + aesEncrypt(getUserIP()) + "'"  + "WHERE userid = " + "'" + self.userID + "'"
        #print sql
        try:
            config.statement.execute(sql)
            config.conn.commit()
        except Exception, e:
            print "error in ippp"
            print repr(e)
            config.conn.rollback()
            flag = 0

        closeConnection()

    def fetchLastFailedLoginTime(self):
        establishConnection()
        time = ""
        ip =""
        sql = "SELECT failed_login_time,failedLogin_ip FROM login_stats WHERE userid = " + "'" + self.userID + "'"
        try:
            config.statement.execute(sql)
            results = config.statement.fetchall()
            for row in results:
                time = aesDecrypt(row[0]).replace("#"," ")
                ip = aesDecrypt(row[1])

        except Exception, e:
            print repr(e)
            config.conn.rollback()
            flag = 0

        closeConnection()
        if ip == "":
            ip = "NA"
        return ip + " " + convertUTCToLocal(time)

    def fetchLastSuccessfulLoginTime(self):
        establishConnection()
        time = ""
        ip =""
        sql = "SELECT login_time,login_ip FROM login_stats WHERE userid = " + "'" + self.userID + "'"
        try:
            config.statement.execute(sql)
            results = config.statement.fetchall()
            for row in results:
                time = aesDecrypt(row[0]).replace("#"," ")
                ip = aesDecrypt(row[1])

        except Exception, e:
            print repr(e)
            config.conn.rollback()
            flag = 0

        closeConnection()
        return ip+ " " + convertUTCToLocal(time)

class LoginDetailMessages:
    def __init__(self,userID = ""):
        self.userID = userID

    def loggedIn(self):
        userMobile = ""
        userEmail = ""
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


        sql = "SELECT email FROM user WHERE userid =" + "'" + self.userID + "'"
        try:
            config.statement.execute(sql)
            results = config.statement.fetchall()

            for row in results:
                userEmail = aesDecrypt(row[0])

        except Exception, e:
            print repr(e)
            config.conn.rollback()
            flag = 0


        sendTextMobile(userMobile,config.succesfulLoginMessageText + fetchLocation())
        sendEmail(userEmail,config.succesfulLoginMessageTextEmail_part1 + fetchLocation() + config.succesfulLoginMessageTextEmail_part2 + config.succesfulLoginMessageTextEmail_part3+config.messageTextSignature,config.emailSuccesfulLoginSubject)

    def failedLogin(self):

        userMobile = ""
        userEmail = ""
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


        sql = "SELECT email FROM user WHERE userid =" + "'" + self.userID + "'"
        try:
            config.statement.execute(sql)
            results = config.statement.fetchall()

            for row in results:
                userEmail = aesDecrypt(row[0])

        except Exception, e:
            print repr(e)
            config.conn.rollback()
            flag = 0

        sendTextMobile(userMobile,config.failedLoginMessageText + fetchLocation())
        sendEmail(userEmail,config.failedLoginMessageText + fetchLocation() + config.failedLoginMessageText_part2 + config.messageTextSignature,config.emailFailedLoginSubject)
