import komiker as _k

class download:
	
	def __init__(self, url=None, **kwargs):
		
		self.ex = _k._ex()	
		self.regex = _k._j(self.ex.read())
		alias = [j for j in list(self.regex)]
		site = kwargs.get('site')
		rar = kwargs.get('rar')
		if site != None and url != None:
			self.ex.err("Masukan input parameter satu saja!!\n\nContoh:\n\n komik.download(site='mk').generate() \n\n\tatau\n\n komik.download(url='https://bacakomik.co/manga/solo-leveling/').generate()")
		elif site != None and site in alias:
			list_manga = True
		elif url != None:
			list_manga = False
		else:
			self.ex.err(f"Tidak ada argument pada komik.download()\n\nurl= ['url manga']\nsite= {sorted(alias)}")
		rar = rar if rar != None else False
		if rar == True or rar == False: self.rar = rar
		else: self.ex.err('mode gambar/ .rar tidak jelas!')
		self.mode = list_manga
		self.url = url
		if list_manga != True and self.url != None:
			try:
				for i in range(len(self.regex)):
					if self.url.find(list(self.regex.values())[i][3]) != -1:
						self.alias = list(self.regex)[i]
				self.lib = _k._l(self.alias)
			except AttributeError: 
				self.ex.err("Link yang dimasukan tidak ada di pilihan daftar komik!")
		elif list_manga != False and site in alias:
			self.alias = site	
			self.lib = _k._l(self.alias)
		
	def getData(self):
		def result(url):
			getMod = self.getMode()
			dict_url = self.lib.json(url, getMod[0])
			none = ''
			for key in dict_url.keys():none += '%s • '% key
			return dict_url, 'NB: urutan chapter => 《%s 》\n'%none[:-3], getMod
		
		if self.mode != False:
			url = self.lib.initData()
			return url[0], result(url[1])
		elif self.mode != True:
			url = self.url
			if url != '':
				title = _k._c(r'(\/manga\/|\/komik\/)(.*)').findall(url)[0][1].translate(str.maketrans({'-':' ', '/':''})).title()
				return title, result(url)
			else:
				self.ex.err('mode tidak ada!')
		else:
			exit()

	def getMode(self):
		ver = self.lib.ver
		if ver != None: print(f'\33[32m\nUpdate: versi {ver} telah tersedia! Silakan download ulang!\33[0m')
		pM = '\nPilih mode download:\n1. Semua chapter\n2. Satu chapter\n3. Pilih chapter a-b\n'
		sR = eval(self.regex.get(self.alias)[5])
		def cMod(lim):
			in_mode = input('🥀 Masukan angka: ')
			if in_mode.isnumeric():
				n_mode = int(in_mode)
			else:
				self.ex.err('Masukan angka saja!')
			lim += 1
			b_mode = n_mode > 0 and n_mode < lim
			if b_mode: mode = n_mode
			else: self.ex.err('Masukan angka %s saja!' % ', '.join([str(x) for x in range(1, lim)]))
			return mode
		def gRar():
			print(pM)
			return False, 4, cMod(3)
		if not self.rar:
			print(pM+'4. Unduh dalam bentuk berkas .rar\n')
			mode = cMod(4)
			if mode == 4:return gRar()
			return True, mode, False
		elif self.rar: return gRar()
	
	def generate(self):		
		login = self.getData()
		x_x = login[1][2][1]
		T_T = login[1][2][2]
		t = login[0]
		h = login[1][2][0]
		e = login[1][0]	
		sad = '[bold]  《Informasi》'
		life = list(e)
		a = f'{self.lib.dir}/{t}'
		fuck = f'[white]Judul: {t}\n{login[1][1]}[/white]'
		
		def go(d): self.execute(d, e, a, t, h)
		def the(man, x='', y=''):
			if  T_T == 2: print('\n※ Chapter: %s ⤵'%x)
			elif T_T == 3: print('\n※ Chapter: %s sampai %s ⤵'%(x,y))
			return _k._t(man)
		def oh():
			__ = _k._cs.Console()
			__.print()
			__.rule(sad)
			__.print()
			__.print(fuck)
			__.rule()
			__.print()
		if x_x == 1:
			heaven = e
			for hell in heaven: go(hell)
		elif x_x == 2:
			oh()
			hell = self.di(e, '※ Chapter ke: ')[1]
			go(hell)
		elif x_x == 3:
			oh()
			lo = self.di(e, '※ Chapter awal: ')[0]
			ve = self.di(e, '※ Chapter akhir: ')[0]
			ice= [life[null] for null in (range(ve, lo+1) if lo > ve else range(lo, ve+1))]
			for hell in ice: go(hell)
		elif x_x == 4:
			if T_T == 1:
				dream = e
				for hell in the(dream): go(hell)
			elif T_T == 2:
				oh()
				hell = self.di(e, '※ Chapter ke: ')[1]
				for _ in the(range(1), hell): go(hell)
			elif T_T == 3:
				oh()
				lo = self.di(e, '※ Chapter awal: ')
				ve = self.di(e, '※ Chapter akhir: ')
				def me(ok):
					return [ve[ok], (lo[ok]+1 if ok == 0 else lo[ok])] if lo[ok] > ve[ok] else [lo[ok], (ve[ok]+1 if ok == 0 else ve[ok])]
				to = me(0)
				tHe = me(1)
				sky = [life[null] for null in range(to[0], to[1])]
				for hell in the(sky, tHe[0], tHe[1]): go(hell)
			else:
				self.ex.err('\nMasukan angka 1, 2, 3 saja!')
		else:
			self.ex.err('\nMasukan angka 1, 2, 3, 4 saja!')
		
	def di(self, list_url, text):
		def gText(t): return input(t).zfill(len(str(len(list_url))))
		I = gText(text)
		if I.find('.') != -1: I = I.zfill(len(str(len(list_url)))+2)
		while list_url.get(I) == None:
			self.ex.err('Angka yang dimasukan tidak ada di urutan chapter!\n%sPerhatikan dengan benar ;)' % ('\040' * 7), False)
			try:
				I = gText(text)
				if list_url.get(I) != None:		
					break
			except Exception as e:
				print(e)
		l = list(list_url).index(I)
		return l, I
	
	def execute(self, a, b, c, d, e):
		l = str(a).zfill(len(str(len(b))))
		self.lib.saveFile(b[l], l, c, d, e)