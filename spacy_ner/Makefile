setup: cleanup.py nicer.py known_names.txt words_alpha.txt

cleanup.py:
	ln -s ../cleanup.py cleanup.py

nicer.py:
	ln -s ../nicer.py nicer.py

known_names.txt:
	ln -s ../known_names.txt known_names.txt

words_alpha.txt:
	ln -s ../words_alpha.txt words_alpha.txt




train:
	python -m spacy train config.cfg --paths.train ./train.spacy --paths.dev ./train.spacy
	# python -m spacy train config.cfg --paths.train ./train.spacy --paths.dev ./dev.spacy

debug:
	python -m spacy debug data config.cfg --paths.train ./train.spacy --paths.dev ./dev.spacy

.PHONY: train debug setup
