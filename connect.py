# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import json
import codecs

# import pandas as pd
# import numpy as np
##resp = requests.get("https://jwlin.github.io/py-scraping-analysis-book/ch1/connect.html")

########
# 資料順序跑掉ㄌ
#
#######
resp = requests.get("https://www.cwb.gov.tw/V7/forecast/week/week.htm")
resp.encoding = "utf-8"
soup = BeautifulSoup(resp.text, "html.parser")
# Get Table
table = soup.find("table")
print("table", table)
columns = [x.text for x in table.tr.find_all("th")]
print("columns", columns)
to_week = {}
for x in range(7):
    to_week["d" + str(x + 1)] = columns[x + 2]
print(json.dumps(to_week, ensure_ascii=False, encoding='UTF-8'))

ths = table.find_all("th")
print("ths", ths)
for tr in ths:
    for td in tr:
        if td.string != None:
            print(td.string)
# Get Table Height
height = len(table.findAll(lambda tag: tag.name == "tr" and len(tag.findAll("td")) >= 1))
print(height)
for row in table.find_all("tr"):
    print(len(row.find_all("td")))

tds = table.find_all("td")
i = 1
for td in tds:
    # for td in table:
    # if (td.string != None):
    print(str(i) + ":" + td.text.strip())
    i += 1

wtf = []
# Get Temp.
texts = soup.find_all(lambda tag: tag.name == "td" and tag.findAll("img"))
for x in texts:
    print(x.text.strip())
    # wtf.append({"temp": x.text.strip()})
print("x.length:" + str(len(texts)))
# Get Img.
imgs = [x.img for x in texts]
# print(imgs)
# imgs = soup.find_all(lambda tag: tag.name == "img" and tag.has_attr("src"))
srcs = [i.attrs["src"] for i in imgs]
print(srcs)
sources = [src.replace("../..", "https://www.cwb.gov.tw/V7") for src in srcs]
for x in sources:
    print(x)
    # wtf.append({"weather": x})
for x in range(len(texts)):  # 0-307
    www = {}
    www["temp"] = texts[x].text.strip()
    www["weather"] = sources[x]
    wtf.append(www)
print(wtf)
wtf2 = []
for x in range(len(texts) / 2):  # 0-153
    www2 = {}
    www2["白天"] = wtf[(x % 7) + 2 * (x / 7) * 7]
    www2["晚上"] = wtf[(x % 7) + (2 * (x / 7) + 1) * 7]
    wtf2.append(www2)
print(wtf2)
wtf3 = []
for x in range(len(texts) / 2):  # 0-153
    www3 = {}
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
a = []
b = {}
c = {}
d = {}
c["氣溫"] = "21-23"
c["天氣狀態"] = "img1"
d["氣溫"] = "22-26"
d["天氣狀態"] = "img2"
b["白天"] = c
b["晚上"] = d
a.append(
    {"date": "04/25",
     "weather": b
     })
info = {}
i = 0
for x in table.find_all("th"):  # 0-21
    if (x.string != None):
        print(x.string)
        info[x.string] = wtf4[i]
        i += 1

info_obj = json.dumps(info, ensure_ascii=False, encoding='UTF-8')
print(info_obj)

with codecs.open("info.json", "w", "utf-8") as f:
    # json.dump(info, f, ensure_ascii=False)
    f.write(info_obj)
    f.close()

print(1 / 7)
# with open('info.json', 'w') as f:
#     json.dump(info, f, ensure_ascii=False, encoding='UTF-8')
# print(info[0][u'\u57fa\u9686\u5e02'][0]["date"])

# df = pd.DataFrame(data = np.full((height,10), " ", dtype = "U"))
# print(df)

# columns = [x.text for x in table.tr.finAll("th")]
# columns = [x.replace("\xa0", " ") for x in columns]
# ulist = []
# trs = soup.find_all("th")
# for th in trs:
#     ui = []
#     # for td in th:
#     print(th.string)
#     ui.append(th.string)
#     # ulist.append(ui)
