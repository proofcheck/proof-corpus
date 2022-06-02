#!/usr/bin/env python
import re

# import xml.etree.ElementTree as ET
# tree = ET.parse("metha-metadata.xml")
# root = tree.getroot()
# # d = {"Hello":"World"}
# d = {}
# count = 0
# for arxiv in tree.findall(".//{http://arxiv.org/OAI/arXiv/}arXiv"):
#     print(arxiv.find("{http://arxiv.org/OAI/arXiv/}id").text)
#     # categories = arxiv.find("{http://arxiv.org/OAI/arXiv/}categories").text
#     # cats = categories.split(" ")
#     # for cat in cats:
#     #     if cat in d:
#     #         d[cat] += 1
#     #     else:
#     #         d[cat] = 1
#     count += 1
# d["total papers"] = count
# print(d)

f = open("successful-proof-ids", "r")
ids = f.readlines()
f.close()
ids = [s[:-1] for s in ids]
for s in ids:
    s = re.sub(r"([A-Za-z-]+)([0-9]+)", "\\1" + "hi" + "\\2", s)
print(ids[0:100])
    # print(arxiv.find("{http://arxiv.org/OAI/arXiv/}id").text)
    # if count > 100:
    #     break
    # print(arxiv.find("{http://arxiv.org/OAI/arXiv/}categories").text)
    # count += 1