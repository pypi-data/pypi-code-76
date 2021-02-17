import os
import sys
import logging
import traceback

# Advanced Info on Error
def error_description():
	"""
	This function gets the file path and error line number 
	when a system exception occurs
	"""
	_, _, exc_tb = sys.exc_info()
	fobj = traceback.extract_tb(exc_tb)[-1]
	fname = fobj.filename
	line_no = fobj.lineno
	return fname, line_no, ''.join(traceback.format_tb(exc_tb))

def construct_error_message(header, bounds, description, filename, line_number, tb):
	"""
	This function constructs the error debug message by breaking line
	"""
	file_message = 'Occured in file: {} \n'.format(filename)
	line_number_message = 'At line: {} \n'.format(line_number)
	error_message = tb+header + '\n' + description + '\n' + file_message + line_number_message + bounds + '\n'
	return error_message

# define Python user-defined exceptions
class GadosServerError(Exception):
	"""
	Base class for other exceptions
	filename: The file where the exception happens
	line_number: Line number where the exception occurs
	"""
	def __init__(self, description, fn=None, lineno=None, tb=None):
		super().__init__()
		self.description = description
		self.json_response = {"indicator":False, "message":description}
		self.bounds = "************************************************\n"
		self.fname, self.line_number, self.tb = fn, lineno, tb
		
	def __str__(self):
		self.header = super().__str__()
		if self.fname == None or self.line_number == None or self.tb == None:
			self.fname, self.line_number, self.tb = error_description()
		error_message = construct_error_message(self.header,self.bounds,self.description,self.fname,self.line_number, self.tb)
		logging.error(error_message)
		return error_message

	@classmethod
	def buildfromexc(cls, desc, fname, lineno, tb):
		"""
		This is the class method to return
		an instance based on existing exception
		"""
		return cls(desc, fname, lineno, tb)

class LackOfArgumentsError(Exception):
	'''
	Raised when it's missing some arguments in the input

	Input Arguments
	--------------------
	exec_info: all the system execution information. can be obtained by sys.exc_info()
	missing_arguments: all the missing arguments (list of strings)
	'''

	def __init__(self, missing_arguments):
		super().__init__("")
		self.missing_arguments = missing_arguments
		self.bounds = "************************************************\n"
		self.description  = "Missing: {}".format(missing_arguments)
		self.json_response = {"indicator":False, "message":self.description}

	def __str__(self):
		self.header = super().__str__()
		self.fname, self.line_number, self.tb = error_description()
		error_message = construct_error_message(self.header,self.bounds,self.description,self.fname,self.line_number, self.tb)
		logging.error(error_message)
		return error_message

class FileMissingError(Exception):
	"""
	If the file is not found in the folder, this error will be raised.
	"""
	def __init__(self, missing_file):
		super().__init__("")
		self.missing_file = missing_file
		self.bounds = "************************************************\n"
		message = "Missing: {}".format(missing_file)
		self.json_response = {"indicator":False, "message":message}

	def __str__(self):
		header = super().__str__()
		return header + "File: "+str(self.missing_file)+".\n"+self.bounds


class ModifyDatabaseError(Exception):
	"""
	Error occur when dealing with the post requests.
	Can't modify the database.
	"""
	def __init__(self, action_type, description):
		super().__init__(description)
		self.action_type = action_type

	def __str__(self):
		header = super().__str__()
		return header + "for Action: "+str(self.action_type)+".\n"+self.bounds


class TestCaseMismatchError(Exception):
	'''
	Raised when some values or keys in test cases mismatch

	Input Arguments
	--------------------
	exec_info: all the system execution information. can be obtained by sys.exc_info()
	missing_arguments: all the missing arguments (list of strings)
	'''
	def __init__(self, key, response_value, result_value):
		super().__init__("")
		self.key = key
		print ("self.key = ",self.key)
		self.response_value = response_value
		print ("self.response_value = ",self.response_value)
		self.result_value = result_value
		print ("self.result_value = ",self.result_value)

	def __str__(self):
		header = super().__str__("")
		print ("Inside string")
		error_message = str(self.key) + str(self.response_value) + str(self.result_value)
		# error_message = "Key: {} Response {} does not match result {}".format(str(self.key),str(self.response_value),str(self.result_value))
		print ("Error message = ",error_message)
		return header + ".\n" +self.bounds
    

