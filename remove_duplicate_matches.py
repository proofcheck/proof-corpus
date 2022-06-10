#!/usr/bin/env python

"""
Checks for duplicate .tex files, and comments out the one with the longer path.

E.g.,
 ./texes/1202/1202.1779/arxiv files/Graphs_of_Epidemics.tex
 ./texes/1202/1202.1779/Graphs_of_Epidemics.tex

becomes
 # ./texes/1202/1202.1779/arxiv files/Graphs_of_Epidemics.tex
 ./texes/1202/1202.1779/Graphs_of_Epidemics.tex

Also comments out files ending in .bak, .svn, .backup, .orig, .tex_ , ...
"""

# e.g.,
# ./remove_duplicate_matches.py matches/eng-matches > matches/eng-matches2
# mv matches/eng-matches2 matches/eng-matches

import re
import sys
from typing import List

import nicer

CMT = "#"

if __name__ == "__main__":
    nicer.make_nice()

    prev_index = 20000
    prev_ID = None
    prev_path = "?" * 200
    prev_name = "?" * 200
    all_lines: List[str] = []
    for filename in sys.argv[1:]:
        with open(filename, "r") as fd:
            for tex_path in fd:
                tex_path = tex_path.strip()
                all_lines.append(tex_path)
                next_index = len(all_lines) - 1

                if tex_path.startswith("#"):
                    continue

                if (
                    tex_path.endswith(".bak")
                    or tex_path.endswith(".backup")
                    or tex_path.endswith(".bk")
                    or tex_path.endswith(".sav")
                    or tex_path.endswith(".source")
                    or tex_path.endswith(".orig")
                    or tex_path.endswith(".doc")
                    or tex_path.endswith("_")
                    or "/.svn/" in tex_path
                    or re.search(r"[.]tex[.]\S+$", tex_path, re.IGNORECASE)
                ):
                    all_lines[next_index] = f"{CMT} " + all_lines[next_index]
                    continue

                m = re.search(
                    r"^./texes/([^/]+/[^/]+)(.*?/)([^/]*)$", tex_path
                )
                if not m:
                    print("ERROR:", tex_path)
                    exit(-1)
                next_ID, next_path, next_name = (
                    m.group(1),
                    m.group(2),
                    m.group(3),
                )

                if prev_ID == next_ID and prev_name.strip(
                    "_"
                ) == next_name.strip("_"):
                    #  print("match", prev_ID, next_ID, prev_name, next_name)
                    if len(next_name) + len(next_path) < len(prev_name) + len(
                        prev_path
                    ):
                        all_lines[prev_index] = (
                            f"{CMT} " + all_lines[prev_index]
                        )
                        prev_path = next_path
                        prev_index = next_index
                    else:
                        all_lines[next_index] = (
                            f"{CMT} " + all_lines[next_index]
                        )
                else:
                    prev_ID = next_ID
                    prev_name = next_name
                    prev_path = next_path
                    prev_index = next_index

    for line in all_lines:
        print(line)
