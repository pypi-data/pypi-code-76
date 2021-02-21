
from runtype import dataclass

class Type:
	def __add__(self, other):
		return SumType.create((self, other))
	def __mul__(self, other):
		return ProductType((self, other))

class DataType(Type):
	def __init__(self, name):
		self.name = name

	def __repr__(self):
		return self.name

	def __le__(self, other):
		if isinstance(other, DataType):
			return self == other

		return NotImplemented

class SumType(Type):
	def __init__(self, types):
		self.types = types

	@classmethod
	def create(cls, types):
		x = set()
		for t in types:
			if isinstance(t, SumType):
				x |= set(t.types)
			else:
				x.add(t)

		if len(x) == 1:
			return list(x)[0]
		return cls(x)

	def __repr__(self):
		return '(%s)' % '+'.join(map(repr, self.types))

	def __le__(self, other):
		return all(t <= other for t in self.types)

	def __ge__(self, other):
		return any(other <= t for t in self.types)

	def __eq__(self, other):
		return self.types == other.types
	def __hash__(self):
		return hash(frozenset(self.types))

class ProductType(Type):
	def __init__(self, types):
		self.types = types

	def __repr__(self):
		return '(%s)' % '*'.join(map(repr, self.types))

	def __hash__(self):
		return hash(self.types)
	def __eq__(self, other):
		return self.types == other.types

	def __le__(self, other):
		if isinstance(other, ProductType):
			if len(self.types) != len(other.types):
				return False

			return all(t1<=t2 for t1, t2 in zip(self.types, other.types))
		elif isinstance(other, DataType):
			return False

		return NotImplemented


class PhantomTypeInstance(Type):
	def __init__(self, phantom, inner):
		self.phantom = phantom
		self.inner = inner

	def __repr__(self):
		return '%r[%r]' % (self.phantom, self.inner)

	def __le__(self, other):
		if isinstance(other, PhantomType):
			return self.phantom == other
		elif isinstance(other, PhantomTypeInstance):
			return self.phantom == other.phantom and self.inner <= other.inner
		elif isinstance(other, SumType):
			return NotImplemented

		return self.inner <= other

	def __ge__(self, other):
		assert isinstance(other, (DataType, PhantomType))	# XXX What if inner is Any?
		return False

	def __hash__(self):
		return hash((self.phantom, self.inner))
	def __eq__(self, other):
		return self.phantom == other.phantom and self.inner == other.inner

class PhantomType(Type):
	def __init__(self, name):
		self.name = name

	def __repr__(self):
		return self.name

	def __getitem__(self, other):
		return PhantomTypeInstance(self, other)

	def __le__(self, other):
		if isinstance(other, PhantomType):
			return self == other
		return NotImplemented


num = DataType('num')
text = DataType('text')
proj = PhantomType('projected')
agg = PhantomType('aggregated')

# Test Sum/Product types equality
assert (num + text + text) == num + text
assert (num + text * text) == num + text * text
assert (num + text * (text + num) + num) == text * (num + text) + num
assert (num*text+num*text) == num*text
assert (text*num+num*text) == num*text+text*num

# Test subtyping
assert num <= text+(num+text)
assert text*num <= text+num+text*num

# Test Phantom types equality
assert (text+proj+proj) == text + proj
assert (text+proj[num]+proj[num]) == text + proj[num]
assert (text+proj[num]+proj[text]) != text + proj[text]
assert proj + agg == agg + proj
assert proj != agg
assert proj[num] != agg[num]
assert agg[text] <= proj[num] + agg[text] 
assert not agg[num] <= proj[num] + agg[text] 

# Test Phantom subtyping
assert( proj[num] <= num)
assert( proj[num] <= proj)
assert( proj <= proj)
assert( not proj <= proj[num])
assert( not proj[num] <= proj[text])
assert( proj[num] <= proj[text+num])
assert( not num+text <= proj[text]+num)
assert( not proj[num]+text <= proj[text]+num)
assert( not proj[num]+text <= proj[text])
assert( proj[num]+text <= num+text)

assert(proj[num] + proj[text] <= proj[num + text])
assert( proj[text] <= proj[text]+num)

# print(proj[num + text] <= proj[num] + proj[text] )
# print( proj[num+text] <= proj[text]+num)