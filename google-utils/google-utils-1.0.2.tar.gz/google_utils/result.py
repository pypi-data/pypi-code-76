from typing import Optional

class Result:
	'''Result returned from google.com'''
	def __init__(self, **kwargs):
		
		self.title: Optional[str] = kwargs.get('title') #: The title of a result
		self.link: Optional[str] = kwargs.get('link') #: The link of a result
		self.domain: Optional[str] = kwargs.get('domain') #: The domain of a result
		self.answer: Optional[str] = kwargs.get('answer') #: The math answer of a result
		self.question: Optional[str] = kwargs.get('question') #: The parsed math question of a result
		self.phrase: Optional[str] = kwargs.get('phrase') #: The parsed phrase of a result
		self.pronunciation: Optional[str] = kwargs.get('pronun') #: The pronunciation of a result
		self.type: Optional[str] = kwargs.get('type') #: The type of a phrase of a result
		self.meaning: Optional[str] = kwargs.get('meaning') # The meaning of a result
		self.weather: Optional[str] = kwargs.get('weather') # The weather of the location
		self.temperature: Optional[str] = kwargs.get('temp') # The temperature of the location