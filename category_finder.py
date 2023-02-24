#!/usr/bin/env python
import re
import os
import xml.etree.ElementTree as ET

""" An all around modular function to examine the Arxiv tagged topics of papers.
It has the potential to extract a lot of information about the proofs, like the 
individual categories of each paper, the overall categories, the categories by date,
and can easily be customized to do more. It runs with no arguments on the command line,
any changes must be made within the code. """



years = list(range(21)) + list(range(91, 100))
years = ["0" + str(x) if len(str(x)) == 1 else str(x) for x in years] # a list of all two-digit year codes, from 91 to 20

f = open("successful-proof-ids.txt", "r")
ids = f.readlines()
f.close()

ids = [s[:-1] for s in ids]         # remove \n characters
for s in range(len(ids)):
    ids[s] = re.sub(r"(([A-Za-z]|[-])+)([0-9]+)", "\\1/\\3", ids[s])   # add / in middle for changed formatting of certain IDs

tree = ET.parse("metha-metadata.xml")
root = tree.getroot()
# d = {"Hello":"World"}
d = {}
d2 = {"Math":0, "CS":0, "Phys":0, "Biology":0, "Systems": 0, "Econ": 0}         # a dictionary for counting the overall larger categories
d3 = {0: "Math", 1: "CS", 2: "Phys", 3: "Biology", 4: "Systems", 5: "Econ"}     # a dictionary for matching a number with the large categories
d4 = {"Math":0, "CS":1, "Phys":2, "Biology":3, "Systems": 4, "Econ": 5}         # # a dictionary for matching the large categories with a number
d5 = {}
types = {'math.CO': 'Math', 'math.NT': 'Math', 'hep-th': 'Phys', 'math.FA': 'Math', 'math.OA': 'Math', 'math.AC': 'Math',
 'math.AG': 'Math', 'math.GT': 'Math', 'math.QA': 'Math', 'math.RT': 'Math', 'nlin.CG': 'Systems', 'cs.DM': 'CS', 'cs.LO': 'CS',
  'math.DG': 'Math', 'math.RA': 'Math', 'math-ph': 'Math', 'math.MP': 'Math', 'math.SG': 'Math', 'math.GR': 'Math', 'math.AT': 'Math',
   'math.CT': 'Math', 'math.PR': 'Math', 'math.ST': 'Math', 'stat.TH': 'Math', 'math.CV': 'Math', 'math.OC': 'Math', 'math.CA': 'Math',
    'math.AP': 'Math', 'math.DS': 'Math', 'math.GM': 'Math', 'stat.CO': 'Math', 'quant-ph': 'Phys', 'math.KT': 'Math', 'cs.CG': 'CS',
     'cs.NE': 'CS', 'cs.GT': 'CS', 'cs.CC': 'CS', 'math.NA': 'Math', 'gr-qc': 'Phys', 'nlin.SI': 'Systems', 'cs.CR': 'CS', 'cs.DC': 'CS',
      'cs.SC': 'CS', 'math.MG': 'Math', 'cs.LG': 'CS', 'q-bio.GN': 'Biology', 'q-bio.QM': 'Biology', 'nlin.CD': 'Systems', 'cs.IR': 'CS',
       'cs.AI': 'CS', 'cs.DS': 'CS', 'math.LO': 'Math', 'math.GN': 'Math', 'math.SP': 'Math', 'cs.NI': 'CS', 'cs.CL': 'CS',
        'cond-mat.other': 'Phys', 'astro-ph': 'Phys', 'q-bio.SC': 'Biology', 'cs.PL': 'CS', 'nlin.PS': 'Math', 'cond-mat.stat-mech': 'Phys',
         'cs.DB': 'CS', 'adap-org': 'Systems', 'nlin.AO': 'Systems', 'q-bio': 'Biology', 'alg-geom': 'Math', 'q-alg': 'Math', 'chao-dyn': 'Systems',
          'cmp-lg': 'CS', 'cond-mat': 'Phys', 'cond-mat.str-el': 'Phys', 'cond-mat.dis-nn': 'Phys', 'cond-mat.soft': 'Phys',
           'cond-mat.mes-hall': 'Phys', 'q-bio.PE': 'Biology', 'physics.soc-ph': 'Phys', 'cs.CE': 'CS', 'cs.CV': 'CS', 'cs.NA': 'CS',
            'cs.AR': 'CS', 'cs.MA': 'CS', 'cs.SE': 'CS', 'cs.PF': 'CS', 'q-bio.BM': 'Biology', 'cs.GR': 'CS', 'physics.data-an': 'Phys',
             'cs.RO': 'CS', 'cs.CY': 'CS', 'cs.OH': 'CS', 'cs.DL': 'CS', 'cs.GL': 'CS', 'cs.MS': 'CS', 'cs.HC': 'CS', 'cs.MM': 'CS',
              'q-bio.MN': 'Biology', 'dg-ga': 'Math','funct-an': 'Math', 'hep-lat': 'Phys', 'hep-ph': 'Phys', 'physics.class-ph': 'Phys',
               'math.HO': 'Math', 'physics.chem-ph': 'Phys', 'physics.flu-dyn': 'Phys', 'physics.atom-ph': 'Phys', 'physics.comp-ph': 'Phys',
                'physics.geo-ph': 'Phys', 'physics.optics': 'Phys', 'stat.ML': 'Math', 'physics.plasm-ph': 'Phys', 'q-bio.TO': 'Biology',
                 'solv-int': 'Math', 'nucl-th': 'Phys', 'nucl-ex': 'Phys', 'patt-sol': 'Systems', 'physics.bio-ph': 'Phys', 'physics.gen-ph': 'Phys',
                  'physics.ed-ph': 'Phys', 'physics.acc-ph': 'Phys', 'q-bio.OT': 'Biology', 'q-bio.CB': 'Biology', 'q-bio.NC': 'Biology',
                   'stat.AP': 'Math', 'stat.ME': 'Math', 'cs.IT': 'CS', 'math.IT': 'Math', 'cond-mat.mtrl-sci': 'Phys', 'physics.ao-ph': 'Phys',
                    'physics.hist-ph': 'Phys', 'cond-mat.supr-con': 'Phys', 'cs.OS': 'CS', 'bayes-an': 'Phys', 'comp-gas': 'Phys',
                     'physics.space-ph': 'Phys', 'physics.ins-det': 'Phys', 'q-fin.PR': 'Econ', 'q-fin.CP': 'Econ', 'q-fin.ST': 'Econ',
                      'q-fin.RM': 'Econ', 'q-fin.GN': 'Econ', 'q-fin.PM': 'Econ', 'q-fin.TR': 'Econ', 'astro-ph.EP': 'Phys', 'cs.FL': 'CS',
                       'astro-ph.SR': 'Phys', 'astro-ph.HE': 'Phys', 'cond-mat.quant-gas': 'Phys', 'astro-ph.GA': 'Phys', 'astro-ph.CO': 'Phys',
                        'physics.atm-clus': 'Phys', 'stat.OT': 'Math', 'cs.SY': 'CS', 'physics.med-ph': 'Phys', 'cs.SI': 'CS', 'hep-ex': 'Phys',
                         'cs.ET': 'CS', 'astro-ph.IM': 'Phys', 'physics.pop-ph': 'Phys', 'cs.SD': 'CS', 'q-fin.MF': 'Econ', 'q-fin.EC': 'Econ',
                          'physics.app-ph': 'Phys', 'econ.EM': 'Econ', 'eess.SP': 'Systems', 'eess.AS': 'Systems', 'eess.IV': 'Systems',
                           'econ.TH': 'Systems', 'econ.GN': 'Econ', 'eess.SY': 'Systems'} # a dictionary containing all of the subtypes represented in the papers
yearCats = [[0,0,0,0,0,0] for l in years]        # a list of lists to track big categories for all years


# the which main categories correspond to which smaller categories
types = {'math.CO': r'Math', 'math.NT': r'Math', 'hep-th': r'Phys', 'math.FA': r'Math', 'math.OA': r'Math', 'math.AC': r'Math', 'math.AG': r'Math', 'math.GT': r'Math', 'math.QA': r'Math', 'math.RT': r'Math', 'nlin.CG': r'Systems', 'cs.DM': r'CS', 'cs.LO': r'CS', 'math.DG': r'Math', 'math.RA': r'Math', 'math-ph': r'Math', 'math.MP': r'Math', 'math.SG': r'Math', 'math.GR': r'Math', 'math.AT': r'Math', 'math.CT': r'Math', 'math.PR': r'Math', 'math.ST': r'Math', 'stat.TH': r'Math', 'math.CV': r'Math', 'math.OC': r'Math', 'math.CA': r'Math', 'math.AP': r'Math', 'math.DS': r'Math', 'math.GM': r'Math', 'stat.CO': r'Math', 'quant-ph': r'Phys', 'math.KT': r'Math', 'cs.CG': r'CS', 'cs.NE': r'CS', 'cs.GT': r'CS', 'cs.CC': r'CS', 'math.NA': r'Math', 'gr-qc': r'Phys', 'nlin.SI': r'Systems', 'cs.CR': r'CS', 'cs.DC': r'CS', 'cs.SC': r'CS', 'math.MG': r'Math', 'cs.LG': r'CS', 'q-bio.GN': r'Biology', 'q-bio.QM': r'Biology', 'nlin.CD': r'Systems', 'cs.IR': r'CS', 'cs.AI': r'CS', 'cs.DS': r'CS', 'math.LO': r'Math', 'math.GN': r'Math', 'math.SP': r'Math', 'cs.NI': r'CS', 'cs.CL': r'CS', 'cond-mat.other': r'Phys', 'astro-ph': r'Phys', 'q-bio.SC': r'Biology', 'cs.PL': r'CS', 'nlin.PS': r'Math', 'cond-mat.stat-mech': r'Phys', 'cs.DB': r'CS', 'adap-org': r'Systems', 'nlin.AO': r'Systems', 'q-bio': r'Biology', 'alg-geom': r'Math', 'q-alg': r'Math', 'chao-dyn': r'Systems', 'cmp-lg': r'CS', 'cond-mat': r'Phys', 'cond-mat.str-el': r'Phys', 'cond-mat.dis-nn': r'Phys', 'cond-mat.soft': r'Phys', 'cond-mat.mes-hall': r'Phys', 'q-bio.PE': r'Biology', 'physics.soc-ph': r'Phys', 'cs.CE': r'CS', 'cs.CV': r'CS', 'cs.NA': r'CS', 'cs.AR': r'CS', 'cs.MA': r'CS', 'cs.SE': r'CS', 'cs.PF': r'CS', 'q-bio.BM': r'Biology', 'cs.GR': r'CS', 'physics.data-an': r'Phys', 'cs.RO': r'CS', 'cs.CY': r'CS', 'cs.OH': r'CS', 'cs.DL': r'CS', 'cs.GL': r'CS', 'cs.MS': r'CS', 'cs.HC': r'CS', 'cs.MM': r'CS', 'q-bio.MN': r'Biology', 'dg-ga': r'Math','funct-an': r'Math', 'hep-lat': r'Phys', 'hep-ph': r'Phys', 'physics.class-ph': r'Phys', 'math.HO': r'Math', 'physics.chem-ph': r'Phys', 'physics.flu-dyn': r'Phys', 'physics.atom-ph': r'Phys', 'physics.comp-ph': r'Phys', 'physics.geo-ph': r'Phys', 'physics.optics': r'Phys', 'stat.ML': r'Math', 'physics.plasm-ph': r'Phys', 'q-bio.TO': r'Biology', 'solv-int': r'Math', 'nucl-th': r'Phys', 'nucl-ex': r'Phys', 'patt-sol': r'Systems', 'physics.bio-ph': r'Phys', 'physics.gen-ph': r'Phys', 'physics.ed-ph': r'Phys', 'physics.acc-ph': r'Phys', 'q-bio.OT': r'Biology', 'q-bio.CB': r'Biology', 'q-bio.NC': r'Biology', 'stat.AP': r'Math', 'stat.ME': r'Math', 'cs.IT': r'CS', 'math.IT': r'Math', 'cond-mat.mtrl-sci': r'Phys', 'physics.ao-ph': r'Phys', 'physics.hist-ph': r'Phys', 'cond-mat.supr-con': r'Phys', 'cs.OS': r'CS', 'bayes-an': r'Phys', 'comp-gas': r'Phys', 'physics.space-ph': r'Phys', 'physics.ins-det': r'Phys', 'q-fin.PR': r'Econ', 'q-fin.CP': r'Econ', 'q-fin.ST': r'Econ', 'q-fin.RM': r'Econ', 'q-fin.GN': r'Econ', 'q-fin.PM': r'Econ', 'q-fin.TR': r'Econ', 'astro-ph.EP': r'Phys', 'cs.FL': r'CS', 'astro-ph.SR': r'Phys', 'astro-ph.HE': r'Phys', 'cond-mat.quant-gas': r'Phys', 'astro-ph.GA': r'Phys', 'astro-ph.CO': r'Phys', 'physics.atm-clus': r'Phys', 'stat.OT': r'Math', 'cs.SY': r'CS', 'physics.med-ph': r'Phys', 'cs.SI': r'CS', 'hep-ex': r'Phys', 'cs.ET': r'CS', 'astro-ph.IM': r'Phys', 'physics.pop-ph': r'Phys', 'cs.SD': r'CS', 'q-fin.MF': r'Econ', 'q-fin.EC': r'Econ', 'physics.app-ph': r'Phys', 'econ.EM': r'Econ', 'eess.SP': r'Systems', 'eess.AS': r'Systems', 'eess.IV': r'Systems', 'econ.TH': r'Systems', 'econ.GN': r'Econ', 'eess.SY': r'Systems'}
# Math: "math.CO", "math.NT", "math.FA", "Math.OA", "math.AC", "math.AG", "math.GT", "math.QA", "math.RT", "nlin.CG", "math.DG", "math.RA", "math-ph", "math.MP", "math.SG", "math.GR", 
# CS: "cs.DM", "cs.LO", 
# Phys: "hep-th", 
count = 0
allIds = []
ids = set(ids)          # ensure faster lookup
for arxiv in tree.findall(".//{http://arxiv.org/OAI/arXiv/}arXiv"):         # iterate through the tree
    arxivId = arxiv.find("{http://arxiv.org/OAI/arXiv/}id").text            # extract the proof ID
    if arxivId in ids:                                                      # ensure that the paper is actually a valid english one containing a nonempty proof
#         if "." in arxivId:
#             yr = arxivId[0:2]
#         else:q
#             yr = arxivId[arxivId.index("/")+1:arxivId.index("/")+3]
        if "." in arxivId:
            date = arxivId[0:4]
        else:
            date = arxivId[arxivId.index("/")+1:arxivId.index("/")+5]
        categories = arxiv.find("{http://arxiv.org/OAI/arXiv/}categories").text  # find the proof's categories
        cats = categories.split(" ")
        print(f"{arxivId}\t{cats}")
        # if "math.CO" in cats:   # code to extract all proof IDs in the math.CO category. There currently is no supported way to use this list
        #     arxid = re.sub(r"(([A-Za-z]|[-])+)\/([0-9]+)", "\\1\\3", arxivId)
        #     proofs =  os.listdir(f'./texes/{date}/{arxid}/')
        #     for x in proofs:
        #         if x[-3:] == "tex":
        #             print(f"./texes/{date}/{arxid}/{x}")
                
""" the commented code below contains other ways to use the above code. Uncommenting blocks can allow counting by major or minor categories, or by year
 it contains different methods of dealing with ties, papers with multiple categories, and other counting edge cases """


#         bigCats = set()
# # #         # largeCats = [0]*6
#         for cat in cats:
# # #             if cat in d:
# # #                 d[cat] += 1
# # #             else:
# # #                 d[cat] = 1
#             bigCats.add(types[cat])
#         for x in bigCats:
#             yearCats[years.index(yr)][d4[x]] += 1
# for x in years:
#     d5[x] = yearCats[years.index(x)]
# print(d5)
# print(yearCats)
# print(years)
#             d2[x] += 1
#         #     largeCats[d4[types[cat]]] += 1
#         # for x in range(6):
#         #     if largeCats[x] == max(largeCats):
#         #         d2[d3[x]] += 1
#         # largeCats[d4[types[cat]]] += 1
#         # d2[d3[largeCats.index(max(largeCats))]] += 1
#         # if largeCats.count(max(largeCats)) > 1:
#         #     d2["Ties"] += 1
#         

#         count += 1
# d["total papers"] = count
# print(d)
# print("\n")
# print(d2)
# print(d.keys())


    # print(arxiv.find("{http://arxiv.org/OAI/arXiv/}id").text)
    # if count > 100:
    #     break
    # print(arxiv.find("{http://arxiv.org/OAI/arXiv/}categories").text)
    # count += 1

