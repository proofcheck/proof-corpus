#!/usr/bin/env python
"""Cleans up extracted proofs."""

# foreach y (`seq 92 99` `seq -w 0 20`)
# find proofs/$y* -type f -name "*.txt" -print0 | sort -z | xargs -0 cat >! proofs$y.raw.txt
# end

# Cleanup each of the years of English proofs
# foreach y (`seq 92 99` `seq -w 0 20`)
# ./cleanup.py proofs$y.raw > proofs$y.txt
# end

# If you have GNU Parallel installed,
# parallel "./cleanup.py proofs{}.raw >! proofs{}.txt" ::: `seq 92 99` `seq -w 0 20`


import argparse
import functools
from multiprocessing import Pool
import re
import sys
from typing import List, Match
import unicodedata

import nicer


# Regular expression for uppercase letters (as a string)n
#   equivalent to "[A-Z]" but also including non-ASCII
upperLetter = "[{}]".format(
    "".join([chr(i) for i in range(sys.maxunicode) if chr(i).isupper()])
)

# Regular expression for lowercase letters (as a string)n
#   equivalent to "[a-z]" but also including non-ASCII
lowerLetter = "[{}]".format(
    "".join([chr(i) for i in range(sys.maxunicode) if chr(i).islower()])
)

# Regular expression (as a string) for anything of the form
#     42, 5a, 4.1bc, 1.C. 3-5, ...
numAlpha = "(?:(?![.])[a-zA-Z0-9.]*\\d[a-zA-Z0-9.-]*(?<![.]))"

# Regular expression (as a string) for anything of the form
#    3,  5a, IV, i, xii, ..., A, a, 1.C  eq:symmetric
atomicID = (
    f"(?:(?<![.])(?:{numAlpha}|[IVX]+|[ivx]+|"
    f"\\b[A-Z][A-Z]?\\b|\\b[a-z]\\b|\\bREF\\b|\\(REF\\))(?![.]\\S)|"
    f"\\b(?:eq|thm|fig):[A-Za-z0-9][A-Za-z0-9:]*)"
)

# Regular expression (as a string) for anytinng of the form
#    (3), (3.5), (3.5.2), (3.5a), (I), (IV), (i), (iv), (IV.4), (a), (A),...
#    (E MATH), (L-MATH)
#    [3], [iii], [iv.4], etc.  And [(3)], etc.
parenID = (
    f"(?:(?:\\({atomicID}(?:\\.{atomicID})*\\))|"
    f"(?:\\[{atomicID}(?:\\.{atomicID})*\\])|"
    f"(?:\\[\\({atomicID}(?:\\.{atomicID})*\\)\\])|"
    f"(?:\\([A-Za-z][- ]?MATH\\))|"
    f"(?:\\([A-Za-z][- ][0-9]\\)))"
)

# REF, REF(3.2), REF.a, 3, 3.5a, (IV), (IV.2), 2(a), 4.1bc
# Not: IV, IV.2
theoremNumber = (
    f"(?:REF(?:\\s?{parenID}|[.][a-z]\\b)?|{parenID}+|"
    f"{numAlpha}(?:[.]{numAlpha}|[.]?{parenID}|[.][a-z]\\b)*|"
    f"(?<![A-Za-z]){atomicID}(?![A-Za-z]))"
)

# Prop, Th., Theorem, Formula, ...
theorem_word = (
    r"(?:(?i:(?:\b(?:Props?|Prps?|prps?|Thms?|Cor|Th|Lem|Rem|Eqn?s?|Defs?|Ex|Alg)(?:\b|\.))"
    r"|"
    r"(?:\b(?:Propositions?|Theorems?|Corollar(?:y|ies)|Lemm(?:a|as|e|ata)|"
    r"Remarks?|Equations?|Diagrams?|Claims?|Statements?|Axioms?|Conditions?|"
    r"Definitions?|Expressions?|Criteri(?:a|on)|Formulas?|"
    r"Steps?|Hypothes[ie]s|Observations?|"
    r"Algorithms?|Inequalit(?:y|ies)|Assumptions?|Problems?|Exercises?|"
    r"Methods?|Facts?|Parts?|Rules?|Ad)\b)))"
)

# A set of words that probably are words, and not someone's name.
known_words: set[str] = set()
with open("words_alpha.txt") as fd:
    for word in fd.readlines():
        word = word.strip()
        known_words.add(word)
    known_words.add("profinite")
    known_words.add("interpolants")

# A set of names that might arise in Mathy text.
known_names: set[str] = set()
with open("known_names.txt") as fd:
    for word in fd.readlines():
        word = word.strip()
        known_names.add(word)
    # Remove names that are more likely to occur
    # at the start of a sentence than be actual names.
    known_names.remove("fix")
    known_names.remove("case")
    known_names.remove("and")
    known_names.remove("its")
    known_names.remove("small")
    known_names.remove("pick")
    # Hack, though really we should add this to known_names.txt
    known_names.add("gau")

#############
# Functions #
#############


def splitMATH(proof: str, debug: bool = False, aggressive: bool = True):
    r"""
    Break 'MATHsystem' (one word) into MATH system, etc.

    E.g.,
         GF$(2)$ -> GFMATH -> MATH
        sinceMATH -> since MATH
        ( $\alpha-$decomposition -> ) MATHdecomposition -> MATH-decomposition
        ($n$th element -> ) MATHth element -> MATH-th element

    Plus, do the same for CITE and REF.
    """
    proof = re.sub("(\\w+)-?(CITE|REF)", "\\1 \\2", proof)
    proof = re.sub("(CITE|REF)-?(\\w+)", "\\1 \\2", proof)
    proof = re.sub("\\b([A-Z0-9]+|[a-z0-9]{1,2})-?MATH", "MATH", proof)
    proof = re.sub("(\\w+)MATH", "\\1-MATH", proof)
    proof = re.sub("MATH(\\w+)", "MATH-\\1", proof)
    # proof = re.sub("MATH\\s*-?(th|st|nd|rd)\\b", "MATH", proof)

    if debug:
        print("0010", proof)
    return proof


def ner(proof: str, debug: bool = False, aggressive: bool = True):
    """
    Replace names with 'NAME'.

    E.g.,
       Smith -> NAME
       Smith's -> NAME 's
       Riesz' -> NAME 's
    """
    # Regular expression (as string) for something that might
    # be a name.
    #
    # Allows a trailing ' only if there' no matching ` scare-quote
    #    at front, and the word ends with an s sound.
    #
    # Guivarc'h is a name.
    # I've also seen Poincar'e and Maz'ya
    potential_name = (
        "((?<!['`])(?:\\w'\\w|\\w)+[sz]'(?!s))|"
        "((?:\\w'\\w|\\w)+\\w(?:'s\\b|'h\\b|'e|'ya\\b)?)|"
        "\\bKy Fan\\b"  # 1911/1911.08637
    )

    def lookup(g: Match[str]) -> str:
        """
        Given a match that might be a string, check it out.

        Returns either the string unchanged (not a name)
        or the string "NAME". (Or, if there was a possessive
        like "Smith's", return "NAME 's")
        """
        w: str = g.group(0)
        # print("NER?", w)
        # Check that it's capitalized,
        # but not because of MATH token
        # and it's not completely uppercase (e.g., the author wrote "CASE")
        if (
            w[0].isupper()
            and "MATH" not in w
            and "REF" not in w
            and "CITE" not in w
            and w != w.upper()
            and not (re.match(theorem_word, w))
        ):
            # print("lookup: ", w)
            if w.endswith("'s"):
                w = w[:-2]
                possessive = " 's"
            elif w.endswith("s'") or w.endswith("z'"):
                w = w[:-1]
                possessive = " 's"
            else:
                possessive = ""
            wl = w.lower()
            if possessive or (wl not in known_words) or (wl in known_names):
                return "NAME" + possessive
            else:
                return g.group(0)
        return w

    # Apply the lookup function to every possible name in the proof.
    proof = re.sub(potential_name, lookup, proof)

    if debug:
        print("0110", proof)

    # (van Trapp -> ) van NAME -> NAME
    # Similarly von NAME, van de NAME, el NAME, st. NAME, ibn NAME, le NAME, Du Name ...
    #   mc NAME, mac Name
    proof = re.sub(
        "(\\b(?i:v[oa]n|d[eo]s|de[nr]?|la|le|el|st\\.|ibn|du|ma?c|del|al)\\s+)+NAME",
        "NAME",
        proof,
    )

    # Qi-keng -> NAME-keng ->NAME
    proof = re.sub(
        "NAME-(\\w+)\\b",
        lambda match: "NAME"
        if match.group(1) in known_names
        else "NAME-" + match.group(1),
        proof,
    )

    if debug:
        print("0120", proof)

    # NAME and NotRecognizedAsName -> NAME and NAME
    # NotRecognizedAsName and NAME -> NAME and NAME
    proof = re.sub(f"\\bNAME and {upperLetter}\\w+\\b", "NAME and NAME", proof)

    proof = re.sub(
        f"(\\s){upperLetter}\\w+\\b and NAME\\b", "\\1NAME and NAME", proof
    )

    proof = re.sub(
        f"(?<![.] )\\b{upperLetter}\\w+ CITE\\b", "NAME CITE", proof
    )

    # proof = re.sub("NNAME", "NAME", proof)

    if debug:
        print("0125", proof)

    # van-Trapp -> NAME
    def remove_upto_dash(s: str) -> str:
        after_dash = s.index("-") + 1
        return s[after_dash:]

    proof = re.sub(
        "(\\b(v[oa]n|d[eo]s|de[nr]?|la|el|st\\.|ibn)-[A-Z]\\w+\\b)",
        # Check that the following word is purely alphabetic
        lambda w: "NAME"
        if remove_upto_dash(w.group(0)).isalpha()
        else w.group(0),
        proof,
    )

    if debug:
        print("0130", proof)

    # (A. Greene -> ) A. NAME -> NAME
    # (J.-P. Serre -> ) J.-P. NAME -> NAME
    proof = re.sub(
        f"(?<!\\w)({upperLetter}(\\.-?\\s*|\\s+))+NAME", "NAME", proof
    )

    if debug:
        print("0140", proof)

    # R. G. Swan -> NAME
    proof = re.sub(
        f"(?<!\\w)({upperLetter}(\\.-?\\s*|\\s+))+ NAME", "NAME", proof
    )

    if debug:
        print("0150", proof)

    proof = re.sub("NAME([- ]*NAME)*", "NAME", proof)

    if debug:
        print("0160", proof)

    proof = re.sub(
        f"([Tt]he )?NAME( and NAME)*\\s*('s)? (\\w+\\s*)?(?i:{theorem_word})",
        "REF",
        proof,
    )

    # the theorem of NAME -> REF
    # an elementary theorem of Mori -> REF
    # NOT:   the definition of Gröbner bases -> REF bases
    proof = re.sub(
        f"\\b([Tt]he |[Aa]n? )(\\s?\\w+ )?({theorem_word}) of NAME\\b",
        lambda m: "REF"
        if m.group(3).lower() not in {"definition", "assumption"}
        else m.group(0),
        proof,
    )

    # NAME et al. -> NAME
    proof = re.sub(r"NAME\s*(?i:et(\.)?\s*a(l)+(\.?))", "NAME", proof)

    proof = re.sub(r"\s*(?i:case)\s*[0-9]\s*(:)", " REF", proof)
    proof = re.sub(f">\\s*({upperLetter})", "\\1", proof)

    if debug:
        print("0170", proof)

    return proof


def treat_unbalanced_parens(
    filename: str, proof: str, debug: bool = False, aggressive: bool = True
):
    """Look for common reasons for unbalanced ('s and )'s."""

    # Case 1) This follows by -> CASE: This follows by
    # 1) This follows by -> CASE: This follows by
    # complete. 2) We consider -> complete. CASE: We consider
    proof = re.sub(
        f"(^|[.;:,] )(?:Case\\s+)?{atomicID}[.]?\\):?( {upperLetter})",
        "\\1CASE:\\2",
        proof,
    )

    if debug:
        print(1510, proof)

    if proof.count("(") == proof.count(")"):
        return proof

    if aggressive:
        # by part b) we have -> by we have
        # by part b) MATH -> by REF MATH
        # by part b). -> by REF.
        # by part ii) we have -> by REF we have
        # by part ii) MATH -> by REF MATH
        # by Theorem 2.1) -> by REF) -> by REF
        proof = re.sub(
            f"{theorem_word}\\s?{atomicID}[.]?\\)"
            f"((?:[ ]{lowerLetter}|[ ]MATH|[,.:]))",
            "REF \\1",
            proof,
        )
    if debug:
        print(1520, proof)

    if proof.count("(") == proof.count(")"):
        return proof

    proof = re.sub(f"(^| ){atomicID}[.]?\\)", "\\1REF", proof)

    if debug:
        print(1530, proof)

    if proof.count("(") == proof.count(")"):
        return proof

    # print("unbalanced:", filename, file=sys.stderr)
    # print(proof, file=sys.stderr, flush=True)

    # Delete unbalanced open parens
    cs: List[str] = []
    nesting = 0
    for c in proof:
        if c == "(":
            nesting += 1
        elif c == ")":
            if nesting > 0:
                nesting -= 1
            else:
                # Skip this close paren
                continue
        cs.append(c)

    # Delete unbalanced open parens
    # By traversing characters from the end to the beginning.
    cs2: List[str] = []
    nesting = 0
    for c in reversed(cs):
        if c == ")":
            nesting += 1
        elif c == "(":
            if nesting > 0:
                nesting -= 1
            else:
                # Skip this open paren
                continue
        cs2.append(c)

    proof = "".join(reversed(cs2))
    return proof


def cleanup(
    filename: str, proof: str, debug: bool = False, aggressive: bool = True
):
    """Simplify proof outputs."""
    if debug:
        print("0999", proof)
    if aggressive:
        # Normalize Abbreviations
        # i.e. ie  i.e., ie., ... -> that is,
        # e.g. eg  e.g., eg., ... -> for example,
        proof = re.sub(r"\bi[. ]?e[.]?,?\s", "that is, ", proof)
        proof = re.sub(r"\bI[. ]?e[.]?,?\s", "That is, ", proof)
        proof = re.sub(r"\be[. ]?g[.]?,?\s", "for example, ", proof)
        proof = re.sub(r"\bE[. ]?g[.]?,?\s", "For example, ", proof)

        proof = re.sub(r"\bi[. ]?e[.]?,?(?!\w)", "that is ", proof)
        proof = re.sub(r"\bI[. ]?e[.]?,?(?!\w)", "That is ", proof)
        proof = re.sub(r"\be[. ]?g[.]?,?(?!\w)", "for example ", proof)
        proof = re.sub(r"\bE[. ]?g[.]?,?(?!\w)", "For example ", proof)

        # w.l.o.g  wlog ... -> without loss of generality
        # WLOG  W.l.o.g ... -> Without loss of generality
        proof = re.sub(
            r"\b([Ww])[.]?[Ll][.]?[Oo][.]?[Gg][.]?(\W)",
            r"\1ithout loss of generality\2",
            proof,
        )
        # wolog WOLOG -> [Ww]ithout loss of generality
        proof = re.sub(
            "\b([Ww])[Oo][Ll][Oo][Gg]\b", r"\1ithout loss of generality", proof
        )

        # i.i.d iid ... -> iid    I.I.D.  I.i.d IID  ... -> Iid
        proof = re.sub(
            r"\b([Ii])[.]?i[Ii][.]?[Dd][.]?(\W)",
            r"\1ndependent and identically distributed\2",
            proof,
        )

        # cf. -> compare
        proof = re.sub("\\b([Cc])[.]?f[. ]*", r"\1ompare ", proof)

        # loc. cit. -> CITE
        proof = re.sub("(?i:loc[.]? cit(?:[.]|\\b))", "CITE", proof)

        # QED Q.E.D. qed q.e.d -> QED .
        # QED. -> QED .
        # QED . -> QED .
        proof = re.sub("\\b[Qq]\\.?[Ee]\\.?[Dd]\\.?(\\s\\.)?", "QED .", proof)

        # resp. -> respectively,
        proof = re.sub(
            "(?i:\\b(?<![.])(r)esp(?:[.]|\\b)[,]?)", r"\1espectively,", proof
        )

        # rhs r.h.s. RHS R.H.S. r. h. s.  r h s -> rhs   R.H.S RHS -> Rhs
        proof = re.sub(
            "(?i:\\b(?<![.])(r)[.]?[ ]?h[.]?[ ]?s(?:[.]|\\b))",
            r"\1ight-hand side",
            proof,
        )

        # s.t. -> such that
        proof = re.sub("\\b(?<![.])s[.]t[.]([ ,:])", r"such that\1", proof)

        # w.r.t -> with respect to
        proof = re.sub(
            "(?i:\\b(?<![.])(w)[.]?r[.]?t(?:[.]|\\b))",
            r"\1ith respect to",
            proof,
        )

    if debug:
        print(1000, proof)

    # Delete any leftover dimensions or keys
    # We hope there aren't any, but just in case...

    real_re = "(?:[+-]?(?:\\d+(?:[.,]\\d*)?|\\d*(?:[.,]\\d+)))"
    dimen_re2 = f"(?:{real_re}(?:[ ]?true[ ]?)?(?:in)\\b)"
    dimen_re = f"(?:{real_re}[ ]?(?:true[ ]?)?(?:pt|cm|mm|bp|em|ex|sp)\\b|{dimen_re2})"
    inf_re = f"(?:{real_re}[ ]?fill?l?)"
    dori_re = f"(?:{dimen_re}|{inf_re})"
    glue_re = (
        f"(?:{dimen_re}(?:[ ]?plus[ ]?{dori_re})?(?:[ ]?minus[ ]?{dori_re})?)"
    )

    # [5.2pt]
    proof = re.sub(f"\\[\\s*{glue_re}\\s*\\]", "", proof)

    # [width=5.2pt, boundary=solid]
    proof = re.sub("\\[\\s?[a-z_]+=.*?\\]", "", proof)

    # 5pt
    # =5pt
    # 5pt plus 1fil minus 5pt
    proof = re.sub(f"(=[ ]?)?{glue_re}", "", proof)

    # toric.eps
    proof = re.sub("[-_A-Za-z0-9]+[.](jpg|jpeg|eps|pdf|png|svg|ps)", "", proof)

    if debug:
        print("1020", proof)

    if aggressive:
        # by 1. of REF -> by REF of REF
        proof = re.sub(
            f"\\b(?i:(to|by|of|from))\\s*{numAlpha}[.](\\s+[a-z])",
            "\\1 REF \\2",
            proof,
        )

        # by 6.3 -> by REF
        # to 2-4a -> to REF
        # NOT  dividing by 2 -> dividing by REF
        # NOT  equal to 4 -> equal to REF
        # NOT  from 1 to 2. -> from REF to REF.
        # i.e., don't replace raw integers
        proof = re.sub(
            f"\\b(?i:(to|by|of|from))\\s*({numAlpha})",
            lambda match: match.group(1) + " " + match.group(2)
            if re.fullmatch(r"\d+", match.group(2))
            else match.group(1) + " REF",
            proof,
        )

        proof = re.sub(
            f"in CITE, {numAlpha}[.](\\s+[a-z])", "in CITE \\1", proof
        )
        proof = re.sub(f"in CITE, {numAlpha}", "in CITE", proof)

        # .. -> .
        # . . -> .
        proof = re.sub(r"(\.\s*)+\.", ".", proof)

        # MATH.1 to MATH
        # REF.1 to REF
        proof = re.sub(r"(MATH|CASE|REF|CITE)\.([0-9]){1,3}", r"\1", proof)


        # (i) MATH (ii) -> MATH
        # (i)MATH(ii) -> MATH
        proof = re.sub(f"{parenID} ?(MATH ?{parenID})+", " MATH ", proof)


        # (iii 'a-ds,.) -> REF
        # MATH(iii) -> REF
        proof = re.sub(
            r"(MATH)?\((\s*(SII|[iI]+)([0-9]|[A-Za-z]|['.,\-–]|\s){0,10}\s*)+\)",
            " REF ",
            proof,
        )

        # (sketch) -> ""
        proof = re.sub("\\(\\s*(?i:sketch)\\s*\\)", " ", proof)

        # (Base case) -> REF (then likely to CASE: later)
        proof = re.sub(r"\(\s*(?i:base)\s*(?i:case).{0,5}\s*\)", "REF", proof)

        proof = re.sub(r"Base\s*(?i:case)", "REF", proof)

    # Case 1: -> CASE
    proof = re.sub(r"[cC]ase\s*([0-9]*|MATH|REF)\s*(:)", "REF", proof)

    # ad 1 -> CASE
    proof = re.sub(f"(?i:ad)\\s*{numAlpha}(.)?", " CASE:", proof)

    if debug:
        print(1050, proof)

    if aggressive:

        # Simplify references to theorems, etc.
        # Prop. 2.1 -> REF
        # by Propositions 6.3 and 6.4. -> by REF.
        # by Propositions 6.3, 6.4 -> by REF
        # by Proposition 6.3 or 6.4 -> by REF

        # NOT by definition a nonempty -> by REF nonempty
        # NOT in fact a very -> in REF very
        # NOT uses Theorem 2. A consequence of -> uses REF . REF consequence of

        proof = re.sub(
            f"{theorem_word}\\s?((?![Aa]n?[ ])"
            f"{theoremNumber}(?:\\s?(?:[,-—]|and|or|with)\\s*"
            f"(?![Aa]n?[ ]){theoremNumber})*)",
            lambda m: re.sub(theoremNumber, "REF ", m.group(1)),
            proof,
        )

        # by Theorem I we have -> by REF we have
        # by Theorem IIa we have -> by REF we have
        proof = re.sub(f"{theorem_word}\\s?[IVX]+[a-z]?\\b", "REF", proof)

        # by Theorem MATH we have -> by REF we have
        proof = re.sub(f"\\b(([Bb]y|of|that|apply|from|using|in|is|to|^|[.(,]\s*)\\s+){theorem_word}\\s*MATH", "\\1REF", proof)

        # Part 3 of the theorem -> REF of the theorem -> REF
        proof = re.sub(f"REF of the {theorem_word}", "REF", proof)

        if debug:
            print(1100, proof)

        proof = re.sub(
            r"\(\s*([-0-9]+|[a-zA-Z])(\s*,\s*([0-9.,'-]+|[a-zA-Z])\s*)+\)",
            "MATH",
            proof,
        )

        proof = re.sub(
            r"\b(?i:(figure|fig))\s*([.]\s*[0-9]+)?(\s*REF)?", "REF ", proof
        )


        # Ad (i)MATH(ii) -> Ad MATH -> REF
        # By Theorem MATH, ->
        # oops... "by the mean value theorem MATH" -/->  "by the mean value REF"
        # proof = re.sub(f"{theorem_word}\s*MATH\\b", "REF", proof)


    # eliminate extra spaces
    proof = re.sub("[ ]+", " ", proof)

    if debug:
        print(1200, proof)


    if debug:
        print(1250, proof)

    # Case ii) We have -> CASE: We have
    proof = re.sub(
        f"(^|[.;:\\])] )(?:Case\\s+)?{parenID}:? "
        f"((?!CASE\\b|REF\\b){upperLetter})",
        "\\1CASE: \\2",
        proof,
    )
    if debug:
        print(1300, proof)

    # Case 1: We have -> CASE: We have
    proof = re.sub(
        f"(^|[.;:] )(?i:(sub)?cas)e\\s+(?:{numAlpha}|[ivx]+|[IVX]+|\\w)[:.]",
        "\\1CASE:",
        proof,
    )
    if debug:
        print(1350, proof)

    # Case $(1)$. -> Case MATH. -> CASE:
    # Case $(1)$-$(3). -> CASE MATH-MATH -> CASE:
    # Case MATH, MATH, or MATH -> CASE:
    proof = re.sub(
        "(^|[.;:] )\\b(?i:case)\\s+MATH(([-, ]|and|or)*MATH)*[:.]",
        "\\1CASE:",
        proof,
    )

    # ( MATH ) : -> -> CASE :
    proof = re.sub(r"\(\s*MATH\s*\)\s*:", "CASE :", proof)

    # (Case 1) -> REF
    proof = re.sub(
        f"\\((?i:case)\\s*{atomicID}+\\)",
        "REF ",
        proof,
    )

    if aggressive:
        # dfajfdkls Case 1 dfhaslsfdlk -> dfajfdkls REF dfhaslsfdlk
        proof = re.sub(
            f"({lowerLetter}+\\s+)(?i:case)\\s*{atomicID}*(\\s+{lowerLetter}+)",
            "\\1REF\\2",
            proof,
        )

    # # (i) We have -> REF We have -> CASE: We have
    # # BUT NOT:  T's Theorem CITE implies -> REF CITE implies -> CASE: implies
    # proof = re.sub(
    #     f"(^|[.;:] )REF[.: ]+({upperLetter}\\w+)",
    #     lambda m: m.group(1) + "CASE: " + m.group(2)
    #     if m.group(2) not in {"CITE", "REF"}
    #     else m.group(0),
    #     proof,
    # )

    if debug:
        print(1360, proof)

    # "1.) Let x be even..." --> "CASE: Let x be even..."
    # NOT  "(cf. REF) MATH -> cf. CASE: MATH"
    proof = re.sub(
        f"(^|[.;:\\])] )(?<!cf. ){atomicID}\\.?\\) ({upperLetter})",
        "\\1CASE: \\2",
        proof,
    )
    # We proceed in steps. 1. Let x be -> ...steps. CASE: Let x be
    proof = re.sub(
        f"(^|[.;:\\])] ){atomicID}\\. ({upperLetter})",
        "\\1CASE: \\2",
        proof,
    )

    proof = re.sub(f"(?i:stage)\\s*{atomicID}\\s*(.)", "", proof)

    proof = re.sub(
        f"\\(\\s*([iI]|{atomicID})*\\s*MATH\\s*([iI]|{atomicID})*\\s*\\)\\s*({upperLetter}|{lowerLetter})",
        " REF \\3",
        proof,
    )

    # proof = re.sub(f"\\(\\s*{atomicID}\\s*\\)", "REF", proof)

    proof = re.sub("CASE\\s*:(\\s*CASE\\s*:)+", "CASE:", proof)

    # base and inductive step labeling to CASE only when followed by capital letter
    proof = re.sub(
        rf"((\()?\s*(?i:basis)\s*(\))?|(\()?\s*(?i:induction)\s*(\))?)\s*(?!(?:MATH|REF|CASE|CITE|NAME))([A-Z])",
        " CASE: \\6",
        proof,
    )

    if debug:
        print(1400, proof)

    proof = re.sub(parenID, " REF ", proof)
    proof = re.sub("[ ]+", " ", proof)
    if debug:
        print(1500, proof)

    proof = re.sub("\\([ ]*\\)", " ", proof)

    if proof.count("(") != proof.count(")"):
        proof = treat_unbalanced_parens(filename, proof, debug, aggressive)

    if debug:
        print(1600, proof)

    # We write `MATH' to denote -> We write MATH to denote
    # We write ``MATH'' to denote -> We write MATH to denote
    proof = re.sub(r"['`]+MATH(\.?)['`]+", r"MATH\1", proof)
    # We write "MATH" to denote -> We write MATH to denote
    proof = re.sub(r"\"MATH(\.?)\"", r"MATH\1", proof)

    if debug:
        print(1700, proof)

    #
    # MENTIONS OF SECTIONS/CHAPTERS/APPENDICES
    #

    # e.g., Section 4 or Appendix B2
    section_word = (
        r"(?:(?i:(?:\b(?:Sect?s?|Apps?|Chs?|Vols?)(?:\b|\.))"
        r"|"
        r"(?:\b(?:Sections?|Appendi(?:x|ces)|Chapters?|Parts?|Steps?)\b)))"
    )

    # 5.3.2
    section_atom = "(?:[A-Z]\\d*\\b|[A-Z]?\\d+|\\b[IXV]+\\b|\\bREF\\b)"
    section_identifier = f"(?:\\b{section_atom}(?:[\\.]{section_atom})*)"
    section_maybe_range = (
        f"(?:{section_identifier}(?:\\s*[-–—,]\\s*{section_identifier})?)"
    )

    section_name = f"(?i:{section_word}\\s+(?:{section_maybe_range}))"

    # Simplify references to sections, e.g.,
    # Appendix A -> REF
    # Section 3.1 -> REF
    # Part (iv) -> REF
    proof = re.sub(section_name, r"REF", proof, 0)

    if debug:
        print(9600, proof)

    page = "([Pp][PpGg]?\\.?|[Pp]ages?\\b)"
    num_or_range = "\\d+(\\s*[-–—]\\s*\\d+)?"

    proof = re.sub(
        f"\\bCITE(\\s|[,])+({page}\\s*{num_or_range})", r"CITE", proof
    )

    proof = re.sub(r"(?i:subref)", "REF", proof)

    # p.45 of CITE -> REF of CITE
    proof = re.sub(f"{page}\\s*{num_or_range}", r"REF", proof)

    # NAME CITE -> CITE
    # NAME and NAME CITE -> CITE
    # NAME, NAME CITE -> CITE
    proof = re.sub("\\bNAME(([, ]|and)*NAME)* CITE", "CITE", proof)

    if debug:
        print(9650, proof)

    # p.45 of CITE -> REF of CITE -> REF
    # Theorem 2 in CITE -> REF in CITE -> REF
    proof = re.sub("\\bREF (of|in) CITE\\b", r"REF", proof)

    if debug:
        print(9700, proof)

    # (REF) -> REF
    proof = re.sub("\\(\\s*REF\\s*\\)", " REF ", proof)

    # (1) $\Rightarrow$ (2) => REF MATH REF => MATH
    proof = re.sub("\\bREF(\\s*MATH\\s*REF)+\\b", "MATH", proof)

    if debug:
        print(9750, proof)

    # Collapse adjacent references,
    # Appendix A Theorem 4 -> REF REF -> REF
    # (Appendix A Theorem 4) -> (REF REF) -> (REF) -> REF
    proof = re.sub(r"(\*)\s*REF\b", "REF", proof)
    proof = re.sub("\\bREF(\\s*REF)*\\b", r"REF", proof)
    proof = re.sub("\\(\\s*REF\\s*\\)", " REF ", proof)

    if debug:
        print(9800, proof)

    # Final cleanup

    # remove 2 = MATH or MATH = 2
    proof = re.sub(
        r"([0-9]+\s*=\s*MATH|MATH\s*=\s*[0-9]+|MATH\s*=\s*MATH)", "MATH", proof
    )

    # remove spurious periods after MATH
    # e.g., 0002/math0002001/finalversion.txt
    proof = re.sub(f"MATH \\. ({lowerLetter}\\w+)", "MATH \\1", proof)

    # add missing periods after MATH
    proof = re.sub(f"MATH ({upperLetter}{lowerLetter})", "MATH . \\1", proof)

    # Remove spurious extra periods (empty sentences)
    proof = re.sub("\\. (\\. )+", ". ", proof)

    # Remove unintelligible MATH MATH MATH sequences
    proof = re.sub("\\bMATH( MATH)*", "MATH", proof)

    # Remove sub-references in citations
    # \cite{smith}, Section 4 -> CITE, REF -> CITE
    # But Smoth \cite{smith} Theorem 2 -> NAME CITE, REF -> REF
    # proof = re.sub("CITE,? REF", "REF", proof)

    # Remove sub-references in citations
    # the theorem of Pick CITE -> REF CITE -> REF
    proof = re.sub("\\bREF,? CITE\\b", "REF", proof)
    # CITE, Theorem 2 -> CITE, REF -> REF
    proof = re.sub("\\bCITE,? REF\\b", "REF", proof)

    # ( CITE, Theorem 2) -> (CITE, REF) -> REF
    # ( CITE, 5.2) -> REF
    proof = re.sub(f"\\(\\s*CITE[ ,]+(REF|{numAlpha})\\s*\\)", " REF ", proof)

    # ( CITE ) -> CITE
    proof = re.sub("\\(\\s*CITE\\s*\\)", "CITE", proof)

    if debug:
        print(9850, proof)

    # [KMMT] -> CITE
    # [Abs98] -> CITE
    # [KMMT Theorem 5.] -> CITE
    proof = re.sub(
        "\\[[A-Z][A-Za-z]*\\s*\\d*([, ]+REF[.]?)?\\]", "CITE", proof
    )

    if debug:
        print(9860, proof)

    # [NAME, REF] -> CITE
    # (NAME, REF) -> CITE
    proof = re.sub("\\[\\s*NAME(,\\s*|\\s+)REF\\s*\\]", "CITE", proof)
    proof = re.sub("\\(\\s*NAME(,\\s*|\\s+)REF\\s*\\)", "CITE", proof)

    # The REF determines -> REF determines
    proof = re.sub("\\b[Tt]he REF\\b", "REF", proof)

    # (of REF) -> ""
    # (proof of REF) -> ""
    # (end of the proof of the claim) -> ""
    proof = re.sub(
        "\\(\\s*(?i:proof)?\\s*((?i:of\\s*(the)?\\s*theorem)|(?i:of\\s*REF(\\s*,\\s*REF)?)|(?i:of\\s*(the)?\\s*claim)|(?i:outline)|(?i:of\\s*proposition)|(?i:of\\s*lemma))\\s*\\)",
        "",
        proof,
    )

    # an MATH -> a MATH
    proof = re.sub("\\b([Aa])n[ ]MATH\\b", r"\1 MATH", proof)

    # MATH MATH -> MATH
    # MATHMATH -> MATH
    # proof = re.sub(r"(MATH\s*,\s*|MATH\s*((?i:and)|&)\s*)+MATH", "MATH ", proof)
    proof = re.sub(r"(MATH\s*)+MATH", "MATH", proof)

    # figure REF ii -> REF

    proof = re.sub(
        "(\\(\\s*(?i:figure)\\s*REF\\s*i*\\s*\\)|(?i:figure)\\s*REF\\s*i*\\s*)",
        " REF ",
        proof,
    )

    # Case REF -> REF
    proof = re.sub(r"\b([Ss]ub)?(?i:case(s)?)\s*(MATH|REF)", "REF", proof)

    proof = re.sub(r"\(\s*REF\s*\)\s*([A-Z])", "REF \\1", proof)

    # (i) We have -> REF We have -> CASE: We have
    # BUT NOT:  T's Theorem CITE implies -> REF CITE implies -> CASE: implies
    proof = re.sub(
        f"(^|[.;:] )REF[.: ]+({upperLetter}\\w+)",
        lambda m: m.group(1) + "CASE: " + m.group(2)
        if m.group(2) not in {"CITE", "REF"}
        else m.group(0),
        proof,
    )

    if debug:
        print(9890, proof)

    # MATH.1 to MATH
    # REF.1 to REF
    proof = re.sub(r"(MATH|CASE|REF|CITE)\.([\.A-Za-z0-9]){1,5}", r"\1", proof)

    proof = re.sub(
        r"([Ss]ub)?[Cc]ase\s*([0-9]|[A-Za-z]|[',-–]|\s){0,5}([.,])\s*",
        "REF\\2 ",
        proof,
    )

    # (see REF) -> (REF)
    proof = re.sub(r"\(\s*((?i:see)|(?i:by))\s*REF\s*\)", "(REF)", proof)
    # proof = re.sub(r"\(\s*(?i:see)\s*REF\s*.{0,100}\)", "(REF)", proof)

    proof = re.sub(r"(CASE:\s*)(CASE:\s*)+", "CASE: ", proof)

    # REF in REF -> REF
    # REF, REF -> REF
    proof = re.sub(r"REF(\s*(in|and|,)\s*REF)+", "REF", proof)

    # ( REF ) -> REF   (possibly a repeat, but maybe there are more single REFs now)
    proof = re.sub(r"\(\s*REF\s*\)", " REF ", proof)

    if debug:
        print(9900, proof)

    proof = re.sub(
        f"\\.({upperLetter}({upperLetter}|{lowerLetter})+)", ". \\1", proof
    )

    # add a space around and normalize any dashes
    proof = re.sub(r"([﹘–—⸺⸻])", r" - ", proof)

    # simplify and replace weird single and double quotation marks from proofs
    proof = re.sub(r"[‘’‛′´❜❛]", "'", proof)
    proof = re.sub(r"[“”‟″˝¨❝❞]", '"', proof)

    # replace two single quotes with a double quote
    proof = re.sub("''", '"', proof)

    # Remove any duplicate spaces we introduced
    proof = re.sub("[ ]+", " ", proof)

    proof = proof.strip()

    if debug:
        print(9999, proof)

    return proof


URL = re.compile(
    r"""\b(?:https?|ftp|gopher)\s?:\s?/{1,3}\s?(?:[-a-z0-9_%@']+[.])+[-a-z0-9_%@]+(?:[:][0-9]+)?(?:\s*[/]\s*[.a-z0-9_%#~&@*()'~-]*)*\s*(?:[/]\s*[a-z0-9_%#~&@*()'~-]*[/]|[/][a-z0-9_%#~&@*()'~-]*)""",
    re.IGNORECASE,
)


def urls(proof, debug=False):
    # Don't let it end with a period
    proof = re.sub(URL, " REF ", proof)
    return proof


def clean_proof(
    orig: str,
    debug: bool = False,
    filename: str = "<unknown>",
    aggressive: bool = True,
):
    if "\t" in orig:
        (prefix, line) = orig.split("\t")
        prefix += "\t"
    else:
        (prefix, line) = ("", orig)

    clean = unicodedata.normalize("NFKC", line)
    clean = clean.replace("�", "")  # 0810/0810.4782
    if debug:
        print("0000", clean)
    clean = urls(clean, debug)
    clean = splitMATH(clean, debug, aggressive)
    clean = ner(clean, debug, aggressive)
    if debug:
        print("0200", clean)
    clean = cleanup(filename, clean, debug, aggressive)
    # clean = remove_extra_rparens(clean)
    return prefix + clean


def skip_this_proof(proof: str) -> bool:
    """Skip very specific proofs."""
    forbidden_strings = [
        "Angenommen",  #  1410/1410.313
        "C1234, C23456, C2659",  # 2003/2003.06204
        "Pl-B-Match",  # 2001/2001.01493
        "if@tlamode",  # 1908/1908.05535, 2002/2002.03613, 1508/1508.02705
        "10_139",  # 2004/2004.08699
        "5_2(-1,1)",  # 2004/2004.08699
    ]
    for s in forbidden_strings:
        if s in proof:
            return True
    return False


def quietly_clean_proof(filename: str, aggressive: bool, orig: str):
    return clean_proof(orig, False, filename, aggressive)


if __name__ == "__main__":
    nicer.make_nice()

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-d", "--debug", help="Show tracing output", action="store_true"
    )
    parser.add_argument(
        "-a", "--aggressive", help="Intensity of cleanup", action="store_false"
    )
    parser.add_argument(
        "-p", "--cores", help="Number of cores to use", type=int, default=8
    )
    parser.add_argument(
        "files", nargs="*", type=argparse.FileType("r"), default=[sys.stdin]
    )
    args = parser.parse_args()

    if args.debug:
        print("Debugging enabled; will not use multiple cores")
        args.cores = 1
        args.p = 1

    for fd in args.files:
        if args.cores == 1:
            for orig in fd.readlines():
                clean = clean_proof(orig, args.debug, fd.name, args.aggressive)
                if args.debug:
                    print()
                    print(orig.strip())
                    print("   --->")
                    print(clean)
                    print()
                else:
                    if not skip_this_proof(clean):
                        print(clean)
        else:
            assert not args.debug
            lines = fd.readlines()
            with Pool(processes=args.cores) as p:
                # p.map(pf, tex_files, 1)
                for line in p.imap(
                    functools.partial(
                        quietly_clean_proof, fd.name, args.aggressive
                    ),
                    lines,
                    50,
                ):
                    if not skip_this_proof(line):
                        print(line)

        fd.close()
