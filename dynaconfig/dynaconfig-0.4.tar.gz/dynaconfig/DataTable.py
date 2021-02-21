import io
import re
import pint, numpy, scipy.interpolate

class DataTable:
  '''Class that wraps a simple data table.'''

  ureg=pint.UnitRegistry()

  def __init__( self, filename = None, spec = dict()):
    self._filename = filename
    self._spec = spec
    self._data = None
    self._interp = None

    if not self._filename is None:
      self.load()

  def __getstate__(self):
    '''Add pickle support.'''

    return { 'filename' : self._filename
           , 'spec' : self._spec
           , 'data' : self._data
           }

  def __setstate__(self,state):
    '''Add pickle support.'''

    self._filename = state['filename']
    self._spec = state['spec']
    self._data = state['data']
    self._setup_interp()

  def _setup_interp(self):
    self._interp = [ scipy.interpolate.interp1d( self._data[0], self._data[j] ) for j in range(1,len(self._data) ) ]
    return

  def __call__(self,i,j=None):
    if j is None:
      j = i
      i = 0
    return self._data[j][i]

  def _get_units(self,col):
    units = ""
    if 'units' in self._spec:
      if col < len(self._data):
        units = self._spec['units'][col]
    return units

  def _make_Q(self,v,col):
    '''Return a Quantity with units determined by the column number.'''

    # if the val is a string, try to convert it to a quantity
    if isinstance(v,str):
      try:
        v = self.ureg.Quantity( v )
      except:
        pass

      if v.units == self.ureg.dimensionless:
        v = v.magnitude

    if not isinstance(v, pint.quantity._Quantity):
      v = self.ureg.Quantity( v, self._get_units(col) )

    v = v.to( self._get_units(col) )

    return v


  def load(self, fn = None):
    if not fn is None:
      self._filename = fn

    with open(self._filename) as f:
      self.loadfh(f)

  def loadfh(self, fh):

    # scan for spec data first
    for line in fh:
      line = line.strip()
      if len(line) > 0 and line[0] == '#':
        tokens = line[1:].split()
        key = tokens[0]
        key = key.strip()
        key = key.strip(':')
        self._spec[ key ] = tokens[1:]

    # reset fh
    fh.seek(0,0)
    self._data = numpy.loadtxt( fh, unpack=True )
    self._setup_interp()


    return

  def loads(self, text):
    fh = io.StringIO(text)
    self.loadfh(fh)


  def get(self,i,j=None,unit=None,default=None):
    '''Return a quantity from the table. This will return a quantity with units.
       If you just want the value of the quantity, use __call__.'''
    if j is None:
      j = i
      i = 0

    v = self(i,j)
    q = self._make_Q(v, j)
    if unit:
      q.ito(unit)

    return q

  def interp(self,x,j=None):
    '''Return an interpolated value from the table.'''
    if j is None:
      j = 1

    v = self._interp[j-1]( x )
    return v

  def iget(self,x,j=None,unit=None):
    '''Return an interpolated quantity from the table.'''
    if j is None:
      j = 1

    x = self._make_Q(x,0)

    v = self.interp(x.magnitude,j)
    v = self._make_Q(v, j)
    if unit:
      v.ito(unit)

    return v

  def rowstr(self,x,cols,units=None):
    '''Build and return a row string.'''
    if not isinstance(cols,list):
      cols = [cols]
    if not isinstance(units,list):
      units = [units]

    x = self._make_Q(x,0)

    vals = []
    for i in range(len(cols)):
      vals.append( self.iget(x,cols[i],units[i]) )

    text = str(x.magnitude)
    for v in vals:
      text += " " + str(v.magnitude)

    return text


  def __str__(self):
    text = ""
    for i in range(len(self._data)):
      x = self._data[i][0]
      text += self.rowstr( x, list(range(1,len(self._data))) )
      text += "\n"
    return text


