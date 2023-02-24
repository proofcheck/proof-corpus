#!/usr/bin/env python

from pathlib import Path
import sys

""" a quick script to run through every proof text file and compile them all into a proofs file for the given year """


p = Path("proofs")

for filename in sorted(p.glob(sys.argv[1] + "*/**/*.txt")):
    with open(filename, "r") as fd:
        id = "/".join(filename.parts[1:3])
        for line in fd:
            print(f"{id}\t{line.strip()}")
