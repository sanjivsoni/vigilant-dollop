from helperFunctions import*

'''from UserClass import*
from LoginDetailsClass import*
from AuthenticationClass import*
from UserCredentialsRecoveryClass import *


userid = hashEncrypt("bhatshubhs")
pwd = hashEncrypt("123456")
email = aesEncrypt(config.key,"bhatshubhs12@gmail.com")
mobile = aesEncrypt(config.key,"+919810158269")
sudoPwd = aesEncrypt(pwd,"Macintoshiou")

fname = "shubham"
lname = "bhat"
dob = "26/08/1995"
ssnid = "2ewfrefeg"
ssn_type = "2"
address = "h#no#1696,kngnfmkmfg,gjfngjf,gkfkgj"
pincode = "110081"
country = "india"
ques1 = "3"
ques2 = "7"
ans1 = "hjk"
ans2 = "dfg"
#data = NewUser.getCurrentUser() + "#MAC#Address#->#" + hex(get_mac())
time = currentUTC()

#quer = userid + " " + time + " "+ time + " "+ time + " "+ time + " "+ time + " "+ time + " " + data
quer = userid + " " + pwd + " " + email + " " + mobile + " " + sudoPwd
quer2 = fname + " " +lname + " " +dob + " " +ssnid + " " +ssn_type + " " +address + " " +pincode + " " +country
quer3 = ques1 + " " + ques2 + " " + ans1 + " " + ans2

NewUser = User(quer)
NewUser.createUser()
#NewUser.addSecurityQuestions(quer3)
#print config.db_pass

#au = UserRecovery()
#print au.recoverUserLevel1(1, "+919810158269")
#print au.recoverUserLeveL2("2","2ewfrefeg")
#print au.recoverUserLeveL3("3","hjk")

#NewUser.user(quer)
#NewUser.checkUser("bhatshubhs","123456")

client = TwilioRestClient(config.account_sid, config.auth_token)
message = client.messages.create(to = "+919810030997", from_ = config.from_number, body = config.succesfulLoginMessageText + fetchLocation())
au = LoginDetailsMessages("bhatshubhs")
#au.succesfulLoginMessage()
au.failedLoginMessage()
'''
