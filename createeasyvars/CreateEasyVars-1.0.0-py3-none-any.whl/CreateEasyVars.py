import poetry

def test():
	names = ["admin", "root", "developer", "dev"]
	developername = input("Enter developer name: ")
	if developername not in names:
		print("Invalid login!")
	else:
		passwords = ["admin", "root", "developer", "dev"]
		developerpassword = input("Enter password: ")
		if developerpassword not in passwords:
			print("Invalid password!")
		else:
			print("Test complete!")

def intvar(chislo):
	print("Your int var: " + str(chislo))

def string(stroka):
	print("Your str var: " + stroka)

def boolean(logicbool):
	print("Your bool var: " + str(logicbool))

def help():
	print("Testing commands:")
	print("pypin.test():\nDevelopers names: admin, root, developer, dev\nPassword: admin, root, developer, dev")
	print("---")
	print("Main commands:")
	print("pypin.intvar(var (1, 2, 3, 4 or >))")
	print("pypin.string(\"string (text)\"")
	print("pypin.boolean(True or False)")