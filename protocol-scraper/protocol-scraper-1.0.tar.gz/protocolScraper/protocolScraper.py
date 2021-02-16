#!/usr/bin/env python

import requests
import re
import click

def search_page(string):
	''' Given search string will return JSON format of the search page for that string '''

	base = 'https://www.protocols.io/api/v3/protocols' # http request base
	payload = {'filter': 'public', "order_field" : 'relevance', "key" : string} # api parameters : https://apidoc.protocols.io/#get-list
	r = requests.get(base, params=payload) # requests page information
	jason = r.json() # page as json format

	return jason

def protocol_ids(jason):
	''' Given JSON of search page, will return list of ids in descending order of releveancy '''

	ids = []
	for item in jason['items']: # this format because dictionary into list
		ids.append(item['id'])

	return ids

def get_protocols(ids, limit):
	''' Returns list of protocol objects through api '''

	base = 'https://www.protocols.io/api/v3/protocols/'
	protocol_list = [] # holds jason of protocol objects for top 3 relevent protocols

	count = 0
	while count < limit: # CHANGE THIS limit to however many files you want to generate
		number = str(ids[count]) # gets id from list and converts to string for search
		url = base + number # plugs id into url
		r = requests.get(url) # request api
		jason = r.json() # converts json
		protocol_list.append(jason)
		click.echo('Gathered Protocol ' + str(count+1) + '.' )
		count += 1

	return protocol_list

def single_translate_steps(protocol):
	''' Takes a protocol object and returns list of steps as strings with title of protocol being first element '''

	steps = protocol['protocol']['steps'] # steps object of protocol
	step_list = ['Steps:'] # stores cleaned text with title of protocol being first item in list
	for step in steps:
		step_description = step['components'][1]['source']['description'] # navigates JSON to description which holds html of step text
		cleanr = re.compile('<.*?>')
		clean_text = re.sub(cleanr, '', step_description) # removes html syntax from step text
		step_list.append(clean_text)

	count = 1
	while count < len(step_list):
		step_list[count] = str(count) + '. ' + step_list[count] # adds step number to description but not to title
		count += 1

	return step_list

def single_translate_material(protocol):
	''' Takes protocol object and returns list of materials for protocol '''

	title = protocol['protocol']['title'] # title of protocol
	materials = protocol['protocol']['materials']
	material_list = [title, 'Materials:']

	for reagent in materials:
		material_list.append(reagent['name']) # gets material name + quant.

	count = 2
	while count < len(material_list):
		material_list[count] = '* ' + material_list[count] # adds bullet point to material description

		count +=1

	if len(material_list) == 2:
		material_list.append('None') # checks to see if materials are included in protocol

	return material_list

def find_credit(protocol):
	''' Finds author credit from protocol object and protocol url '''

	credit = ['Reference:'] # holds information on author, authors' institution and protocol url on protocol.io
	authors = protocol['protocol']['authors']

	for item in authors:
		credit.append(item['name']) # finds authors name

		if item['affiliation'] != 'null':
			credit.append(item['affiliation']) # finds authors institution if given

	url = protocol['protocol']['url'] # finds url for protocol on protocol.io
	credit.append(url)

	return credit

def write_protocols(protocol_list):
	''' Writes the protocol information to files '''

	count = 0
	while count < len(protocol_list):
		translation = single_translate_steps(protocol_list[count]) # translates protocol object into plain text steps (see single_translate function) + remove spaces
		material_list = single_translate_material(protocol_list[count])
		credit_list = find_credit(protocol_list[count])
		title = material_list[0].replace(' ', '_') # first element in material_list is always title

		f = open(str(count+1)+ '_' + title + '.txt', 'w') # creates file with unique name

		for material in material_list: # writes materials section + title
			f.write(material + '\n')

		for step in translation: # writes steps
			 step = step.encode('cp1252', 'replace').decode('cp1252') # this fixes bug that brings up UnicodeEncodeError for greek/roman symbol
			 f.write(step + '\n') # writes out steps to file

		for item in credit_list:
			item = item.encode('cp1252', 'replace').decode('cp1252')
			f.write(item + '\n')

		f.close()
		count += 1


@click.command()
@click.argument('protocol')
@click.option('-l', '--limit', default = 3, type=int, help='Number of test protocols to write. Default = 3' )
def cli(protocol, limit):

	"""Arguments:\n
    PROTOCOL The protocol to write.
    """
	
	click.echo('Accessing protocols.io API.')
	jason = search_page(protocol)
	ids = protocol_ids(jason)
	protocol_list = get_protocols(ids, limit)
	click.echo('Writing Protocols...')
	write_protocols(protocol_list)
	click.echo('Protocol Generation Complete.')
	click.echo(str(len(protocol_list)) + ' Protocols Written.')

if __name__ == '__main__':
	cli()
