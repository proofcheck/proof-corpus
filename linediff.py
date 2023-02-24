#!/usr/bin/env python

"""Display differences between two files, line by line."""

import re
from signal import signal, SIGPIPE, SIG_DFL
import sys
from typing import List, Tuple

import diff_match_patch  # type: ignore

SHOW_WORDS = 3


def strikethrough(s: str):
    """
    Return a string with strikethrough markup.

    Uses unicode combining-strikethrough character.
    """
    cs: List[str] = []
    for c in s:
        cs.append("\u0336")
        cs.append(c)
    return "".join(cs)


def print_diff(diff: List[Tuple[int, str]], show_del: bool = True):
    """Pretty-print the result of the line diff."""

    num_diffs = len(diff)
    for i in range(num_diffs):
        n, s = diff[i]
        if n == 0:
            words = re.split(r"\s+", s)
            num_words = len(words)

            # Abbreviate text with lots of words
            if i == 0 and num_words > SHOW_WORDS:
                # omit leading words in the sentence
                s = "…" + " ".join(words[-SHOW_WORDS:])
            elif i == num_diffs - 1 and num_words > SHOW_WORDS:
                # omit trailing words in the sentence
                s = " ".join(words[:SHOW_WORDS])
                while s.endswith(".") or s.endswith(")") or s.endswith(","):
                    # delete trailing punctuation too
                    s = s[:-1]
                s = s + "…"
            elif num_words > SHOW_WORDS * 2:
                # omit middle words in the middle of a sentence
                #
                # when s ends with a space (which is common), the last word
                # in the list words will be an empty string.
                # In that case, we emit one extra (hopefully visible) word
                # after the ellipsis, so there are SHOW_WORDS visible words.
                s = (
                    " ".join(words[:SHOW_WORDS])
                    + "…"
                    + " ".join(
                        words[-SHOW_WORDS - (1 if s[-1] == " " else 0) :]
                    )
                )

            print(s, end="")
        elif n == -1:
            if show_del or i + 1 < num_diffs and diff[i + 1][0] == 0:
                print(
                    "\033[31m\033[1m" + strikethrough(s) + "\033[0m",
                    end="",
                )
        elif n == 1:
            if s.strip() == "":
                s = s.replace(" ", "⎵")
            print(
                "\033[32m\033[1m" + s + "\033[0m",
                end="",
            )
    print()


if __name__ == "__main__":

    # Ignore SIG_PIPE and don't throw exceptions on it...
    #   (http://docs.python.org/library/signal.html)
    signal(SIGPIPE, SIG_DFL)

    if len(sys.argv) != 3:
        print("Usage: linediff.py <file1> <file2>")
        sys.exit(1)

    file1 = sys.argv[1]
    file2 = sys.argv[2]

    dmp = diff_match_patch.diff_match_patch()

    lines = 0
    with open(file1, "r") as fd1:
        with open(file2, "r") as fd2:
            try:
                for (line1, line2) in zip(fd1.readlines(), fd2.readlines()):
                    lines += 1
                    line1 = line1.strip()
                    line2 = line2.strip()
                    if line1 == line2:
                        continue

                    diff: List[
                        Tuple[int, str]
                    ] = dmp.diff_main(  # type: ignore
                        line1, line2
                    )
                    dmp.diff_cleanupSemantic(diff)  # type: ignore
                    print(lines, end=" ")
                    print_diff(diff)
            except IOError as e:
                print("wow")
                print(e)
