

import re


def slugify( string ):
	""" Returns a URL safe slug from a string."""
	slug = re.sub(r"[^A-Za-z0-9\s\-_]", '', string)
	slug = tokenize( slug )
	return slug

def tokenize( string ):
	""" Returns a string formatted in snake case. """
	token = re.sub('(.)([A-Z][a-z]+)', r'\1-\2', string)
	token = re.sub('([a-z0-9])([A-Z])', r'\1-\2', token).lower()
	token = re.sub(r"[_\s]+-?", '-', token)
	return token

def pluralize( string ):
	""" Correctly convert singular noung to plural noun. """

	if string.endswith('y'):
		plural = string[:-1] + 'ies'

	elif string.endswith('us'):
		plural = string[:-2] + 'i'

	else:
		plural = string + 's'

	return plural