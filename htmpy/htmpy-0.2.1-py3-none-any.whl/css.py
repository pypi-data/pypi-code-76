



###########
# Classes #
###########

class styleSheet:
	""" object for the stylesheet"""
	def __init__(self):
		"""creates the sheet"""
		self.rules = []
	def add(self,rule):
		""" to add a rule to the sheet """
		self.rules.append(rule)

	def render(self):
		""" to render the rules (one by one but it will be grouped later) """
		r = ''
		for rule in self.rules:
			r+=rule.render()+'\n'
		return r




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


if __name__=='__main__':
	s=styleSheet()
	a = rule('border','blue','a','test','test')
	b = rule('height','50%','p','p1','allp')
	s.add(a)
	s.add(b)
	print(s.render())

