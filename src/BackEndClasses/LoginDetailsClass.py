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
        except (AttributeError, MySQLdb.OperationalError):
            print "Reconnecting"
            establishConnection()
            config.statement.execute(sql)
            config.conn.commit()

        closeConnection()

    def returnLastFailedLoginTime(self):
        establishConnection()
        time = ""
        sql = "SELECT failed_login_time FROM login_stats WHERE userid = " + "'" + self.userID + "'"
        try:
            config.statement.execute(sql)
            results = config.statement.fetchall()
            for row in results:
                if row[0] == "0":
                    time = "0"
                else:
                    time = aesDecrypt(row[0]).replace("#"," ")

        except (AttributeError, MySQLdb.OperationalError):
            print "Reconnecting"
            establishConnection()
            config.statement.execute(sql)
            results = config.statement.fetchall()
            for row in results:
                time = aesDecrypt(row[0]).replace("#"," ")

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

        except (AttributeError, MySQLdb.OperationalError):
            print "Reconnecting"
            establishConnection()
            config.statement.execute(sql)
            results = config.statement.fetchall()
            for row in results:
                attemptNo = int(aesDecrypt(row[0]))

        closeConnection()
        #print "Current Attempt in DB ->" , attemptNo 
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

        except (AttributeError, MySQLdb.OperationalError):
            print "Reconnecting"
            establishConnection()
            config.statement.execute(sql)
            config.conn.commit()

        closeConnection()

    def passwordChanged(self):

        establishConnection()
        sql = "UPDATE login_stats SET pwd_changed_at = '" + aesEncrypt(currentUTC()) + "'" + " WHERE userid = " + "'" + self.userID + "'"
        try:
            config.statement.execute(sql)
            config.conn.commit()
        except (AttributeError, MySQLdb.OperationalError):
            print "Reconnecting"
            establishConnection()
            config.statement.execute(sql)
            config.conn.commit()

        closeConnection()

    def recordUpdated(self):

        establishConnection()
        sql = "UPDATE login_stats SET updated_at = '" + aesEncrypt(currentUTC()) + "'" + "WHERE userid = " + "'" + self.userID + "'"
        try:
            config.statement.execute(sql)
            config.conn.commit()

        except (AttributeError, MySQLdb.OperationalError):
            print "Reconnecting"
            establishConnection()
            config.statement.execute(sql)
            config.conn.commit()

        closeConnection()

    def updateFailedLoginTime(self):

        conn = MySQLdb.connect(config.db_hostip, config.db_user, config.db_pass, config.db_name)
        statement = conn.cursor()
        sql = "UPDATE login_stats SET failed_login_time = '" + aesEncrypt(currentUTC()) + "'" + ",failedLogin_ip = '" + aesEncrypt(getUserIP()) + "'"  + "WHERE userid = " + "'" + self.userID + "'"
        try:
            statement.execute(sql)
            conn.commit()
            print "Failed Login Time updated"
        except (AttributeError, MySQLdb.OperationalError):
            print "Reconnecting"
            conn = MySQLdb.connect(config.db_hostip, config.db_user, config.db_pass, config.db_name)
            statement = conn.cursor()
            statement.execute(sql)
            conn.commit()

        if conn.open:
            conn.close()

    def updateLoginTime(self):
        establishConnection()
        sql = "UPDATE login_stats SET login_time = '" + aesEncrypt(currentUTC()) + "'" + ",login_ip = '" + aesEncrypt(getUserIP()) + "'"  + "WHERE userid = " + "'" + self.userID + "'"
        #print sql
        try:
            config.statement.execute(sql)
            config.conn.commit()
            print "Login Time updated"
        except (AttributeError, MySQLdb.OperationalError):
            print "Reconnecting"
            establishConnection()
            config.statement.execute(sql)
            config.conn.commit()
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
                if row[0] == "0":
                    time = "0"
                    ip = "0"
                else:
                    time = aesDecrypt(row[0]).replace("#"," ")
                    ip = aesDecrypt(row[1])

        except (AttributeError, MySQLdb.OperationalError):
            print "Reconnecting"
            establishConnection()
            config.statement.execute(sql)
            results = config.statement.fetchall()
            for row in results:
                if row[0] == "0":
                    time = "0"
                    ip = "0"
                else:
                    time = aesDecrypt(row[0]).replace("#"," ")
                    ip = aesDecrypt(row[1])


        closeConnection()
        if ip == "0":
            ip = "NA"
        return ip + " " + convertUTCToLocal(time)

    def fetchLastSuccessfulLoginTime(self):
        establishConnection()
        time = ""
        ip =""
        sql = "SELECT login_time,login_ip FROM login_stats WHERE userid = " + "'" + self.userID + "'"
        #print sql
        try:
            config.statement.execute(sql)
            results = config.statement.fetchall()
            for row in results:
                if row[0] == "0":
                    time = "0"
                    ip = "0"
                else:
                    time = aesDecrypt(row[0]).replace("#"," ")
                    ip = aesDecrypt(row[1])

        except (AttributeError, MySQLdb.OperationalError):
            print "Reconnecting"
            establishConnection()
            config.statement.execute(sql)
            results = config.statement.fetchall()
            for row in results:
                if row[0] == "0":
                    time = "0"
                    ip = "0"
                else:
                    time = aesDecrypt(row[0]).replace("#"," ")
                    ip = aesDecrypt(row[1])

        closeConnection()
        if ip == "0":
            ip = "NA"

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

        except (AttributeError, MySQLdb.OperationalError):
            print "Reconnecting"
            establishConnection()
            config.statement.execute(sql)
            results = config.statement.fetchall()
            for row in results:
                userMobile = aesDecrypt(row[0])


        sql = "SELECT email FROM user WHERE userid =" + "'" + self.userID + "'"
        try:
            config.statement.execute(sql)
            results = config.statement.fetchall()

            for row in results:
                userEmail = aesDecrypt(row[0])

        except (AttributeError, MySQLdb.OperationalError):
            print "Reconnecting"
            establishConnection()
            config.statement.execute(sql)
            results = config.statement.fetchall()
            for row in results:
                userEmail = aesDecrypt(row[0])

        closeConnection()


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

        except (AttributeError, MySQLdb.OperationalError):
            print "Reconnecting"
            establishConnection()
            config.statement.execute(sql)
            results = config.statement.fetchall()
            for row in results:
                userMobile = aesDecrypt(row[0])


        sql = "SELECT email FROM user WHERE userid =" + "'" + self.userID + "'"
        try:
            config.statement.execute(sql)
            results = config.statement.fetchall()

            for row in results:
                userEmail = aesDecrypt(row[0])

        except (AttributeError, MySQLdb.OperationalError):
            print "Reconnecting"
            establishConnection()
            config.statement.execute(sql)
            results = config.statement.fetchall()
            for row in results:
                userEmail = aesDecrypt(row[0])

        closeConnection()

        sendTextMobile(userMobile,config.failedLoginMessageText + fetchLocation())
        sendEmail(userEmail,config.failedLoginMessageText + fetchLocation() + config.failedLoginMessageText_part2 + config.messageTextSignature,config.emailFailedLoginSubject)
