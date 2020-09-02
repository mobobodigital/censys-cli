# !/usr/bin/env python
# -*- coding: utf-8 -*-
 
from termcolor import colored
import argparse
import json
import requests
import codecs
import locale
import os
import sys
import ast
import time
 
   
class Censys:
	def __init__(self, q, o):
		self.API_URL = "https://www.censys.io/api/v1"
		self.UID = ""
		self.SECRET = ""
		self.q = q
		self.o = o
 
	def search(self):
		pages = 10
		page = 1
		fp = open(o, 'a+')
 
		while page <= pages:
			print('[*] start searching page %d' % page)
			params = {'query' : self.q, 'page' : page}
			res = requests.post(self.API_URL + "/search/ipv4", json = params, auth = (self.UID, self.SECRET))
			if res.status_code != 200:
				print('error occured: %s' % res.json()['error'])
				sys.exit(1)
			else:
				for r in res.json()['results']:
					# now we should check the protocols
					protocols = r['protocols']
					for proto in protocols:					
						proto = proto.split('/')
						if proto[1] == 'http':
							print(r['ip'] + ':' + proto[0])
							fp.write(r['ip'] + ':' + proto[0] + '\n')
			
			page += 1							
			time.sleep(5)

parser = argparse.ArgumentParser(description = 'CENSYS.IO Web Server Search')
parser.add_argument('-f', '--find', help='CENSYS Search', required = True)
parser.add_argument('-o', '--output', help='Output File', required = True)
 
 
args = parser.parse_args()
q = args.find
o = args.output
 
censys = Censys(q, o)
censys.search()
