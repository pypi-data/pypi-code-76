import komiker as _k

dó, án, von = '',[],''	# íslenska

class lib:
	
	def __init__(self, *args):
		
		self.alias = args[0]
		self.ex = _k._ex()
		self.path = self.ex.path
		self.regex = _k._j(self.ex.read())
		self.web = self.regex.get(self.alias)[3]
		self.ver = self.update()
		self.dir = '/storage/emulated/0/Download/Manga'
		
	def initData(self):
		v = open(f'{self.path}/data/{self.alias}.json')
		y = 0
		global dó, án
		string = dó
		array = án
		for i in _k._j(v.read()):
			arr = _k._c(r'(.*) => (.*)').findall(i)
			array.append({_k._u(arr[0][0]):arr[0][1]})	
		v.close()
		#'''
		for j in array:
			y +=1
			for x in j.keys():
				string += f'\33[32mid:{str(y).zfill(len(str(len(array))))} -- ※ {x}\n\33[0m'		
		pr = _k._cs.Console()
		pr.rule(f' daftar manga {self.web}'.title())
		print('\n%s' % string)
		pr.rule()
		'''
		df = _k._tb.Table(title=f'daftar manga {self.web}'.title())
		df.add_column('[green]ID[/green]', justify='center')
		df.add_column('[green]Judul Manga[/green]', justify='left')
		for j in array:
			y += 1
			for x in j.keys():
				df.add_row(f'[green]id:{str(y).zfill(len(str(len(array))))}[/green]', f'[green]※ {x}[/green]')
		_k._cs.Console().print(df) #'''
		idn = input('🥀 Masukan id manga: ')
		if idn.isnumeric(): idi = int(idn)
		else: self.ex.err('Masukan angka saja!')
		if idi > 0 and idi <= len(array):
			title = list(array[idi-1].keys())[0]	
			uid = list(array[idi-1].values())[0]
			dó, án = '', []
			del string, array
			return title, uid
		else: self.ex.err('Masukan id manga dengan benar!')
			
	def contentWeb(self, link):
	 	req = _k._g(link, headers=self.ref('https://'+self.web))
	 	sts = req.status_code
	 	if sts == 404: self.ex.err('Website tidak ditemukan!', False)
	 	elif sts == 503: self.ex.err('Server website sedang penuh, silakan cek kembali nanti!')
	 	elif sts != 200: self.ex.err(sts, False)
	 	return req, sts
	
	def ref(self, a):
		headers = _k._h(headers=False).generate()
		headers['Referer'] = a
		return headers
	
	def findText(self, a, b, c):
		return _k._c(r'%s' % self.regex.get(a)[b]).findall(c)

	def json(self, a, b):
		I = _k._s('\n|\t', '', self.contentWeb(a if self.alias != 'mt' else (a if a.find('/episodes') != -1 else f'{a}/episodes' ))[0].text)
		ps = ['mc', 'mp', 'mw', 'kb', 'pm']
		if self.alias in ps:
			jd = _k._j(_k._c(r'var manga = (.*?);').findall(I)[0])
			ht = {'action':'manga_get_chapters','manga':jd['manga_id']}
			III = _k._s('\n|\t', '', _k._p(jd['ajax_url'], data=ht, headers=self.ref(jd['home_url'])).text)
		self.eB = eval(self.regex.get(self.alias)[5])
		if not b: b = True if self.eB != True else b
		II = I if self.alias not in ps else III
		if b: d = self.findText(self.alias, 1, II)
		else: d = self.findText(self.alias, 0, II)
		say, ara, araa = [], [], []
		apa_ini = r'\-| |\;|\:|\/|\!|\~|\&|\_|\[|\]|\{|\}|\(|\)|\^|\%|\$|\#|\@|\<|\>|\?|\\'
		def you(au, ah):
			def y(o,u): return o.zfill(len(str(len(d)))+u)
			global von
			asc = range(len(d)-1,-1,-1) if self.alias not in ['mi', 'mt'] else range(len(d))
			for i in asc:
				ax = d[i][ah]
				if ax == '': ax = str(int(float(d[i-1][ah])-1)) if i != 0 else '0'
				elif ax[0] == str(0) and len(ax) > 1: ax = ax[1:]
				ox = y(ax, 0)
				if ox.find('.') != -1: ox = y(ax, 2)
				if ox[0].isdigit() != False: say.append(_k._sp(apa_ini , ox)[0])
				else: say.append(ox)
				ara.append(eval(au))
			for n in say:
				if len(n) <= len(str(len(d))) and n.find('.') == -1: araa.append(y(n, 0))
				elif len(n) <= len(str(len(d))) and n.find('.') != -1: araa.append(y(n, 2))
				else: araa.append(n)
			hehe = self.fixArray(araa)
			for e in range(len(ara)):
				von +=  ('"%s":"%s",'%(hehe[e],ara[e])) if self.alias not in ['kg', 'kk', 'mt'] else ('"%s":"https://%s%s",'%(hehe[e], self.regex.get(self.alias)[3],ara[e]))
		if b: you('d[i][0]', 1)
		else: you('self.regex.get(self.alias)[4] + d[i][1]', 0)
		global von
		jr = _k._j('{'+von[:-1]+'}')
		von = ''
		return jr
				
	def saveFile(self, a, b, c, d, e):
		def dirSv(p) :
			if _k._o.isdir(p) != True:
				_k._m(p)
		dirSv(self.dir)
		dirSv(c)
		end = '%s/%s - Chapter %s'%(c, d, b)
		yi = self.alias
		
		def save(url):	
			total = 6  #variabel total = max thread
			rl = []					
			x = 0
			length = len(url)
			cz = int(_k._C(int(length) / int(total)))
			for _ in range(total):
				if(x + cz) < length:
					ry = {y:url[y] for y in range(x, x + cz)}
				else:
					ry = {y:url[y] for y in range(x, length)}
				x += cz
				rl.append(ry)
		
			def dl(ur):	
				for r, u in ur.items():
					get = self.contentWeb(u)
					if get[1] == 200:
						with open(f'{end}/{r}.jpg', 'wb') as w:
							w.write(get[0].content)
							w.close()
					if e: pd.update(1)
			if e:
				print('\n※ Chapter: %s ⤵'%b)
				pd = _k._t(total=length)
			tda = []
			for t in range(total):
				tdr = _k._T(target=dl, args=([rl[t]]))
				tda.append(tdr)
			for ts in tda: ts.start()
			for tj in tda: tj.join()			
			if e: pd.close()
		
		def mz(pq):
			_k._z(pq, 'zip', pq)
			_k._r(pq, ignore_errors=True)
			
		def Img():
			I = _k._s('\t|\n', '', self.contentWeb(a)[0].text)
			ti = ['bk', 'mb', 'mt', 'kn', ['mc', 'mg', 'mp', 'mw', 'kg', 'kl', 'pm'], ['dd', 'kb', 'kc', 'ki', 'kk', 'ks', 'kz', 'md', 'mi', 'mo', 'ng']]
			dirSv(end)
			if yi in ti[5]:
				l = self.findText(yi, 2, (I if yi in ['kk', 'kb'] else I.split('"readerarea"' if yi not in ['dd', 'md'] else 'reader-area')[1].split('div' if yi not in ['ki', 'ks', 'kz', 'md'] else ('kln' if yi not in ['ks', 'kz'] else 'nextprev'))[0]))
				if len(l) == 0 and yi == 'md': self.ex.err('Butuh password untuk download!')
				if yi == 'kc': l = list(filter(None, l))
				save(l)
			elif yi == ti[0]:
				l = self.findText(yi, 2, I)[0]
				y ='"imgdata.xyz/%s' % _k._a.new(l[0], _k._a.MODE_CBC, _k._b(l[1])[:_k._a.block_size]).decrypt(_k._b(l[1])[_k._a.block_size:]).decode('utf8')
				v = _k._c(r'"(.*?)"').findall(y.replace('\\',''))
				ll = ['https://'+w for w in v]
				save(ll)			
			elif yi == ti[1]:
				y = _k._j(_k._c(r"fff = '(.*?)'").findall(I)[0])		
				v = _k._a.new(_k._ah(_k._hx(_k._pb('sha512', '_0xcfdi'.encode('utf8'), _k._uh(y['salt']), 999, 32)).decode('utf8')), _k._a.MODE_CBC, _k._ah(y['iv']), segment_size=64).decrypt(_k._ab(y['ciphertext'])).decode('utf8')
				l = self.findText(yi, 2, v)
				save(l)
			elif yi == ti[2]:
				l = _k._j(self.findText(yi, 2, I)[0])
				r = {'encrypted': 'watermark', 'webp': 'jpg'} 
				ll = list(filter(None, [_k._c("|".join(r.keys())).sub(lambda u: r[u.group(0)], (x['url'] if x['url'].find('encrypted') != -1 else '')) for x in l]))
				save(ll)
			elif yi == ti[3]:
				l = self.findText(yi, 2, I)
				ll = [(x if x.find('http')!=-1 else 'https:'+x) for x in l]
				save(ll)
			elif yi in ti[4]:
				l = self.findText(yi, 2, I.split('"reading-content"' if yi != 'kg' else '<div id="all" style="text-align: center; ">')[1].split('script' if yi != 'kg' else 'div')[0])
				if len(l) == 0 and yi == 'kl': l =_k._j('[%s]' % _k._c(r'var chapter_preloaded_images = \[(.*?)\]').findall(I)[0])
				save(l)
			else:
				l = _k._j(I.split('"sources":')[1].split(',"lazy')[0])[0]['images']
				save(l)
				
		if e: Img()							
		else:
			try:
				if self.eB: 
					a += '&continue=1'
					rc = self.contentWeb(a)[0].content
					if len(rc) > 444:		
						o = open((f'{end}.zip'), 'wb')
						o.write(rc)
						o.close()
					else:
						self.ex.err(rc.decode('utf8'), False)
				else:
					Img()
					mz(end)
			except _k._e.RequestException as eer:
				print(eer.response.text)
				
	def fixArray(self, a):
		arr, ars = {}, {}
		c = -1
		def sorting(x, y): return {p:u for p, u in sorted(x.items(), key=lambda item: item[y])} 

		for i in range(len(a)):
			if a.count(a[i]) > 1 and a[i][0].isdigit():
				ars[i] = [a[i]]
			else:
				pass
				
		for j in range(len(ars)):
			val = ars.get(list(ars)[j])[0]
			dec = a.count(ars.get(list(ars)[j])[0])
			for k in range(dec):
				pf = k/dec
				kf = float(val)+pf
				if kf not in arr:
					arr[kf] = round(pf, 2)
		sa = sorting(ars, 1)
		sl = list(sorting(arr, 0).values())
		
		for l in sa:
			c +=1
			sa[l] = sa[l][0] + (str(sl[c])[1:] if str(sl[c])[1:].replace('.','') != '0' else '')
			a[l] = sa[l]
		return a
		
	def update(self):
		
		def j(e): return _k._j(e)
		def reWrite(a, b, c=True):
			a.seek(0)
			a.truncate(0)
			if c:
				a.write(_k._ds(b))
			else:
				a.write(b)
				a.close()
		def getNew(a, b, c):
			if a != b:
				reWrite(c, b, False)
				return True
			else:
				return False
		def nextUp(a, b):			
			x = open(a, 'r+') 
			y = x.read() 
			z = _k._g(b).text 
			return getNew(y, z, x)
			
		url = 'https://raw.githubusercontent.com/komiker-py/json/main/update.json'
		p = '%s/update.json' % self.path
		oData = open(p, 'r+')
		jData = j(oData.read())
		last = _k._d.fromtimestamp(jData['date'])
		now = _k._d.now()
		defisit = now - last
		if defisit.days > 1:
			jData["date"] = _k._d.now().timestamp()
			reWrite(oData, jData)
			uData = j(_k._g(url).text)			
			if jData['data'] != uData['data']:
				jData['data'] = uData['data']
				reWrite(oData, jData)
				status = True
			else: status = False
			oData.close()
			if status:
				result = nextUp('%s/data.json' % self.path, uData['data'])
				if result:
					nextUp('%s/data/%s.json' % (self.path, self.alias), self.regex.get(self.alias)[6])
			if jData['version'] != uData['version']:
				return uData['version']