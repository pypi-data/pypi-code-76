from htmpy.css import *

###########
# Classes #
###########

class TSQSTemplate:
	""" 3 state query sheet template  """
	def __init__(self):
		""" creates the template """
		self.destopRules = []
		self.tabletRules = []
		self.smartphoneRules = []

	def getRules(self):
		return self.destopRules,self.tabletRules,self.smartphoneRules

	def addRules(desktop=[],tablet=[],smartphone=[]):
		""" to add rules to one or more device type """
		self.destopRules+=desktop
		self.tabletRules+=tablet
		self.smartphoneRules+=smartphone

class blankTemplate(TSQSTemplate):
	"""blank with nothing in it
	"""
	def __init__(self,arg=None):
		TSQSTemplate.__init__(self)

class columnTemplate(TSQSTemplate):
	"""column with a system of different number columns in desktop tablet and smartphone"""
	def __init__(self,arg=(4,2,1)):
		TSQSTemplate.__init__(self)
		self.dcol,self.tcol,self.scol = arg
		self.generate()

	def generate(self):
		self.destopRules = createBatch(('.column'),[('float','left'),('width',str(100/self.dcol)+'%')])
		self.tabletRules = [rule('width',str(100/self.tcol)+'%','.column')]
		self.smartphoneRules = [rule('width',str(100/self.scol)+'%','.column')]


#############
# functions #
#############

def C3SQSheet(breakpoints = (600,992),template = blankTemplate()):
	""" function to create a styleSheet with 3 differents states corresponding
	to desktops, tablets and smartphones
	we can ajusts breakpoints and choose a template
	getTemplateDict() to get a dict with all templates
	returns the sheet, the desktop query and the tablet query
	the desktop and tablet querys are already added to the sheet
	"""
	sheet = styleSheet()
	b1,b2 = breakpoints
	qMTablet = mediaQuery('only','screen','minwidth:'+str(b1))
	qMDesktop = mediaQuery('only','screen','minwidth:'+str(b2))
	sheet.addQuery(qMTablet)
	sheet.addQuery(qMDesktop)

	d,t,s = template.getRules()

	qMTablet.addList(t)
	qMDesktop.addList(d)
	sheet.addList(s)

	return sheet,qMTablet,qMDesktop

	

#############
# Constants #
#############

templateDict = {}


templateDict['blank'] = blankTemplate
templateDict['column'] = columnTemplate



if __name__ == '__main__':

	style,qt,qd = C3SQSheet((600,992),columnTemplate())

	print(style.render())


