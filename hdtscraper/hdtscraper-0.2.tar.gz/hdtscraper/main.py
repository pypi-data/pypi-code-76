import requests
from bs4 import BeautifulSoup
import re
import time
import os

class hdtscraper:
	page_url = 'https://hdtorrents.xyz/index.php?page={}'
	__session = None
	__session_start = None

	def __init__(self, username, password, login_url='https://hdtorrents.xyz/takelogin.php', home_url='https://hdtorrents.xyz'):
		self.username = username
		self.password = password
		self.login_url = login_url
		self.home_url = home_url

	def __login(self):
		self.__session = requests.Session()
		self.__session_start = time.time()
		response = self.__session.get(self.login_url)
		assert response.status_code == 200, f'The login url "{self.login_url}" returned status code "{response.status_code}"'

		credentials = dict(username=self.username, password=self.password)

		csrf_token = response.raw.headers._container['set-cookie'][1].split('=')[1].split(';')[0]
		credentials['csrfmiddlewaretoken'] = csrf_token

		response = self.__session.post(self.login_url, data=credentials, headers={'Referer': self.home_url})
		assert response.status_code == 200, f'The login url "{self.login_url}" returned status code "{response.status_code}"'

	def login(self):
		if self.__session_start is None or time.time() > (self.__session_start + (10 * 60)):
			self.__login()
		return self.__session

	def get_last(self, movie_count, max_pages=50):
		movies = []
		for i in range(max_pages):
			movies = movies + self.get_page(i)
			if len(movies) >= movie_count:
				break
		return movies[:movie_count]

	def get_new(self, hd_id, max_pages=50):
		movies = []
		hd_ids = []
		for i in range(max_pages):
			movies = movies + self.get_page(i)
			hd_ids = [m['hd_id'] for m in movies]
			if str(hd_id) in hd_ids:
				break
		if str(hd_id) in hd_ids:
			return movies[:hd_ids.index(str(hd_id))]
		else:
			return movies	

	def get_page(self, page_index):
		session = self.login()
		response = session.get(self.page_url.format(page_index))
		content = response.content
		soup = BeautifulSoup(content, "html.parser")
		raw_movies = soup.find_all('td',{'style':'text-align: left;'})
		movies = []
		for movie_content in raw_movies:
			try:
				movie = {}
				movie['resolution'] = movie_content.find_all('img',{'align':'right', 'border':'0'})[0]['title']
				movie['imdb_url'] = movie_content.find_all('a',{'target':'blank'})[0]['href']
				movie['imdb_code'] = movie['imdb_url'].split('/')[-2]
				movie['size'] = float(re.findall(r'(?P<size>\d+\.\d+) GB', str(movie_content))[0])

				right_content = movie_content.find_all('div',{'align':'right'})[0]
				movie['torrent_url'] = self.home_url + '/' + right_content.find_all('a')[0]['href']
				movie['torrent_name'] = movie['torrent_url'].split('=')[-1]
				movie['torrent_details_url'] = self.home_url + '/' + right_content.find_all('a')[1]['href']
				movie['hd_id'] = movie['torrent_details_url'].split('=')[-1]
				movies.append(movie)
			except:
				pass
		return movies

	def download_torrent(self, movie, dst_path):
		session = self.login()
		response = session.get(movie['torrent_url'])

		with open(os.path.join(dst_path, movie['torrent_name']), 'wb') as torrent:
			torrent.write(response.content)
	
if __name__ == '__main__':
	import getpass

	username = input('Username: ')
	password = getpass.getpass('Password: ')
	hd = hdtscraper(username, password)
	movie = hd.get_last(1)[0]
	hd.download_torrent(movie, '.')