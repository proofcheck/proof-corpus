matches/matches%: matches/eng-matches
	grep "/texes/$*" matches/eng-matches | grep -v "^#" > $@

proofs%.raw: matches/matches% naive.py
	./naive.py -p50 -m $<
	# find proofs/${*}* -type f -name "*.txt" -print0 | xargs -0 cat > proofs$*.raw
	#foreach file (`find proofs/${*}* -type f -name "*.txt"`); sed s:'^':$${file:h4:t2}'\t': "$$file"; end > proofs$*.raw
	./collect_raw_proofs.py $* > proofs$*.raw

proofs%.txt: proofs%.raw cleanup.py
	./cleanup.py -p50 $< > $@

sent%.txt: proofs%.txt sentize2.py
	./sentize2.py -p50 $< > $@

sorted%.txt: sent%.txt
	cut -f2 $< | sort | uniq -c | sort -nr > $@

backup%:
	cp sorted$*.txt

.PRECIOUS: matches/matches% proofs%.raw proofs%.txt sent%.txt sorted%.txt
