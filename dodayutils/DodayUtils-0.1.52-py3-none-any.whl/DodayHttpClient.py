#-*-coding:utf-8 -*-
from DodayUtils._dwrappers import *
import requests
import urllib.parse

class DodayHttpClient:
	"""
	This is the http client
	class. 
	"""
	def __init__(self, **configs):
		for key in configs:
			if "_http_url" in key:
				setattr(self, key, configs[key])

	def __getitem__(self, key):
		return getattr(self, key)
		
	def client_get(self, key, input_dict):
		get_query = self[key]

		# assign query list
		query_list = ["?"]
		for key in input_dict:
			query_list.extend([str(key), "=", input_dict[key], "&"])

		# concatenate together
		get_query += "".join(query_list[:-1])

		r = requests.get(get_query)
		response = r.text 
		return response

	def client_post(self, key, input_dict, urlencode=False):
		post_query = self[key]

		if urlencode:
			r = requests.post(post_query, data=input_dict)
		else:
			r = requests.post(post_query, json=input_dict)
		response = r.text

		return response

