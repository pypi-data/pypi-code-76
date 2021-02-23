#!/usr/bin/env python3

# PYTHON_ARGCOMPLETE_OK

import os, sys, re, json, argparse, argcomplete, logging, requests

from GoldenChild.xpath import *


def argue():
	parser = argparse.ArgumentParser('download wsdl and imports')

	parser.add_argument('-v', '--verbose', action='store_true')
	parser.add_argument('-u', '--username', action='store', help='your user name')
	parser.add_argument('-p', '--password', action='store', help='your pass word')
	parser.add_argument('-d', '--directory', action='store', default='.wsdl')
	parser.add_argument('wsdl', action='store')

	argcomplete.autocomplete(parser)
	args = parser.parse_args()
	if args.verbose:
		sys.stderr.write('%s\n' % json.dumps(vars(args), indent=4))
	return args


def download(url):
	print(url)

	auth = None
	if args.username and args.password:
		auth = (args.username, args.password)

	headers = {'Content-Type': 'text/xml'}

	response = requests.get(url, auth=auth, headers=headers)
	print(response)
	xml = response.text

	del response
	del headers
	del auth

	name = os.path.basename(url)
	print(name)

	if not name in list(names.keys()):
		names[name] = 0
	else:
		names[name] += 1

	f = '%s/%s.%s' % (args.directory, names[name], name)

	with open(f, 'w') as fo:
		fo.write(xml)
		fo.close()

	(doc, ctx, nsp) = getContextFromStringWithNS(xml, None)

	psn = {}
	for p in list(nsp.keys()):
		psn[nsp[p]] = p

	#print json.dumps(psn,indent=4)

	xsp = 'xs'
	xsd = 'http://www.w3.org/2001/XMLSchema'
	ctx.xpathRegisterNs(xsp, xsd)

	r = doc.getRootElement()

	children = []

	# save children references
	for xi in ctx.xpathEval('//xs:import') + ctx.xpathEval('//xs:include'):
		child = getAttribute(xi, 'schemaLocation')
		if child:
			children.append(child)

	files = {
		#namespace: filepath
	}

	# save inline schema
	if r.name == 'definitions':
		for si in ctx.xpathEval('//xs:schema'):
			si.unlinkNode()
			tns = getAttribute(si, 'targetNamespace')
			setAttribute(si, 'xmlns:tns', tns)
			for p in list(nsp.keys()):
				if p != 'tns':
					setAttribute(si, 'xmlns:%s' % p, nsp[p])
			f = '%s/%s.xsd' % (args.directory, tns)
			files[tns] = f
			print(f)
			with open(f, 'w') as fo:
				fo.write(str(si))
				fo.close()

	del doc
	del ctx

	# reindex schema locations
	for ns in list(files.keys()):
		(doc, ctx) = getContextFromFile(files[ns])
		for xi in ctx.xpathEval('//xs:import'):
			tns = getAttribute(xi, 'namespace')
			if not getAttribute(xi, 'schemaLocation'):
				setAttribute(xi, 'schemaLocation',
					files[tns].lstrip(args.directory).lstrip('/')
				)
		fo = open(files[ns], 'w')
		fo.write(str(doc))
		fo.close()

	for child in children:
		download(child)

	return


def main():
	global args, names
	args = argue()
	names = {}

	level = logging.INFO
	if args.verbose:
		level = logging.DEBUG

	logging.basicConfig(level=level)

	if not os.path.isdir(args.directory):
		os.makedirs(args.directory)

	download(args.wsdl)
	return


if __name__ == '__main__': main()


