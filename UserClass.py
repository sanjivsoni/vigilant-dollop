from helperFunctions import *

class User:

    def __init__(self,userDetails):
        self.userID = (userDetails).split()[0]
        self.userDetails = userDetails

    def createUser(self):

        establishConnection()
        sql = "INSERT INTO user(userid,password,email,mobile,sudoPwd) VALUES" + insertQueryHelper(self.userDetails)

        try:
            config.statement.execute(sql)
            config.conn.commit()
            flag = 1
        except Exception, e:
            print repr(e)
            config.conn.rollback()
            flag = 0
        closeConnection()

    def addPersonalDetails(self,info):

        encryptedInfo = aesEncrypt(config.key,info)
        establishConnection()
        sql = "INSERT INTO personal(userid,first_name,last_name,dob,ssnid,ssn_type,address,pincode,country) VALUES" + insertQueryHelper(self.userID + " " + encryptedInfo)
        print sql
        try:
            config.statement.execute(sql)
            config.conn.commit()
            flag = 1
        except Exception, e:
            print repr(e)
            config.conn.rollback()
            flag = 0

        closeConnection()

    def addSecurityQuestions(self,info):

        encryptedInfo = aesEncrypt(config.key,info)
        establishConnection()
        sql = "INSERT INTO security_ques(userid,ques1,ques2,ans1,ans2) VALUES" + insertQueryHelper(self.userID + " " + encryptedInfo)
        try:
            config.statement.execute(sql)
            config.conn.commit()
            flag = 1
        except Exception, e:
            print repr(e)
            config.conn.rollback()
            flag = 0

        closeConnection()
