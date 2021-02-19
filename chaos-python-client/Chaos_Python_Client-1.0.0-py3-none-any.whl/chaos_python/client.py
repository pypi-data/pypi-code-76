import requests

def chaosAPI(domain, key, opt):
	url = f"https://dns.projectdiscovery.io/dns/{domain}/subdomains"
	headers = {'Authorization': key}
	response = requests.request("GET", url, headers=headers).json()
	domain = response['domain']
	
	options = ['default','count','json']
	
	if opt in options:
		if opt == 'default':
			return response['subdomains']
		elif opt == 'count':
			return len(response['subdomains'])
		elif opt == 'json':
			return response
	else:
		return "Please define an options"