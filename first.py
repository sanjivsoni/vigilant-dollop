from main_class import*
import config



userid = encrypt("bhatshubhs")
pwd = encrypt("123456")
email = encrypt("bhatshubhs12@gmail.com")
sudoPwd = "Macintoshiou"
#data = NewUser.getCurrentUser() + "#MAC#Address#->#" + hex(get_mac())
time = currentUTC()

#quer = userid + " " + time + " "+ time + " "+ time + " "+ time + " "+ time + " "+ time + " " + data
quer = userid + " " + pwd + " " + email + " " + encryptSudo(pwd,sudoPwd)

#NewUser = User(quer)
#NewUser.createUser()

au = Authentication(quer)
au.unlockItem("Desktop/Images")

#NewUser.user(quer)
#NewUser.checkUser("bhatshubhs","123456")'''
