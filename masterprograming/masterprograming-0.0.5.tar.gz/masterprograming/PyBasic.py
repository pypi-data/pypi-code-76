
def PyBasic(topic):
	if topic == 'variable' or topic == 'Variable' or topic == 'variables' or topic == 'Variables' or topic == 'VARIABLE' or topic == 'VARIABLES':
		data = "Variable jab create kiya jata hai tab interpreter dauvara value ko store karne ke liye memory location assign ki jati hai.\n Variable par koi bhi data type ki value store ki ja sakti hai | Example : Number , String, List, Tuple, Dictionary."	
		example = """
For Example:
-------------------
a = 6   # Number
b = "Hello World"  # sting
c = [3,2,4]  # list
print(a,b,c)
--------------------
Output:
-------------------
6 Hello World [3,2,4]

		"""
		print(data)
		print(example)
	elif topic == 'Escape Character' or topic == 'Escape character' or topic == 'escape character' or topic == 'escape' or topic == 'ESCAPE':
		data = "Escape Sequence ka use python me sabse jyada hota hai. Jese Ki Agar aapko New Line Me print karana hoto aapko escape sequence use karna hota hai "
		example = """
Code	Result	
-----------------
\\'	Single Quote	
\\\\  Double Backslash	
\\n	New Line	
\\r	Carriage Return	
\\t	Tab	
\\b	Backspace	
\\f	Form Feed
-----------------	
		"""
		print(data)
		print(example)

	elif topic == 'Row String' or topic == 'row string' or topic == 'rowstring' or topic == 'row' or topic == 'ROW' or topic == 'Row':
		data = "Row String Ko Ham Jab Use Karte hai jab hamme koi escape sequence ko print karana ."
		example = """
Example
-----------------------------
print(r"Line A \\\\n Line B")
------------------------------
Output
-----------------
Line A \\n Line B
-----------------

Row String ko use karne ke liye Appko starting me small ( r ) ka use karna padta hai .

		"""
		print(data)
		print(example)

	elif topic == 'emoji' or topic == 'Emoji' or topic == 'Emoji Print' or topic == 'emoji print' or topic == 'EMOJI' or topic == 'emojicode' or topic == 'emoji code':
		data = "Emoji print karne ke liye python me sabse pahle aap emoji ka url ki jarurat hoti hai \n jese aapko koi emoji print karana hai to emoji ka url code hota hai Agar Aapko imoji ka url nhi pata hai to aap ye website par ja sakte hai |"
		example = """
Emoji Website : – https://unicode.org/emoji/charts/full-emoji-list.html
-----------------------------------------------------------------------			
Example
-----------------------------
print("\U0001F620")
------------------------------
		"""
		print(data)
		print(example)

	elif topic == 'Arithmetic Operator' or topic == 'Arithmetic' or topic == 'arithmetic Operator' or topic == 'Operator' or topic == 'Operators' or topic == 'operators' or topic == 'OPERATORS':
		data = "Arithmetic Operator Sabhi programming language me istemal hote hai . Arithmetic Operator ko programming me sabse jyada use kiya jata hai."
		example = """		
Example
---------------------
print(4+7)
print(12-5)
print(6*6)
print(30/5)
print(10%4)
print(18//5)
print(3**5)
---------------------
Output
---------------------
11
7
36
6
2
3
243
		"""
		print(data)
		print(example)	

	elif topic == 'string' or topic == 'String' or topic == 'STRING' or topic == 'string function' or topic == 'str' or topic == 'String Function' or topic == 'strings':
		data = "String ek data type hota hai Collection of Character, String python me us time istemal karte hai jahah par Hame ek se jyada character use karne padte hai."
		example = """
Example
---------------------
Name = "Masterprogramming"      #string 
print(Name)
a = "masterprogramming"
print(a + str('3'))    # use str function
---------------------
Output
---------------------
Mastrprogramming
masterprogramming3
		"""
		print(data)
		print(example)	
	
			
	else:
		print("Wrong Input")	


a = input("Enter Python Topic Name :")
PyBasic(a)		

