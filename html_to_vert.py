from bs4 import BeautifulSoup
import sys

def test(src):
	file = open(src, encoding="ISO-8859-2")
	
	print(file.read())
	soup = BeautifulSoup(file, "lxml")

	for a in soup.find_all('p'):
  		print(a.string)

	#parts = soup.find_all("p")

	#for part in parts:
	#	print(part)

	file.close()


if __name__ == '__main__':
	test("gathered/002schuz/s002004.htm")