import komiker as _k

class extra:
	
	def __init__(self):
		self.path = _k._o.dirname(__file__)
		
	def read(self):
		bo = open(f'{self.path}/data.json').read()
		bp = ''.join(([chr(k) for k in range(65, 91)])[x]+([chr(j) for j in range(97, 123)])[x] for x in range(26))
		bq = _k._b(''.join((lambda c: (bp[26:]+bp[:26])[bp.find(c)] if bp.find(c) > -1 else c)(c) for c in bo)).decode('utf-8')
		return bq
		
	def err(self, string, bool=True):
		print(f'\33[32m\nError: {string}\33[0m')
		if bool: exit()