#!/usr/bin/env python3

# PYTHON_ARGCOMPLETE_OK

import sys, os, re, xmltodict, argparse, argcomplete, json, vobject, datetime

parser = argparse.ArgumentParser('Convert microsoft .contact to .vcard')

parser.add_argument(
	'-v', '--verbose', action='store_true', help='show detailed output')
parser.add_argument('-o', '--output', action='store', help='output dir')
parser.add_argument('contacts', nargs='*')

argcomplete.autocomplete(parser)
args = parser.parse_args()

if args.verbose:
	sys.stderr.write('args:')
	json.dump(vars(args), sys.stderr, indent=4)
	sys.stderr.write('\n')


def populate(source, name, default=''):
	value = default
	if name in list(source.keys()):
		if '#text' in source[name]:
			value = source[name]['#text']
		else:
			value = source[name]
	return value


def labels(source):
	values = []
	if 'c:LabelCollection' in list(source.keys()):
		if 'c:Label' in source['c:LabelCollection']:
			items = source['c:LabelCollection']['c:Label']
			if type(items) != list:
				items = [items]
			for label in items:
				if type(label) == dict and '#text' in list(label.keys()):
					values.append(label['#text'])
				else:
					values.append(label)
	return values


def convert(source):
	input = open(source)
	contact = xmltodict.parse(input)
	input.close()

	vcard = vobject.vCard()

	name = contact['c:contact']['c:NameCollection']['c:Name']
	vcard.add('n')
	vcard.n.value = vobject.vcard.Name(
		given=populate(name, 'c:GivenName'),
		additional=populate(name, 'c:MiddleName'),
		family=populate(name, 'c:FamilyName'), )

	vcard.add('fn')
	vcard.fn.value = populate(name, 'c:FormattedName')

	#print contact
	position = contact['c:contact']['c:PositionCollection']['c:Position']

	vcard.add('org')
	vcard.org.value = [populate(position, 'c:Company')]

	vcard.add('title')
	vcard.title.value = populate(position, 'c:JobTitle')

	emails = contact['c:contact']['c:EmailAddressCollection']
	for email in emails['c:EmailAddress']:
		ve = vcard.add('email')
		if 'Preferred' in labels(email):
			#ve.type = 'pref'
			None
		ve.type_param = 'internet'
		ve.value = populate(email, 'c:Address')

	addresses = contact['c:contact']['c:PhysicalAddressCollection']
	for address in addresses['c:PhysicalAddress']:
		va = vcard.add('adr')
		for tipe in labels(address):
			#ve = ve.type = tipe
			None
		va.value = vobject.vcard.Address(
			street=populate(address, 'c:Street'),
			city=populate(address, 'c:Locality'),
			code=populate(address, 'c:PostalCode'),
			country=populate(address, 'c:Country'))

	phones = contact['c:contact']['c:PhoneNumberCollection']
	for phone in phones['c:PhoneNumber']:
		vt = vcard.add('tel')
		for tipe in labels(phone):
			#vt.type_param = tipe
			None
		vt.value = populate(phone, 'c:Number')

	vcard.add('note')
	vcard.note.value = contact['c:contact']['c:Notes']['#text']

	vcard.prettyPrint()

	target = '%s.vcf' % source
	if args.output:
		target = '%s/%s' % (args.output, target)

	output = open(target, 'w')
	vcard.serialize(buf=output)
	output.close()
	return


def main():
	if args.output and not os.path.isdir(args.output):
		os.makedirs(args.output)

	for file in args.contacts:
		try:
			convert(file)
		except:
			sys.stderr.write('%s\n' % file)
	return


if __name__ == '__main__': main()


