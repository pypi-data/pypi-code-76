

import typing
import json

from .ColumnDef import ColumnDef
from .Table import Table






class LineList(list):

	################################################################################################################################
	## Constructors
	################################################################################################################################

	def __init__(self, *args):
		super().__init__()
		if len(args) == 0:
			pass
		elif len(args) == 1:
			if isinstance(args[0], str):
				self.extend(args[0].rstrip().split("\n"))
			elif isinstance(args[0], (tuple,list)):
				self.extend(args[0])
			else:
				raise TypeError()
		else:
			raise Exception("Parameters!")
	#

	################################################################################################################################
	## Public Properties
	################################################################################################################################

	################################################################################################################################
	## Helper Methods
	################################################################################################################################

	################################################################################################################################
	## Public Methods
	################################################################################################################################

	#
	# Returns a line numbers of lines that are empty.
	#
	def getLineNumbersOfEmptyLines(self, bStrip:bool = True) -> list:
		assert isinstance(bStrip, bool)

		ret = []
		for lineNo, line in enumerate(self):
			if bStrip:
				line = line.strip()
				if not line:
					ret.append(lineNo)
		return ret
	#

	def isVerticalSpaceColumn(self, pos:int) -> bool:
		for i in range(0, len(self)):
			line = self[i]
			if pos < len(line):
				if not line[pos].isspace():
					#print("@ " + str(pos) + " with " + repr(line[pos]) + " of " + repr(line))
					return False
		#print("@ " + str(pos) + " is space")
		return True
	#

	def dump(self, prefix:str = None, printFunc = None):
		if prefix is None:
			prefix = ""
		else:
			assert isinstance(prefix, str)

		if printFunc is None:
			printFunc = print
		else:
			assert callable(printFunc)

		# ----

		lines = json.dumps(self, indent="\t").split("\n")
		for line in lines:
			printFunc(prefix + line)
	#

	#
	# For every single line count the number of leading space characters. Put all these counts into a list (= one count for every line) and return this list.
	#
	# @return				int[]			Returns a list of counts that indicate how many leading space characters there are in each line.
	#
	def getLeadingSpaceCounts(self) -> typing.List[int]:
		counts = []
		for line in self:
			bCounted = False
			for n, c in enumerate(line):
				if not c.isspace():
					counts.append(n)
					bCounted = True
					break
			if not bCounted:
				counts.append(len(line))
		minPos = min(counts)

		return counts
	#

	#
	# @param		bool bRStrip		Perform an <c>rstrip()</c> on each line.
	#
	def extractColumn(self, fromPos:typing.Union[int,None], toPos:typing.Union[int,None], bRStrip:bool = True) -> list:
		if fromPos is not None:
			isinstance(fromPos, int)
		if toPos is not None:
			isinstance(toPos, int)
		if (fromPos is None) and (toPos is None):
			raise Exception("Parameters!")
		assert isinstance(bRStrip, bool)

		ret = []

		for line in self:
			s = line[fromPos:toPos]
			if bRStrip:
				ret.append(s.rstrip())
			else:
				ret.append(s)

		return ret
	#

	#
	# Get a list of columns. Each column contains the strings found in the specified position range.
	#
	# @param		bool bRStrip		Perform an <c>rstrip()</c> on each line.
	#
	def extractColumns(self, positions:typing.Union[tuple,list], bRStrip:bool = True) -> list:
		ret = []
		for i in range(1, len(positions)):
			fromPos, toPos = positions[i-1], positions[i]
			ret.append(self.extractColumn(fromPos, toPos, bRStrip))
		ret.append(self.extractColumn(positions[-1], None, bRStrip))
		return ret
	#

	#
	# This method creates a string table from this line list.
	# It splits the lines at the specified positions and returns an instance of <c>StringTable</c>
	# containing all data.
	#
	# @param		bool bRStrip		Perform an <c>rstrip()</c> on each line.
	#
	def createStrTableFromColumns(self,
		positions:typing.Union[tuple,list],
		bRStrip:bool = True,
		bFirstLineIsHeader:bool = False) -> Table:

		assert isinstance(bFirstLineIsHeader, bool)

		columnsData = self.extractColumns(positions, bRStrip)
		nColumns = len(columnsData)
		nRows = len(columnsData[0])

		ret = []
		for nRow in range(0, nRows):
			row = []
			for nCol in range(0, nColumns):
				row.append(columnsData[nCol][nRow])
			ret.append(row)

		if bFirstLineIsHeader:
			headers = ret[0]
			del ret[0]
		else:
			headers = [ None ] * len(ret[0])

		for i in range(0, nColumns):
			if headers[i] is None:
				headers[i] = ColumnDef(str(i), None)
			else:
				headers[i] = ColumnDef(headers[i], None)

		return Table(headers, ret)
	#

	#
	# Invokes <c>createStrTableFromColumns()</c> to 
	#
	# @param		bool bRStrip		Perform an <c>rstrip()</c> on each line.
	#
	def createDataTableFromColumns(self,
		positions:typing.Union[tuple,list],
		bRStrip:bool = True,
		bFirstLineIsHeader:bool = False,
		columnDefs:typing.Union[tuple,list,None] = None) -> Table:

		assert isinstance(bFirstLineIsHeader, bool)

		table = self.createStrTableFromColumns(positions, bRStrip)

		if columnDefs is not None:
			assert isinstance(columnDefs, (tuple,list))
			if len(columnDefs) != len(positions):
				raise Exception("Number of header entries specified does not match the number of columns specified!")
			_tmp = []
			for item in columnDefs:
				if isinstance(item, str):
					_tmp.append(ColumnDef(item, None))
				elif isinstance(item, ColumnDef):
					_tmp.append(item)
				else:
					raise ValueError()
				columnDefs = _tmp
			if bFirstLineIsHeader:
				del table[0]
		else:
			if bFirstLineIsHeader:
				columnTitles = table[0]
				del table[0]
				columnDefs = [ ColumnDef(columnTitle) for columnTitle in columnTitles ]
			else:
				raise Exception("Header specification required!")

		# extract value parsers

		valueParsers = [ x.valueParser for x in columnDefs ]

		# build data table

		ret = []
		for row in table:
			rowData = []
			for s, valueParser in zip(row, valueParsers):
				if valueParser:
					rowData.append(valueParser(s))
				else:
					rowData.append(s)
			ret.append(rowData)
		return Table(columnDefs, ret)
	#

	#
	# Splits the current list of lines at empty lines.
	#
	# @param		bool bRStrip		Perform an <c>rstrip()</c> on each line.
	#
	def splitAtEmptyLines(self, bRStrip:bool = True) -> list:
		assert isinstance(bRStrip, bool)

		ret = []
		buffer = LineList()

		for line in self:
			if bRStrip:
				line = line.rstrip()
			if line:
				buffer.append(line)
			else:
				if buffer:
					ret.append(buffer)
					buffer = LineList()

		if buffer:
			ret.append(buffer)

		return ret
	#

	#
	# This method modifies this line list *in place*. It removes all trailing white spaces of each line.
	#
	def rightTrimAllLines(self):
		for i in range(0, len(self)):
			self[i] = self[i].rstrip()
	#

	#
	# This method modifies this line list *in place*. It removes all emtpy lines at the beginning of this line list.
	#
	def removeLeadingEmptyLines(self):
		while self and not self[0]:
			del self[0]
	#

	#
	# This method modifies this line list *in place*. It removes all emtpy lines at the end of this line list.
	#
	def removeTrailingEmptyLines(self):
		while self and not self[-1]:
			del self[-1]
	#

	#
	# This method modifies this line list *in place*. It calls <c>getLeadingSpaceCounts()</c> in order to get a map of leading spaces and then trims the start of the line to
	# have all common (!) leading spaces removed.
	#
	def removeAllCommonLeadingSpaces(self):
		counts = self.getLeadingSpaceCounts()
		minPos = min(counts)
		if minPos > 0:
			newLines = [ s[minPos:] for s in self ]
			self.clear()
			self.extend(newLines)
	#

	################################################################################################################################
	## Static Methods
	################################################################################################################################

#









