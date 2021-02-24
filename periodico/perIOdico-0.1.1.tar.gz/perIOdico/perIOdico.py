#venv/bin/python3.8
from bs4 import BeautifulSoup
from datetime import datetime
import requests
import shutil

import sys
import subprocess


def get_date():
	while True:
		try:
			date_str = input("When were you born? (DD-MM-YYYY): ")
			return datetime.strptime(date_str, '%d-%m-%Y')
		except ValueError:
			print("Date is incorrect, try again")


class perIOdico:
	def __init__(self, date, verbose=False):
		self.verbose = verbose
		str_date = date.strftime('%Y/%m/%d')
		self.url = 'https://elpais.com/hemeroteca/elpais/portadas/{}'.format(str_date) 

	def get_image(self):
		try:
			self.response = requests.get(self.url)
		except requests.exceptions.MissingSchema:
			if self.verbose: 
				print('There is not a page for that day')

		soup = BeautifulSoup(self.response.content, 'html.parser')
		image_url = soup.find_all('img')[0].get('src')

		self.image = requests.get(image_url, stream=True)

		if self.image.status_code == 200:
			with open("img.jpg", 'wb') as f:
				self.image.raw.decode_content = True
				shutil.copyfileobj(self.image.raw, f)
		else:
			if self.verbose:
				print("I could not find first page for that day")
			return

	def open_image(path):
	    viewer = {'linux':'xdg-open',
	                                  'win32':'explorer',
	                                  'darwin':'open'}[sys.platform]

	    subprocess.run([viewer, 'img.jpg'])