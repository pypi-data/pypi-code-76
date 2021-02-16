white = (255,255,255)
black = (0,0,0)
grey = (127,127,127)
darkgrey = (60, 60, 60)
red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)
yellow = (255,255,0)
orange = (225,165,0)
cyan = (0,225,225)
purple = (128,0,128)
navy = (0,0,128)
pink = (225,20,147)

def transform(color, transvalue):
	if not type(color) == tuple:
		raise ValueError('first argument must be an 3-value tuple')
	if not len(color) == 3:
		raise ValueError('first argument must be an 3-value tuple')
	if not type(transvalue) == tuple and not type(transvalue) == int:
		raise ValueError('second argument must be a 3-value tuple or an int')

	if type(transvalue) == tuple:
		if not len(transvalue) == 3:
			raise ValueError('second argument must be a 3-value tuple or an int')
		clist = list(color)
		translist = list(transvalue)

		clist[0] += translist[0]
		clist[1] += translist[1]
		clist[2] += translist[2]

		return tuple(clist)

	if type(transvalue) == int:
		clist = list(color)

		clist[0] += transvalue
		clist[1] += transvalue
		clist[2] += transvalue

		return tuple(clist)		

def help():
	print('	Colors module help:')
	print('		importing: "import colors" or "from colors import *"')
	print('		get rgb of color: "colors.<color>"')
	print('		transform color: "colors.transform(<rgb tuple>, <3-value tuple or int>)')
	print('		transform color will return a scaled/transformed color. 2nd arg is the added value (3-value tuple or int)')

print('Thanks for using the Colors module! Run "print(colors.help)" for help.')