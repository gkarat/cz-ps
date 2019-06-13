#!/usr/bin/python3

"""

Parses .prevert file to .vert format


"""

import sys
import re
from bs4 import BeautifulSoup


def print_speech_block(fout, speech):
	fout.write(speech[0])
	fout.write("\n")


def print_paragraph(fout, p):
	for line in p[1:]:
		line = line.strip()
		if line.startswith("<"):			# if it is only <p> or another tag in line
			fout.write(line + "\n")
			continue
		line = line.split()			# if it is a normal line, then split every word
		for word in line:
			if word[-1] in [',', '.', '?', '!']:
				fout.write(word[:-1] + "\n")
				fout.write("<g/>\n" + word[-1] + "\n")
			else:
				fout.write(word[:-1] + "\n")


def to_vert(filename, target):
	with open(filename, encoding = "ISO-8859-1") as file:
		content = file.read()
	fout = open(target, "w")
	soup = BeautifulSoup(content, "lxml")
	for speech in soup.find_all('speech'):
		speech = str(speech).splitlines()
		print_speech_block(fout, speech)
		print_paragraph(fout, speech)
	fout.close()


to_vert("test.prevert", "test.vert")