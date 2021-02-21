from slacki.slacki import slacki
import slacki.utils.check_connection as check_connection

__author__ = 'Erdogan Tasksen'
__email__ = 'erdogant@gmail.com'
__version__ = '1.0.0'

# module level doc-string
__doc__ = """
slacki
=====================================================================

Description
-----------
Python package slacki for reading and posting in slack groups.

Example
-------
>>> from slacki import slacki
>>> sc = slacki(channel='new_channel', token='xoxp-123234234235-123234234235-123234234235-adedce74748c3844747aed48499bb')
>>>
>>> # Get some info about the channels
>>> channels = sc.get_channels()
>>>
>>> # Get some info about the users
>>> users = sc.get_users()
>>> 
>>> # Send messages
>>> queries=['message 1','message 2']
>>> sc.post(queries)
>>> 
>>> # Snoozing
>>> sc.snooze(minutes=1)
>>> 
>>> # Post file
>>> sc.post_file(file='./data/slack.png', title='Nu ook met figuren uploaden :)')
>>> 
>>> # listen (retrieve only last message)
>>> out = sc.retrieve_posts(n=3, retrieve_names=True)
>>>

References
----------
https://github.com/erdogant/slacki

"""
