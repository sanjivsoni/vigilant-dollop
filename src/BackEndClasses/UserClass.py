from ..helperFunctions import *
from LoginDetailsClass import *

class User:

    def __init__(self,userDetails):
        self.userID = hashEncrypt((userDetails).split()[0])
        self.pwd = hashEncrypt((userDetails).split()[1])
        self.userDetails = userDetails


    def createUser(self,info):
        ifContactVerified = str(0)
        aesEncryptedInfo = aesEncrypt(info + " " + ifContactVerified)
        establishConnection()
        sql = "INSERT INTO user(userid,password,email,mobile,sudoPwd,contactVerified) VALUES" + insertQueryHelper(self.userID + " " + self.pwd + " " +  aesEncryptedInfo)
        #print sql
        try:
            config.statement.execute(sql)
            config.conn.commit()
            flag = 1
        except Exception, e:
            print repr(e)
            config.conn.rollback()
            print "Error in create user"
        closeConnection()

    def addPersonalDetails(self,info):

        aesEncryptedInfo = aesEncrypt(info)
        establishConnection()
        sql = "INSERT INTO personal(userid,first_name,last_name,dob,ssn_type,ssnid) VALUES" + insertQueryHelper(self.userID + " " + aesEncryptedInfo)
        #print sql
        try:
            config.statement.execute(sql)
            config.conn.commit()
            flag = 1
        except Exception, e:
            print repr(e)
            config.conn.rollback()
            flag = 0
            print "Error in add personal details"

        closeConnection()

    def addSecurityQuestions(self,info):

        aesEncryptedInfo = aesEncrypt(info)
        establishConnection()
        sql = "INSERT INTO security_ques(userid,ques1,ques2,ans1,ans2) VALUES" + insertQueryHelper(self.userID + " " + aesEncryptedInfo)
        try:
            config.statement.execute(sql)
            config.conn.commit()
            flag = 1
        except Exception, e:
            print repr(e)
            config.conn.rollback()
            flag = 0
            print "Error in security q"

        closeConnection()

    def updateUserContactDetails(self,flag,newContact):
        checkFlag = 0
        establishConnection()
        if flag == 0:
            sql = "UPDATE user SET mobile = '" + aesEncrypt(newContact) + "'"  + "WHERE userid = " + "'" + self.userID + "'"
        elif flag == 1:
            sql = "UPDATE user SET email = '" + aesEncrypt(newContact) + "'"  + "WHERE userid = " + "'" + self.userID + "'"
        elif flag == 2:
            sql = "UPDATE user SET email = '" + aesEncrypt(newContact.split()[0]) + "', mobile = '" + aesEncrypt(newContact.split()[1]) + "'"   + " WHERE userid = " + "'" + self.userID + "'"

        try:
            config.statement.execute(sql)
            config.conn.commit()
            checkFlag = 1

        except Exception, e:
            print repr(e)
            config.conn.rollback()
            checkFlag = 0


        closeConnection()

        return checkFlag

class VerifyUserCredentials:

    def __init__(self,userid):
        self.userID = hashEncrypt(userid)

    def fetchUserContactDetails(self):

        userMobile = ""
        userEmail = ""

        establishConnection()

        sql = "SELECT email,mobile from user WHERE userid = '" + self.userID + "'"
        #print sql

        try:
            config.statement.execute(sql)
            results = config.statement.fetchall()
            for row in results:
                userEmail = aesDecrypt(row[0])
                userMobile = aesDecrypt(row[1])

        except Exception, e:
            print repr(e)
            config.conn.rollback()

        closeConnection()
        return userEmail + " " + userMobile

    def setContactVerificationStatus(self):
        establishConnection()

        sql = "UPDATE user SET contactVerified = '" + aesEncrypt(str(1)) + "' WHERE userid = '" + self.userID + "'"
        print sql

        try:
            config.statement.execute(sql)
            config.conn.commit()
        except Exception, e:
            print repr(e)
            config.conn.rollback()

        closeConnection()

    def getContactVerificationStatus(self):

        status = ""
        establishConnection()

        sql = "SELECT contactVerified from user WHERE userid = '" + self.userID + "'"

        try:
            config.statement.execute(sql)
            results = config.statement.fetchall()
            for row in results:
                status = int(aesDecrypt(row[0]))

        except Exception, e:
            print repr(e)
            config.conn.rollback()

        closeConnection()

        print "status", status
        return status
