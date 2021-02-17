

import typing

try:
	import jk_datamatrix
	bHasDataMatrix = True
except:
	bHasDataMatrix = False

from .ColumnDef import ColumnDef






#
# This class is derived from <c>list</c> and represents a very simple table. The items in this (table) list are rows of this table.
#
class Table(list):
	# @field		ColumnDef[] columnDefs		The table column definitions

	################################################################################################################################
	## Constructors
	################################################################################################################################

	#
	# @param		ColumnDef[] columnDefs		The table column definitions
	# @param		str[][] rows				The list of row data for this table.
	#
	def __init__(self, columnDefs:typing.List[ColumnDef], rows:list):
		assert isinstance(columnDefs, (tuple, list))
		assert isinstance(rows, (tuple, list))
		assert len(columnDefs) == len(rows[0])
		for h in columnDefs:
			assert isinstance(h, ColumnDef)

		super().__init__()

		self.columnDefs = columnDefs
		self.extend(rows)
	#

	################################################################################################################################
	## Public Properties
	################################################################################################################################

	#
	# Returns the number of columns of this table.
	#
	@property
	def nColumns(self) -> int:
		return len(self[0])
	#

	#
	# Returns the number of rows in this table.
	#
	@property
	def nRows(self) -> int:
		return len(self)
	#

	#
	# The variable <c>columnDefs</c> contains all header specifications. This property returns the header titles only.
	#
	# @return		str[]			Returns the titles of the column definitions.
	#
	@property
	def columnTitles(self) -> typing.List[str]:
		return self.__createListOfTitles(self.columnDefs)
	#

	################################################################################################################################
	## Helper Methods
	################################################################################################################################

	def __createListOfTitles(self, columnDefs:typing.List[ColumnDef]) -> list:
		assert isinstance(columnDefs, (tuple,list))
		for x in columnDefs:
			assert isinstance(x, ColumnDef)

		return [ x.name for x in columnDefs ]
	#

	def __createListOfValueParsers(self, columnDefs:typing.List[ColumnDef]) -> list:
		assert isinstance(columnDefs, (tuple,list))
		for x in columnDefs:
			assert isinstance(x, ColumnDef)

		return [ x.valueParser for x in columnDefs ]
	#

	################################################################################################################################
	## Public Methods
	################################################################################################################################

	#
	# Build a data matrix from this table.
	#
	def toDataMatrix(self, columnDefs:typing.List[ColumnDef] = None):
		if not bHasDataMatrix:
			raise Exception("For invoking toDataMatrix() you need to install jk_datamatrix first: 'pip install jk_datamatrix'")

		# ----

		if columnDefs is None:
			columnDefs = self.columnDefs
		assert len(columnDefs) == self.nColumns

		columnTitles = self.__createListOfTitles(columnDefs)
		valueParsers = self.__createListOfValueParsers(columnDefs)

		m = jk_datamatrix.DataMatrix(columnTitles)

		for row in self:
			rowData = []
			for s, valueParser in zip(row, valueParsers):
				if valueParser:
					rowData.append(valueParser(s))
				else:
					rowData.append(s)
			m.addRow(*rowData)

		return m
	#

#









