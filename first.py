from libraries import*


userid = hashEncrypt("bhatshubhs")
pwd = hashEncrypt("123456")
email = aesEncrypt(userid,"bhatshubhs12@gmail.com")
mobile = aesEncrypt(userid,"+919810158269")
sudoPwd = aesEncrypt(userid,"Macintoshiou")
#data = NewUser.getCurrentUser() + "#MAC#Address#->#" + hex(get_mac())
time = currentUTC()

#quer = userid + " " + time + " "+ time + " "+ time + " "+ time + " "+ time + " "+ time + " " + data
quer = userid + " " + pwd + " " + email + " " + mobile + " " + sudoPwd

#NewUser = User(quer)
#NewUser.createUser()

au = Authentication(quer)
au.sendOTP_email(1)
#au.checkUserLevel2(2,'yc60ns')
#au.unlockItem("Desktop/Images")

#NewUser.user(quer)
#NewUser.checkUser("bhatshubhs","123456")'''
