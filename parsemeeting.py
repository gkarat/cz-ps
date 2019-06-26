#!/usr/bin/python3

# coding=windows-1250

"""
Thanks to the files with the names such as 6-1.htm, 6-2.htm and etc. we can
parse every meeting's day and also write down information about single meeting

And that is actually what that program does, calling then to_prevert function from
another file on every single sXXX.htm like file

"""

#import cProfile, pstats, io 			# for speed control

import os
import glob
import re
import sys
from collections import OrderedDict

from toprevert import to_prevert

months_endings = {
	"dna": 	"01",
	"ra": 	"02",
	"zna": 	"03",
	"bna": 	"04",
	"tna": 	"05",
	"vna": 	"06",
	"ence": "07",
	"pna": 	"08",
	"í": 	"09",
	"jna": 	"10",
	"du": 	"11",
	"ince": "12"
}


def define_month(month):
	"""
	By the ending of the single month in Czech we can define its number
	"""
	for ending in months_endings.keys():
		if month.endswith(ending):
			return months_endings[ending]
	return None


def print_docs_tag(fout, title):
	"""
	Prints information about the new day of a meeting

	title's format example: "Stenografický zápis 5. schůze, 21. ledna 2014"
	"""
	meeting_number = re.search("[0-9].*(?=. sch)", title).group(0)
	meeting_day = re.search("(?<=ze, ).[0-9]*", title).group(0)
	
	if len(meeting_day) == 1:
		meeting_day = '0' + meeting_day

	month = re.search("(?<=, [0-9].{3}).*(?=.[0-9]{4})", title).group(0)
	meeting_month = define_month(month)

	if meeting_month == 'None':
		sys.exit("^^^ Invalid month format!")

	meeting_year = re.search("[0-9]{4}", title).group(0)
	date = meeting_year + "-" + meeting_month + "-" + meeting_day

	fout.write("<docs meeting=\"%s\" date=\"%s\" period=\"PS-VII-2013\">\n" % 
		(meeting_number, date))


def parse_meeting(meeting_name, fout):
	days_list = glob.glob('unpacked/%s/[0-9]*' % meeting_name)
	days_list.sort()

	for day in days_list:		# parsing "1-2.htm" like documents, which contains order information in their titles
		with open(day, encoding = "windows-1250") as fday:
			day_content = fday.read()

		title = re.search("(?<=<title>).*(?=<)", day_content).group(0).replace("&nbsp;", " ")
		print_docs_tag(fout, title)

		protocols = re.findall("(?<=<a href=\")s.*(?=#)", day_content)
		protocols = list(OrderedDict.fromkeys(protocols))
		for protocol_name in protocols:
			to_prevert('unpacked/%s/%s' % (meeting_name, protocol_name), fout)		# go through single protocol and write down to the summary file


if __name__ == '__main__':
	# pr = cProfile.Profile()
	# pr.enable()

	if not os.path.exists("unpacked/%s" % sys.argv[1]):
		sys.exit()
	with open("preverts/%s.prevert" % sys.argv[1], "w")	as fout:
		parse_meeting(sys.argv[1], fout)


	# pr.disable()
	# s = io.StringIO()
	# sortby = 'cumulative'
	# ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
	# ps.print_stats()
	# print(s.getvalue())