from UserClass import User
from libraries import *

class LoginDetails(User):

    def userCreated(self):
        details = self.userID + " " + currentUTC() + " " + getUserDetails()

        establishConnection()
        sql = "INSERT INTO login_stats(userid,created_at,system_details) VALUES " + insertQueryHelper(details)
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
        sql = "UPDATE login_stats SET pwd_changed_at = '" + currentUTC() + "' " + ",system_details = '" + getUserDetails() + "'"  + " WHERE userid = " + "'" + self.userID + "'"
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
        sql = "UPDATE login_stats SET updated_at = '" + currentUTC() + " '" + ",system_details = '" + getUserDetails() + "'"  + "WHERE userid = " + "'" + self.userID + "'"
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
        sql = "UPDATE login_stats SET failed_login_time = '" + currentUTC() + " '" + ",system_details = '" + getUserDetails() + "'"  + "WHERE userid = " + "'" + self.userID + "'"
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
        sql = "UPDATE login_stats SET logout_time = '" + currentUTC() + " '" + ",system_details = '" + getUserDetails() + "'"  + "WHERE userid = " + "'" + self.userID + "'"
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

    def updateMobileLastOTPtime(self):

        establishConnection()
        sql = "UPDATE login_stats SET mobile_last_otp_time = '" + currentUTC() + " '" + ",system_details = '" + getUserDetails() + "'"  + "WHERE userid = " + "'" + self.userID + "'"
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

    def updateEmailLastOTPtime(self):

        establishConnection()
        sql = "UPDATE login_stats SET email_last_otp_time = '" + currentUTC() + " '" + ",system_details = '" + getUserDetails() + "'"  + "WHERE userid = " + "'" + self.userID + "'"
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
