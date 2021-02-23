#!/usr/bin/env python3

# PYTHON_ARGCOMPLETE_OK

import os, re, sys, json, xmltodict

from collections import OrderedDict

from xlrd import open_workbook, xldate_as_tuple

from Argumental.Argue import Argue

args = Argue()


@args.argument(short='v', flag=True)
def verbose():
	return False


@args.command(single=True)
class TextToOPML(object):
	'''
    convert between slash seperated lines and opml
    '''

	def _load(self, bits, parent):
		if len(bits) == 0:
			return parent
		if bits[0] not in list(parent.keys()):
			parent[bits[0]] = dict()
		return self._load(bits[1:], parent[bits[0]])

	def _unload(self, input, output):
		if len(input) == 0:
			return
		output['outline'] = []
		for key in list(input.keys()):
			if key == '@note':
				for note in input['@note']:
					if note and len(note) > 0:
						child = {}
						child['@text'] = note
						output['outline'].append(child)
				continue
			child = {'@text': key}
			output['outline'].append(child)
			self._unload(input[key], child)
		return

	@args.operation
	@args.parameter(name='input', short='i', help='the text file')
	@args.parameter(name='output', short='o', help='the opml file')
	def opml(self, input=None, output=None):
		'''
        output opml
        '''

		_input = sys.stdin
		if input:
			_input = open(input, 'rb')

		_output = sys.stdout
		if output:
			_output = open(output, 'w')

		tree = dict()

		baddies = '[\x80-\xff]'
		replace = re.compile(baddies, re.MULTILINE)
		pattern = re.compile('.*%s.*' % baddies, re.MULTILINE)

		wb = open_workbook(file_contents=_input.read())

		for s in wb.sheets():

			for r in range(s.nrows):
				bits = list()
				bits.append(s.name)

				for c in range(s.ncols):

					v = s.cell(r, c).value
					t = s.cell(r, c).ctype

					if t == 3:  #date
						v = dateFixer(wb, v)

					v = str(v).encode('UTF-8')
					while pattern.match(v):
						v = replace.sub('', v)

					bits.append(v)

				if len(bits) > 1:
					node = self._load(bits, tree)
					if '@note' not in list(node.keys()):
						node['@note'] = list()
					node['@note'].append(v)

		opml = dict(opml=OrderedDict([
			#('@xmlns:xsi', 'http://www.w3.org/2001/XMLSchema-instance'),
			#('@xsi:noNamespaceSchemaLocation', 'http://www.eclipse.org/buckminster/schemas/opml-2.0.xsd'),
			('@version', '1.0'),
			(
				'head',
				OrderedDict([
					('title', input or 'sys.stdin'),
					#('expansionState',0)
				])),
			('body', dict())
		]))

		self._unload(tree, opml['opml']['body'])

		if verbose():
			json.dump(opml, sys.stderr, indent=4)

		xmltodict.unparse(opml, output=_output, pretty=True)

		if output:
			_output.close()

		return


if __name__ == '__main__':
	args.execute()


