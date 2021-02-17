



###########
# Classes #
###########

class styleSheet:
	""" object for the stylesheet"""
	def __init__(self):
		"""creates the sheet"""
		self.rules = []
		self.medias = []
	
	def sort(self):
		""" to sort all the rule and make blokcs of rule """
		sortedDict = {}
		for rule in self.rules:
			if rule.selectors in sortedDict.keys():
				sortedDict[rule.selectors].append((rule.property,rule.value))
			else:
				sortedDict[rule.selectors] = [(rule.property,rule.value)]
		return sortedDict

	def getRules(self):
		""" returns the list of all the rules"""
		return self.rules

	def getQuerys(self):
		""" returns the list of all the querys """
		return self.medias


	def addQuery(self,query):
		""" to add a media query """
		self.medias.append(query)

	def add(self,rule):
		""" to add a rule to the sheet """
		self.rules.append(rule)

	def addList(self,listr):
		"""to add a list of rule"""
		for rule in listr:
			self.add(rule)

	def render(self):
		""" to render the rules (one by one but it will be grouped later) """
		r = ''
		
		ruleDict = self.sort()

		for Selector,declaration in ruleDict.items():
			r+=rule.renderBlock(Selector,declaration)

		for media in self.medias:
			r+=media.render()
		return r
	
	def save(self,path):
		""" to save the sheet in a file after aving render it
		/!\\ don't forget the .css"""
		with open(path,'w') as towrite:
			towrite.write(self.render())
			towrite.close()


class mediaQuery(styleSheet):
	""" object for the query """
	def __init__(self,ON,mediatype,conditions):
		""" creates the query """
		styleSheet.__init__(self)
		self.ON = ON
		self.mediatype = mediatype
		if type(conditions) == str:
			conditions = [conditions]
		self.conditions = conditions

	def render(self):
		""" render the query """
		
		r = f'@media {self.ON} if {self.mediatype} '
		
		for condition in self.conditions:
			r+='and ('+condition+') '

		r+='{\n'
		rend = styleSheet.render(self)
		rend = '\n'.join(['\t'+e for e in rend.split('\n')])
		rend = rend[:-1]
		r+=rend
		r+='}'
		# print(rend)
		return r


class rule:
	""" object for the css rule """
	def __init__(self,_property,value,selectors):
		""" creates the rule with the the property, the value and the selectors of the rule of the rule 
		selectors must be a list or a tuple
		"""
		if type(selectors)==str:
			selectors = [selectors]
		self.selectors = tuple(selectors)
		self.property = _property
		self.value = value

	def render(self):
		"""render the rule alone"""
		r = ''
		
		for selector in self.selectors:
			r+=selectors+' '

		r+='\n{\n\t'

		r+=self.property+' : '
		r+=str(self.value)+';\n}'
		return r

	def renderBlock(Selectors,declarations):
		"""to render a block with a batch of declaration"""
		r = ''
		for selector in Selectors:
			r+=selector+' '
		r+='\n{\n'



		for _property,value in declarations:
			if type(value) in (list,tuple):
				value = ' '.join(list(value))
			r+='\t'+_property+' : '+value+';\n'

		r+='}\n'
		return r


#############
# functions #
#############

def createBatch(selectors,declarations):
	""" to create a batch of rule with the same declarator 
	selectors : a list or a tuple of selector(s)
	declarations : a list of tuples (property,value)
	"""
	r = []
	for _property,value in declarations:
		r.append(rule(_property,value,selectors))
	return r


if __name__=='__main__':
	s=styleSheet()
	
	m1 = mediaQuery('only','screen','minwidth:600ppx')
	b1 = createBatch(('a','div:hover'),[('color','green'),('background-color','blue')])
	print(b1)
	m1.addList(b1)

	s.addQuery(m1)


	print(s.render())
	s.save('style.css')

