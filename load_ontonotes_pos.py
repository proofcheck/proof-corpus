from nltk.corpus.reader.bracket_parse import BracketParseCorpusReader

# E.g., to get the sentences from sections 00 through 18,
# which is what nltk's default tagger seems to have been trained on
#
#   sentences = []
#   for sect in range(0,19):
#      sentences += load_section(sect)

def load_section(sect):
    "Return tagged sentences from section sect of ontonotes WSJ."
    if isinstance(sect,int):
        sect = f'{sect:02d}'
    DIR = f"/research/proofcheck/ontonotes-release-5.0/data/files/data/english/annotations/nw/wsj/{sect}"
    corpus = BracketParseCorpusReader(DIR, ".*parse")
    return list(corpus.tagged_sents())



