from ..helperFunctions import *
from LoginDetailsClass import *

class User:

    def __init__(self,userDetails):
        self.userID = hashEncrypt((userDetails).split()[0])
        self.pwd = hashEncrypt((userDetails).split()[1])
        self.userDetails = userDetails


    def createUser(self,info):
        aesEncryptedInfo = aesEncrypt(info)
        establishConnection()
        sql = "INSERT INTO user(userid,password,email,mobile,sudoPwd) VALUES" + insertQueryHelper(self.userID + " " + self.pwd + " " +  aesEncryptedInfo)
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
