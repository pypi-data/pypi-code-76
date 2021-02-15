



###########
# Classes #
###########

class styleSheet:
	""" object for the stylesheet"""
	def __init__(self):
		"""creates the sheet"""
		self.rules = []
	
	def sort(self):
		sortedDict = {}
		for rule in self.rules:
			if (rule.tag,rule.id,rule._class) in sortedDict.keys():
				sortedDict[(rule.tag,rule.id,rule._class)].append((rule.property,rule.value))
			else:
				sortedDict[(rule.tag,rule.id,rule._class)] = [(rule.property,rule.value)]
		return sortedDict

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

		return r
	
	def save(self,path):
		""" to save the sheet in a file after aving render it
		/!\\ don't forget the .css"""
		with open(path,'w') as towrite:
			towrite.write(self.render())
			towrite.close()



class rule:
	""" object for the css rule """
	def __init__(self,_property,value,tag=None,_id=None,_class=None):
		""" creates the rule with the id,the class, the property and the value of the rule"""
		self.tag = tag
		self.id = _id
		self._class = _class
		self.property = _property
		self.value = value

	def render(self):
		"""render the rule alone"""
		r = ''
		
		if self.tag:
			r+=self.tag + ' '
		if self.id:
			r+='#'+self.id +' '
		if self._class:
			r+='.'+self._class

		r+='\n{\n\t'

		r+=self.property+' : '
		r+=str(self.value)+';\n}'
		return r

	def renderBlock(Selector,declarations):
		"""to render a block with a batch of declaration"""
		tag,_id,_class = Selector
		r = ''
		if tag:
			r+=tag+' '
		if _id:
			r+='#'+_id+' '
		if _class:
			r+='.'+_class
		r+='\n{\n'

		for _property,value in declarations:
			r+='\t'+_property+' : '+value+';\n'

		r+='}\n'
		return r





if __name__=='__main__':
	s=styleSheet()
	a = rule('border','blue','a','test')
	b = rule('height','50%','p','p1','allp')
	c = rule('color','green','a','test')
	s.addList([a,b,c])
	print(s.render())
	print(s.sort())
	s.save('style.css')

