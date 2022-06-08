#!/usr/bin/env python

"""
Checks for english proof-output.

Reads a list of tex files (from a file) and checks if the
corresponding proof file seems to be in English. Prints the
same list to stdout, but comments out (with a leading #)
the ones likely to be problematic.
"""

# e.g.,
# time ./filter_dup_matches.py matches/eng-matches > filtered-eng-matches

import re
import os
import sys

import nicer


if __name__ == "__main__":
    nicer.make_nice()

    for filename in sys.argv[1:]:
        with open(filename, "r") as fd:
            for tex_path in fd:
                tex_path = tex_path.strip()
                if tex_path[0] == "#":
                    print(tex_path)
                    # sys.stderr.write(f"skipping {tex_path}\n")
                    continue
                TEXES = "texes/"
                proof_path: str = (
                    "proofs/" + tex_path[tex_path.find(TEXES) + len(TEXES) :]
                ).replace(".tex", ".txt")
                if os.path.isfile(proof_path):
                    with open(proof_path, "r") as pfd:
                        text = pfd.read().strip()
                        if re.match(
                            r"See\b.*(Appendix|REF|CITE|Supplement)|Direct calculation|Standard|Trivial",
                            text,
                            re.IGNORECASE,
                        ):
                            # Definitely a false positive
                            pass
                        elif re.fullmatch(
                            r"\W+",
                            text,
                        ):
                            # not really english
                            print(f"# {tex_path} ?? {repr(excerpt(text))}")
                            continue
                        elif text and len(text) > 5:
                            try:
                                lang: str = langdetect.detect(text)
                            except langdetect.LangDetectException:
                                lang = "unknown"
                            if lang != "en":
                                if lang == "fr" or (
                                    lang
                                    in {
                                        "de",
                                        "es",
                                        "pt",
                                        "ru",
                                        "it",
                                        "jp",
                                        "pl",
                                        "ja",
                                        "fi",
                                        "uk",
                                        "bg",
                                        "ca",
                                        "tr",
                                        "el",
                                    }
                                    and len(text) > 40
                                ):
                                    print(
                                        f"# {tex_path} {lang} {excerpt(text)}"
                                    )
                                    continue
                                else:
                                    # probably a false positive
                                    sys.stderr.write(f"{lang}\n{tex_path}\n")
                                    sys.stderr.write(f">> {text[:320]}\n\n")

                print(tex_path)
