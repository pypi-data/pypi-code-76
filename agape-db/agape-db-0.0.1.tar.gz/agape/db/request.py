

from threading import local
thread_data = local()



def set_request(request):
	""" Store the current request to the current thread so the request data may
	be accessed anywhere in the program. """
	setattr( thread_data, 'request', request )

def get_request():
	""" Get the current request as set on the thread data. """
	return getattr( thread_data, 'request', None )

def get_user():
	""" Get the current user via the thread data. """
	request = get_request()

	if not request or not hasattr(request, 'user'):
		# AnonamyousUser is imported locally because an error thrown about models not being loaded yet if imported in header of file
		from django.contrib.auth.models import AnonymousUser
		return AnonymousUser()

	return request.user
