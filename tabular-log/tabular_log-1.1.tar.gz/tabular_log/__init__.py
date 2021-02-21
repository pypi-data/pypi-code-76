"""tabular_log
"""
from csv import DictWriter
from datetime import datetime as dt

__author__ = "help@castellanidavide.it"
__version__ = "01.01 2021-2-21"

class tabular_log:
	def __init__ (
					self, 
					file="trace.log", 
					fieldnames=['Execution code', 'Message', 'Message time', 'Message time for users'], 
					message_style={'Execution code': '{start_time}', 'Message': '{message}', 'Message time': '{message_time}', 'Message time for users': '{message_time_for_users}'},
					format_style={}
				):
		"""Where it all begins
		"""
		# Init variabiles
		self.file = file
		self.fieldnames = fieldnames
		self.message_style = message_style
		self.format_style = format_style
		self.start = int(dt.now().timestamp())

		# Setup functions
		self.header()
		
	def header(self):
		"""If not exist add header
		"""
		try:
			if open(self.file, 'r+').readline() == "":
				assert(False)
		except:
			open(self.file, 'w+').write(str(self.fieldnames)[1:-1].replace("'", "\"").replace("\", \"", "\",\"") + "\n")

	def print(self, message):
		"""Write one line
		I open every time the file, because with this method if there is a crash I can be sure that all previous line are into it
		"""

		# Add my values to given format_style
		format_style = {**self.format_style, **{'start_time': f'{self.start}', 'message': message, 'message_time': f'{dt.now().timestamp()}', 'message_time_for_users': f'{dt.now().strftime("%c")}'}}

		# Format the message
		message_style = {}
		for key, value in self.message_style.items():
			message_style[key] = value.format(**format_style)

		# Prints message to file
		DictWriter(open(self.file, 'a+', newline=''), fieldnames=self.fieldnames, restval='').writerow(message_style)

	def prints(self, messages):
		"""Print lots of lines
		"""
		for message in messages:
			self.print(message)
		
if __name__ == "__main__":
	tabular_log()
