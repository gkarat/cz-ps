#!/usr/bin/python3

"""

Goes through the all content, which was gathered by parsezip.py
and calls to_prevert function on every html file ("sXXX.htm") found 


"""

import sys
import os
from toprevert import to_prevert


def create_folder(name):
	try:
		os.mkdir(name)
	except OSError:  
		sys.exit("failed creating %s" % name)


if __name__ == '__main__':
	create_folder('gathered-vert')
	for subfolder in os.listdir('gathered'):
		print("parsing content of %s..." % subfolder, end="")
		create_folder('gathered-vert/%s' % subfolder)
		for filename in os.listdir('gathered/%s' % subfolder):
			if filename[0] != 's':
				continue
			to_prevert('gathered/%s/%s' % (subfolder, filename), 'gathered-vert/%s/%s.prevert' % (subfolder, filename))
		print("OK")

