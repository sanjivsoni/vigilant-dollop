from src.helperFunctions import*
from src.KivyClasses.LoginProcessClasses import *
from src.KivyClasses.SignUpClass import *
#from libraries import *
Builder.load_file("GUI_builderForm.kv")
Window.size = (700, 700)

screenManager = ScreenManager( transition = FadeTransition() )

if userDoesNotExists():
    screenManager.add_widget(SudoPasswordScreen ( name = 'sudoPasswordScreen' ) )
    screenManager.add_widget( SignupScreen( name = 'signupScreen' ) )

screenManager.add_widget( UsernameScreen( name = 'usernameScreen' ) )
screenManager.add_widget( RecoverScreen( name = 'recoverScreen' ) )
screenManager.add_widget( LevelTwoScreen( name = 'levelTwoScreen' ) )
screenManager.add_widget( HomeScreen( name = 'HomeScreen' ))

class ThreeLevelAuthApp(App):
	def build(self):
		return screenManager

if __name__ == '__main__':
	ThreeLevelAuthApp().run()
