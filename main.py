from src.helperFunctions import*
from src.KivyClasses.LoginProcessClasses import *
from src.KivyClasses.SignUpClass import *
#from libraries import *

Builder.load_file("GUI_builderForm.kv")
Window.size = (700, 700)
screenManager = ScreenManager( transition = FadeTransition() )
#screenManager.add_widget( SignupScreen( name = 'signupScreen' ) )
screenManager.add_widget( UsernameScreen( name = 'usernameScreen' ) )
screenManager.add_widget( LevelOneScreen( name = 'levelOneScreen' ) )
'''screenManager.add_widget( LevelTwoScreen( name = 'levelTwoScreen' ) )
screenManager.add_widget( LevelThreeScreen( name = 'levelThreeScreen' ) )
screenManager.add_widget( RecoveryLevelTwoScreen( name = 'recoverylevelTwoScreen' ) )
screenManager.add_widget( UsernameRecover( name = 'usernameRecoverScreen' ) )
screenManager.add_widget( PasswordRecover( name = 'passwordRecoverScreen' ) )
screenManager.add_widget( UserRecoveryLevelThreeScreen( name = 'userrecoverylevelThreeScreen' ) )
screenManager.add_widget( PasswordRecoveryLevelThreeScreen( name = 'passwordrecoverylevelThreeScreen' ) )
screenManager.add_widget( RecoverySecQuestion( name = 'recoverysecQuestion' ) )
screenManager.add_widget( PasswordReset( name = 'passwordReset' ) )
screenManager.add_widget( HomeScreen( name = 'homeScreen' ) )'''

class ThreeLevelAuthApp(App):
	def build(self):
		return screenManager

if __name__ == '__main__':
	ThreeLevelAuthApp().run()

#values: "Your Childhood Hero?", "Time Of The Day Were You Born ?", "The steet you grew up in?", "Your Childhood Nickname?"
#values: "Mother's Maiden Name ?", "Pet's Name ?", "First Teacher's Name ?", "Favourite Holiday Destination?"
