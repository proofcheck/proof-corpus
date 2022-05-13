#!/usr/bin/env python

"""Display differences between two files, line by line."""

from signal import signal, SIGPIPE, SIG_DFL
import sys
from typing import List, Tuple

import diff_match_patch  # type: ignore


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
    LONG = 18  # how long is a "long" amount of common text?
    # abbreviate a common prefix
    if diff and diff[0][0] == 0 and len(diff[0][1]) > LONG:
        words = diff[0][1].split(" ")
        diff[0] = (0, "…" + " ".join(words[-4:]))

    if diff and diff[-1][0] == 0 and len(diff[-1][1]) > LONG:
        words = diff[-1][1].split(" ")
        suffix = " ".join(words[:4])
        while (
            suffix.endswith(".")
            or suffix.endswith(")")
            or suffix.endswith(",")
        ):
            suffix = suffix[:-1]
        diff[-1] = (0, suffix + "…")

    for (n, s) in diff:
        if n == 0:
            if len(s) > 2 * LONG and "…" not in s:
                s = s[: (LONG - 1)] + "…" + s[-(LONG - 1) :]
            print(s, end="")
        elif n == -1 and show_del:
            print(
                "\033[31m\033[1m" + strikethrough(s) + "\033[0m",
                end="",
            )
        elif n == 1:
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
