import requests
from bs4 import BeautifulSoup

# 目標網址
# 寶可夢列表（按全國圖鑑編號） - 神奇寶貝百科
url = "https://wiki.52poke.com/wiki/%E5%AE%9D%E5%8F%AF%E6%A2%A6%E5%88%97%E8%A1%A8%EF%BC%88%E6%8C%89%E5%85%A8%E5%9B%BD%E5%9B%BE%E9%89%B4%E7%BC%96%E5%8F%B7%EF%BC%89"

# 設置 headers 以模擬瀏覽器
headers = {
    "User-Agent": "XXXXXXXXXX", # 要修改為自己的 User-Agent
    "Accept-Language": "zh-TW,zh;q=0.9"
}

# 請求網頁內容
response = requests.get(url, headers=headers)
response.encoding = "utf-8"

# 解析網頁內容
soup = BeautifulSoup(response.text, "html.parser")

# 提取表格
rows = soup.select("table.roundy tbody tr")

# 建立 Pokedex
Pokedex = []

# 解析表格
for row in rows:
    cols = row.find_all("td")
    if len(cols) < 8:                                       # 跳過非數據行
        continue

    # 提取數據
    id = cols[0].text.strip()                               # 全國圖鑑編號
    name_cn = cols[3].text.strip()                          # 中文名字
    name_jp = cols[4].text.strip()                          # 日文名字
    name_en = cols[5].text.strip()                          # 英文名字
    type1 = cols[6].text.strip()                            # 屬性 1
    type2 = cols[7].text.strip() if len(cols) > 7 else ""   # 屬性 2

    # 過濾無效的屬性2
    if type2.startswith("{{") or type2.startswith("[["):
        type2 = ""

    # 判斷是否為地區型態
    def is_region_variant(name):
        return "的樣子" in name

    # 跳過地區型態的寶可夢
    if is_region_variant(name_cn):
        continue

    # 保存到 Pokedex
    Pokedex.append({
        "id": id,
        "name_cn": name_cn,
        "name_jp": name_jp,
        "name_en": name_en,
        "type1": type1,
        "type2": type2
    })

# 輸出结果
for pokemon in Pokedex:
    print(pokemon)

print("----------------------------------------------------------------------------------------")

# 保存為 csv
import csv
with open("Pokedex.csv", "w", newline="", encoding="utf-8-sig") as f:
    writer = csv.DictWriter(f, fieldnames=["id", "name_cn", "name_jp", "name_en", "type1", "type2"])
    writer.writeheader()
    writer.writerows(Pokedex)
print("已保存 Pokedex.csv")

# 保存為 json
import json
with open("Pokedex.json", "w", encoding="utf-8") as f:
    json.dump(Pokedex, f, ensure_ascii=False, indent=4)
print("已保存 Pokedex.json")