#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from .common import _seemsValidText
from telegram_util import matchKey

SHORT_ARTICLE = ['每日书摘']

def _seemsValidRawArticle(soup, text_limit = 500):
	if not _seemsValidText(soup, limit = text_limit):
		return False
	return not not soup.find('img')

def _getInnerArticle_(soup, domain):	
	applicators = [
		lambda x: x.find("article"),
		lambda x: x.find("article"),
		lambda x: x.find("main"),
		lambda x: x.find("div", {"id" : "article_cont"}),
		lambda x: x.find("div", {"id" : "js_content"}),
		lambda x: x.find("div", {"id" : "bodyContent"}),
		lambda x: x.find("div", {"id" : "content_JS"}),
		lambda x: x.find("div", class_ = "main-post"),
		lambda x: x.find("div", class_ = "article"),
		lambda x: x.find("div", class_ = "field-name-body"),
		lambda x: x.find("div", class_ = "content"),
		lambda x: x.find("div", class_ = "u-content"),
		lambda x: x.find("div", class_ = "RichContent-inner"),
		lambda x: x.find("div", class_ = "entry-content"),
		lambda x: x.find("div", class_ = 'pf-content'),
		lambda x: x.find("div", class_ = 'pn-single-post-wrapper__content'),
		lambda x: x.find("div", class_ = 'post-content'),
		lambda x: x.find("div", class_ = 'inner_content'),
		lambda x: x.find("div", class_ = 'content_wrapper'),
		lambda x: x.find("div", class_ = "story-body__inner"),
		lambda x: x.find("div", class_ = "answercell"),
		lambda x: x.find("div", class_ = "post-text"),
		lambda x: x.find("div", class_ = "post-body"),
		lambda x: x.find("div", class_ = "mainContent"),
		lambda x: x.find("div", class_ = "pane-node-body"),
	]
	domain_specific_applicators = {
		'': [lambda x: x.find("body")],
		'matters': [lambda x: x.find("div", class_ = "u-content")],
		'douban': [
			lambda x: x.find("div", {"id" : "link-report"}),
			lambda x: x.find("div", class_ = "note"),
			lambda x: x.find("div", class_ = "review-content"),
			lambda x: x.find("div", class_ = "status-wrapper"),],
		'thepaper': [
			lambda x: x.find("div", class_ = "news_txt"),
			lambda x: x.find('div', class_ = 'news_part')],
		'greenpeace.org': [
			lambda x: x.find("section", class_ = 'ct-container'),
			lambda x: x.find("div", class_ = 'descriptiveParagraph')],
		'gravitysworm': [lambda x: x.find("div", class_ = "copy")],
		'opinion.cw.com.tw': [lambda x: x.find("article"),],
		'chinaworker.': [lambda x: x.find("div", class_ = 'pf-content'),],
		'thesocietypages.org': [lambda x: x.find("div", class_ = 'post-content'),],
		'chinadigitaltimes.': [lambda x: x.find("div", class_ = 'post-content'),],
		'twreporter.org':[lambda x: x.find("div", {"id" : "article-body"}),],
		'bbc.co.uk': [lambda x: x.find("div", {"dir": "ltr"})],
		'bbc.com': [lambda x: x.find("article"), lambda x: x.find("main")],
		'equalityrights.hku.hk': [lambda x: x.find("article")],
	}
	is_short = matchKey(soup.text, SHORT_ARTICLE)
	text_limit = 150 if is_short else 500
	for applicator in applicators:
		candidate = applicator(soup)
		if _seemsValidRawArticle(candidate, text_limit = text_limit):
			soup = candidate
	for d, applicators in domain_specific_applicators.items():
		if d in domain:
			for applicator in applicators:
				candidate = applicator(soup)
				if candidate:
					soup = candidate
	return soup

def _getInnerArticle(soup, domain):
	all_content = str(soup)
	inner = _getInnerArticle_(soup, domain)
	index = all_content.find(str(inner))
	if index == -1:
		return inner, None
	return inner, all_content[:index]