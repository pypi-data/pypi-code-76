logins = ["api", "tikot", "developer", "dev", "tikotshop"]
passwords = ["pass", "p", "api", "tikotshop", "developer", "dev", "tikot"]
services = ["tikot shop", "developer console"]
raitings = ["3+", "6+", "7+", "12+", "16+", "18+"]

def connect():
	print("Get login and password: tikotstudio@yandex.ru")
	

	selectservice = input("Select service (tikot shop): ")
	login1 = input("Enter login: ")
	password1 = input("Enter password: ")
	
	if login1 not in logins:
		print("Invalid login! Get login: tikotstudio@yandex.ru")
	elif password1 not in passwords:
		print("Invalid password! Get password: tikotstudio@yandex.ru")
	else:
		print("Great! Input this command: tikotapi.panel_tikotshop(\"login\", \"password\")")

def panel_tikotshop(login2, password2):
	if login2 not in logins:
		print("Invalid login in args!")
	elif password2 not in passwords:
		print("Invalid password in args!")
	else:
		secretkeys = ["Kzk1WKyRepTxsfjfP6K37ibeM3EJ20ZIL6ioFPxJflGZgebbQW"]
		print("Welcome " + login2 + "! Press enter secret key")
		secretkey = input("")
		if secretkey not in secretkeys:
			print("Invalid key! Get key in developer panel")
			print("List keys:\n1. *****KyRepTxsfjfP6K37ibeM3EJ20ZIL6ioFPx***********")
			print("If your key not is this list send message in mail: tikotstudio@yandex.ru")
		elif secretkey == secretkeys[0]:
			print("8DirectLabirint - 8ДириктоЛабиринт")
			print("Raiting: " + raitings[0])

			yn1 = input("Yes/No? ")
			if yn1 == "Yes":
				print("Statistic game: CRT: 0% Downloads: NOT ADDED BUTTON DOWNLOAD!")
			elif yn1 == "No":
				print("View your secret key in developer panel!")
			else:
				print("Aborted!")