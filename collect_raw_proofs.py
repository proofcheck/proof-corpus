#!/usr/bin/env python

from pathlib import Path
import sys

p = Path("proofs")

for filename in p.glob(sys.argv[1] + "*/**/*.txt"):
    with open(filename, "r") as fd:
        id = "/".join(filename.parts[1:3])
        for line in fd:
            print(f"{id}\t{line.strip()}")
