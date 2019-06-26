dir_guard=@mkdir -p $(@D)			# prevents non-existing directories

INDEX_URL=https://www.psp.cz/eknih/2013ps/stenprot/zip/index.htm
ZIP_URL=https://www.psp.cz/eknih/2013ps/stenprot/zip/

INDEX=001			# used for a single meeting parsing, always 3-digit number

ALL_MEETINGS=$(shell curl $(INDEX_URL) 2>/dev/null|grep -a schuz.zip |cut -f 2 -d '"')		# list of all meetings
DOWNLOADED_MEETINGS=$(shell ls zips 2>/dev/null || echo "")

.PHONY: getallzips prev prevall prevavail clean

all:
	@echo "Usage: make getzips; make prevall; make prevavail; make prev [INDEX=<ind>]; make clean; make cleanall\n"
	@echo "\e[32m $$ make getallzips: 		\e[0m download all zips from www.psp.cz"
	@echo "\e[32m $$ make prevall: 		\e[0m download zips (if needed) and make vert of all meetings from www.psp.cz"
	@echo "\e[32m $$ make prevavail:		\e[0m make vert of all currently downloaded (available) meetings"
	@echo "\e[32m $$ make prev [INDEX=<ind>]: 	\e[0m download zip (if needed) and make vert of a certain meeting (default INDEX = 001), use only 3-digit indicies"
	@echo "\e[32m $$ make clean: 			\e[0m remove directories unpacked/ and zips/"
	@echo "\e[32m $$ make cleanall:		\e[0m remove unpacked/, zips/ and preverts/ folders"

getallzips: $(ALL_MEETINGS:%=zips/%)

prevall: $(ALL_MEETINGS:%.zip=preverts/%.prevert)

prevavail: $(DOWNLOADED_MEETINGS:%.zip=preverts/%.prevert)

prev: $(INDEX:%=preverts/%schuz.prevert)

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
	@wget -q -O $@ $(ZIP_URL)$*.zip 2>/dev/null || (echo '$* is not accessible!'; rm $@)

clean:
	@rm -rf unpacked zips

cleanall:
	@rm -rf unpacked zips preverts