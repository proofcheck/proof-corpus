SHELL=/bin/zsh

OS:=$(shell uname -s)
ifeq ($(OS),Linux)
        NUMPROC := $(shell grep -c ^processor /proc/cpuinfo)
else ifeq ($(OS),Darwin)
        NUMPROC := $(shell sysctl hw.ncpu | awk '{print $$2}')
endif

# Don't use all the CPUs
NUMPROC := $(shell echo "$(NUMPROC)*9/10"|bc)

ifeq ($(NUMPROC),0)
        NUMPROC = 1
endif


all:
	-rm -rf proofs
	-rm -f proofs*.tsv
	-rm -f cleanproofs*.tsv
	-rm -f sent*.tsv
	-rm -f sorted.txt
	-rm -f successful-proof-ids
	./naive.py -p$(NUMPROC) -m matches/eng-matches > log.txt 2>&1
	foreach y (`seq 92 99` `seq -w 0 20`); ./collect_raw_proofs.py $$y >! proofs$$y.tsv; end
	foreach y (`seq 92 99` `seq -w 0 20`); ./cleanup.py -p$(NUMPROC) proofs$$y.tsv > cleanproofs$$y.tsv; end
	foreach y (`seq 92 99` `seq -w 0 20`); ./sentize2.py -p$(NUMPROC) cleanproofs$$y.tsv > sent$$y.tsv; end
	find proofs -name "*.txt" -not -empty | cut -d'/' -f3 | sort > successful-proof-ids
	cut -f2 sent*.tsv | sort | uniq -c | sort -rn > sorted.txt

matches/matches%: matches/eng-matches
	grep "/texes/$*" matches/eng-matches | grep -v "^#" > $@

proofs%.tsv: matches/matches% naive.py collect_raw_proofs.py
	./naive.py -p50 -m $<
	# find proofs/${*}* -type f -name "*.txt" -print0 | xargs -0 cat > proofs$*.raw
	#foreach file (`find proofs/${*}* -type f -name "*.txt"`); sed s:'^':$${file:h4:t2}'\t': "$$file"; end > proofs$*.raw
	./collect_raw_proofs.py $* > proofs$*.tsv

cleanproofs%.tsv: proofs%.tsv cleanup.py
	./cleanup.py -p$(NUMPROC) $< > $@

sent%.tsv: cleanproofs%.tsv sentize2.py
	./sentize2.py -p$(NUMPROC) $< > $@

sorted%.txt: sent%.tsv
	cut -f2 $< | sort | uniq -c | sort -nr > $@

successful-proof-ids:
	find proofs -name "*.txt" -not -empty | cut -d'/' -f3 > successful-proof-ids

.PRECIOUS: matches/matches% proofs%.tsv cleanproofs%.tsv sent%.tsv sorted%.txt
.PHONY: test archive

DATE=$(shell date "+%Y-%m-%d")
archive:
	mkdir $(DATE)
	mv *.tsv successful-proof-ids sorted.txt $(DATE)/


test: new_cleanproofs10.tsv
	./linediff.py 2023-01-01/cleanproofs10.tsv new_cleanproofs10.tsv | less -R

new_cleanproofs10.tsv: cleanup.py
	./cleanup.py -p15 2023-01-01/proofs10.tsv > new_cleanproofs10.tsv
