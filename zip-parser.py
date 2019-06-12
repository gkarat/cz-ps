#!/usr/bin/python3

#####
#####
##### Gets url as an argument and searches for all links with .zip files to download
##### Then it downloads them and sort its content to every new created folder
#####
#####

import os
import sys
import re
import urllib.request
import requests, zipfile, io

def create_target_folder():
	try:
		os.mkdir('gathered')
	except OSError:  
		sys.exit("Creation of the directory 'gathered/' failed")
	else:  
		print ("Successfully created the directory 'gathered/'")


def zip_download(zip_url):
	print("parsing %s..." % zip_url)
	r = requests.get(zip_url)

	if r.status_code == 404:
		print("%s is not available! \nSkipping..." % zip_url)
		return False
	return zipfile.ZipFile(io.BytesIO(r.content))


def zip_extract(zipf, zip_name):
	if not zipf:
		return
	zipf.extractall("gathered/%s" % zip_name)


if __name__ == '__main__':
	src_link = sys.argv[1]
	print("Source link: %s" %src_link)
	
	create_target_folder()

	### reading content of web-page
	file = urllib.request.urlopen(src_link)
	html_content = file.read().decode('windows-1250')

	### finding all links with .zip ending
	for zip_name in (re.findall("[\\d][^\\s]+.zip", html_content)):
		url = re.search(r"http[^\s]+[^index.htm]", src_link).group(0) + zip_name
		### downloading and unzipping
		zip_extract(zip_download(url), zip_name[:-4])

	file.close()