


#########
# Const #
#########
ETAGLIST = ['area',
			'base',
			'basefont',
			'br',
			'col',
			'frame',
			'hr',
			'img',
			'input',
			'isindex',
			'link',
			'meta',
			'param',
			'source'
			]

#########
# Class #
#########
class tag:
	"""tag element"""
	def __init__(self,_type,attributes={}):
		"""generate a tag element
		attributes correspond to the html attributes
		_type corresponds to the tag name"""
		self.attributes = attributes
		self.type = _type
		self.emptytag = False
		if self.type in ETAGLIST:
			self.emptytag=True
		self.children = []

	def generate_attributes(self):
		"""generate a string with all the attributes
		like this : attrname = \"value\""""
		r = ' '

		if self.attributes == {}:
			return ''

		for attn,value in self.attributes.items():
			r+= attn + " = \"" + value + "\" "


		return r

	def render(self,d=0):
		"""generate the tag as a string with chidrens and text inside"""
		r = ''
		if self.type == 'html':
			r+='<!DOCTYPE html>\n'
		r+='<'+self.type
		r+=self.generate_attributes()
		r+='>\n'
		if not self.emptytag:
			for c in self.children:
				r+='\t'*(d+1)
				if type(c) != str:
					r+=c.render(d=d+1)
				else:
					r+=str(c)
				r+='\n'
			r+='\t'*d
			r+='</'+self.type+'>'
		return r

	def save(self,path):
		"""save the tag and all his children in an html file
		/!\\ don't forget the .html at the end
		""" 
		with open(path,'w') as savefile:
			savefile.write(self.render())

	def add(self,toadd):
		"""add a new children. It can be a tag or text"""
		self.children.append(toadd)
		return toadd

	def addList(self,toadd):
		"""add a list of elements at new children in order"""
		for e in toadd:
			self.add(e)
		return tuple(toadd)

class form(tag):
	"""a html form"""
	def __init__(self,PorG,action):
		"""create a html form
		PorG : method (post/get)
		action : link to redirect when submit"""
		attr = {}
		attr['method']=PorG
		attr['action']=action
		tag.__init__(self,'form',attr)

	def addInput(self,inputType,label=None,name=None,attr={}):
		"""add a input with a label before 
		(expept for button, submit and reset where the label is at the attribute value)"""
		if inputType in ('submit','button','reset'):
			customattr = {}
			customattr['type'] = inputType
			if label:
				customattr['value'] = label
			inputTag = tag('input',dict(attr, **customattr))
			self.add(inputTag)
			self.add(tag('br'))
			return inputTag
		else:
			customattr = {}
			labelTag = tag('label')
			labelTag.add(label)
			customattr['type'] = inputType
			if name:
				customattr['name'] = name
			inputTag = tag('input',dict(attr, **customattr))
			if inputType in ('checkbox','radio'):
				self.add(inputTag)
				self.add(labelTag)
			else:
				self.add(labelTag)
				self.add(inputTag)
			self.add(tag('br'))
			return labelTag,inputTag




##################
# body for tests #
##################
if __name__ == '__main__':
	pass