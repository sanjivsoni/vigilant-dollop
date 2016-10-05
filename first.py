from main_class import*
import config


NewUser = User()

userid = encrypt("bhatshubhs")
pwd = encrypt("123456")
email = encrypt("bhatshubhs12@gmail.com")
s_pwd = "a"
data = getpass.getuser() + "#MAC#Address#->#" + hex(get_mac())
time = currentUTC()

quer = userid + " " + time + " "+ time + " "+ time + " "+ time + " "+ time + " "+ time + " " + data
q = insertQueryHelper(quer)


NewUser.loginStats(q)
