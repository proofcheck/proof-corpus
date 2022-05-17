matches/matches%: matches/eng-matches
	grep "/texes/$*" matches/eng-matches | grep -v "^#" > $@

proofs%.raw: matches/matches% naive.py
	./naive.py -p8 -m $<
	find proofs/${*}* -type f -name "*.txt" -print0 | xargs -0 cat > proofs$*.raw

proofs%.txt: proofs%.raw cleanup.py
	./cleanup.py $< > $@

sent%.txt: proofs%.txt
	./sentize2.py $< > $@

sorted%.txt: sent%.txt
	sort $< | uniq -c | sort -nr > $@

.PRECIOUS: matches/matches% proofs%.raw proofs%.txt sent%.txt sorted%.txt
