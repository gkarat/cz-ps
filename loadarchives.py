#!/usr/bin/python3

"""

Gets url as an argument and searches for all links with .zip files to download
then downloads them and sort its content to every new created folder with the same name as a zip


https://www.psp.cz/eknih/2013ps/stenprot/zip/index.htm
"""

import os
import sys
import re
import urllib.request
import requests, zipfile, io

def create_folder(name):
	try:
		os.mkdir(name)
	except OSError:  
		sys.exit("failed creating %s" % name)


def zip_download(zip_url):
	print("downloading %s... " % zip_url, end="")
	r = requests.get(zip_url)
	if r.status_code == 404:
		print("\n%s is not available! \nSkipping..." % zip_url)
		return False
	return zipfile.ZipFile(io.BytesIO(r.content))


def zip_extract(zipf, zip_name):
	if not zipf:
		return
	zipf.extractall("gathered/%s" % zip_name)
	print("OK")


if __name__ == '__main__':
	source_link = sys.argv[1]
	print("SOURCE %s" % source_link)

	create_folder("gathered")
	file = urllib.request.urlopen(source_link)					# reading content of web-page
	html_content = file.read().decode('windows-1250')

	for zip_name in (re.findall("[\\d][^\\s]+.zip", html_content)):						# finding all links with .zip ending
		url = re.search(r"http[^\s]+[^index.htm]", source_link).group(0) + zip_name
		zip_extract(zip_download(url), zip_name[:-4])									# downloading and unzipping

	file.close()