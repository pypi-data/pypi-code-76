#!/usr/bin/env python2

import os, re, sys, xmltodict, yaml

outline = {
	'opml': {
		'head': {
			'title': {
				'#text': 'MyOutline'
			}
		},
		'body': {
			'outline': []
		}
	}
}

body = outline['opml']['body']['outline']

fp = open('outlines.txt')
bits = yaml.load(fp)


def addBits(node, parent):
	for name in list(node.keys()):
		value = node[name]
		if type(value) == str:
			parent.append({'@text': name, '@_note': value})
		if type(value) == dict:
			child = {'@text': name, 'outline': []}
			parent.append(child)
			addBits(value, child['outline'])
	return


addBits(bits, body)

opml = xmltodict.unparse(outline, indent=4)

print(opml)


