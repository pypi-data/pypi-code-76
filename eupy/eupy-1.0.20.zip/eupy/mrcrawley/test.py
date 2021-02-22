#!/usr/bin/env python
# -*- coding: utf-8 -*-

import crawler as cr
import hermes

def test():

	mail = hermes.gmail("fivos_ts@hotmail.com")

	try:
		cr.crawlWeb(['https://www.azlyrics.com/p/pinkfloyd.html'], "/home/fivosts/PhD/Code/pinkySpeaker/dataset")
		mail.broadcast("MrCrawley script", "AZ Lyrics scraping has finished")
	except Exception as e:
		print(e)
		mail.broadcast("MrCrawley script", e)
	return

if __name__ == "__main__":
	test()
