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
