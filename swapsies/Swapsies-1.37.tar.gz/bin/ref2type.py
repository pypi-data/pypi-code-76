#!/usr/bin/env python3

import os,re,sys

from GoldenChild.xpath import *
from Perdy.parser import printXML

file=sys.argv[1]

(doc,ctx,nsp) = getContextFromFile(file)

ctx.xpathRegisterNs('xs',"http://www.w3.org/2001/XMLSchema")

elements = getElements(ctx,'/xs:schema/xs:element[@name]')
for element in elements:
	if getAttribute(element, 'ref'): continue
	name = getAttribute(element,'name')

	tipe = getAttribute(element, 'type')
	if tipe:
		st = addElement(doc, 'simpleType')
		setAttribute(st, 'name', name)
		rs = addElement(doc, 'restriction', st)
		setAttribute(rs, 'base', tipe)
	else:
		ct = getElement(ctx,'xs:complexType',element)
		if not ct: continue
		ct.unlinkNode()
		setAttribute(ct, 'name', name)
		doc.getRootElement().addChild(ct)

	element.unlinkNode()
	element.freeNode()

elements = getElements(ctx,'//xs:element[@ref]')
for element in elements:
	if getAttribute(element,'name'): continue
	
	ref = getAttribute(element, 'ref')

	tipe = getElement(ctx, '/xs:schema/xs:complexType[@name="%s"]'%ref) \
		or getElement(ctx, '/xs:schema/xs:simpleType[@name="%s"]'%ref)

	property = getElement(ctx, '@ref', element)
	property.unlinkNode()
	property.freeNode()
	
	setAttribute(element, 'name', ref)
	setAttribute(element, 'type', ref)

with open(file.replace('.xsd','.types.xsd'),'w') as output:
	root_name = sys.argv[2]
	root = addElement(doc, 'element')
	setAttribute(root, 'name', root_name)
	setAttribute(root, 'type', root_name)
	printXML(str(doc),output=output)


