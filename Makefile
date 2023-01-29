SHELL=/bin/zsh

test: new_cleanproofs10.tsv
	./linediff.py 2023-01-01/cleanproofs10.tsv new_cleanproofs10.tsv | less -R

new_cleanproofs10.tsv: cleanup.py
	./cleanup.py -p15 2023-01-01/proofs10.tsv > new_cleanproofs10.tsv

all:
	-rm -rf proofs
	-rm -rf proofs*.tsv
	-rm -rf cleanproofs*.tsv
	-rm -rf sent*.tsv
	-rm -rf sorted.txt
	./naive.py -p36 -m matches/eng-matches > log.txt 2>&1
	foreach y (`seq 92 99` `seq -w 0 20`); ./collect_raw_proofs.py $$y >! proofs$$y.tsv; end
	foreach y (`seq 92 99` `seq -w 0 20`); ./cleanup.py -p36 proofs$$y.tsv > cleanproofs$$y.tsv; end
	foreach y (`seq 92 99` `seq -w 0 20`); ./sentize2.py -p36 cleanproofs$$y.tsv > sent$$y.tsv; end
	find proofs -name "*.txt" -not -empty | cut -d'/' -f3 | sort > successful-proof-ids
	cut -f2 sent*.tsv | sort | uniq -c | sort -rn > sorted.txt

matches/matches%: matches/eng-matches
	grep "/texes/$*" matches/eng-matches | grep -v "^#" > $@

proofs%.tsv: matches/matches% naive.py
	./naive.py -p50 -m $<
	# find proofs/${*}* -type f -name "*.txt" -print0 | xargs -0 cat > proofs$*.raw
	#foreach file (`find proofs/${*}* -type f -name "*.txt"`); sed s:'^':$${file:h4:t2}'\t': "$$file"; end > proofs$*.raw
	./collect_raw_proofs.py $* > proofs$*.tsv

cleanproofs%.tsv: proofs%.tsv cleanup.py
	./cleanup.py -p50 $< > $@

sent%.tsv: cleanproofs%.tsv sentize2.py
	./sentize2.py -p50 $< > $@

sorted%.txt: sent%.tsv
	cut -f2 $< | sort | uniq -c | sort -nr > $@

backup%:
	cp sorted$*.txt

successful-proof-ids:
	find proofs -name "*.txt" -not -empty | cut -d'/' -f3 > successful-proof-ids

.PRECIOUS: matches/matches% proofs%.tsv cleanproofs%.tsv sent%.tsv sorted%.txt
.PHONY: test
