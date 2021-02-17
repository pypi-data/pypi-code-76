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

		for i in range(len(clist)):
			if clist[i] + transvalue[i] < 0:
				clist[i] = 0
			elif clist[i] + transvalue[i] > 225:
				clist[i] = 225
			else:
				clist[i] += transvalue[i]

		return tuple(clist)

	if type(transvalue) == int:
		clist = list(color)

		for i in range(len(clist)):
			if clist[i] + transvalue < 0:
				clist[i] = 0
			elif clist[i] + transvalue > 225:
				clist[i] = 225
			else:
				clist[i] += transvalue

		return tuple(clist)		

def help():
	print('Colors module help:')
	print('	importing: "import easycolors" or "from easycolors import *"')
	print('	get rgb of color: "easycolors.<color>"')
	print('	transform color: "easycolors.transform(<rgb tuple>, <3-value tuple or int>)')
	print('	transform color will return a scaled/transformed color. 2nd arg is the added value (3-value tuple or int)')

print('Thanks for using the easycolors module! Run "easycolors.help()" for help.')