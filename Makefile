dir_guard=@mkdir -p $(@D)			# prevents non-existing directories

INDEXURL=https://www.psp.cz/eknih/2013ps/stenprot/zip/index.htm

INDEX=001			# used for a single meeting parsing, always 3-digit number

ALL_MEETINGS=$(shell curl $(INDEXURL) 2>/dev/null|grep -a schuz.zip |cut -f 2 -d '"')		# list of all meetings

.PHONY: allzips toprevall toprev clean

all:
	@echo "Usage: make getzips; make toprevall; make toprev <INDEX=XXX>; make clean\n"
	@echo "- make getzips: 		download all available zips from INDEXURL"
	@echo "- make toprevall: 		format all meetings into prevert format"
	@echo "- make toprev <INDEX=XXX>: 	format a certain meeting with 3-digit index (default = 001)"
	@echo "- make clean: 			remove directories unpacked/ and zips/"
	@echo "\n! bs4 MODULE HAS TO BE INSTALLED ON YOUR MACHINE FOR CORRECT SCRIPT WORK !\n"

getzips: $(ALL_MEETINGS:%=zips/%)

toprevall: $(ALL_MEETINGS:%.zip=preverts/%.prevert)

toprev: $(INDEX:%=preverts/%schuz.prevert)

preverts/%.prevert: unpacked/%
	$(dir_guard)
	@echo 'parsing $* into prevert...'
	@python3 parsemeeting.py $*
	@echo

unpacked/%: zips/%.zip
	$(dir_guard)
	@echo 'unpacking $*.zip...'
	@unzip -q zips/$*.zip -d $@ 2>/dev/null || echo '$* not found in zips/!'

zips/%.zip:
	$(dir_guard)
	@echo 'downloading $*.zip...'
	@wget -q -O $@ https://www.psp.cz/eknih/2013ps/stenprot/zip/$*.zip 2>/dev/null || (echo '$* is not accessible!'; rm $@)

clean:
	@rm -rf unpacked
	@rm -rf zips