#!/usr/bin/env python

"Map IDs in TSVs from source IDs to online IDs."

# When building the corpus it is convenient to use IDs that reference
# the specific source directory, e.g.,
#      2001/2001.00002
#      9302/alg-geom9302003
# because the data labeled <id> was extracted from the source directory
#      texes/<id>
#
# But for public-facing purposes, it is more convenient to use the
# simpler IDs used online by arXiv.org, which don't include the
# (redundant) YYMM prefix, and which require a slash between the
# alphabetic part (if any) and the numeric part
#      2001.00002
#      alg-geom/9302003
# because this is how the paper is referenced in metadata, and a
# also we can map <id> to the online URL
#      https://arxiv.org/abs/<id>

import argparse
import re
import sys

# Turn xxxx/ddd.dddd      into ddd.dddd
# Turn xxxx/aaa-aaddd.ddd into aaa-aa/ddd.ddd
tagfix_re = re.compile(r"^\d\d\d\d/([a-zA-Z-]*)([0-9.]+)\w*\t", re.MULTILINE)

def fixtag(m : re.Match) -> str:
    if m.group(1):
        return m.group(1) + "/" + m.group(2) + "\t"
    else:
        return m.group(2)+"\t"

if __name__ == "__main__":

    parser = argparse.ArgumentParser()

    parser.add_argument("files", nargs="*", type=argparse.FileType("r"),
                        default=[sys.stdin],
                        help="tsv files to update")
    args = parser.parse_args()

    for fd in args.files:
        text = fd.read()
        tabs = text.count("\t")
        assert tabs > 0
        (text, tags_fixed) = re.subn(tagfix_re, fixtag, text)
        if tabs == tags_fixed:
            print(text)
        else:
            error(f"{tabs} tabs, but {tags_fixed} tags found")
