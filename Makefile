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

.PRECIOUS: matches/matches% proofs%.tsv cleanproofs%.tsv sent%.tsv sorted%.txt