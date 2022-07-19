#!/usr/bin/env python3

"""Extracts proofs from .tex files, naively."""

import argparse
from itertools import repeat
from multiprocessing import Pool
import os
from pathlib import Path
import random
import re
import sys
import traceback
from typing import List, Optional

import bs4
import more_itertools

import kpse
import nicer

"""
Typical usage:
   time ./naive.py -m matches/eng-matches > log.txt 2>&1

 or for a single file,
   ./naive.py t.tex

 Merge commands:
   find proofs -type f -name "*.naive.txt" -print0 \
          | sort -z | xargs -0 ./en_cat.py >! proofs.txt
   ./sentize2.py proofs.txt > sentences.txt

 Or, if we don't care about order:
   find proofs -type f -name "*.naive.txt" -print \
       | xargs ./en_cat.py >! proofs.txt
"""


class SkipThisProof(Exception):
    """Exception if something goes badly wrong while extracting a proof."""

    pass


# Set of LaTeX environments that implicitly switch to math mode.
MATH_ENVS = {
    "align",
    "alignat",
    "displaymath",
    "equation",
    "eqnarray",
    "flalign",
    "gather",
    "multline",
    "dmath",
    "darray",
    "empheq",
    "math",
    "equ",
    "equs",
    # tikz-cd package
    "tikzcd",
    # mathtools package
    "refeq",
    # 1901/1901.07820
    "myequation",
    # 0408/math-ph0408016
    "equa",
    # 0412/math0412117
    "xalignat",  # obsolete amsmath?
    "xxalignat",  # obsolete amsmath?
    # 0409/math0409109
    "endproofeqnarray",
}

# Maps each LaTeX \ref-like command to its number of arguments
# See also https://tinyurl.com/tbj99fsp
TEX_REFS = {
    "\\Autoref": 1,
    "\\autoref": 1,
    "\\cpageref": 1,
    "\\cpagerefrange": 2,
    "\\Cref": 1,
    "\\Crefrange": 2,
    "\\Cpageref": 1,
    "\\Cpagerefrange": 2,
    "\\cref": 1,
    "\\crefrange": 2,
    "\\eqref": 1,
    "\\labelcref": 1,
    "\\nameref": 1,
    "\\pageref": 1,
    "\\ref": 1,
    "\\vref": 1,
    "\\hyperref": 1,
    # commath package
    "\\lemref": 1,
    "\\propref": 1,
    "\\thmref": 1,
    "\\defnref": 1,
    "\\secref": 1,
    "\\remref": 1,
    "\\exref": 1,
    "\\figref": 1,
    "\\colref": 1,
    "\\appref": 1,
    "\\assref": 1,
    # prettyref
    "\\prettyref": 1,
    # theoremref
    "\\thref": 1,
    "\\thnameref": 1,
    # memoir
    "\\fref": 1,
    "\\tref": 1,
    "\\pref": 1,
    "\\Aref": 1,
    "\\Bref": 1,
    "\\Pref": 1,
    "\\Cref": 1,
    "\\Sref": 1,
    # fancyref
    "\\Fref": 1,
    # iopart
    "\\eref": 1,
    "\\Eref": 1,
    "\\fref": 1,
    "\\Fref": 1,
    "\\sref": 1,
    "\\Sref": 1,
    "\\tref": 1,
    "\\Tref": 1,
    # Misc
    "\\relref": 1,
    "\\fullref": 1,
    # subfigure
    "\\subref": 1,
    "\\Subref": 1,
    # 0107/math0107004
    "\\DHrefpart": 1,
    # 0404/cs0404006
    "\\refrange": 2,
    # 1504/1504.06475
    "\\wref": 1,
    # 0209/math-ph0209020
    "\\itemref": 1,
    # 1902/1902.07230
    # 1905/1905.13429
    "\\irref": 1,
}

# Set of LaTeX \cite-like commands
TEX_CITES = {
    "\\cite",
    "\\citealp",
    "\\citealt",
    "\\citeauthor",
    "\\citep",
    "\\citepalias",
    "\\citet",
    "\\citetalias",
    "\\citetext",
    "\\citeyear",
    "\\citeyearpar",
    "\\Citealp",
    "\\Citealt",
    "\\Citeauthor",
    "\\Citep",
    "\\Citet",
    # amsref
    "\\citelist",
    "\\cites",
    # 0304/math0304192
    "\\mycite",
    "\\citeA",
    "\\citeyearNP",
    "\\citeauthorNP",
    "\\citeNP",
    "\\nocite",
    "\\nocitemeta",
    "\\fullcite",
    "\\fullcite",
    "\\fullciteA",
    "\\fullciteNP",
    "\\fullciteauthor",
    "\\fullciteauthorNP",
    "\\shortcite",
    "\\shortciteA",
    "\\shortciteNP",
    "\\shortciteauthor",
    "\\shortciteauthorNP",
    "\\maskcite",
    "\\maskciteA",
    "\\maskciteNP",
    "\\maskciteauthor",
    "\\maskciteauthorNP",
    "\\maskciteyear",
    "\\maskciteyearNP",
    "\\maskfullcite",
    "\\maskfullciteA",
    "\\maskfullciteNP",
    "\\maskfullciteauthor",
    "\\maskfullciteauthorNP",
    "\\maskshortcite",
    "\\maskshortciteA",
    "\\maskshortciteNP",
    "\\maskshortciteauthor",
    "\\maskshortciteauthorNP",
    "\\masknocite",
    "\\masktext",
    "\\citep",
    "\\citet",
    "\\citeyearpar",
    "\\citealp",
    "\\citealt",
    "\\citenum",
    "\\Citep",
    "\\citep*",
    "\\shortcites",
    "\\defcitealias",
    "\\citepalias",
    "\\citetalias",
    "\\citetext",
    "\\citeauthort",
    "\\citeauthorp",
    "\\Citeauthort",
    "\\Citeauthorp",
    "\\bibstyle@apacite",
    "\\bibstyle@apa",
    "\\maskcitep",
    "\\maskcitet",
    "\\maskciteauthor",
    "\\maskciteyear",
    "\\maskciteyearpar",
    "\\maskcitealp",
    "\\maskcitealt",
    "\\maskcitenum",
    "\\maskcitetalias",
    "\\maskcitepalias",
    "\\maskCitep",
    "\\maskCitet",
    "\\maskCiteauthor",
    "\\maskCitealp",
    "\\maskCitealt",
    "\\maskciteauthorp",
    "\\maskciteauthort",
    "\\maskCiteauthorp",
    "\\maskCiteauthort",
    "\\masknocite",
    "\\masktext",
    "\\onlinecite",
}


DELETE_ENVS = {
    # Tables
    "longtable",
    "longtabu",
    "tabbing",
    "table",
    "tabu",
    "tabular",
    "tabularx",
    # Other
    "diagram",
    "minipage",
    "prooftree",
    "tikzpicture",
    "lpic",
    # 1509/1509.06811
    "tz",
    # 2004/2004.04514
    "config",
    # 1602/1602.00521
    "mma",
    # 1902/1902.07230
    # 1905/1905.13429
    "sequentdeduction",
    # 0610/math0610416
    "miniboard",
    # 0011/math0011123
    "diag",
}

DELETE_UNINTERPRETED_ENVS = {
    # Verbatim
    "alltt",
    "code",
    "verbatim",
    "Verbatim",
    "BVerbatim",
    "LVerbatim",
    "lstlisting",
    "mathematica",
    "maplettyout",
    "maplegroup",
    "mapleinput",
    "maplelatex",
    # Figure
    "figure",
    "Figure",
    "floatingfigure",
    # Picture
    "picture",
    "pspicture",
    "overpic",
    # Other
    "comment",
    "filecontents",
    "filecontents*",
    "xy",
    # 1811/1811.04372
    "DGCpicture",
    # 1007.4266
    # 1005.5278
    "haskell",
    # 9911/math9911074
    "texdraw",
    # diagrams package
    "codi",
    # pstricks
    "psmatrix",
}


TEX_IFS = {
    "\\iffalse",
    "\\iftrue",
    "\\ifnum",
    "\\ifdim",
    "\\ifodd",
    "\\ifvmode",
    "\\ifhmode",
    "\\ifmmode",
    "\\ifinner",
    "\\if",
    "\\ifcat",
    "\\ifx",
    "\\ifvoid",
    "\\ifeof",
    "\\ifcase",
    "\\ifcsname",
    "\\ifdefined",
}

VERB_COMMANDS = {
    "\\verb",
    "\\Verb",
    "\\lstinline",
}

MATHONLY_COMMANDS = {
    "_",
    "\\alpha",
    "\\approx",
    "\\beta",
    "\\bigcap",
    "\\bigcup",
    "\\cap",
    "\\cdot",
    "\\chi",
    "\\choose",
    "\\circ",
    "\\cong",
    "\\cup",
    "\\delta",
    "\\Delta",
    "\\epsilon",
    "\\eta",
    "\\frac",
    "\\gamma",
    "\\Gamma",
    "\\geq",
    "\\hookrightarrow",
    "\\in",
    "\\int",
    "\\kappa",
    "\\kappa",
    "\\lambda",
    "\\Lambda",
    "\\langle",
    "\\lceil",
    "\\leadsto",
    "\\left",
    "\\leftarrow",
    "\\leftrightarrow",
    "\\LeftRightArrow",
    "\\leq",
    "\\lfloor",
    "\\Longleftrightarrow",
    "\\mapsto",
    "\\mathbb",
    "\\mathcal",
    "\\mathit",
    "\\mathord",
    "\\mathrel",
    "\\mathrm",
    "\\mathsf",
    "\\mathtt",
    "\\models",
    "\\mu",
    "\\neq",
    "\\nu",
    "\\omega",
    "\\Omega",
    "\\oplus",
    "\\oslash",
    "\\otimes",
    "\\parallel",
    "\\partial",
    "\\phi",
    "\\Phi",
    "\\pi",
    "\\Pi",
    "\\pm",
    "\\prec",
    "\\prec",
    "\\preqeq",
    "\\prod",
    "\\propto",
    "\\psi",
    "\\Psi",
    "\\rangle",
    "\\rho",
    "\\right",
    "\\rightarrow",
    "\\Rightarrow",
    "\\rightharpoonup",
    "\\rightleftharpoons",
    "\\sim",
    "\\simeq",
    "\\subset",
    "\\subseteq",
    "\\succ",
    "\\succ",
    "\\succeq",
    "\\sum",
    "\\supset",
    "\\supseteq",
    "\\tau",
    "\\theta",
    "\\Theta",
    "\\times",
    "\\varphi",
    "\\vdash",
    "\\vee",
    "\\wedge",
    "\\xi",
    "\\Xi",
    "\\zeta",
    "^",
}

NO_ARGUMENT_NOOPS = {
    "\\maketitle",
    "\\frontmatter",
    "\\tableofcontents",
    "\\tiny",
    "\\scriptsize",
    "\\footnotesize",
    "\\small",
    "\\normal",
    "\\large",
    "\\Large",
    "\\LARGE",
    "\\huge",
    "\\Huge",
    "\\rm",
    "\\sl",
    "\\bf",
    "\\tt",
    "\\it",
    "\\sf",
    "\\sc",
    "\\cal",
    "\\rmfamily",
    "\\slfamily",
    "\\bfseries",
    "\\itshape",
    "\\mdseries",
    "\\sffamily",
    "\\ttfamily",
    "\\normalfont",
    "\\cal",
    "\\narrower",
    "\\indent",
    "\\noindent",
    "\\magstephalf",
}

IGNORED_REDEFINES = (
    set(TEX_IFS)
    .union(TEX_CITES)
    .union(TEX_REFS.keys())
    .union(
        [
            "\\HyphConv",
            "\\expandafter",  # 0003/math0003117
            "\\Section",  # 0505/math0505626
            "\\section",
            "\\subsection",
            "\\subsubsection",
            "\\chapter",
            "\\csname",  # # 1603/1603.00294
            "\\MakeDeclareMathSetCommand",  # 1603/1603.00294
        ]
    )
)

IGNORED_INCLUDES = {
    "amsfont",
    "cd",  # 0210/math0210194
    "custalgorithm",  # 0906/0906.4261
    "diagcat",  # 1811/1811.04372
    "dynkin",  # 1210/1210.0342
    "epsf",
    "epsf1990",
    "fig4tex",  # 0312/math0312037
    "floatmodif",  # 1402/1402.4958
    "hyperref",
    "jltmac2e",  # 0007/math0007039
    "moveproofs",  # 1806/1806.03205
    "myfloat",  # 0603/math0603228
    "myurl",  # 0110/cs0110030
    "psfig",
    "scrpage2",  # 0501/math-ph0501039
    "sw20bams",  # 0102/math-ph0102018
    "warmread",  # 0601/math0601187
    "wick",  # 0109/hep-th0109182
    "haskell",  # 1007.4266 1005.5278
    "mathlig",  # 1908.03268
    "figbox",  # 0009/cs0009023
}


# Regular expression for a LaTeX comment.
# The comment runs from the percent sign to the end of line
#   (and the following whitespace on the next line).
#
# But escaped percents (preceeded by a backslash) aren't comments.
# But comments following two backslashes (or an even number of backslashes)
#   are still comments.
# So:
#    % comment
#    \% not a comment
#    \\% comment
#    \\\% not a comment
#    \\\\% comment
# but
#    \\\ \% not a comment
#    \ \\\% not a comment
#
# Assumes every line in this multiline string ends with a newline!
# Non-ASCII ٪ character appears in 1901/1901.05588
TEX_COMMENT = re.compile(r"((?<!\\)(\\\\)+|(?<!\\))[%٪].*?\n[ \t]*")


def decomment(tex_source: str) -> str:
    r"""
    Delete all TeX comments from multiline source code.

    Assumes every line (including the last) ends with \n.
    """
    # Special case: if a line ends with \foo%
    # we don't want to completely dekete the newline
    # and the space starting the next line because
    #    \foo%
    #    bar
    # will then be iterpreted as \foobar rather than foo{}bar
    # In this case, we replace the comment with a space (which will be
    # harmlessly consumed when we read the \foo)
    result = re.sub("(\\\\[A-Za-z]+)[%٪].*?\n[ \t]*", r"\1 ", tex_source)
    result = re.sub(TEX_COMMENT, "", result)
    return result


def fixup(filename: str, tex_source: str) -> str:
    """
    Fixup annoyances in isolated .tex inputs.

    I had been modifying the actual file in texes/*, but
    that's dangerous since there are copies of this
    directory floating around on different computers.
    """
    if "solpara-arxiv-2" in filename:
        tex_source = tex_source.replace(
            "\\providecommand{ }[1]{\\textcolor{blue}{#1}}", ""
        )
    elif "Leb2Poi" in filename:
        tex_source = tex_source.replace(
            "Moreover. the set", "Moreover, the set"
        )
    elif "Journal_Hyp_2020January" in filename:
        tex_source = tex_source.replace(
            "same endpoints. and if", "same endpoints, and if"
        )
    elif "pseudo." in filename:
        tex_source = re.sub(r"\{e\}\$.\s+for \$j", r"{e}$ for $j", tex_source)
    elif "canonicaldomainDMT." in filename:
        tex_source = tex_source.replace(r"\alpha^\sigma$.", r"\alpha^\sigma$,")
    elif "paper_beta_arxiv." in filename:
        tex_source = tex_source.replace("(???)", " REF ")
    elif "abci." in filename:
        tex_source = tex_source.replace("Picture?????", "")
    elif "monotone." in filename:
        tex_source = tex_source.replace("see??.", ".")
    elif "lipschitzfree." in filename:
        tex_source = tex_source.replace("Proposition ???", "Proposition 42")
    elif "shi-yang-eppo." in filename:
        tex_source = tex_source.replace("(??)", "")
    elif "46-100." in filename:
        tex_source = tex_source.replace("？？？？？？？", "")
    elif "CDS-SU2n." in filename:
        # Defines a 2-argument version of \fullref, which
        # we can't handle (because reference commands like
        # \fullref are considered immutable)
        tex_source = tex_source.replace("\\fullref", "\\myfullref")
        tex_source = tex_source.replace("\\pref", "\\mypref")
    elif "modularDD." in filename:
        tex_source = tex_source.replace("\\NewCons{}{} ", "MATH ")
    elif "Harriss_OSTWI." in filename:
        tex_source = tex_source.replace(
            "\\WARMprocessEPS{2to1_three_steps_window}{eps}{bb}", ""
        )
    return tex_source


def tokenize_string(filename: str, tex_source: str):
    """
    Turn a string (representing an entire file) into a stream of TeX-ish words.

    This is a generator function returning strings (tokens).
    """
    # Remove a few known-bad lines

    # 0002/math0002136/zinno.tex
    #  (boxedeps.tex)
    tex_source = tex_source.replace(
        "{\\catcode`\\%=12\\gdef\\P@S@{%!}\\gdef\\pct@@{%%}}", ""
    )

    # Remove ps junk
    tex_source = tex_source.replace("%%BoundingBox", "BB")

    # Fix line endings
    tex_source = tex_source.replace("\r\n", "\n")
    tex_source = tex_source.replace("\r", "\n")

    # Remove all the comments
    tex_source = decomment(tex_source)

    # Ad-hoc fixups
    tex_source = fixup(filename, tex_source)

    # Insert "\par" where there were blank lines
    tex_source = re.sub("^[ \\t]*$", "\\\\par", tex_source, flags=re.MULTILINE)

    # Create a peekable stream of characters.
    chars: more_itertools.peekable[str] = more_itertools.peekable(tex_source)

    while chars:
        # Start building the next input word by grabbing
        # a single charcter.
        word: str = next(chars)
        if word == "\\":
            word += next(chars)
            # It's a command
            if word[1].isalpha() or word[1] == "@":
                # It's an (alphabetic) control sequence.
                # Grab the rest of the word
                while True:
                    ch = chars.peek("!")
                    if ch.isalpha() or ch == "@":
                        word += next(chars)
                    else:
                        break
                # Spaces after _alphabetic_ control sequences
                # are ignored by TeX. Not newlines
                while chars.peek("!") in [" ", "\t"]:
                    next(chars)
        # Treat all space-like characters the same.
        # Any sequence of spaces (including a newline
        # and spaces at the start of the next line) are
        # treated as a single space.
        elif word.isspace():
            word = " "
            while chars.peek("!").isspace():
                next(chars)
        elif word == "$":
            # It's tempting to peek ahead for another "$" and return "$$", but
            # $\alpha$$\beta$ needs to show up as four single $'s.
            pass
        # elif word == "~":
        #    word = " "
        elif word == "#":
            # Make #1 through #9 into single tokens
            d = chars.peek("!")
            if d.isdigit() and d != "0":
                next(chars)
                word += d
        elif word == "`":
            if chars.peek("!") == "`":
                next(chars)
                word = '"'
        elif word == "'":
            if chars.peek("!") == "'":
                next(chars)
                word = '"'
        elif word == "-":
            if chars.peek("!") == "-":
                next(chars)
                if chars.peek("!") == "-":
                    next(chars)
                    word = "—"  # em-dash
                else:
                    word = "–"  # en-dash
        yield word
    return


def get_words(filename: str):
    """Get a stream of words from the given file."""

    path = Path(filename)
    if not path.exists():
        # in case the source code is assuming a case-insensitive
        # file system, and we're running on a linux server with a
        # case-sensitive file system.
        directory, name = os.path.split(path)
        directory, name = (directory or "."), name.lower()
        for f in os.listdir(directory):
            newpath = os.path.join(directory, f)
            if f.lower() == name:
                filename = newpath
                break

    with open(filename, "r") as fh:
        try:
            tex_source: str = fh.read()
        except UnicodeDecodeError:
            with open(filename, "rb") as f:
                tex_bytes = f.read()
                tex_source = bs4.UnicodeDammit.detwingle(tex_bytes)
                tex_source = bs4.UnicodeDammit(tex_source).unicode_markup
                if not tex_source:
                    tex_source = ""

    return more_itertools.peekable(tokenize_string(filename, tex_source))


def skip_ws(words: "more_itertools.peekable[str]"):
    """Skip whitespace characters."""
    while words.peek("!").isspace():
        next(words)


def get_arg(words: "more_itertools.peekable[str]") -> List[str]:
    """Get contents (words) of a single macro argument."""
    skip_ws(words)
    # by default the argument is a single token/word
    w = next(words)
    if w == "{":
        # but if there are curly braces, keep reading
        # words until we find the matching close-brace
        # (allowing for nesting brackets)
        nesting = 1
        arg = []
        while True:
            w = next(words)
            if w == "}":
                nesting -= 1
                assert nesting >= 0  # nosec
                if nesting == 0:
                    break
            elif w == "{":
                nesting += 1
            arg.append(w)
    else:
        arg = [w]
    if arg in [["}"], ["$"], ["\\begin"], ["\\end"]]:
        # Something went wrong (probably because we're not really
        # implementing the full LaTeX language, and the next word
        # can't possibly be a valid argument. Put back whatever we
        # found onto the input stream, and pretend the
        # argument was {} (no words).
        words.prepend(*arg)
        arg = []
    return arg


def skip_optional_eq(words: "more_itertools.peekable[str]"):
    """Skip whitespace, plus an equals-sign & more whitespace if present."""
    skip_ws(words)
    if words.peek("!") == "=":
        next(words)
        skip_ws(words)


def skip_optional_arg(words: "more_itertools.peekable[str]", macros):
    """Skip an optional (bracketed) argument, if present."""
    skip_ws(words)
    if words.peek("!") == "[":
        next(words)
        if words[:3] == ["$", "$", "]"]:
            next(words)
            next(words)
            next(words)
            return
        skip_rest_optional_arg(words, macros)


def skip_rest_optional_arg(words: "more_itertools.peekable[str]", macros):
    """Skip to the end of the bracketed argument we're currently in."""
    while True:
        w = next(words)
        if w in {"$", "\\[", "\\("} and w not in macros:
            single_dollar: bool = False
            if w == "$":
                single_dollar = True
                if words.peek("!") == "$":
                    next(words)
                    single_dollar = False
            skip_rest_math(words, macros, single_dollar)
        elif w == "\\begin":
            get_arg(words)
            skip_rest_env(words, macros)
        elif w == "{":
            words.prepend(w)
            get_arg(words)
        elif w == "]":
            break


def get_optional_arg(words: "more_itertools.peekable[str]"):
    """Get one optional macro argument."""
    w = next(words)
    assert w == "["  # nosec
    arg = []
    while True:
        if words.peek() == "{":
            arg.append("{")
            arg.extend(get_arg(words))
            arg.append("}")
        else:
            w = next(words)
            if w == "]":
                break
            arg.append(w)
    # print("get_optional_arg", arg, words[:10])
    return arg


def skip_rest_conditional(
    words: "more_itertools.peekable[str]", macros, stop_on_else: bool = True
):
    r"""
    Skip the rest of the conditional arm we are currently inside.

    Looks for \fi, and optionally \else. Skips nested
    conditionals, but does not pay attention to { } grouping.
    """
    while True:
        w = next(words)
        # print(f"xxx skipping <<{w}>>")
        if w == "\\fi" or (w == "\\else" and stop_on_else):
            return
        elif w == "\\loop" and w not in macros:
            # Ignore primitive loops
            while next(words) != "\\repeat":
                pass
        elif w in TEX_IFS or w in macros["new ifs"]:
            # If we're skipping past a nested conditional, we want to go
            # all the way to the \fi (not just to the \else), even if
            #  we'd be OK stopping at the \else of the outermost conditional.
            skip_rest_conditional(words, macros, stop_on_else=False)


def skip_num(words: "more_itertools.peekable[str]"):
    """Skip a (decimal) integer or float number."""
    skip_ws(words)
    # Funny numbers like `\@
    if words.peek() == "`":
        next(words)
        return
    # Digits
    if words.peek("x") in {"+", "-"}:
        next(words)
    if words.peek("x").isdigit():
        while words.peek("x").isdigit():
            next(words)
        if words.peek("x") in {",", "."}:
            next(words)
            while words.peek("x").isdigit():
                next(words)
    elif words.peek("x") in {",", "."}:
        next(words)
        while words.peek("x").isdigit():
            next(words)
    else:
        # e.g., \vskip-\topskip
        next(words)


def skip_dimen(words: "more_itertools.peekable[str]"):
    """Skip a TeX dimension (with unit)."""
    skip_num(words)
    skip_ws(words)
    if words[:4] == ["t", "r", "u", "e"]:
        for _ in range(4):
            next(words)
    skip_ws(words)
    try_skip_keywords(
        words,
        [
            "pt",
            "mm",
            "cm",
            "in",
            "ex",
            "em",
            "mu",
            "pc",
            "dd",
            "cc",
            "bp",
            "sp",
            "nd",
            "nc",
        ],
    )
    return


def skip_glue(words: "more_itertools.peekable[str]"):
    """Skip TeX glue (dimension with optional stretch/shrink)."""
    skip_dimen(words)
    while try_skip_keywords(words, ["plus", "minus"]):
        skip_dimen(words)


def get_primitive_def(
    words: "more_itertools.peekable[str]",
    debug: bool = False,
    verbose: bool = False,
):
    r"""
    Process the contents of a \def.

    We currently abuse this to also handle
    \gdef, \xdef, and \edef; we don't respect
    local-global definitions, and don't
    expand the bodies.
    """
    # Get name
    name = next(words)
    if debug:
        print("   defining", name)
    if name == "\\csname":
        while next(words) != "\\endcsname":
            pass
        skip_to_lbrace(words)
        get_arg(words)
        return None, [[]], None
    elif not name.startswith("\\") or name in IGNORED_REDEFINES:
        skip_to_lbrace(words)
        get_arg(words)
        return None, [[]], None
    skip_ws(words)

    # Gather the formal parameter tokens (but don't process them yet)
    parameter_tokens: List[str] = []
    while True:
        tok = next(words)
        if tok == "{":
            break
        parameter_tokens.append(tok)

    # Get body
    words.prepend(tok)  # put back the left brace
    body = get_arg(words)

    # Parse the parameter list
    if len(parameter_tokens) > 0 and parameter_tokens[-1] == "#":
        # A trailing "#" is weird and special
        parameter_tokens[-1] = "{"
        body.append("{")

    # Get parameters
    # Parameter list with n arguments is of the form
    #    [[..], [..], [..], [..], [..]]
    # where the (n+1) [..] parts are lists of delimiter tokens,
    # which might be empty
    parameters: List[List[str]] = [[]]
    # num_params = 0
    # print(f"{parameter_tokens=}")
    for tok in parameter_tokens:
        if tok[0] == "#" and len(tok) == 2:
            # parameter number
            # parameter_number = ord(tok[2]) - ord("0")
            # assert num_params == parameter_number  # nosec
            parameters += [[]]
        else:
            # delimiter
            parameters[-1].append(tok)  # type: ignore

    if debug:
        print(f"Saw def {parameters} {body}")
    return name, parameters, body


def get_newcommand(words):
    r"""Process what follows \newcommand & similar."""
    # Skip optional asterisk
    if words.peek() == "*":
        next(words)
        skip_ws(words)
    # Get name
    names = get_arg(words)
    if len(names) != 1 or names[0] in IGNORED_REDEFINES:
        skip_optional_arg(words, {})
        get_arg(words)
        return None, 0, 0, None
    name = names[0]

    skip_ws(words)
    # print(f" definition {name=}")
    # Not true for active characters
    # assert name.startswith("\\")  # nosec
    # Get parameters
    num_params = 0
    if words.peek() == "[":
        next(words)
        while True:
            d = next(words)
            if d.isdigit():
                num_params = num_params * 10 + int(d)
            elif d.isspace():
                pass
            else:
                assert d == "]"  # nosec
                break

    skip_ws(words)
    # print(f" definition {num_params=}")
    # Get optional parameter
    optional_param: Optional[List[str]] = None
    if words.peek() == "[":
        optional_param = get_optional_arg(words)

    # Save parameters
    # Non-optional parameter list with n arguments is of the form
    #    [[], [], [], [], []]
    # where the (n+1) [] parts are lists of delimiter tokens,
    # which might be empty.
    #   Warning: if there is an optional parameter, then
    #   there are only n [] parts, because there's one
    #   fewer "normal" parameter than the count indicates
    parameters = [[] for _ in range(num_params + 1)]
    if optional_param is not None:
        parameters.pop()

    # Get body
    skip_ws(words)
    # print(" definition getting body from", "".join(words[:100]))
    body = get_arg(words)
    # print(f"Saw ndef {name} {num_params} "
    #       f"{parameters} {optional_param} {body}")
    return name, parameters, optional_param, body


def try_expand(words, parameters, optional_param, body):
    """
    Try to expand a macro.

    We're given information from the definition for a macro
    we just saw, plus the stream of upcoming words. If we
    can find enough arguments, we take them off the
    stream and return the tokens of the substituted macro-body

    If we can't find enough arguments, we consume everything
    we could find, and return an empty list. (We probably
    weren't supposed to expand the macro at this point anyway.)
    """
    # print("try_expand 1")
    param_dict = {}
    # handle optional arg
    if optional_param is not None:
        skip_ws(words)
        if words.peek("!") == "[":
            param_dict["#1"] = get_optional_arg(words)
        else:
            param_dict["#1"] = optional_param
        first_required = 2
    else:
        first_required = 1
    # handle required args
    # primitive tex initial delimeter
    for expected_tok in parameters[0]:
        found_tok = next(words)
        if expected_tok != found_tok:
            return []
    for arg_num, delim in enumerate(parameters[1:], start=first_required):
        parameter_token = "#" + str(arg_num)
        if delim:
            param_dict[parameter_token] = []
            groups_found = 0
            nongroups_found = 0

            while words[: len(delim)] != delim:
                # print(f"looking for {delim=}")
                # print(f"upcoming: {''.join(words[: len(delim)])}")
                # curly braces entirely around a delimited
                if words.peek() == "{":
                    param_dict[parameter_token].append("{")
                    param_dict[parameter_token].extend(get_arg(words))
                    param_dict[parameter_token].append("}")
                    groups_found += 1
                else:
                    param_dict[parameter_token].append(next(words))
                    nongroups_found += 1
            # Remove curly braces if it's a single
            # group, per §400
            if groups_found == 1 and nongroups_found == 0:
                param_dict[parameter_token] = param_dict[parameter_token][1:-1]
            for _ in delim:
                next(words)
        else:
            param_dict[parameter_token] = get_arg(words)

        if param_dict[parameter_token] in [["}"], ["$"]]:
            # Something went wrong; missing argument?
            words.prepend(*param_dict[parameter_token])
            return []

    substituted_body = []
    for tok in body:
        if tok in param_dict:
            substituted_body.extend(param_dict[tok])
        else:
            substituted_body.append(tok)
    # print(f"{body=} {substituted_body=}")
    # Hack: If macro ends with $ and there's a $ immediately following,
    #  it's probably smarter not to treat this as $$.
    #  E.g., 0301/math0301115/waldspurger.tex
    if substituted_body[-1:] == ["$"]:
        substituted_body.append(" ")
    return substituted_body


def skip_rest_math(
    words, macros, single_dollar: bool, debug=False, verbose=False
) -> bool:
    r"""
    Skip past the close of the current math sequence.

    Returns whether the last printable character of the sequence
    is a period (heuristically).
    """
    nwords_seen = 0
    final_period = False
    while True:
        if words.peek() == "{":
            arg = get_arg(words)
            while arg and (arg[-1].isspace() or arg[-1].startswith("\\")):
                arg.pop()
            if arg:
                final_period = arg[-1] == "."
        else:
            # print("srm", words[:20])
            w = next(words)
            nwords_seen += 1
            if nwords_seen >= 100_000:
                print("skip_rest_math", nwords_seen)
                raise SkipThisProof

            if debug:
                print(
                    f"skip_rest_math {single_dollar=} saw: {w} {w in macros}"
                )
                print("   ", "".join(words[:20]))
                if verbose:
                    print("    ", words[:10])
            if w == "$":
                if single_dollar:
                    # Done.
                    break
                else:
                    # Grab the second $ in the $$
                    if words.peek("!") == "$":
                        next(words)
                        break
                    # Hmmm... somehow we reached a $ inside $$ or \[ or ...
                    # Skip the rest of the $...$, and hope for the best
                    if debug:
                        print("entering recursive skip-math")
                    skip_rest_math(words, macros, single_dollar=True)
                    if debug:
                        print("leaving recursive skip-math")
                    continue
            if (w == "\\)" or w == "\\]") and w not in macros:
                break
            elif (w == "\\(" or w == "\\[") and w not in macros:
                skip_rest_math(
                    words,
                    macros,
                    single_dollar=(w == "\\("),
                    debug=debug,
                    verbose=verbose,
                )
            elif w == ".":
                final_period = True
            elif w == "\\end":
                if words:
                    env_name_words = get_arg(words)
                    env_name = "".join(env_name_words)
                    if env_name.startswith("proof"):
                        # oops...hit the end of the proof while we're still
                        # in math mode. abort! abort!
                        words.prepend("\\end", "{", *env_name_words, "}")
                        break
            elif w == "\\label":
                skip_optional_arg(words, macros)
                get_arg(words)
            elif w == "\\eqno" or w == "\\leqno":
                # Make eq. no. doesn't confuse our "final period" flag.
                skip_rest_math(
                    words,
                    macros,
                    single_dollar=False,
                    debug=debug,
                    verbose=verbose,
                )
                break
            elif w == "\\begin":
                env_name = "".join(get_arg(words))
                skip_optional_arg(words, macros)
                if env_name.rstrip("*") in DELETE_UNINTERPRETED_ENVS:
                    print("SKIPPING ", env_name)
                    final_period = skip_rest_env(words, {}, stop_at=env_name)
                else:
                    final_period = skip_rest_env(words, macros)

            elif w == "}":
                # Something weird; too many right braces.
                # Maybe this was {$} in an argument
                # to something?  Pretend we didn't see math.
                return False

            elif not w.isspace() and not w.startswith("\\"):
                final_period = False

            elif w == "\\ifmmode":
                # Usually we assume all conditionals except \iftrue
                # are false, but if we're skipping math,
                # we're probably in math mode.
                pass

            elif w.startswith("\\") or w in macros:
                execute(
                    w, words, macros, nomath=False, debug=debug, inproof=False
                )

    return final_period


def skip_rest_env(words, macros, stop_at=None) -> bool:
    r"""
    Skip to past the \end{...} of the environment we are in.

    Returns whether the last printable character of the enviroment
    is a period (heuristically).
    """
    nwords_seen = 0
    final_period = False
    env_nesting = 1
    # tag = random.random()
    while words:
        w = next(words)
        # print("ske", w, tag, stop_at)
        # if stop_at:
        #     print("".join(words[:80]))
        nwords_seen += 1
        if nwords_seen >= 400_000 and stop_at is None:
            print("skip_rest_env", nwords_seen)
            raise SkipThisProof

        if w == "\\begin" and stop_at is None:
            get_arg(words)
            skip_optional_arg(words, macros)
            env_nesting += 1
        elif w == "\\end":
            env_name = "".join(get_arg(words))
            # print("skip-rest-env saw end", env_name)
            # print(stop_at, env_name == stop_at)
            env_nesting -= 1
            if (env_nesting == 0 and stop_at is None) or env_name == stop_at:
                break

        elif w == ".":
            final_period = True
        elif w == "\\label" and stop_at is None:
            get_arg(words)
        elif not w.isspace() and not w.startswith("\\"):
            final_period = False
        elif (w.startswith("\\") or w in macros) and stop_at is None:
            execute(w, words, macros, nomath=False, debug=False, inproof=False)

    return final_period


def get_filename(words) -> str:
    """Look for something that might be a filename."""
    if words.peek() == "{":
        # it's in curly braces
        return "".join(get_arg(words))
    elif words.peek() == '"':
        # it's in double quotes
        words.next()
        components: List[str] = []
        while True:
            w = next(words)
            if w == '"':
                return "".join(components)
            components.append(w)
    else:
        # it's a sequence of characters without spaces
        components = []
        while not words.peek("!").isspace():
            components.append(next(words))
        return "".join(components)


def try_skip_keywords(words, keywords) -> bool:
    """Look for 0 or more alphanumeric keywords from a list of keywords."""
    # Don't skip whitespace unless we find the keyword
    kws = list(keywords) + [" " + kw for kw in keywords]
    # print("tsw", " ".join(words[:15]), keywords)
    for kw in kws:
        if "".join(words[: len(kw)]) == kw:
            for _ in kw:
                next(words)
            return True
    return False


def skip_int(words):
    """Skip an integer."""
    if words.peek("x") == " ":
        next(words)
    if words.peek("x") == "-":
        next(words)
    while words.peek("x").isdigit():
        next(words)
    return


def try_assign(words, allow_space: bool = False) -> bool:
    """
    Look for potential assignment statement RHS.

    See if this is something that syntactically
    seems like part of a TeX assignment statement. If so,
    skip it (i.e., don't let the RHS show up in output).
    """
    # print("try_assign: ", " ".join(words[:15]))
    if words.peek("") in (["=", " "] if allow_space else ["="]):
        assignment_operator = words.peek("")
        # print("TA: 000")
        w23 = words[1:3]
        if len(w23) < 2:
            print("ta: too short")
            return False

        # print("ta: w23", w23)
        if w23[0] == " ":
            tok = w23[1]
            skip = 2
        else:
            tok = w23[0]
            skip = 1
        # print("ta: ", tok, skip)

        if tok.isdigit() or tok in ["-", "."]:
            for _ in range(skip):
                next(words)  # Drop the '=' (or ' ')
        elif tok == "{":
            for _ in range(skip):
                next(words)  # Drop the '=' (or ' ')
            get_arg(words)
            return True
        elif assignment_operator == "=" and tok.startswith("\\"):
            # e.g., \baselineskip=\normalbaselineskip
            for _ in range(skip):
                next(words)  # Drop the '=' (or ' ')
            get_arg(words)
            return True
        else:
            # print("TA: no 1")
            return False
    # print("ta': ", " ".join(words[:15]))
    if words.peek("x").isdigit() or (
        words.peek("x") in ["-", "."] and words[1].isdigit()
    ):
        # print("ta skipglue1", words[:15])
        skip_glue(words)
        # print("ta skipglue2", words[:15])

        # if words.peek("x") != ".":
        #     skip_int(words)
        # # decimal?
        # if words.peek("x") in [".", ","]:
        #     next(words)  # skip the '.'
        #     skip_int(words)
        # print("ta3: ", " ".join(words[:15]))

        # # Skip units
        # try_skip_units(words)
        # # print("  try_assign", " ".join(words[:15]))
        return True
    else:
        # print("TA: no 2")
        return False


def try_skip_units(words):
    """Skip optional dimensional units, e.g., pt or true cm."""
    try_skip_keywords(words, ["true"])
    try_skip_keywords(
        words,
        {
            "pt",
            "in",
            "mm",
            "cm",
            "pc",
            "sp",
            "em",
            "ex",
            "truept",
            "truein",
            "truecm",
            "truecm",
            "truepc",
            "truesp",
            "trueem",
            "trueex",
        },
    )


#
# Key function - the fake LaTeX interpreter
#


def execute(cmd, words, macros, nomath=True, debug=False, inproof=False):
    """Naively attempt to interpret TeX and LaTeX commands."""
    if cmd == "\\ensuremath":
        get_arg(words)
        return ["MATH"]

    # Override Paul Taylor's macros
    if cmd == "\\prooftree":
        while next(words) != "\\endprooftree":
            pass
        return [" "]

    # Override xy macros
    if cmd == "\\xy" and "\\endxy" in words[:]:
        nesting = 1
        while True:
            word = next(words)
            if word == "\\xy":
                nesting += 1
            elif word == "\\endxy":
                nesting -= 1
                if nesting == 0:
                    break
        return [" "]

    if cmd == "\\pspicture":
        while next(words) != "\\endpspicture":
            pass
        return [" "]

    if cmd == "\\psmatrix":
        while next(words) != "\\endpsmatrix":
            pass
        return [" "]

    # pictex
    if cmd == "\\beginpicture":
        while next(words) != "\\endpicture":
            pass
        return [" "]

    if cmd == "\\begindc":
        while next(words) != "\\enddc":
            pass
        return [" "]

    if cmd == "\\beginpgfgraphicnamed":
        while next(words) != "\\endpgfgraphicnamed":
            pass
        return [" "]

    # Override pinlabel
    if cmd == "\\labellist":
        while next(words) != "\\endlabellist":
            pass
        return [" "]

    if cmd not in macros:
        # Allow user to override these, but otherwise
        # translate accent commands to unicode
        if cmd == "\\`":
            skip_ws(words)
            if words.peek("!").isalpha():
                # \` means something different in a tabbing environment
                return ["".join(get_arg(words)) + "\u0300"]
        if cmd == "\\'":
            skip_ws(words)
            if words.peek("!").isalpha():
                # \' means something different in a tabbing environment
                return ["".join(get_arg(words)) + "\u0301"]
        if cmd == "\\^":
            return ["".join(get_arg(words)) + "\u0302"]
        if cmd == "\\~":
            arg = "".join(get_arg(words))
            if arg.strip():
                return [arg + "\u0303"]
            else:
                return "~"
        if cmd == "\\=":
            skip_ws(words)
            if words.peek("!").isalpha():
                # \= means something different in a tabbing environment
                return ["".join(get_arg(words)) + "\u0304"]
        if cmd == "\\u" and cmd not in macros:
            return ["".join(get_arg(words)) + "\u0306"]
        if cmd == "\\.":
            return ["".join(get_arg(words)) + "\u0307"]
        if cmd == '\\"':
            return ["".join(get_arg(words)) + "\u0308"]
        if cmd == "\\r":
            return ["".join(get_arg(words)) + "\u030a"]
        if cmd == "\\H":
            return ["".join(get_arg(words)) + "\u030c"]
        if cmd == "\\v":
            return ["".join(get_arg(words)) + "\u030c"]
        if cmd == "\\c":
            return ["".join(get_arg(words)) + "\u0327"]
        if cmd == "\\d":
            return ["".join(get_arg(words)) + "\u0323"]
        if cmd == "\\k":
            return ["".join(get_arg(words)) + "\u0328"]
        if cmd == "\\b":
            return ["".join(get_arg(words)) + "\u0331"]

        if cmd in NO_ARGUMENT_NOOPS:
            # If the user hasn't redefined this command, it does nothing
            # and takes no arguments.(We'd expect them to do nothing anyway,
            # but the extractor gets confused by {\bf 2}, which gets
            # interpreted as an abbreviation for the assignment {\bf=2}.)
            return []

    if cmd in {
        r"\ ",
        r"\,",
        r"\:",
        r"\>",
        "\\enspace",
        "\\quad",
        "\\qquad",
        "\\bigskip",
        "\\medskip",
        "\\smallskip",
        "\\eject",
        "\\clearpage",
        "\\cleardoublepage",
    }:
        # ignore these (no argument)
        return [" "]

    if cmd in {
        "\\label",
        "\\message",
        "\\errmessage",
        "\\ClassInfo",
        "\\ClassWarning",
        "\\ClassWarningNoLine",
        "\\ClassError",
        "\\TBInfo",  # tugboat class
        "\\TBWarning",
        "\\TBError",
        "\\TBWarningNL",
        "\\string",  # valid but unlikely to produce anything helpful.
        "\\linethickness",
        "\\newsavebox",
        "\\enlargethispage",
        "\\special",
        "\\rlap",
        "\\llap",
        "\\ding",
        "\\nocite",
        # mathtools
        "\\noeqref",
    }:
        # ignore these (and their argument)
        # Skip optional asterisk
        if words.peek("!") == "*":
            next(words)
        skip_optional_arg(words, macros)
        get_arg(words)
        return []

    if cmd == "\\index":
        skip_optional_arg(words, macros)
        get_arg(words)
        if "two-argument \\index" in macros:
            get_arg(words)
        return []

    if cmd in [
        "\\asciiabstract",
        "\\epsfig",
        "\\psfig",
        "\\epsffile",
        "\\epsfgetbb",
    ]:
        get_arg(words)
        return [" "]

    if cmd == "\\epsfbox":
        skip_optional_arg(words)
        get_arg(words)
        return [" "]

    if cmd == "\\figbox" and cmd not in macros:
        # 0009/cs0009023
        skip_optional_arg(words, macros)
        get_arg(words)
        get_arg(words)
        get_arg(words)
        get_arg(words)

    if cmd in ["\\DeclareMathSymbol", "\\mathchoice"]:
        get_arg(words)
        get_arg(words)
        get_arg(words)
        get_arg(words)
        return []

    if cmd in {"\\mathpalette", "\\fontsize"}:
        get_arg(words)
        get_arg(words)
        return []

    if cmd == "\\kern":
        if words.peek() == "{":
            get_arg(words)
        else:
            skip_dimen(words)
        return [" "]

    if cmd in ["\\hskip", "\\vskip", "\\mskip"]:
        skip_glue(words)
        return [" "]

    if cmd in {"\\hspace", "\\vspace", "\\addvspace"}:
        # Skip optional asterisk
        if words.peek("!") == "*":
            next(words)
        get_arg(words)
        return [" "]

    if cmd == "\\iftrue":
        return []

    if cmd == "\\ifdefined" and words.peek("") == "\\hyperref":
        # Hack: make "\ifdefined\hyperref" true, to handle 1404/1404.2618
        next(words)
        return []

    if cmd in ["\\hyperlink", "\\hypertarget"]:
        get_arg(words)  # skip a label
        return []

    if cmd in TEX_IFS:
        # Treat all built-in conditionals as false.
        # (except iftrue, which we handled above)
        skip_rest_conditional(words, macros, stop_on_else=True)
        return []

    if cmd == "\\else":
        skip_rest_conditional(words, macros, stop_on_else=False)
        return []

    if cmd == "\\fi":
        return []

    if cmd == "\\loop":
        # Ignore primitive loops
        while next(words) != "\\repeat":
            pass
        return []

    if cmd == "\\penalty":
        # Skip an integer
        skip_int(words)
        return []

    if cmd in ["\\hbox", "\\vbox", "\\vtop", "\\hrule", "\\vrule"]:
        # print("X1: ", cmd, words[:10])
        while try_skip_keywords(
            words, ["width", "height", "depth", "to", "spread"]
        ):
            # print("X2: ", cmd, words[:10])
            try_assign(words, allow_space=True)
            # print("X3: ", cmd, words[:10])
        # print("X4: ", cmd, words[:10])
        return []

    if cmd == "\\rule":
        skip_optional_arg(words, macros)
        get_arg(words)
        get_arg(words)
        return [" "]

    if cmd == "\\raisebox":
        get_arg(words)
        skip_optional_arg(words, macros)
        skip_optional_arg(words, macros)
        return []

    if cmd == "\\parbox":
        skip_optional_arg(words, macros)
        get_arg(words)
        return []

    if cmd in {"\\makebox", "\\framebox"}:
        skip_optional_arg(words, macros)
        skip_optional_arg(words, macros)
        return []

    if cmd in ["\\resizebox"]:
        if words.peek("!") == "*":
            next(words)
        get_arg(words)
        get_arg(words)
        return []

    if cmd in [
        "\\setlength",
        "\\addtolength",
        "\\setcounter",
        "\\addtocounter",
    ]:
        get_arg(words)
        get_arg(words)
        return []

    if cmd in [
        "\\advance",
        "\\multiply",
        "\\divide",
    ]:
        get_arg(words)
        try_skip_keywords(words, ["by"])
        skip_num(words)
        try_skip_units(words)

    if cmd == "\\setbox":
        # Ignore "\setbox17="
        # Ignore "\setbox\mybox="
        # Ignore "\setbox\endbox{...}"
        skip_ws(words)
        if words.peek().isdigit():
            while words.peek().isdigit():
                next(words)
        else:
            next(words)
        skip_optional_eq(words)
        return []

    if cmd in ["\\stepcounter", "\\refstepcounter"]:
        get_arg(words)
        return []

    if cmd == "\\item":
        skip_optional_arg(words, macros)
        return [" CASE: "]

    if cmd in ["\\paragraph", "\\subparagraph"]:
        get_arg(words)
        return [" CASE: "]

    if cmd in ["\\includegraphics", "\\marginpar", "\\adjincludegraphics"]:
        skip_optional_arg(words, macros)
        get_arg(words)
        return [" "]

    if cmd == "\\marginnote":
        skip_optional_arg(words, macros)
        get_arg(words)
        skip_optional_arg(words, macros)
        return [" "]

    if cmd == "\\@ifnextchar":
        # \define@key is in 1603/1603.00294
        get_arg(words)
        get_arg(words)
        get_arg(words)
        return []

    if cmd == "\\define@key":
        # 1603/1603.00294
        get_arg(words)
        get_arg(words)
        skip_optional_arg(words, macros)
        get_arg(words)
        return []

    if cmd in VERB_COMMANDS:
        end_ch = next(words)
        while next(words) != end_ch:
            pass
        return [" VERBATIM "]

        # end_ch = next(words)
        # arg: List[str] = []
        # while True:
        #     w = next(words)
        #     if w == end_ch:
        #         return "".join(arg)
        #     else:
        #         arg.append(w)

    if cmd == "\\lstinputlisting":
        skip_optional_arg(words)
        get_arg(words)
        return [" "]

    if cmd == "\\footnote":
        # Footnotes can interrupt sentences, and do not necessarily
        # contain normal "proof-like" wording.
        get_arg(words)
        return []

    if cmd in ["\\phantom", "\\hphantom", "\\vphantom"]:
        # Ignore invisible text
        get_arg(words)
        return []

    if cmd in ["\\\\", "\\\\*"]:
        skip_optional_arg(words, macros)
        return [" "]

    if cmd == "\\savebox":
        get_arg(words)
        if words.peek() == "(":
            while next(words) != ")":
                pass
        skip_optional_arg(words, macros)
        skip_optional_arg(words, macros)
        get_arg(words)  # If we're saving it, it shouldn't be emitted here.
        return []

    if cmd == "\\roman":
        get_arg(words)
        return ["v"]
    if cmd == "\\Roman":
        get_arg(words)
        return ["V"]
    if cmd == "\\arabic":
        get_arg(words)
        return ["4", "2"]
    if cmd == "\\alph":
        get_arg(words)
        return ["q"]
    if cmd == "\\Alph":
        get_arg(words)
        return ["Q"]
    if cmd == "\\fnsymbol":
        get_arg(words)
        return []
    if cmd == "\\S":
        return ["Section "]

    if cmd in {"\\ifthenelse", "\\IfFileExists", "\\iftoggle"}:
        # Assume the conditional is false;
        # remove braces around the result
        get_arg(words)
        get_arg(words)
        words.prepend(*get_arg(words))
        return []

    if cmd == "\\@ifstar":
        # Assume the conditional is _true_ (1708/1708.06228)
        # remove braces around the result
        w1 = get_arg(words)
        get_arg(words)
        words.prepend(*w1)
        return []

    if cmd == "\\ifstrequal" or cmd == "\\ifnumequal" or cmd == "\\IfEq":
        a1 = "".join(get_arg(words))
        a2 = "".join(get_arg(words))
        if a1 == a2:
            then_arg = get_arg(words)
            get_arg(words)  # skip else
            words.prepend(*then_arg)
        else:
            get_arg(words)
            # leave the else alone (in braces)
        return []

    # xstring
    if cmd == "\\IfBeginWith":
        if words.peek("!") == "*":
            next(words)
        skip_optional_arg(words, macros)
        a1 = "".join(get_arg(words))
        a2 = "".join(get_arg(words))
        if a1.startswith(a2):
            then_arg = get_arg(words)
            get_arg(words)  # skip else
            words.prepend(*then_arg)
        else:
            get_arg(words)
            # leave the else alone (in braces)
            return []

    if cmd == "\\IfEndWith":
        if words.peek("!") == "*":
            next(words)
        skip_optional_arg(words, macros)
        a1 = "".join(get_arg(words))
        a2 = "".join(get_arg(words))
        if a1.endswith(a2):
            then_arg = get_arg(words)
            get_arg(words)  # skip else
            words.prepend(*then_arg)
        else:
            get_arg(words)
            # leave the else alone (in braces)
            return []

    if cmd == "\\IfSubStr":
        if words.peek("!") == "*":
            next(words)
        skip_optional_arg(words, macros)
        a1 = "".join(get_arg(words))
        a2 = "".join(get_arg(words))
        if a2 in a1:
            then_arg = get_arg(words)
            get_arg(words)  # skip else
            words.prepend(*then_arg)
        else:
            get_arg(words)
            # leave the else alone (in braces)
            return []

    if cmd == "\\IfStrEqual":
        if words.peek("!") == "*":
            next(words)
        skip_optional_arg(words, macros)
        a1 = "".join(get_arg(words))
        a2 = "".join(get_arg(words))
        if a1 == a2:
            then_arg = get_arg(words)
            get_arg(words)  # skip else
            words.prepend(*then_arg)
        else:
            get_arg(words)
            # leave the else alone (in braces)
            return []

    if cmd == "\\write":
        if words.peek("q").isdigit():
            while words.peek("q").isdigit():
                next(words)
        else:
            get_arg(words)
        skip_ws(words)
        get_arg(words)
        return []

    if cmd == "\\protected@write":
        if words.peek("q").isdigit():
            while words.peek("q").isdigit():
                next(words)
        else:
            get_arg(words)
        skip_ws(words)
        get_arg(words)
        get_arg(words)
        return []

    if cmd in [
        "\\section",
        "\\subsection",
        "\\subsubsection",
        "\\paragraph",
        "\\subparagraph",
    ]:
        # Skip optional asterisk
        if words.peek("!") == "*":
            next(words)
        # OK, this is debatable, but we will completely ignore the
        #    contents of section/paragraph/etc. headers.
        # They're rarely full sentences, and often lack periods
        #    so they get glommed on to the first sentence of the
        #    section/paragraph itself.
        get_arg(words)
        return [" CASE: "]

    if cmd == "\\htmladdnormallink":
        # Ignore the second argument, but not the first.
        arg1 = get_arg(words)
        get_arg(words)  # skip hyperlink
        words.prepend(*arg1)
        return []

    if cmd == "\\href":
        skip_optional_arg(words, macros)
        get_arg(words)  # url
        return []  # will emit the text argument normally

    if cmd == "\\hyperref" and cmd not in macros:
        skip_ws(words)
        if words.peek() == "[":
            skip_optional_arg(words, macros)
            return []  # will emit the text argument normally
        else:
            get_arg(words)
            get_arg(words)
            get_arg(words)
            return []  # will emit the text argument normally

    if cmd in {"\\color", "\\textcolor", "\\colorbox"}:
        skip_optional_arg(words, macros)
        get_arg(words)  # color
        return []

    if cmd == "\\definecolor":  # tikz
        get_arg(words)
        get_arg(words)
        get_arg(words)
        return []

    if cmd == "\\colorlet":  # tikz
        get_arg(words)
        get_arg(words)
        return []

    if cmd == "\\tikzset":
        get_arg(words)  # ignore argument
        return []

    if cmd == "\\adjustimage":
        get_arg(words)
        get_arg(words)
        return [" "]

    if cmd in {
        "\\AxiomC",
        "\\UnaryInfC",
        "\\BinaryInfC",
        "\\TrinaryInfC",
        "\\QuaternaryInfC",
        "\\QuinaryInfC",
        "\\LeftLabel",
        "\\RightLabel",
    }:
        # bussproofs, e.g., 1708/1708.05896
        get_arg(words)
        return [""]

    if cmd == "\\DisplayProof":
        # bussproofs, e.g., 1708/1708.05896
        return [" MATH "]

    if cmd in {"\\noLine", "\\doubleLine"}:
        # bussproofs, e.g., 1708/1708.05896
        return [""]

    if cmd == "\\adjustbox":
        get_arg(words)  # ignore scaling
        # implicitly leave the content alone
        return []

    if cmd == "\\tikz":
        skip_optional_arg(words, macros)
        if words.peek() == "{":
            get_arg(words)
        else:
            while True:
                if next(words) == ";":
                    break

    if cmd == "\\tikzstyle":
        get_arg(words)
        skip_optional_eq(words)
        skip_optional_arg(words, macros)
        return []

    if cmd == "\\pdfstringdefDisableCommands":
        # hyperref
        get_arg(words)
        return []

    if cmd == "\\textattachfile":
        skip_optional_arg(words, macros)
        get_arg(words)
        # implicitly leave the text alone
        return []

    if cmd == "\\theoremstyle":
        get_arg(words)

    if cmd == "\\newtheorem":
        get_arg(words)
        skip_optional_arg(words, macros)
        get_arg(words)
        skip_optional_arg(words, macros)
        return []

    if cmd == "\\xspace":
        XSPACE_EXCEPTIONS = {
            ",",
            ".",
            "’",
            "'",
            "/",
            "?",
            ";",
            ":",
            "!",
            "~",
            "-",
            ")",
            "\\ ",
            "\\/",
            "\\bgroup",
            "\\egroup",
            "\\@sptoken",
            "\\space",
            "\\@xobeysp",
            "\\footnote",
            "\\footnotemark",
        }
        upcoming = words.peek(".")
        if upcoming not in XSPACE_EXCEPTIONS:
            return [" "]
        else:
            return []

    if cmd == "\\put" and cmd not in macros:
        while next(words) != ")":
            pass
        get_arg(words)
        return []

    # if cmd == "\\useshorthands" or cmd == "\\useshorthands*":
    #     if '"' in "".join(get_arg(words)):
    #         macros["german shorthands"] = True
    #         print("GS")
    #         exit(-1)
    #     return []

    if cmd == "\\languageshorthands":
        argument = "".join(get_arg(words))
        if "german" in argument:
            macros["german shorthands"] = True
        return []

    if cmd == "\\catcode":
        # 1504/1504.0647
        # Terrible hack to check for german shorthands
        if words[:5] == ["`", '"', "=", "1", "3"]:
            macros["german shorthands"] = True
            for i in range(5):
                next(words)
        return []

    if cmd == "\\ednote":
        # 2004/2004.08576
        get_arg(words)
        return []

    if cmd == "\\the":
        get_arg(words)
        return ["42"]

    if cmd == "\\tabto":
        get_arg(words)
        return [" "]

    if cmd == "\\glossary":
        get_arg(words)
        return []

    if cmd == "\\setboolean":
        get_arg(words)
        get_arg(words)
        return []

    if cmd in macros:
        if cmd == "\\BoxedEPSF":
            # Hack for 0002/math0002136/zinno.tex
            get_arg(words)
            return []

        if macros[cmd] != "frozen":
            # print(f"calling try_expand on {cmd}")
            expansion = try_expand(words, *macros[cmd])
            # Filter out recursion!
            expansion = [
                w if w != cmd else "\\nopenopenope " for w in expansion
            ]
            words.prepend(*expansion)
            # print(words[:10])
            return []

    if nomath and cmd in MATHONLY_COMMANDS:
        print(
            f"Oops: encountered {cmd} before "
            f'{" ".join(words[:20])} ({os.getpid()})',
            file=sys.stdout if debug else sys.stderr,
        )
        raise SkipThisProof(f"oops: encountered {cmd}")

    if inproof and cmd in {
        "\\psset",
        "\\psline",
        "\\rput",
        "\\uput",
        "\\pspolyline",
        "\\newrgbcolor",
        "\\pscircle",
        "\\qline",
        "\\ncline",
    }:
        raise SkipThisProof(f"oops: encountered {cmd}")

    if try_assign(words):
        return []

    return []


def skip_to_lbrace(words):
    """Discard tokens up to (but not including) the next left brace."""
    while words.peek() != "{":
        next(words)


def get_all_proofs(
    words,
    directory,
    macros,
    verbose=False,
    debug=False,
    strip=True,
    input_nesting=0,
):
    """
    Collect the proofs in the paper.

    Unlike the simple get_proofs, can recover from errors inside a proof;
    we just ignore that proof and see if we can get anything from
    the rest of the paper.
    """
    proofs: List[str] = []
    while words:
        try:
            get_proofs(
                words,
                directory,
                macros,
                proofs,
                verbose,
                debug,
                strip,
                input_nesting,
            )
            # If get_proofs finished normally, we don't
            # want to loop.
            break
        except SkipThisProof:
            # Go to \end{proof} (which we're just guessing is the
            # name of the enclosing environment) and loop
            # to see if there are any more acceptable proofs?
            print("WARNING: proof skipped")
            skip_rest_env(words, {}, stop_at="proof")
    return proofs


def get_proofs(
    words,
    directory,
    macros,
    proofs: List[str],
    verbose=False,
    debug=False,
    strip=True,
    input_nesting=0,
):
    """Try to get proofs from this stream of TeX tokens."""
    if input_nesting > 5:
        return []

    tokens_at_this_level = 0

    proof_nesting = 0
    current_proof_words: List[str] = []

    tag = random.random()  # nosec

    while words:
        w = next(words)
        tokens_at_this_level += 1
        # print(tokens_at_this_level)
        if tokens_at_this_level > 1_000_000:
            break
        # print(f"{w=} {current_proof_words=} {macros=}")
        if debug:
            print("get_proofs: ", w, w in macros, tag, tokens_at_this_level)
            # print(
            #     f"get proofs: {w=} {w in macros}"
            #     f" UPCOMING: {''.join(words[:60])}"
            # )
            # print(",".join(list(macros.keys())))

        if w == "~" and w not in macros:
            if proof_nesting > 0:
                current_proof_words.append(" ")
                continue

        if w in [
            "\\def",
            "\\edef",
            "\\gdef",
            "\\xdef",
        ]:
            name, parameters, body = get_primitive_def(words, debug, verbose)
            if body is not None and name is not None:
                optional_arg = None
                if name in macros and macros[name] == "frozen":
                    pass
                elif (
                    name in TEX_REFS and TEX_REFS[name] == len(parameters) - 1
                ):
                    pass
                else:
                    macros[name] = (parameters, optional_arg, body)
                # print("defined ", name, macros[name])

        elif w == "\\csdef":
            # ignore macros defined with etoolbox's \csdef
            get_arg(words)
            skip_to_lbrace(words)
            get_arg(words)

        elif w in ["\\input", "\\include"]:
            # I saw one file that just had a bare \input with no filename.
            #  (0103/math0103176/paper.tex)
            # Try not to crash.
            fn = Path(get_filename(words).lower())
            if fn.stem not in IGNORED_INCLUDES and not kpse.in_TeX_path(
                fn.name
            ):
                subfname: Path = directory / fn
                try:
                    try:
                        subwords = get_words(subfname.as_posix() + ".tex")
                        if verbose or debug or True:
                            print(f"  loading {subfname}.tex", file=sys.stderr)
                    except FileNotFoundError:
                        subwords = get_words(subfname.as_posix())
                        if verbose or debug or True:
                            print(f"  loading {subfname}", file=sys.stderr)

                    # print("macros in", list(sorted(macros.keys())))
                    subproofs = get_all_proofs(
                        subwords,
                        directory,
                        macros,
                        verbose,
                        debug,
                        strip,
                        input_nesting + 1,
                    )
                    # print("macros out", list(sorted(macros.keys())))
                    proofs.extend(subproofs)
                except FileNotFoundError:
                    if verbose or debug:
                        print(
                            f" can't process {subfname} or {subfname}.tex",
                            file=sys.stderr,
                        )

        elif w in ["\\usepackage", "\\RequirePackage"]:
            if words.peek() == "[":
                optional = get_optional_arg(words)
            else:
                optional = ""
            filenames = "".join(get_arg(words)).split(",")
            for filename in filenames:
                fn = Path(filename.strip().lower())
                if fn.name == "babel":
                    if "german" in optional:
                        macros["german shorthands"] = True
                    continue
                if fn.name == "amsmidx":
                    macros["two-argument \\index"] = True
                    continue
                if fn.suffix == "":
                    fn = fn.with_suffix(".sty")
                if fn.stem in IGNORED_INCLUDES or kpse.in_TeX_path(fn.name):
                    continue
                subfname = directory / (fn.with_suffix(".sty"))
                try:
                    subwords = get_words(subfname.as_posix())
                    if verbose or debug or True:
                        print(f"  loading {subfname}", file=sys.stderr)
                    subproofs = get_all_proofs(
                        subwords,
                        directory,
                        macros,
                        verbose,
                        debug,
                        strip,
                        input_nesting + 1,
                    )
                    proofs.extend(subproofs)
                except FileNotFoundError:
                    # Probably a standard library package
                    # For now, we won't try to find these.
                    pass

        elif w in [
            "\\newcommand",
            "\\renewcommand",
            "\\DeclareRobustCommand",
            "\\DeclareMathOperator",
            "\\providecommand",
            "\\@namedef",
        ]:
            # Skip optional asterisk
            if words.peek("!") == "*":
                next(words)
            name, parameters, optional_args, body = get_newcommand(words)
            if body is not None:
                if name in macros and macros[name] == "frozen":
                    pass
                else:
                    macros[name] = (parameters, optional_args, body)

        elif w in ["\\newcounter"]:
            counterName = "".join(get_arg(words))
            skip_optional_arg(words, macros)
            macros["\\the" + counterName] = ([[]], [], ["4", "2"])

        elif w in ["\\newenvironment", "\\renewenvironment"]:
            # Skip optional asterisk
            if words.peek("!") == "*":
                next(words)
            env_name = "".join(get_arg(words))  # env name
            skip_ws(words)
            if words.peek("!") == "{":
                begin_tokens = get_arg(words)
                skip_ws(words)
                end_tokens = get_arg(words)

                # Disabled for now; usually the user-defined \begin{foo}
                # invokes an internal \begin{bar}, and
                # skip-rest-env looks for \end{bar}, not \end{foo},
                # and skip-rest-env doesn't expand \begin{} or \end{}
                # macros["\\" + env_name] = ([[]], [], begin_tokens)
                # macros["\\end" + env_name] = ([[]], [], end_tokens)

                begin_code = "".join(begin_tokens)
                if (
                    (
                        "\\begin{array}" in begin_code
                        and "\\end{array}" not in begin_code
                    )
                    or ("\[" in begin_code and "\]" not in begin_code)
                    or (
                        "\\begin{equation}" in begin_code
                        and "\\end{equation}" not in begin_code
                    )
                    or ("$$" in begin_code)
                ):
                    MATH_ENVS.add(env_name)

            else:
                skip_to_lbrace(words)
                get_arg(words)  # begin part
                get_arg(words)  # end part

        elif w in ["\\newif"]:
            newif = next(words)
            macros["new ifs"].append(newif)
            # hack. User-defined conditionals are always false.
            macros[newif] = ([[]], [], ["\\iffalse"])

        elif w == "\\begin":
            env_name = "".join(get_arg(words))
            # print(f"{env_name=}", "".join(words[:20]))
            # Skip optional argument, e.g.,
            #   "Proof of Proposition 4.2"
            #   or "by induction"
            skip_optional_arg(words, macros)
            if debug:
                print("   ", env_name, env_name.rstrip("*"))
                print(words[:80])
            if env_name.startswith(("proof", "Proof")):
                if proof_nesting == 0:
                    current_proof_words = []
                proof_nesting += 1
                skip_ws(words)
                # Some nonstandard proof environments
                # take an extra argument instead of
                # an noptional argument. We assume that
                # if the \begin{proofsect} is *immediately*
                # followed by an argument (on the same line,
                # with no whitespace), it's skippable.
                #
                # I don't know if any environment needs more
                # than one such argument, but just in case...
                guessed_args = 0
                while words.peek() == "{":
                    get_arg(words)
                    guessed_args += 1
                if guessed_args:
                    # Handle things like
                    #   \begin{proof}
                    #     {\em Soundness}. We let...
                    skip_ws(words)
                    if words.peek("x") in {".", ":"}:
                        next(words)

            elif env_name.rstrip("*") in MATH_ENVS:
                fp = skip_rest_env(words, macros)
                if proof_nesting > 0:
                    current_proof_words.append(" MATH ")
                    if fp:
                        current_proof_words.append(" . ")
            else:
                if env_name == "adjustbox":
                    # ignore scaling argument
                    get_arg(words)
                elif env_name.rstrip("*") in DELETE_ENVS:
                    skip_rest_env(words, macros)
                elif env_name.rstrip("*") in DELETE_UNINTERPRETED_ENVS:
                    skip_rest_env(words, {}, stop_at=env_name)
                elif env_name == "step+":
                    # 0109/math0109152/walks
                    # (step+ environment takes an extra label argument that
                    #  shouldn't appear in the output)
                    get_arg(words)
                elif env_name == "list":
                    # The list environment takes two arguments.
                    get_arg(words)
                    get_arg(words)
                elif "\\" + env_name in macros:
                    print("GGG entering user-defined environment", env_name)
                    words.prepend("\\" + env_name)
                    continue

                if proof_nesting > 0:
                    current_proof_words.append(" ")
                    continue

        elif w == "\\end":
            skip_ws(words)
            if not words:
                # plain tex \end ?
                break
            env_name = "".join(get_arg(words))
            if debug:
                print("   ", env_name)
            if env_name.startswith(("proof", "Proof")):
                proof_nesting -= 1
                if proof_nesting == 0:
                    proof = "".join(current_proof_words).strip()
                    if proof:
                        if proof[-1:].isalpha():
                            proof += " ."
                        proof = re.sub("\\s+", " ", proof)
                        proofs.append(proof)
                        if verbose:
                            print("***", proof)
            elif env_name == "document":
                break
            elif "\\end" + env_name in macros:
                print("GGG leaving user-defined environment", env_name)
                words.prepend("\\end" + env_name)
                continue
            else:
                if proof_nesting > 0:
                    current_proof_words.append(" ")
                    continue

        elif w == "\\enddocument":
            break

        elif w == "$":
            if words.peek("!") == "$":
                next(words)
                single_dollar = False
            else:
                # Special case $($ and $)$
                ts = words[:2]
                if len(ts) == 2 and ts[1] == "$":
                    if ts[0] in {"(", ")"}:
                        next(words)
                        next(words)
                        words.prepend(ts[0])
                        continue
                # Normal $ start of math
                single_dollar = True
            fp = skip_rest_math(
                words, macros, single_dollar, debug=debug, verbose=verbose
            )
            if proof_nesting > 0:
                current_proof_words.append("MATH")
                if fp:
                    current_proof_words.append(" . ")

        elif (w == "\\(" or w == "\\[") and w not in macros:
            fp = skip_rest_math(
                words,
                macros,
                single_dollar=(w == "\\("),
                debug=debug,
                verbose=verbose,
            )
            if proof_nesting > 0:
                if w == "\\(":
                    current_proof_words.append("MATH")
                else:
                    current_proof_words.append(" MATH ")
                if fp:
                    current_proof_words.append(" . ")

        elif w == "\\csname":
            name = ""
            while (w2 := next(words)) != "\\endcsname":
                name += w2
            words.prepend("\\" + w)

        elif w in TEX_REFS and (w not in macros or macros[w] == "frozen"):
            # Skip optional asterisk
            if words.peek("!") == "*":
                next(words)
            skip_optional_arg(words, macros)
            for _ in range(TEX_REFS[w]):
                get_arg(words)
            if proof_nesting > 0:
                current_proof_words.append("REF")

        elif w == "\\cite":
            # Special handling for acmref variant of \cite
            # \cite{foo}*{lemma 5}
            # Skip optional asterisk
            if words.peek("!") == "*":
                next(words)
            skip_optional_arg(words, macros)
            get_arg(words)
            if words.peek("!") == "*":
                get_arg(words)
                get_arg(words)
            if proof_nesting > 0:
                current_proof_words.append("CITE")

        elif w in TEX_CITES:
            # Skip optional asterisk
            if words.peek("!") == "*":
                next(words)
            skip_optional_arg(words, macros)
            get_arg(words)
            if proof_nesting > 0:
                current_proof_words.append("CITE")

        # Since we fake "if", we might run into spurious aborts
        # elif w == "\\endinput":
        #     break

        elif w == "\\let":
            lhs = next(words)
            if lhs == "\\csname":
                lhs = ""
                while (w := next(words)) != "\\endcsname":
                    lhs += w
            if debug:
                print("  trying to define", lhs)
            skip_optional_eq(words)
            rhs = next(words)
            if lhs in macros and macros[lhs] == "frozen":
                pass
                if debug:
                    print("  ... definition ignored")
            elif rhs in macros and lhs.startswith("\\"):
                macros[lhs] = macros[rhs]
                if debug:
                    print(f"  ... as copy of macro {rhs}")
            elif lhs.startswith("\\"):
                # Hack
                # If we rename a built-in primitive, and then redefine
                #  that primitive, there's an awfully good chance that the
                #  new definition will refer to the old meaning,
                #  which (due to our naive treatment of "let" as "def"
                #  in this case) will cause loops.
                # So mark the renamed primitive as "frozen" to forbid
                #  any attempt to redefine it. With luck, it won't matter
                #  (particularly if the redefinition takes the same
                #  number of arguments, which is common).
                if rhs.startswith("\\"):
                    macros[rhs] = "frozen"
                macros[lhs] = ([[]], None, [rhs])
                if debug:
                    print(f"  ... as macro for {rhs}")
            else:
                # Something weird like   \let~=\space
                pass

        elif w == "{" and words[:3] == ["e", "q", ":"]:
            # A common mistake is to say "{eq:quadratic}"
            # instead of "\ref{eq:quadratic}"
            while next(words) != "}":
                pass
            if proof_nesting > 0:
                current_proof_words.append("REF")

        elif (w == "{" or w == "}") and strip:
            pass

        elif w.startswith("\\xymatrix"):
            skip_to_lbrace(words)
            get_arg(words)

        elif w == '"' and "german shorthands" in macros:
            if words.peek("x") in ["~", "=", "-", "/"]:
                next(words)
                words.prepend("-")

        # elif w == "[" and words[:2] == ["$$", "]"]:
        #     next(words)
        #     next(words)
        #     pass

        else:
            if w.startswith("\\") or w in macros:
                # There shouldn't be any math commands here, but some
                # of the arXiv .tex files have errors, and
                # if there's an omitted $...$ outside of any
                # proof we're extracting, there's no need to
                # crash.
                potential_output = execute(
                    w,
                    words,
                    macros,
                    nomath=(proof_nesting > 0),
                    debug=debug,
                    inproof=(proof_nesting > 0),
                )
            else:
                potential_output = [w]
            if proof_nesting > 0:
                if debug and potential_output:
                    print("EMIT:", potential_output)
                current_proof_words.extend(potential_output)
                # Heuristic: look for MATH/DMATH followed by a
                # capitalized word. If so, insert a period.
                if (
                    len(current_proof_words) >= 3
                    and current_proof_words[-3].endswith("MATH")
                    and current_proof_words[-2].isspace()
                    and current_proof_words[-1][0].isalpha()
                    and current_proof_words[-1][0].isupper()
                    and words
                    and words[0]
                    and words[0][0].isalpha()
                    and words[0][0].islower()
                ):
                    if debug:
                        print("EMIT IMPLICIT: .")
                    current_proof_words.insert(-1, ". ")

    return proofs


def process_file(
    filename, debug=False, verbose=False, in_parallel=True, only_new=False
):
    """Get proofs from the named file, writing to an external file."""
    orig_dir = Path(filename).parent
    path = Path(re.sub(".*texes/", "proofs/", filename, count=1))
    path.parent.mkdir(parents=True, exist_ok=True)
    out_path = path.with_suffix(".txt")
    err_path = path.with_suffix(".err")
    # Optionally skip this file if the corresponding output exists
    if only_new and (os.path.exists(out_path) or os.path.exists(err_path)):
        return
    print(" ", os.getpid(), filename, file=sys.stderr)
    try:
        words = get_words(filename)
        macros = {"new ifs": []}
        proofs = get_all_proofs(
            words, orig_dir, macros, verbose=verbose, debug=debug
        )

        with out_path.open("w") as fd:
            # print("Writing to ", out_path)
            for proof in proofs:
                print(proof, file=fd)

    except Exception as e:
        print("ERROR: ", filename, file=sys.stderr)
        with err_path.open("w") as fd:
            print("writing ", err_path)
            print(filename, file=fd)
            traceback.print_exc(file=fd)
        if debug:
            traceback.print_exc()
        if not in_parallel and not only_new:
            raise e


if __name__ == "__main__":
    nicer.make_nice()

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-d", "--debug", help="Show tracing output", action="store_true"
    )
    # parser.add_argument(
    #     "-e", "--elide", help="Elide math", action="store_true"
    # )
    parser.add_argument(
        "-v",
        "--verbose",
        help="Echo emitted characters to terminal",
        action="store_true",
    )
    parser.add_argument(
        "-m", "--matches", help="Take a list of files", action="store_true"
    )
    parser.add_argument(
        "-n", "--new", help="Skip input if output exists", action="store_true"
    )

    parser.add_argument(
        "-p", "--cores", help="Number of cores to use", type=int, default=4
    )

    parser.add_argument("files", nargs="+")
    args = parser.parse_args()

    if args.matches:
        tex_files: List[str] = []
        for match_file in args.files:
            with open(match_file) as f:
                tex_files.extend(
                    s.strip() for s in f.readlines() if not s.startswith("#")
                )
    else:
        tex_files = args.files

    os.makedirs("proofs", exist_ok=True)

    if args.new:
        print(f"prescanning {len(tex_files)} files")
        new_tex_files = []
        for filename in tex_files:
            path = Path(re.sub(".*texes/", "proofs/", filename, count=1))
            out_path = path.with_suffix(".txt")
            err_path = path.with_suffix(".err")
            if not (os.path.exists(out_path) or os.path.exists(err_path)):
                new_tex_files.append(filename)
        tex_files = new_tex_files
        print(f"found {len(tex_files)} new files")
        # with open("matches_new", "w") as fd:
        #     for filename in tex_files:
        #         print(filename, file=fd)

    if len(tex_files) > 1 and not (args.cores == 1):
        with Pool(processes=args.cores) as p:
            # p.map(pf, tex_files, 1)
            p.starmap(
                process_file,
                zip(
                    tex_files,
                    repeat(args.debug),
                    repeat(args.verbose),
                    repeat(True),
                    repeat(args.new),
                ),
                # max(4, min(100, len(tex_files) / args.cores / 4))
                50
                # let's try handing out files to CPUs
                # in chunks of 100 (rather than the default
                # which is approximately num-files / CPUS / 4)
            )
    else:
        for tex_file in tex_files:
            process_file(
                tex_file,
                debug=args.debug,
                verbose=args.verbose,
                in_parallel=False,
                only_new=args.new,
            )
        # except SystemExit as exn:
        #     print(f"\nError: {exn}")
        #     print("-----")
        #     for f, l, c in zip(
        #         state.current_files,
        #         state.line_numbers,
        #         state.token_numbers,
        #     ):
        #         print(f"file {f}, line {l}, token {c}")
