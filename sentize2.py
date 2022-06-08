#!/usr/bin/env python

"""Split lines into sentences."""

import argparse
from multiprocessing import Pool
import sys
from typing import List

from nltk.tokenize import PunktSentenceTokenizer
from nltk.tokenize.destructive import NLTKWordTokenizer

import nicer

# suspicious = re.compile("[&_^\x00-\x1f\x80-\xff]")
def inner_parens(s):
    d = {"(": 1, ")": -1}
    tot = 0
    for x in s:
        if x in d.keys():
            tot += d[x]
        if tot < 0:
            return False
    return True


# collected by running
#   grep '[a-z]\.[a-z] \.$' all-sentences.txt
# but perhaps better would be
#   egrep -oh '\b([A-Za-z]+\.)+[a-z]+\.\ ' proofs*.raw | sort | uniq | tee abbrevs.txt
MATH_ABBREVS = set(
    [
        "a.a",
        "a.c.i.m",
        "a.c",
        "a.e",
        "a.k.a",
        "a.m.s",
        "a.m",
        "a.s",
        "a.u",
        "al",
        "b.c.i",
        "c.a.i",
        "c.b",
        "c.c.c.t",
        "c.c",
        "c.d.f",
        "c.e",
        "c.f",
        "c.i",
        "c.p.c",
        "c.p",
        "c.u.c",
        "c.u.p",
        "d.g",
        "d.o.f",
        "d.t.s",
        "dr",
        "e.g",
        "et",  # not really, but it's a very common mistake.
        "f.e",
        "f.g.p.m",
        "f.g",
        "g.c.d",
        "g.l.n",
        "g.l.s",
        "i.e",
        "i.h",
        "i.i.d.r.v",
        "i.i.d",
        "i.o",
        "I.T.",
        "i.u.r",
        "inc",
        "l.c.a.i",
        "l.c.m",
        "l.c",
        "l.h.s",
        "L.H.S",
        "l.m.g.f",
        "l.o.t",
        "l.s.c",
        "m.p",
        "mr",
        "mrs",
        "n.b",
        "N.B",
        "n.c",
        "o.d.e",
        "O.D.E",
        "p.h",
        "p.h",
        "p.l",
        "p.m",
        "p.o",
        "p.s.h",
        "p.s.h",
        "prof",
        "q.c.i",
        "q.c",
        "q.e",
        "q.p",
        "q.s",
        "q.v",
        "r.c.a.i",
        "r.e",
        "r.h.s",
        "R.H.S",
        "r.l.s.c",
        "r.r.v",
        "r.v",
        "s.m.u",
        "u.c.p",
        "u.e",
        "u.i",
        "u.s.c",
        "vs",
        "w.h.e",
        "w.h.p",
        "w.l.o.g",
        "w.p",
        "w.r.t",
        "w.r",
        "A.C",
        "A.D",
        "A.D.M",
        "A.G",
        "A.H",
        "A.I",
        "A.K",
        "A.L",
        "A.M",
        "A.M.S",
        "A.O",
        "A.P",
        "A.P.S",
        "A.Q",
        "A.R",
        "A.S",
        "A.V",
        "A.W",
        "A.a.s",
        "A.e",
        "A.i",
        "A.ii",
        "A.iii",
        "A.iv",
        "A.ix",
        "A.j",
        "A.s",
        "A.v",
        "A.vi",
        "A.vii",
        "A.viii",
        "A.x",
        "ABE.NAME",
        "AS.R",
        "B.A",
        "B.B",
        "B.C.A.P",
        "B.G",
        "B.H",
        "B.I",
        "B.I.C",
        "B.L",
        "B.L.T",
        "B.M",
        "B.P",
        "B.f",
        "B.f.s",
        "B.h",
        "B.iii",
        "B.m",
        "B.w",
        "C.A",
        "C.A.P",
        "C.C.C",
        "C.D",
        "C.D.F",
        "C.E",
        "C.F",
        "C.F.L",
        "C.I",
        "C.L.T",
        "C.M",
        "C.O.M",
        "C.O.N.S",
        "C.P",
        "C.T",
        "C.T.C",
        "C.W",
        "CLT.Mb",
        "Ch.II",
        "Ch.V",
        "Counterexample.nb",
        "D.A",
        "D.A.C",
        "D.A.F",
        "D.B",
        "D.C",
        "D.E",
        "D.G.A",
        "D.G.R",
        "D.L",
        "D.L.M",
        "D.P",
        "D.R",
        "D.REF",
        "D.S",
        "D.T",
        "D.V",
        "D.Z",
        "E.A",
        "E.B",
        "E.B.T",
        "E.C.T",
        "E.D",
        "E.I",
        "E.MATH",
        "E.Opp",
        "E.REF",
        "E.T",
        "E.V",
        "E.V.I",
        "E.q",
        "Eq.s",
        "F.A",
        "F.B.I",
        "F.I",
        "F.I.O",
        "F.J",
        "F.K.G",
        "F.M.T",
        "F.S",
        "F.T.o.C",
        "F.X",
        "F.Y",
        "F.p",
        "F.t",
        "G.A",
        "G.A.G.A",
        "G.A.S",
        "G.C",
        "G.C.D",
        "G.D",
        "G.F",
        "G.F.Q.I",
        "G.G",
        "G.I.T",
        "G.L",
        "G.M",
        "G.N.S",
        "G.O",
        "G.O.D",
        "G.O.S",
        "G.R",
        "G.S",
        "G.T",
        "G.U.E",
        "GT.Eval",
        "H.B",
        "H.D",
        "H.E",
        "H.F",
        "H.G",
        "H.I",
        "H.J",
        "H.N",
        "H.S",
        "H.U.M",
        "H.c",
        "H.m",
        "I.A",
        "I.A.c",
        "I.B",
        "I.C.C",
        "I.D",
        "I.E",
        "I.F.T",
        "I.Fe",
        "I.H",
        "I.I",
        "I.I.D",
        "I.J",
        "I.M",
        "I.M.S",
        "I.N",
        "I.P",
        "I.S",
        "I.T",
        "I.V.T",
        "I.a",
        "I.b",
        "II.A",
        "II.B",
        "II.B.i.b",
        "II.B.ii.a",
        "II.REF",
        "II.a",
        "II.b",
        "II.c",
        "II.d",
        "II.ii",
        "III.H",
        "III.II",
        "III.a",
        "III.b",
        "III.d",
        "III.i",
        "IV.C",
        "IV.b",
        "IV.c",
        "J.C",
        "J.C.C",
        "J.D",
        "J.E",
        "J.E.P",
        "J.F",
        "J.G",
        "J.H.C",
        "J.H.S",
        "J.L",
        "J.M",
        "J.P",
        "J.R",
        "J.T.P",
        "J.W",
        "J.n.f",
        "K.A.M",
        "K.C",
        "K.I",
        "K.K.S",
        "K.K.T",
        "K.M",
        "K.P",
        "K.S",
        "K.T",
        "L.A",
        "L.A.S",
        "L.C.T",
        "L.G.S",
        "L.H",
        "L.H.S",
        "L.HS",
        "L.I",
        "L.I.M",
        "L.L.N",
        "L.O.T",
        "L.P",
        "L.R.A",
        "L.S",
        "L.S.C",
        "L.S.D",
        "L.V",
        "L.h.s",
        "L.t",
        "L.t.s",
        "Loc.cit",
        "M.A",
        "M.B",
        "M.C",
        "M.C.D",
        "M.H",
        "M.I.H",
        "M.I.S",
        "M.L",
        "M.N",
        "M.P",
        "M.R",
        "M.S",
        "M.Sc",
        "M.T",
        "M.V",
        "N.B",
        "N.D",
        "N.E",
        "N.G",
        "N.J.A.S",
        "N.N",
        "N.P",
        "N.S",
        "N.V.S",
        "N.b",
        "Neg.a",
        "Neg.b",
        "Neg.c",
        "Neg.d",
        "O.D",
        "O.D.E",
        "O.K",
        "O.N",
        "O.N.B",
        "O.S",
        "O.U",
        "P.A",
        "P.B",
        "P.B.W",
        "P.C",
        "P.D",
        "P.D.E",
        "P.D.F",
        "P.D.O",
        "P.E",
        "P.G.F",
        "P.H",
        "P.I",
        "P.I.D",
        "P.J",
        "P.L",
        "P.L.I",
        "P.P.P",
        "P.P.T",
        "P.R.I",
        "P.REF",
        "P.S",
        "P.S.D",
        "P.V",
        "P.p.p",
        "Ph.D",
        "Ph.d",
        "Pos.a",
        "Pos.b",
        "Pos.c",
        "Pos.d",
        "Q.D.E",
        "Q.E",
        "Q.E.A",
        "Q.F.T",
        "Q.H.I",
        "Q.U.P",
        "R.A",
        "R.B",
        "R.C",
        "R.E",
        "R.H",
        "R.I",
        "R.I.C",
        "R.I.H",
        "R.I.P",
        "R.I.S",
        "R.I.s.c.c",
        "R.L",
        "R.L.P",
        "R.P",
        "R.R",
        "R.S",
        "R.T",
        "R.V",
        "R.v",
        "REGAL.C",
        "S.A",
        "S.C.C",
        "S.C.R",
        "S.C.U",
        "S.D",
        "S.D.E",
        "S.D.o.F",
        "S.G.S",
        "S.H",
        "S.J",
        "S.L",
        "S.L.T",
        "S.M",
        "S.M.T",
        "S.N",
        "S.N.A.G",
        "S.O",
        "S.O.T",
        "S.P",
        "S.R",
        "S.REF",
        "S.S.A.G.E",
        "S.T",
        "S.V",
        "S.V.Z",
        "S.Y",
        "S.ii",
        "S.iii",
        "S.u.g",
        "T.B.R.B.O",
        "T.CITE",
        "T.D.S",
        "T.E",
        "T.I",
        "T.O",
        "T.P",
        "T.REF",
        "T.S",
        "T.T",
        "T.V",
        "T.o.C",
        "Th.MATH",
        "Token.color",
        "Token.number",
        "Token.session",
        "Top.papernat",
        "U.B.D",
        "U.C",
        "U.C.T",
        "U.F.D",
        "U.I",
        "U.P",
        "U.S.C",
        "V.A",
        "V.B",
        "V.C",
        "V.C.G.C",
        "V.I",
        "V.P",
        "VI.REF",
        "W.B",
        "W.D",
        "W.F",
        "W.F.F",
        "W.H",
        "W.I.T",
        "W.L.G",
        "W.O.L.G",
        "W.W",
        "W.X",
        "W.h.p",
        "W.l.g",
        "W.l.lo.g",
        "W.o.l.g",
        "W.p",
        "W.v.h.p",
        "Weeds.nb",
        "X.C",
        "Y.G",
        "Y.P",
        "Y.Y",
        "Z.L",
        "a.C.M",
        "a.CM",
        "a.a",
        "a.a.e",
        "a.a.k",
        "a.a.p",
        "a.a.s",
        "a.b",
        "a.b.f.o",
        "a.c",
        "a.c.S",
        "a.c.c",
        "a.c.h",
        "a.c.i.m",
        "a.c.i.p",
        "a.c.m",
        "a.c.m.s",
        "a.c.s",
        "a.d",
        "a.d.c.c",
        "a.e",
        "a.e.a.s",
        "a.e.c",
        "a.e.d",
        "a.e.i.t",
        "a.e.p",
        "a.e.p.d.f",
        "a.e.t",
        "a.e.w",
        "a.f",
        "a.f.g",
        "a.f.p",
        "a.f.p.s",
        "a.f.r",
        "a.g.g",
        "a.i",
        "a.i.t",
        "a.ii",
        "a.iii",
        "a.k.a",
        "a.m",
        "a.m.s",
        "a.n",
        "a.o",
        "a.o.a",
        "a.o.p",
        "a.o.u",
        "a.p",
        "a.r",
        "a.s",
        "a.s.CITE",
        "a.s.MATH",
        "a.s.a.a",
        "a.s.continuous",
        "a.s.e",
        "a.s.finite",
        "a.s.g",
        "a.s.nonnegative",
        "a.s.statement",
        "a.s.u",
        "a.s.w",
        "a.sCITE",
        "a.t.t.s",
        "a.u",
        "a.u.c",
        "a.u.c.d",
        "a.u.e",
        "a.u.e.c",
        "a.u.i",
        "a.w.e",
        "a.w.o.p",
        "actioncontainedtangentspace.nb",
        "al.CITE",
        "al.REF",
        "analogously.MATH",
        "arc.transitive",
        "artigos.html",
        "b.MATH",
        "b.MATH.w.a.i",
        "b.a.b",
        "b.a.i",
        "b.a.s",
        "b.a.u",
        "b.c",
        "b.c.c",
        "b.c.i",
        "b.c.p",
        "b.e",
        "b.f",
        "b.i",
        "b.i.m",
        "b.i.p",
        "b.ii",
        "b.iii",
        "b.iv",
        "b.l.u.p",
        "b.o",
        "b.p",
        "b.p.f",
        "b.p.i.r.e",
        "b.p.p",
        "b.q.o",
        "b.s.a",
        "b.s.a.l",
        "b.u.e.m",
        "b.v",
        "b.w",
        "b.w.o.c",
        "basic.REF",
        "bistab.mw",
        "blacka.a",
        "blacki.e",
        "blacks.t",
        "blackw.h.p",
        "blackw.r.t",
        "c.a",
        "c.a.c.s",
        "c.a.d",
        "c.a.d.l.a.g",
        "c.a.f",
        "c.a.g.o.s",
        "c.a.h",
        "c.a.i",
        "c.a.o.s",
        "c.a.s",
        "c.b",
        "c.b.l.f",
        "c.c",
        "c.c.c",
        "c.c.c.iteration",
        "c.c.c.poset",
        "c.c.c.posets",
        "c.c.c.t",
        "c.c.d.f",
        "c.c.h",
        "c.c.p",
        "c.c.r",
        "c.c.s",
        "c.c.s.s",
        "c.c.t",
        "c.c.w",
        "c.d",
        "c.d.f",
        "c.d.f.s",
        "c.d.g.a",
        "c.d.i",
        "c.e",
        "c.e.a",
        "c.e.c",
        "c.e.d",
        "c.e.m.p",
        "c.e.m.p.t",
        "c.g.f",
        "c.g.u.r",
        "c.i",
        "c.i.c",
        "c.i.d",
        "c.i.i",
        "c.i.i.d",
        "c.i.p",
        "c.i.s.t",
        "c.i.t",
        "c.ii",
        "c.iii",
        "c.iii.a",
        "c.iv",
        "c.l.m",
        "c.l.s",
        "c.l.s.b",
        "c.m",
        "c.m.a.p",
        "c.m.m",
        "c.n",
        "c.n.c",
        "c.n.d",
        "c.n.d.f",
        "c.n.i",
        "c.n.i.f",
        "c.n.s",
        "c.n.u",
        "c.o",
        "c.o.D",
        "c.o.c.d",
        "c.o.f.e",
        "c.o.g",
        "c.o.i",
        "c.o.n.s",
        "c.o.p",
        "c.p",
        "c.p.c",
        "c.p.d",
        "c.p.e",
        "c.p.m",
        "c.p.s",
        "c.p.t.p",
        "c.q.e",
        "c.q.g",
        "c.r",
        "c.r.g",
        "c.r.w",
        "c.s",
        "c.s.c",
        "c.s.e",
        "c.s.p",
        "c.s.w",
        "c.t",
        "c.t.p",
        "c.u.b",
        "c.u.c",
        "c.u.d",
        "c.u.i.s",
        "c.u.p",
        "c.u.s",
        "c.v",
        "c.w",
        "c.w.g",
        "c.z",
        "certD.magma",
        "ch.f",
        "ch.v",
        "cl.dejavu",
        "coloroke.g",
        "coloroki.e",
        "companionw.r.t",
        "compcox.lib",
        "computeralgebra.htm",
        "crossings.uos.de",
        "cy.html",
        "d.MATH",
        "d.R.i",
        "d.a.e",
        "d.block",
        "d.blocks",
        "d.c",
        "d.c.c",
        "d.c.e",
        "d.c.i",
        "d.c.s",
        "d.d",
        "d.d.f",
        "d.e.w",
        "d.f",
        "d.f.s",
        "d.g",
        "d.g.a",
        "d.g.p",
        "d.h",
        "d.ii",
        "d.iii",
        "d.l",
        "d.l.b",
        "d.m",
        "d.n.c",
        "d.n.s",
        "d.o.e",
        "d.o.f",
        "d.p",
        "d.p.s",
        "d.r",
        "d.r.a",
        "d.s",
        "d.s.a.e",
        "d.s.h",
        "d.s.v",
        "d.t",
        "d.t.d",
        "d.t.s",
        "d.u",
        "d.u.b",
        "d.v.r",
        "e.N.m",
        "e.REF",
        "e.a",
        "e.a.b",
        "e.a.f",
        "e.a.s",
        "e.a.s.e",
        "e.c",
        "e.c.s",
        "e.c.u",
        "e.d",
        "e.d.HOP",
        "e.d.f",
        "e.e",
        "e.e.d",
        "e.f",
        "e.i",
        "e.i.g",
        "e.m",
        "e.m.p",
        "e.m.p.t",
        "e.n.v",
        "e.o.s",
        "e.q",
        "e.s",
        "e.s.a",
        "e.s.c",
        "e.s.d",
        "e.s.p",
        "e.t.c",
        "e.u.b",
        "e.u.c",
        "e.v",
        "e.v.P",
        "e.v.d",
        "e.x",
        "el.c.s.c",
        "et.al",
        "et.c",
        "euclid.sage",
        "f.B.m",
        "f.a",
        "f.a.a",
        "f.a.i",
        "f.a.p",
        "f.a.s",
        "f.b",
        "f.c",
        "f.c.c",
        "f.c.p",
        "f.d",
        "f.d.a",
        "f.d.d",
        "f.d.nonspacelike",
        "f.d.p",
        "f.d.s.a",
        "f.e",
        "f.ex",
        "f.f",
        "f.f.m.p",
        "f.f.t",
        "f.g",
        "f.g.l",
        "f.g.p",
        "f.g.p.m",
        "f.g.projective",
        "f.h",
        "f.h.e",
        "f.i",
        "f.i.p",
        "f.i.s",
        "f.l",
        "f.l.c",
        "f.l.p",
        "f.m",
        "f.m.b",
        "f.m.g.f",
        "f.m.p.t",
        "f.n",
        "f.n.s",
        "f.o",
        "f.p",
        "f.p.f",
        "f.p.h.e",
        "f.p.r.a.s",
        "f.p.t",
        "f.p.w.h.e",
        "f.r",
        "f.r.m",
        "f.r.p.p",
        "f.r.t",
        "f.r.v",
        "f.s",
        "f.s.c",
        "f.s.d",
        "f.s.n",
        "f.s.o",
        "f.s.o.g",
        "f.t.a",
        "f.v",
        "f.w.c",
        "farsta.html",
        "g.CM",
        "g.c",
        "g.c.d",
        "g.c.m.s",
        "g.c.p",
        "g.c.v",
        "g.conf",
        "g.d",
        "g.e.c",
        "g.e.s",
        "g.f",
        "g.f.q.i",
        "g.g",
        "g.g.g",
        "g.g.s",
        "g.i.d",
        "g.j.d",
        "g.k.n",
        "g.l.b",
        "g.l.n",
        "g.l.s",
        "g.n.h.f",
        "g.o",
        "g.p",
        "g.r.t",
        "g.s",
        "g.s.c",
        "g.s.w.f",
        "g.t",
        "gen.red.s.b",
        "generators.sage",
        "groupprops.subwiki.org",
        "growth.html",
        "h.c",
        "h.c.c.b",
        "h.c.p",
        "h.d",
        "h.e",
        "h.f.c",
        "h.i.t",
        "h.j.i",
        "h.l.c",
        "h.m.c",
        "h.m.p.h",
        "h.n",
        "h.n.f",
        "h.n.p.c",
        "h.o",
        "h.o.a",
        "h.o.t",
        "h.p",
        "h.s",
        "h.s.o.p",
        "h.t",
        "h.u",
        "h.w",
        "hopf.mw",
        "hypothesisw.r.t",
        "i.a",
        "i.a.c",
        "i.a.r",
        "i.b",
        "i.b.s",
        "i.bis",
        "i.c",
        "i.c.c",
        "i.c.i.s",
        "i.c.m",
        "i.c.s",
        "i.d",
        "i.d.d",
        "i.d.f",
        "i.d.i",
        "i.d.o.c",
        "i.f.f",
        "i.f.g",
        "i.f.s",
        "i.g",
        "i.h",
        "i.h.applies",
        "i.h.s",
        "i.i.d",
        "i.i.d.normal",
        "i.i.d.r.v",
        "i.i.d.r.vs",
        "i.i.d.sequences",
        "i.i.d.w.r.t",
        "i.id",
        "i.m",
        "i.n",
        "i.n.d",
        "i.n.i.d",
        "i.o",
        "i.o.e",
        "i.o.p",
        "i.p",
        "i.p.i.d",
        "i.p.m",
        "i.p.s",
        "i.r.p.d.f",
        "i.r.v",
        "i.s",
        "i.s.L",
        "i.s.c",
        "i.s.p.d",
        "i.s.t",
        "i.t",
        "i.t.c.i",
        "i.t.m",
        "i.u",
        "i.u.a.r",
        "i.u.d",
        "i.u.r",
        "i.u.t.l.a",
        "i.v",
        "i.v.p",
        "i.w",
        "ii.a",
        "ii.b",
        "ii.c",
        "iii.a",
        "iii.c",
        "ind.hyp",
        "index.html",
        "inf.mpg.de",
        "inj.dim.MATH",
        "j.c.b",
        "j.n.v.n",
        "j.p.d",
        "k.EXREFalgorithm",
        "k.l.t",
        "l.a",
        "l.a.o",
        "l.a.p",
        "l.a.s",
        "l.b",
        "l.c",
        "l.c.K",
        "l.c.a.i",
        "l.c.c",
        "l.c.d",
        "l.c.i",
        "l.c.m",
        "l.c.p.s",
        "l.c.s",
        "l.c.s.c",
        "l.c.s.c.group",
        "l.collect",
        "l.d",
        "l.d.p",
        "l.d.t",
        "l.e.a.r",
        "l.e.n.s",
        "l.e.o",
        "l.e.s",
        "l.e.v",
        "l.f",
        "l.f.p",
        "l.g.p",
        "l.h",
        "l.h.s",
        "l.h.t",
        "l.i",
        "l.i.m",
        "l.l.t",
        "l.m.v.s",
        "l.main",
        "l.n",
        "l.n.d",
        "l.o",
        "l.o.g",
        "l.o.t",
        "l.p",
        "l.p.R",
        "l.p.c",
        "l.r",
        "l.r.d",
        "l.r.s",
        "l.r.t",
        "l.s",
        "l.s.a",
        "l.s.c",
        "l.s.c.d.s",
        "l.s.d",
        "l.s.f",
        "l.s.o.p",
        "l.t.T",
        "l.topological",
        "l.u.b",
        "l.u.p",
        "l.u.s.c",
        "l.v.a",
        "l.v.c",
        "l.w.a.p",
        "l.w.s.c",
        "l.w.v",
        "loc.cit",
        "loc.cite",
        "loc.sit",
        "m.K.p",
        "m.a.d",
        "m.a.e",
        "m.a.p",
        "m.a.s.a",
        "m.b",
        "m.c",
        "m.c.g.m",
        "m.c.n",
        "m.c.r",
        "m.c.s",
        "m.d.s",
        "m.e",
        "m.e.c",
        "m.e.d",
        "m.e.f",
        "m.f.c",
        "m.g.f",
        "m.g.i",
        "m.g.u",
        "m.h.r",
        "m.h.s",
        "m.i.f",
        "m.l.d",
        "m.l.e",
        "m.l.f",
        "m.l.i",
        "m.m",
        "m.m.e",
        "m.m.s",
        "m.n.e",
        "m.n.f",
        "m.n.i.s.a",
        "m.p",
        "m.p.s",
        "m.p.t",
        "m.r",
        "m.r.n.c",
        "m.r.t",
        "m.s",
        "m.s.e",
        "m.s.g",
        "m.s.o",
        "m.s.o.r.d.f",
        "m.s.s",
        "m.t.i",
        "m.v",
        "m.v.f",
        "mathoverflow.net",
        "matrixmu.equ",
        "mixedcoeffscharpolykb.nb",
        "modpsums.nb",
        "monitorablew.r.t",
        "n.a",
        "n.a.s",
        "n.b",
        "n.b.f",
        "n.c",
        "n.d",
        "n.e",
        "n.e.f",
        "n.f",
        "n.f.s",
        "n.i.b",
        "n.l.c",
        "n.n",
        "n.n.H",
        "n.n.c",
        "n.p",
        "n.p.c",
        "n.s",
        "n.s.a",
        "n.s.d",
        "n.s.f",
        "n.t",
        "n.u",
        "n.w.f.s",
        "npqrec.modu",
        "nspc.f.d",
        "nspc.p.d",
        "o.c",
        "o.c.p",
        "o.d",
        "o.d.e",
        "o.f",
        "o.g.f",
        "o.i",
        "o.k",
        "o.m",
        "o.n",
        "o.n.b",
        "o.n.s",
        "o.p",
        "o.p.a",
        "o.p.c",
        "o.r",
        "o.s",
        "o.s.c",
        "o.s.s",
        "o.v",
        "o.w",
        "observable.diameters.continuous",
        "op.cit",
        "p.A",
        "p.L",
        "p.REF",
        "p.a.h",
        "p.a.o",
        "p.a.p",
        "p.a.s",
        "p.b.i",
        "p.c",
        "p.c.a.p",
        "p.c.c",
        "p.c.o",
        "p.c.s",
        "p.d",
        "p.d.e",
        "p.d.f",
        "p.d.h",
        "p.d.o",
        "p.e",
        "p.e.c",
        "p.e.o",
        "p.f",
        "p.f.d",
        "p.g",
        "p.g.f",
        "p.g.fl",
        "p.g.fs",
        "p.h",
        "p.h.r",
        "p.h.t",
        "p.i",
        "p.i.c",
        "p.i.d",
        "p.i.r",
        "p.i.s.u.n",
        "p.l",
        "p.l.f",
        "p.l.s",
        "p.l.s.b",
        "p.m",
        "p.m.c.s.p",
        "p.m.f",
        "p.m.i",
        "p.m.m",
        "p.m.m.s",
        "p.m.p",
        "p.m.s.p",
        "p.n",
        "p.no",
        "p.o",
        "p.o.t",
        "p.p",
        "p.p.a.s",
        "p.p.a.v",
        "p.p.d",
        "p.p.f",
        "p.p.m",
        "p.p.p",
        "p.p.q.i",
        "p.p.t",
        "p.r",
        "p.r.a",
        "p.r.c",
        "p.r.p",
        "p.r.s",
        "p.s",
        "p.s.d",
        "p.s.h",
        "p.s.s",
        "p.u",
        "p.v",
        "p.w",
        "papers.html",
        "pg.f",
        "positivew.h.p",
        "pre.explorers",
        "proj.dim",
        "proofs.jl",
        "ps.d.o",
        "q.a",
        "q.a.e",
        "q.c",
        "q.c.i",
        "q.d",
        "q.d.e",
        "q.d.f",
        "q.e",
        "q.e.MATH",
        "q.g",
        "q.h",
        "q.i",
        "q.l.s.c",
        "q.m",
        "q.m.d",
        "q.o",
        "q.p",
        "q.p.p",
        "q.p.s.h",
        "q.r",
        "q.s",
        "q.s.d",
        "q.s.o",
        "q.t.i",
        "q.t.p",
        "q.u.p",
        "q.v",
        "q.w.p.p",
        "qc.qs",
        "r.K.m",
        "r.a",
        "r.a.c",
        "r.a.p",
        "r.a.s",
        "r.b",
        "r.c",
        "r.c.a.i",
        "r.c.d",
        "r.c.l.l",
        "r.c.m",
        "r.c.p.d",
        "r.c.p.m",
        "r.d.f",
        "r.e",
        "r.e.a.r",
        "r.e.i",
        "r.f",
        "r.f.d",
        "r.f.g",
        "r.f.m.p",
        "r.h",
        "r.h.t",
        "r.i",
        "r.i.c.e",
        "r.k.H.s",
        "r.l.p",
        "r.l.s.c",
        "r.m",
        "r.n",
        "r.n.b",
        "r.p",
        "r.p.i",
        "r.p.o.v",
        "r.q.c",
        "r.q.e",
        "r.r.v",
        "r.s",
        "r.s.h",
        "r.s.p",
        "r.t",
        "r.u.s.c",
        "r.u.u.s.c",
        "r.v",
        "r.v.s",
        "r.vc",
        "r.vc.s",
        "r.vs",
        "r.w",
        "r.w.i",
        "r.w.r.e",
        "red.gen.s.b",
        "redi.e",
        "s.G.d",
        "s.a",
        "s.a.e",
        "s.a.p",
        "s.a.s",
        "s.b",
        "s.c",
        "s.c.c",
        "s.c.i",
        "s.d",
        "s.d.d",
        "s.d.e",
        "s.d.i",
        "s.d.o.f",
        "s.d.p",
        "s.d.r",
        "s.e",
        "s.e.d",
        "s.e.s",
        "s.e.u",
        "s.f",
        "s.f.d.p",
        "s.f.e",
        "s.f.p",
        "s.f.s",
        "s.f.t.s",
        "s.g",
        "s.g.c.e",
        "s.g.p",
        "s.i",
        "s.i.m.f",
        "s.i.p",
        "s.j.l",
        "s.j.t",
        "s.k.r.p",
        "s.l.c",
        "s.l.e",
        "s.l.i",
        "s.l.r",
        "s.m",
        "s.m.p",
        "s.m.u",
        "s.n",
        "s.n.c",
        "s.n.n.d",
        "s.o",
        "s.o.d",
        "s.o.p",
        "s.o.s",
        "s.o.t",
        "s.p",
        "s.p.a",
        "s.p.c",
        "s.p.d",
        "s.p.i.m.f",
        "s.p.m",
        "s.p.s.h",
        "s.r",
        "s.r.c",
        "s.r.f",
        "s.r.f.s",
        "s.s",
        "s.s.c",
        "s.s.g.p",
        "s.s.p",
        "s.s.t",
        "s.t.c.i",
        "s.t.l",
        "s.t.r",
        "s.th",
        "s.u.e",
        "s.u.i",
        "s.u.m",
        "s.v",
        "s.v.f",
        "s.v.p",
        "s.vanishes",
        "s.w.l.s.c",
        "sig.c",
        "sq.r.r",
        "st.REF",
        "st.n.t",
        "star.html",
        "systemw.r.t",
        "t.MATH",
        "t.b.b.s",
        "t.c",
        "t.d",
        "t.d.l.c",
        "t.d.l.c.group",
        "t.d.l.c.s.c",
        "t.d.l.c.s.c.completion",
        "t.d.l.c.s.c.group",
        "t.d.l.c.s.c.groups",
        "t.d.s",
        "t.e",
        "t.e.c",
        "t.e.r",
        "t.f",
        "t.f.d",
        "t.f.f",
        "t.f.p",
        "t.g",
        "t.i",
        "t.i.s",
        "t.l",
        "t.l.o.g",
        "t.m",
        "t.majorize",
        "t.o.g",
        "t.p",
        "t.p.d",
        "t.p.f",
        "t.p.m",
        "t.s.r",
        "t.t.t",
        "t.u",
        "t.u.b",
        "t.u.i",
        "t.u.p",
        "t.v.d",
        "t.v.i",
        "t.v.s",
        "tape.r.r",
        "timew.r.t",
        "tr.d",
        "translatedw.r.t",
        "u.a",
        "u.a.e",
        "u.a.p",
        "u.a.r",
        "u.a.u.d",
        "u.b",
        "u.c",
        "u.c.a.s",
        "u.c.c",
        "u.c.e",
        "u.c.i.p",
        "u.c.p",
        "u.c.s",
        "u.d",
        "u.d.s",
        "u.e",
        "u.e.i",
        "u.e.m",
        "u.e.p",
        "u.f.p",
        "u.g.g.r",
        "u.h.c",
        "u.h.s",
        "u.i",
        "u.i.b",
        "u.i.d",
        "u.i.n",
        "u.i.u",
        "u.l.c",
        "u.l.f",
        "u.l.g",
        "u.l.m",
        "u.l.p.c",
        "u.m",
        "u.n.d",
        "u.o.c",
        "u.p",
        "u.p.d",
        "u.p.e",
        "u.p.p",
        "u.r.e",
        "u.r.g",
        "u.r.i",
        "u.r.i.c.e",
        "u.r.p",
        "u.s.a",
        "u.s.b.v",
        "u.s.c",
        "u.s.c.d",
        "u.s.e",
        "u.t",
        "u.t.f",
        "u.t.s",
        "u.t.s.s",
        "u.u.t",
        "u.w",
        "u.w.p",
        "ub.v",
        "v.a",
        "v.b",
        "v.d.g",
        "v.g",
        "v.i",
        "v.i.a",
        "v.n",
        "v.p",
        "v.s",
        "v.v.m.f",
        "v.w.s",
        "viii.a",
        "viii.b",
        "viii.c",
        "viii.d",
        "w.a.i",
        "w.a.p",
        "w.a.r.g",
        "w.a.s",
        "w.b",
        "w.c.d.d",
        "w.c.g",
        "w.c.p",
        "w.c.r.s",
        "w.d",
        "w.d.d",
        "w.e",
        "w.e.c",
        "w.e.h.p",
        "w.e.p",
        "w.e.s",
        "w.e.u",
        "w.f.s",
        "w.g.s.c",
        "w.h",
        "w.h.e",
        "w.h.p",
        "w.hp",
        "w.i",
        "w.i.c.s",
        "w.i.s.s",
        "w.l.a.p",
        "w.l.g",
        "w.l.o",
        "w.l.p",
        "w.l.s.c",
        "w.m.p",
        "w.m.v",
        "w.n.a.s",
        "w.n.l.g",
        "w.o",
        "w.o.h.p",
        "w.o.l.g",
        "w.o.l.o.g",
        "w.o.p",
        "w.o.t",
        "w.ov.p",
        "w.p",
        "w.p.a",
        "w.p.a.l",
        "w.p.l",
        "w.p.p",
        "w.q.h",
        "w.q.o",
        "w.r",
        "w.r.g",
        "w.r.o",
        "w.r.o.g",
        "w.r.p",
        "w.r.s",
        "w.s",
        "w.s.c.o.b",
        "w.s.l.s.c",
        "w.t",
        "w.u.c",
        "w.u.g",
        "w.v.h.p",
        "wherem.d.f",
        "x.b",
        "x.c",
        "x.r",
        "z.c.q.v",
        "z.p.c",
        "z.u.e"
    ]
)


sent_tokenizer = PunktSentenceTokenizer()
sent_tokenizer._params.abbrev_types = MATH_ABBREVS

word_tokenizer = NLTKWordTokenizer()


def sentize_proof(line: str) -> List[str]:
    # if re.search(suspicious, line):
    #     continue
    text: str = line.strip()

    if "\t" in text:
        (prefix, text) = text.split("\t")
        prefix += "\t"
    else:
        (prefix, text) = ("", text)

    # sents is the list of sentences in this single proofs.
    sents: List[str] = list(sent_tokenizer.tokenize(text))

    # Loop throught the sentences, clean them slightly,
    # break them into words, and store them in sent_tokens.
    output_sents: List[str] = []
    for sent in sents:
        if sent[0] == "(":
            if sent[-1] == ")":
                interior = sent[1:-1]
                if inner_parens(interior):
                    sent = interior
            elif sent[-2:] == ").":
                interior = sent[1:-2]
                if inner_parens(interior):
                    sent = interior.strip() + " ."
            elif sent[-3:] == ") .":
                interior = sent[1:-3]
                if inner_parens(interior):
                    sent = interior.strip() + " ."

        # If we have multiple sentences inside parentheses
        # they will show up as (sent and sent)
        # This should fix that
        if sent:
            if sent[0] == "(":
                if sent.count("(") - 1 == sent.count(")"):
                    sent = sent[1:]
            elif sent[-1] == ")":
                if sent.count("(") + 1 == sent.count(")"):
                    sent = sent[:-1]

            words: List[str] = word_tokenizer.tokenize(sent)

            output_sents.append(prefix + " ".join(words))

    return output_sents


if __name__ == "__main__":
    nicer.make_nice()

    parser = argparse.ArgumentParser()
    # parser.add_argument(
    #     "-d", "--debug", help="Show tracing output", action="store_true"
    # )
    parser.add_argument(
        "-p", "--cores", help="Number of cores to use", type=int, default=8
    )

    parser.add_argument(
        "files", nargs="*", type=argparse.FileType("r"), default=[sys.stdin]
    )
    args = parser.parse_args()

    for fd in args.files:
        if args.cores > 1:
            with Pool(processes=args.cores) as p:
                # p.map(pf, tex_files, 1)
                for lines in p.imap(
                    sentize_proof,
                    fd.readlines(),
                    50,
                ):
                    for line in lines:
                        print(line)
        else:
            for proof in fd.readlines():
                for line in sentize_proof(proof):
                    print(line)
