#for Database
import MySQLdb

#Hashing Encryption
from Crypto.Hash import SHA256

#for UTC time
from datetime import datetime

#to get current user
import getpass
from uuid import getnode as get_mac

import config

conn = MySQLdb.connect(config.DB_HOSTIP, config.DB_USER, config.DB_PASS, config.DB_NAME)      #Establish Connection with DB
statement = conn.cursor()



def getCurrentUser():
    return getpass.getuser()

def currentUTC():
    return datetime.utcnow().strftime("%Y-%m-%d#%H:%M:%S")



def encrypt(plaintext):
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



class User:

    def user(self,userDetails):

        sql = "INSERT INTO user(userid,password,alternate_pwd,email,otp) VALUES" + userDetails
        print sql;

        try:
            statement.execute(sql)
            conn.commit()
            flag = 1
        except Exception, e:
            print repr(e)
            conn.rollback()
            flag = 0

    def personalDetails(self,info):

        sql = "INSERT INTO user(userid,first_name,last_name,mobile,dob,ssnid,ssn_type,address,pincode,country) VALUES" + info
        try:
            statement.execute(sql)
            conn.commit()
            flag = 1
        except Exception, e:
            print repr(e)
            conn.rollback()
            flag = 0

    def loginStats(self,info):

        sql = "INSERT INTO login_stats(userid,created_at,pwd_changed_at,failed_login_time,updated_at,logout_time,last_otp_time,system_details) VALUES" + info
        sql = sql.replace("#", " ")
        print sql
        try:
            statement.execute(sql)
            conn.commit()
            flag = 1
        except Exception, e:
            print repr(e)
            conn.rollback()
            flag = 0
