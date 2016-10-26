from src.helperFunctions import*
from src.KivyClasses.LoginProcessClasses import *
from src.KivyClasses.SignUpClass import *
#from libraries import *

Config.set('kivy', 'log_level', 'critical')
Config.write()

Window.size = (700, 700)

screenManager = ScreenManager( transition = FadeTransition() )

choice = 10

if choice == 1:
    screenManager.add_widget(SudoPasswordScreen ( name = 'sudoPasswordScreen' ) )
elif choice == 2:
    screenManager.add_widget( SignupScreen( name = 'signupScreen' ) )
elif choice == 3:
    screenManager.add_widget( UsernameScreen( name = 'usernameScreen' ) )
elif choice == 4:
    screenManager.add_widget( RecoverScreen( name = 'recoverScreen' ) )
elif choice == 5:
    screenManager.add_widget( LevelTwoScreen( name = 'levelTwoScreen' ) )
elif choice == 6:
    screenManager.add_widget( HomeScreen( name = 'HomeScreen' ))
elif choice == 7:
    screenManager.add_widget( Reset( name = 'ChangeDetailsScreen' ))
elif choice == 8:
    screenManager.add_widget( OtpVerification( name = 'OTPVerification' ))
elif choice == 9:
    screenManager.add_widget(SudoPasswordScreen ( name = 'sudoPasswordScreen' ) )
    screenManager.add_widget( SignupScreen( name = 'signupScreen' ) )
    screenManager.add_widget( OtpVerification( name = 'OTPVerification' ))
    screenManager.add_widget( UsernameScreen( name = 'usernameScreen' ) )
    screenManager.add_widget( RecoverScreen( name = 'recoverScreen' ) )
    screenManager.add_widget( LevelTwoScreen( name = 'levelTwoScreen' ) )
    screenManager.add_widget( HomeScreen( name = 'HomeScreen' ))
    screenManager.add_widget( Reset( name = 'ChangeDetailsScreen' ))

else:

    if userDoesNotExists():
        screenManager.add_widget(SudoPasswordScreen ( name = 'sudoPasswordScreen' ) )
        screenManager.add_widget( SignupScreen( name = 'signupScreen' ) )
        #screenManager.add_widget( OtpVerification( name = 'OTPVerification' ))
    screenManager.add_widget( UsernameScreen( name = 'usernameScreen' ) )
    screenManager.add_widget( OtpVerification( name = 'OTPVerification' ))
    screenManager.add_widget( RecoverScreen( name = 'recoverScreen' ) )
    screenManager.add_widget( LevelTwoScreen( name = 'levelTwoScreen' ) )
    screenManager.add_widget( HomeScreen( name = 'HomeScreen' ))
    screenManager.add_widget( Reset( name = 'ChangeDetailsScreen' ))


class ThreeLevelAuthApp(App):
	def build(self):
		return screenManager

if __name__ == '__main__':
	ThreeLevelAuthApp().run()
