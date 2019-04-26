# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import json
import codecs


# Get Webpage
resp = requests.get("https://www.cwb.gov.tw/V7/forecast/week/week.htm")

# Encode Webpage Into UTF-8
resp.encoding = "utf-8"

# Parse HTML With BeautifulSoup
soup = BeautifulSoup(resp.text, "html.parser")

# Get Table In Webpage
table = soup.find("table")
print("table", table)

# Get The First Row In Table & Get All TableHeader
columns = [x.text for x in table.tr.find_all("th")]
print("columns", columns)

# Reserve Date In The Last Step & Save In A Dict.
to_week = {}
for x in range(7):
    to_week["d" + str(x + 1)] = columns[x + 2]
print(json.dumps(to_week, ensure_ascii=False, encoding='UTF-8'))

# # Get all "td" in every "th"
# ths = table.find_all("th")
# print("ths", ths)
# for tr in ths:
#     for td in tr:
#         if td.string != None:
#             print(td.string)
#
# # Get Table Height
# height = len(table.findAll(lambda tag: tag.name == "tr" and len(tag.findAll("td")) >= 1))
# print(height)
#
# # Get The Width Of Each Row
# for row in table.find_all("tr"):
#     print(len(row.find_all("td")))
#
# # Get the text in every "td" in table
# tds = table.find_all("td")
# i = 1
# for td in tds:
#     # for td in table:
#     # if (td.string != None):
#     print(str(i) + ":" + td.text.strip())
#     i += 1

# Get Temp.
texts = soup.find_all(lambda tag: tag.name == "td" and tag.findAll("img"))
for x in texts:
    print(x.text.strip())
print("x.length:" + str(len(texts)))

# Get Img.
imgs = [x.img for x in texts]
srcs = [i.attrs["src"] for i in imgs]
print(srcs)
sources = [src.replace("../..", "https://www.cwb.gov.tw/V7") for src in srcs]
for x in sources:
    print(x)

# Get Img. Title
imgs = [x.img for x in texts]
srcs = [i.attrs["title"] for i in imgs]
for x in srcs:
    print(x)


# Package Info. into dict. or list

# Every Half-Day Weather in wtf[]
wtf = []
for x in range(len(texts)):  # 0-307
    www = {}
    www["溫度"] = texts[x].text.strip()
    www["天氣狀態"] = srcs[x]
    wtf.append(www)
print(wtf)

# Every Day Weather in wtf2[]
wtf2 = []
for x in range(len(texts) / 2):  # 0-153
    www2 = {}

    # Map Weather Info. by Formula
    www2["白天"] = wtf[(x % 7) + 2 * (x / 7) * 7]
    www2["晚上"] = wtf[(x % 7) + (2 * (x / 7) + 1) * 7]
    wtf2.append(www2)
print(wtf2)

# Every Day Weather with Date in wtf3[]
wtf3 = []
for x in range(len(texts) / 2):  # 0-153
    www3 = {}

    # Map the Date with Daily-Changed Dict.
    if x % 7 == 0:
        www3["日期"] = to_week["d1"]
    elif x % 7 == 1:
        www3["日期"] = to_week["d2"]
    elif x % 7 == 2:
        www3["日期"] = to_week["d3"]
    elif x % 7 == 3:
        www3["日期"] = to_week["d4"]
    elif x % 7 == 4:
        www3["日期"] = to_week["d5"]
    elif x % 7 == 5:
        www3["日期"] = to_week["d6"]
    else:
        www3["日期"] = to_week["d7"]
    www3["天氣"] = wtf2[x]
    wtf3.append(www3)
print(wtf3)

# Every Day Weather with Date & Package for the City in wtf4[]
wtf4 = []
for x in range(len(texts) / 14):  # 0-21
    www4 = []
    www4.append(wtf3[7 * x])
    www4.append(wtf3[7 * x + 1])
    www4.append(wtf3[7 * x + 2])
    www4.append(wtf3[7 * x + 3])
    www4.append(wtf3[7 * x + 4])
    www4.append(wtf3[7 * x + 5])
    www4.append(wtf3[7 * x + 6])
    wtf4.append(www4)
print(wtf4)

# Map City Name to its Info. List
info = {}
i = 0
for x in table.find_all("th"):  # 0-21
    if (x.string != None):
        print(x.string)
        info[x.string] = wtf4[i]
        i += 1

# Write Dict. into JSON & Open File with Codecs Package to Avoid 中文亂碼
info_obj = json.dumps(info, ensure_ascii=False, encoding='UTF-8')
print(info_obj)
with codecs.open("weather_info.json", "w", "utf-8") as f:
    f.write(info_obj)
    f.close()

