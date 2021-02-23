#!/usr/bin/env python3

# PYTHON_ARGCOMPLETE_OK

import os, re, sys, json, xmltodict

from collections import OrderedDict
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

	def _loadSlashes(self, bits, parent):
		if len(bits) == 0:
			return parent
		if bits[0] not in list(parent.keys()):
			parent[bits[0]] = dict()
		return self._loadSlashes(bits[1:], parent[bits[0]])

	def _unload(self, input, output):
		if len(input) == 0:
			return
		output['outline'] = []
		for key in list(input.keys()):
			if key == '@note':
				for note in input['@note']:
					child = {}
					if ':' in note:
						parts = note.split(':')
						if len(parts) > 1:
							child['@text'] = parts[0]
							text = ':'.join(parts[1:])
							child['@_note'] = text.lstrip()
					else:
						child['@_note'] = note.lstrip()
					output['outline'].append(child)
				continue
			child = {'@text': key}
			output['outline'].append(child)
			self._unload(input[key], child)
		return

	@args.operation
	@args.parameter(name='input', short='i', help='the text file')
	@args.parameter(name='output', short='o', help='the opml file')
	def grep2opml(self, input=None, output=None):
		'''
        input $(grep -n pattern files)
        output opml
        '''

		_input = sys.stdin
		if input:
			_input = open(input)

		_output = sys.stdout
		if output:
			_output = open(output, 'w')

		tree = dict()

		for line in _input.readlines():
			line = line.rstrip('[\r\n]')
			parts = line.split(':')
			if len(parts) == 0:
				note = ''
			else:
				note = ':'.join(parts[1:])
			bits = parts[0].split('/')
			if len(bits) > 1:
				node = self._loadSlashes(bits, tree)
				if '@note' not in list(node.keys()):
					node['@note'] = list()
				node['@note'].append(note.lstrip())

		if verbose():
			json.dump(tree, sys.stderr, indent=4)

		opml = dict(opml=dict(head=dict(title=input or 'sys.stdin'), body=dict()))

		self._unload(tree, opml['opml']['body'])

		if verbose():
			json.dump(opml, sys.stderr, indent=4)

		xmltodict.unparse(opml, output=_output, pretty=True)

		if output:
			_output.close()

		return

	@args.operation
	@args.parameter(name='input', short='i', help='the text file')
	@args.parameter(name='output', short='o', help='the opml file')
	def tabs2opml(self, input=None, output=None):
		'''
        input (\t| {4}) indented text file
        output opml
        '''

		_input = open(os.path.expanduser(input)) if input else sys.stdin
		_output = open(os.path.expanduser(output), 'w') if output else sys.stdout

		opml = OrderedDict([('opml', OrderedDict([
			('head', OrderedDict([
				('title', input or 'sys.stdin'),
			])),
			('body', OrderedDict([])),
		]))])

		body = opml['opml']['body']
		stack = [body]

		p = re.compile('^(\t*| *)(\S.*)$')

		for line in _input.readlines():
			line = line.rstrip('[\r\n]')
			print(line)
			m = p.match(line)
			if not m: continue
			tabs = m.group(1).replace('    ', '\t')

			outline = OrderedDict([('@text', m.group(2))])

			len_of_stack = len(stack) - 1

			if len(tabs) > len_of_stack:
				parent = stack[-1]['outline'][-1]
				stack.append(parent)

			if len(tabs) < len_of_stack:
				stack.pop()

			if 'outline' not in list(stack[-1].keys()):
				stack[-1]['outline'] = []

			stack[-1]['outline'].append(outline)

		if verbose():
			json.dump(opml, sys.stderr, indent=4)

		xmltodict.unparse(opml, output=_output, pretty=True)

		if output:
			_output.close()

		return


if __name__ == '__main__': args.execute()


