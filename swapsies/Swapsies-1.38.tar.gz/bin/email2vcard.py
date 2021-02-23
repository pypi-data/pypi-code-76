#!/usr/bin/env python3

# PYTHON_ARGCOMPLETE_OK

import sys, os, re, xmltodict, argparse, argcomplete, json, vobject, datetime

parser = argparse.ArgumentParser('Convert microsoft .contact to .vcard')

parser.add_argument(
	'-v', '--verbose', action='store_true', help='show detailed output')
parser.add_argument(
	'-o', '--output', action='store', help='output dir', default='vcards')
parser.add_argument(
	'emails',
	action='store',
	help='file containing comma seperated email addresses')

argcomplete.autocomplete(parser)
args = parser.parse_args()

companies = {
	'tradelink.com.au': 'Tradelink',
	'fbu.com': 'Fletcher Building',
	'stibo.com.au': 'Stibo Systems Australia',
	'stibo.com': 'Stibo Systems',
}

if args.verbose:
	sys.stderr.write('args:')
	json.dump(vars(args), sys.stderr, indent=4)
	sys.stderr.write('\n')


def convert(fqn):
	fqn = fqn.strip()
	triangles = re.compile('^([^<]+) <([^>]+)>$')
	match = triangles.match(fqn)
	if match:
		names = match.group(1).split(' ')
		email = match.group(2)
	else:
		email = fqn
		rawemail = re.compile('^([^@]+)@(.*)')
		match = rawemail.match(fqn)
		if match:
			names = match.group(1).split('.')
		else:
			names = ''

	vcard = vobject.vCard()
	vcard.add('n')

	for n in range(len(names)):
		name = names[n - 1]
		if len(name) > 1:
			names[n - 1] = name[0].upper() + name[1:]
		elif len(name) > 0:
			names[n - 1] = name[0].upper()

	if len(names) == 1:
		vcard.n.value = vobject.vcard.Name(
			given=names[0],
			additional='',
			family='', )
	if len(names) == 2:
		vcard.n.value = vobject.vcard.Name(
			given=names[0],
			additional='',
			family=names[1], )
	if len(names) == 3:
		vcard.n.value = vobject.vcard.Name(
			given=names[0], additional=names[1], family=names[2])
	if len(names) > 3:
		sys.stderr.write('error names=%s\n' % names)

	vcard.add('fn')
	vcard.fn.value = ' '.join(names)

	domains = re.compile('^([^@]+)@(.*)$')
	match = domains.match(email)
	if not match:
		sys.stderr.write('domains failed=%s' % email)
		return

	company = match.group(2)

	if company in list(companies.keys()):
		company = '%s' % companies[company]

	vcard.add('org')
	vcard.org.value = [company]

	ve = vcard.add('email')
	ve.value = email

	vcard.prettyPrint()

	target = '%s.vcf' % ' '.join(names)
	if args.output:
		target = '%s/%s' % (args.output, target)

	output = open(target, 'w')
	vcard.serialize(buf=output)
	output.close()
	return


def main():
	if args.output and not os.path.isdir(args.output):
		os.makedirs(args.output)

	input = open(args.emails)
	for email in input.readlines():
		convert(email)
	input.close()

	return


if __name__ == '__main__': main()


