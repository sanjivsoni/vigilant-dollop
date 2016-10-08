from main_class import*
import config



userid = encrypt("bhatshubhs")
pwd = encrypt("123456")
email = encrypt("bhatshubhs12@gmail.com")
s_pwd = "a"
#data = NewUser.getCurrentUser() + "#MAC#Address#->#" + hex(get_mac())
time = currentUTC()

#quer = userid + " " + time + " "+ time + " "+ time + " "+ time + " "+ time + " "+ time + " " + data
quer = userid + " " + pwd + " " + email

#NewUser = User(quer)
#NewUser.createUser()

login = LoginDetails(quer)
#login.userCreated()
login.passwordChanged()
login.updateLogoutTime()
login.updateLastOTPtime()
login.updateFailedLoginTime
login.recordUpdated()

#NewUser.user(quer)
#NewUser.checkUser("bhatshubhs","123456")
