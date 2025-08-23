
import requests
import pandas as pd

# 公式ページから取得した最新CSVのURL（例: 2025年8月時点のURL）
csv_url = "https://www.jpx.co.jp/markets/statistics-equities/misc/tvdivq00000030vg-att/data_j.csv"

# ダウンロード
res = requests.get(csv_url)
res.raise_for_status()
with open("jpx_listed.csv", "wb") as f:
    f.write(res.content)
print("jpx_listed.csv を保存しました。")

# 会社名と証券コードのみ抽出して新CSVに保存
df = pd.read_csv("jpx_listed.csv", encoding="shift_jis")

# 列名の自動判定
code_col = None
name_col = None
for col in df.columns:
    if "コード" in col or "証券コード" in col:
        code_col = col
    if "会社名" in col or "銘柄名" in col or "上場会社名" in col:
        name_col = col

if not code_col or not name_col:
    raise Exception(f"証券コード・会社名の列が見つかりません: {df.columns}")

out_df = df[[code_col, name_col]].copy()
out_df.columns = ["証券コード", "会社名"]
out_df.to_csv("jpx_company_code.csv", index=False, encoding="utf-8-sig")
print("jpx_company_code.csv を保存しました。")


# import requests
# from bs4 import BeautifulSoup

# # JPX公式の銘柄一覧ページ
# url = "https://www.jpx.co.jp/markets/statistics-equities/misc/01.html"

# # ページ取得
# res = requests.get(url)
# res.raise_for_status()
# soup = BeautifulSoup(res.content, "html.parser")


# # hrefに「.csv」が含まれるリンクを抽出
# csv_links = [a["href"] for a in soup.find_all("a", href=True) if ".csv" in a["href"].lower()]

# if not csv_links:
#     raise Exception("CSVリンクが見つかりませんでした")

# # 最初のCSVリンクを使う
# csv_link = csv_links[0]
# if not csv_link.startswith("http"):
#     csv_link = "https://www.jpx.co.jp" + csv_link

# print(f"ダウンロードURL: {csv_link}")

# # CSVダウンロード
# csv_res = requests.get(csv_link)
# csv_res.raise_for_status()
# with open("jpx_listed.csv", "wb") as f:
#     f.write(csv_res.content)

# print("jpx_listed.csv を保存しました。")