#!/usr/bin/env python3

import os, re, sys, PyPDF2

for file in sys.argv[1:]:
	with open(file, 'rb') as input:
		reader = PyPDF2.PdfFileReader(input)
		print(reader.numPages)
		page = reader.getPage(0)
		print(page.extractText())

