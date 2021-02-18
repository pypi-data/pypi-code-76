import os
import signal
signals = ['SIGINT', 'SIGQUIT', 'SIGKILL', 'SIGBREAK', 'SIGCHILD', 'SIGCONT', 'SIGTERM',]

def send_signal(provided=None):
	"""Sends a signal"""
	if not provided in signals:
		raise ValueError('incorrect signal provided')
	else:
		pid = os.getpid()
		string = f'os.kill({pid}, signal.{provided})'
		eval(string)

def help():
	print("syntax example: send_signal('SIGINT')")