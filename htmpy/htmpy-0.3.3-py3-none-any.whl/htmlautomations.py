from htmpy.html import *
import webbrowser
import pathlib

#############
# Fonctions #
#############

def createEmptyPage(title=None,header = False):
	"""create an empty page with a head and a body
	optinal : title,header
	returns the root, the head and the body and present : header and/or footer"""
	root = tag('html')
	head = tag('head')
	body = tag('body')
	root.add(head)
	root.add(body)
	r = [root,head,body]
	if title:
		titleTag = tag('title')
		titleTag.add(title)
		head.add(titleTag)
	if header:
		headerTag = tag('header')
		body.add(headerTag)
		r.append(headerTag)

	return tuple(r)


def paragraph(text):
	"""create a paragraphe with text
	changing \\n by <br> tags"""
	r = tag('p')
	pliste = text.split('\n')
	for e in pliste[:-1]:
		r.add(e)
		r.add(tag('br'))
	r.add(pliste[-1])
	return r

def openInBrowser(page,name):
	""" saves the page as name and open it in the browser """
	page.save(name)
	
	webbrowser.open(str(pathlib.Path().absolute())+'/'+name)


if __name__ == '__main__':
	page,head,body = createEmptyPage('test')
	print(page)
	openInBrowser(page,'test.html')