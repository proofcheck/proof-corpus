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
    parser.add_argument("-k", "--key", help="Replacement key", default="REF")
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
                orig, args.debug, fd.name, aggressive=True
            )
            diff: List[Tuple[int, str]] = dmp.diff_main(  # type: ignore
                orig, clean
            )
            dmp.diff_cleanupSemantic(diff)  # type: ignore
            print(diff)
            # print(lines, end=" ")
            string = ""
            i = 0
            while i < len(diff) - 1:
                if diff[i][0] != 1:
                    string += diff[i][1]
                if diff[i][0] == -1 and diff[i + 1][0] == 1:
                    insert = diff[i + 1][1]
                    if i + 2 < len(diff) and diff[i + 1][0] == -1:
                        print("xxxx")
                        remove = diff[i][1] + diff[i + 2][1]
                        string += diff[i + 2][1]
                        i += 2
                    else:
                        remove = diff[i][1]
                    print(f"{remove} \t-> {insert} ")
                i += 1

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
                # if insert.strip() == args.key:
                #     if (i + 2 < len(diff)) and (diff[i + 2][0] == -1):
                #         next = orig[
                #             len(string)
                #             + len(diff[i][1])
                #             + len(diff[i + 2][1]) :
                #         ][:40]
                #     next = orig[len(string) + len(diff[i][1]) :][
                #         :40
                #     ]  # diff[i + 2][1][:20] if i < len(diff) - 2 else ""
                #     if (i + 1 < len(diff) - 1) and (diff[i + 2][0] == -1):
                #         next += diff[i + 2][1][:20]
                #     print(
                #         string[-40:].rjust(40, " "),
                #         diff[i][1].ljust(40, " "),
                #         next,
                #     )
                #     # print(key, diff[i][1], sep="\t")

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
