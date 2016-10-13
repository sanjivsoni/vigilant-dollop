from helperFunctions import*

from UserClass import*
from LoginDetailsClass import*
from AuthenticationClass import*

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
#data = NewUser.getCurrentUser() + "#MAC#Address#->#" + hex(get_mac())
time = currentUTC()

#quer = userid + " " + time + " "+ time + " "+ time + " "+ time + " "+ time + " "+ time + " " + data
quer = userid + " " + pwd + " " + email + " " + mobile + " " + sudoPwd
quer2 = fname + " " +lname + " " +dob + " " +ssnid + " " +ssn_type + " " +address + " " +pincode + " " +country


#NewUser = User(quer)
#NewUser.addPersonalDetails(quer2)
#print config.db_pass

au = OTP(userid)
au.sendOTPforAuth_mobile()

#NewUser.user(quer)
#NewUser.checkUser("bhatshubhs","123456")'''
