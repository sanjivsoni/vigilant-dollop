
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
emailOtpSubject = "Your Vigilant Dollop OTP"
emailSuccesfulLoginSubject = "Succesful Login"
emailFailedLoginSubject = "Failed Login"
emailPwdChangedSubject = "Password Changed"
emailUsernameChangedSubject = "Username Changed"



#messages
succesfulLoginMessageText = "You have been logged on from "
succesfulLoginMessageTextEmail_part1 = "\nYour Vigilant Dollop account was recently signed in from \n\n"
succesfulLoginMessageTextEmail_part2 = "\n\n\n\nDon't recognise this activity? \n Reveiw your security credentials immediately\n"
succesfulLoginMessageTextEmail_part3 = "\nWhy are we sending this? \nWe take security very seriously and we want to keep you in the loop on important actions in your account."
messageTextSignature = " \n\n\nBest,\nTeam Vigilant Dollop"
passwordChangedText = "Your password has been recently changed from "
usernameChangedText = "Your username has been recently changed from"

failedLoginMessageText = "There was a failed login attempt from "
failedLoginMessageText_part2 = "\n\n\nIf you don't recognise this activity, we urge you to please reveiw your security credentials immediately\n"


#Lock & Unlock commands
changeDirectory = "cd && echo "
changeOwnerToRoot = " | sudo -S chown -R root "
changeOwnerToUser = " | sudo -S chown -R $USER "
lockCommand = "  | sudo -S chmod 000 "
unlockCommand = " | sudo -S chmod 755 "

#path to font
fontPath = '/Library/Fonts/Arial Unicode.ttf'

#global variables
conn=0
statement=0
BLOCK_SIZE = 32

#AES key
key = "*BA@Jy*uHur&v5B7WX%^Ecobv@D&WY#%"

#Secuity_Questions
securityQuestionsPart1 = {1:"Mother's Maiden Name ?",2:"Pet's Name ?",3:"First Teacher's Name ?",4:"Favourite Holiday Destination?"}
securityQuestionsPart2 = {5: "Your Childhood Hero?",6:"Time Of The Day Were You Born ?",7:"The steet you grew up in?",8:"Your Childhood Nickname?"}

#Social Security ID Types
ssnTypes = {1:"Voter ID", 2:"PAN Card", 3:"Aadhaar Card", 4:"Driver's License"}
