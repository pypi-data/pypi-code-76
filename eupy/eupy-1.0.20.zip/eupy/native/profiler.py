#!/usr/bin/env python
import os
import logging

# os.path.basename(frame.f_code.co_filename)

def tracefunc(frame, event, arg):

	print(frame)
	print(frame.f_code)
	print(frame.f_locals)
	print(frame.f_back)
	print(event)
	print(arg)
	if event == "call":
		print("-" + "> call function", frame.f_code.co_name)
	elif event == "return":
		print("<" + "-", "exit function", frame.f_code.co_name)
	return tracefunc

# import sys
# sys.setprofile(tracefunc)
