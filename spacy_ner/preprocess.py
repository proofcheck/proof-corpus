#!/usr/bin/env python

import argparse
import sys
from typing import List, Tuple

import diff_match_patch  # type: ignore
import spacy
from spacy.tokens import DocBin

import cleanup

if __name__ == "__main__":
    # nicer.make_nice()

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-d", "--debug", help="Show tracing output", action="store_true"
    )
    parser.add_argument(
        "-a", "--aggressive", help="Intensity of cleanup", action="store_false"
    )
    parser.add_argument(
        "files", nargs="*", type=argparse.FileType("r"), default=[sys.stdin]
    )
    args = parser.parse_args()

    nlp = spacy.blank("en")
    db = DocBin()

    dmp = diff_match_patch.diff_match_patch()

    for fd in args.files:
        for orig in fd.readlines():
            orig = orig.split("\t")[-1]
            clean = cleanup.clean_proof(
                orig, args.debug, fd.name, args.aggressive
            )
            diff: List[Tuple[int, str]] = dmp.diff_main(  # type: ignore
                orig, clean
            )
            dmp.diff_cleanupSemantic(diff)  # type: ignore
            # print(lines, end=" ")
            string = ""
            for i in range(len(diff) - 1):
                if diff[i][0] == -1 and diff[i + 1][0] == 1:
                    key = diff[i + 1][1].strip()
                    # if key in {"REF", "CITE", "NAME"}:
                    #     chrs = len(string)
                    #     print(
                    #         " " * chrs
                    #         + key
                    #         + "." * (len(diff[i][1]) - len(key))
                    #     )
                    #     # print("REF", chrs, chrs + len(diff[i][1]))

                    # if (
                    #     key in {"REF", "CITE"}  # , "NAME", "CASE:"}
                    #     or (key == "EF" and string.endswith(" R"))
                    #     or (key == "ITE" and string.endswith(" C"))
                    #     or (key == "AME" and string.endswith(" N"))
                    # ):
                    if key == "REF":
                        next = orig[len(string) + len(diff[i][1]) :][
                            :20
                        ]  # diff[i + 2][1][:20] if i < len(diff) - 2 else ""
                        print(
                            string[-20:].ljust(20, " "),
                            diff[i][1].ljust(30, " "),
                            next,
                        )
                        # print(key, diff[i][1], sep="\t")

                if diff[i][0] == 0 or diff[i][0] == -1:
                    string += diff[i][1]
            # print(string)
            # print(diff)


# training_data = [
#     ("Tokyo Tower is 333m tall.", [(0, 11, "BUILDING")]),
# ]
# # the DocBin will store the example documents
# for text, annotations in training_data:
#     doc = nlp(text)
#     ents = []
#     for start, end, label in annotations:
#         span = doc.char_span(start, end, label=label)
#         ents.append(span)
#     doc.ents = ents
#     db.add(doc)
# db.to_disk("./train.spacy")
