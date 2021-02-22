import os

class Master:
	def __init__(self):
		print("MasterPrograming.com")
		print("--------------------")
	def MPInfo(self):
		print('Welcome To MasterPrograming library 2021')
		print('Master Programing is a PIP Package that enables people that aren’t well to Build Software By Coding.')
		print("----------------------------------")
		print('Objects Names')
		print('MPHindi - For Learning Python')
		print('MPSimpleGui - Tkinter Calculator App')
		print('MPPnr - PNR Checker App')
		print('MPKeyboard - Onscreen Keyboard App')
		print('MPCal - Calculator To Add Numbers')
		print('MPQuiz - Quiz App')
		print('MPSciCal - Scientific Calculator App')
		print('MPApp - Tkinter Login And Signup With Database')
		print('MPTodoApp - Todo list App')


	def MPHindi(self):
		os.system('python PyBasic.py &')

	def MPSimpleGui(self):
		os.system('python tkintersimplegui.py &')

	def MPPnr(self):
		os.system('python pnrgui.py &') 

	def MPKeyboard(self):
		os.system('python keyboard.py &')	

	def MPCal(self):
		os.system('python calgui.py &')

	def MPQuiz(self):
		os.system('python quiz.py &')	

	def MPSciCal(self):
		os.system('python sciencecal.py &')		

	def MPApp(self):
		print("Go To This Link -> https://masterprograming.com/tkinter-login-and-registration-form-with-database/")		
		print('--------------------------------------------------------------------------------------------------')

	def MPTodoApp(self):
		os.system('python todogui.py &')	


if __name__=='__main__':
	c = Master()
	c.MPInfo()
	