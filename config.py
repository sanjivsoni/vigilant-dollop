
#Database Login Credentials
db_hostip	= "127.0.0.1"
db_user 	= "root"
db_pass 	= "mysql9165"
db_name 	= "User"

#Twilio Login Credentials
account_sid = "ACe6460aa2ad312f8e2ab12c3216f943e9"
auth_token = "302d20f8065153b56b8f68160c6c3a75"

#OTP Details
mobile_msg = "Your OneTimePassword(OTP) is "
from_number = "+13343848412"

#Email Details
emailid = "vigilant.dollop@gmail.com"
email_pass = "sanshuabh357"
smtp_domain = "smtp.gmail.com"
smtp_port = 587
email_msg = "Your OneTimePassword(OTP) is "
email_subject = "Your Vigilant Dollop OTP"

#Lock & Unlock commands
changeDirectory = "cd && echo "
changeOwnerToRoot = " | sudo -S chown -R root "
lockCommand = "  | sudo -S chmod 666 "
unlockCommand = " | sudo -S chmod 755 "

#path to font
fontPath = '/Library/Fonts/Arial Unicode.ttf'

#global variables
conn=0
statement=0
BLOCK_SIZE = 32
