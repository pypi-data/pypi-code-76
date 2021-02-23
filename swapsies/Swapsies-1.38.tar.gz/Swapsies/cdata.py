#!/usr/bin/env python3

################################################################################
cdata2xmlTokens = [
	{
		'&amp;lt;': '%%%%lt%%%%'
	},
	{
		'&amp;gt;': '%%%%gt%%%%'
	},
	{
		'&amp;amp;': '%%%%amp%%%%'
	},
	{
		'&amp;quot;': '%%%%quot%%%%'
	},
	{
		'&amp;apos;': '%%%%apos%%%%'
	},
	{
		'&lt;': '<'
	},
	{
		'&gt;': '>'
	},
	{
		'&quot;': '\"'
	},
	{
		'&apos;': '\''
	},
	{
		'&nbsp;': ' '
	},
	{
		'&#10;': '\n'
	},
	{
		'&amp;': '&'
	},
	{
		'%%%%lt%%%%': '&lt;'
	},
	{
		'%%%%gt%%%%': '&gt;'
	},
	{
		'%%%%amp%%%%': '%amp;'
	},
	{
		'%%%%quot%%%%': '%quot;'
	},
	{
		'%%%%apos%%%%': '%apos;'
	},
]


def cdata2xmlTokenize(line):
	"""Convert normal xml tags to escaped xml tags"""
	for d in cdata2xmlTokens:
		key = list(d.keys())[0]
		val = d[key]
		while key in line:
			line = line.replace(key, val)
	return line


def cdata2xml(input, output):
	"""Convert normal xml tags to escaped xml tags"""
	for line in input.read().split('\n'):
		output.write(cdata2xmlTokenize(line))
		output.flush()


################################################################################
xml2cdataTokens = [
	{
		'&': '%%%%amp%%%%'
	},
	{
		'<': '&lt;'
	},
	{
		'>': '&gt;'
	},
	{
		'\"': '&quot;'
	},
	{
		'\'': '&apos;'
	},
	{
		'\n': '&#10;'
	},
	{
		'%%%%amp%%%%': '&amp;'
	},
]


def xml2cdataTokenize(line):
	"""Convert xml escaped tags to normal xml inside cdata"""
	for d in xml2cdataTokens:
		key = list(d.keys())[0]
		val = d[key]
		while key in line:
			line = line.replace(key, val)
	return line


def xml2cdata(input, output):
	"""Convert xml escaped tags to normal xml inside cdata"""
	for line in input.read().split('\n'):
		output.write(xml2cdataTokenize(line))
		output.flush()


