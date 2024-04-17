"""
ラベル付きの場所データを処理して、データを整形するスクリプト

※data.jsonは3支店分のデータをまとめてあるJSONファイル（下関、北区、南区）
"""

import json
import pandas as pd
import numpy as np
import re
from dateutil import parser
from datetime import datetime

# JSONファイルのパス
json_file_path = (
    "C:\\Users\\14nn0\\works_new\\あおいホーム様\\script\\移行対象ファイル\\ラベル.json"
)
# 最終的なCSVファイルのパス
final_csv_path = "C:\\Users\\14nn0\\works_new\\あおいホーム様\\script\\ラベル\\updated_with_date_filtered.csv"


# JSONファイルからPandas DataFrameに変換する関数
def json_to_dataframe(json_path):
    with open(json_path, "r", encoding="utf-8") as file:
        json_data = json.load(file)
    data = [
        {
            "Type": feature["type"],
            "Latitude": feature["geometry"]["coordinates"][1],
            "Longitude": feature["geometry"]["coordinates"][0],
            "Name": feature["properties"]["name"],
        }
        for feature in json_data["features"]
    ]
    return pd.DataFrame(data)


# 年が含まれていない日付にデフォルトの年を追加する関数
def format_date_with_default_year(date_str, default_year=2023):
    try:
        # 日付を解析する
        dt = parser.parse(date_str)

        # 年が明示されていない場合、デフォルトの年を使用
        if dt.year == datetime.now().year:
            dt = dt.replace(year=default_year)

        # yyyy/mm/dd 形式にフォーマットする
        return dt.strftime("%Y/%m/%d")
    except ValueError:
        # 日付として解析できない場合は元の文字列を返す
        return date_str


# MM/DD形式の日付を識別し、23/MM/DD形式に置換する正規表現パターン
mm_dd_pattern = re.compile(r"\b(\d{1,2})/(\d{1,2})\b")


def replace_mm_dd_with_year(name):
    # MM/DD形式の日付を23/MM/DD形式に置換する関数
    def replace_match(match):
        # MM/DD形式の日付を23/MM/DD形式に置換
        return f"23/{match.group(1)}/{match.group(2)}"

    # 'YY/MM/DD' 形式を除外するため、先にチェック
    if not re.search(r"\d{2,4}/\d{1,2}/\d{1,2}", name):
        # MM/DD形式を検出し、23/MM/DD形式に置換
        return mm_dd_pattern.sub(replace_match, name)
    return name


# YYYY/MM/DD、YY/MM/DD、YYMMDD 形式の日付を識別し、YYYY/MM/DD形式に変換する関数
def extract_and_format_date(name):
    # YYYY/MM/DD 形式を直接検出
    yyyy_mm_dd_pattern = re.compile(r"\b(\d{4})/(\d{1,2})/(\d{1,2})\b")
    # YY/MM/DD 形式を検出
    yy_mm_dd_pattern = re.compile(r"\b(\d{2})/(\d{1,2})/(\d{1,2})\b")
    # YYMMDD 形式（スペースなし）を検出
    yymmdd_pattern = re.compile(r"(\d{2})(\d{2})(\d{2})")

    match = yyyy_mm_dd_pattern.search(name) or yy_mm_dd_pattern.search(name)
    if not match:
        match = yymmdd_pattern.search(name)
        if match:
            year, month, day = match.groups()
            year = f"20{year}"
    else:
        year, month, day = match.groups()
        if len(year) == 2:
            year = f"20{year}"

    if match:
        month = month.zfill(2)
        day = day.zfill(2)
        return f"{year}/{month}/{day}"
    return ""


# YYYY/MM/DD形式の日付を識別する正規表現パターン
date_pattern = re.compile(r"\b(\d{4})/(\d{1,2})/(\d{1,2})\b")


# 日付を抽出し、YYYY/MM/DD形式に変換する関数
def extract_date_if_missing(row):
    # Date列が空の場合のみ処理を行う
    if pd.isna(row["Date"]) or row["Date"] == "":
        match = date_pattern.search(row["Name"])
        if match:
            year, month, day = match.groups()
            # YYYY/MM/DD形式で返す
            return f"{year}/{month.zfill(2)}/{day.zfill(2)}"
    return row["Date"]


def extract_and_format_date_correctly(row):
    # YY/MM/DD 形式の日付を検出（スペースで区切られていない場合や、前に文字列がある場合も含む）
    yy_mm_dd_pattern = re.compile(r"(\d{2})/(\d{1,2})/(\d{1,2})")

    name = row["Name"]
    # Date列が空か確認
    if pd.isna(row["Date"]) or row["Date"] == "":
        match = yy_mm_dd_pattern.search(name)
        if match:
            year, month, day = match.groups()[:3]  # 最初の3つのグループが年、月、日
            # 年が2桁の場合、2000を加算して4桁の年にする
            year = f"20{year}"
            # 月と日を2桁にフォーマット
            month = month.zfill(2)
            day = day.zfill(2)
            # 正しい日付形式で返す
            formatted_date = f"{year}/{month}/{day}"
            return formatted_date
    return row["Date"]


# 処理の実行
df = json_to_dataframe(json_file_path)
# 'Name'列の日付の形式を変更
df["Name"] = df["Name"].apply(format_date_with_default_year)

# 'Name'列の各レコードに対して置換処理を適用
df["Name"] = df["Name"].apply(replace_mm_dd_with_year)

# 他の条件に基づいてピンNoを割り当てる処理
conditions = [
    df["Name"].str.contains("もうすぐ完成"),
    df["Name"].str.contains("棟中") & df["Name"].str.contains("契約"),
    df["Name"].str.contains("もうすぐ"),
    df["Name"].str.contains("タイミングIK"),
    df["Name"].str.contains("タイミング"),
    df["Name"].str.contains("不在熱い"),
    df["Name"].str.contains("ik|IK|iK|Ik|ｉｋ|ＩＫ|Ｉｋ|ｉＫ"),
    df["Name"].str.contains("済み|設置済み|設置済"),
    df["Name"].str.contains("再訪不可|危険"),
    df["Name"].str.contains("不在") & ~df["Name"].str.contains("不在熱い"),
    df["Name"].str.contains("浮"),
    df["Name"].str.contains("顧客"),
    df["Name"].str.contains("商談外し|APキャン|アポキャン"),
    df["Name"].str.contains("アポ|AP"),
    df["Name"].str.contains(r"\b\d{2,4}/\d{1,2}/\d{1,2}\b$"),
    df["Name"].str.contains(r"\d{2}/\d{1,2}/\d{1,2}.*(建設中|土間|棟)"),
    df["Name"].str.contains(r"\d{2}/\d{1,2}/\d{1,2}"),  # yyyy/mm/dd 形式の日付を検出
]

choices = [13, 12, 12, 1, 1, 7, 5, 16, 6, 2, 9, 8, 10, 4, 13, 13, 13]  # 各条件に対応するピンNo

# 他の条件に基づいてピンNoを割り当てる処理2
# conditions = [
#     df["Name"].str.contains("再訪不可|危険"),
#     df["Name"].str.contains("もうすぐ"),
#     df["Name"].str.contains("不在熱|タイミングIK"),
#     df["Name"].str.contains("不在") & ~df["Name"].str.contains("不在熱"),
#     df["Name"].str.contains("タイミング"),
#     df["Name"].str.contains("済|済み"),
#     df["Name"].str.contains("ik|IK|iK|Ik|ｉｋ|ＩＫ|Ｉｋ|ｉＫ"),
#     df["Name"].str.contains(r"\b\d{2,4}/\d{1,2}/\d{1,2}\b$"),
#     df["Name"].str.contains(r"\d{2}/\d{1,2}/\d{1,2}.*(建設中|土間|棟)"),
#     df["Name"].str.contains(r"\d{2}/\d{1,2}/\d{1,2}"),  # yyyy/mm/dd 形式の日付を検出
# ]

# choices = [6, 12, 7, 2, 1, 16, 5, 13, 13, 17]  # 各条件に対応するピンNo

# 他の条件に基づいてピンNoを割り当てる処理1
# conditions = [
#     df['Name'].str.contains('再訪不可|危険'),
#     df['Name'].str.contains('もうすぐ'),
#     df['Name'].str.contains('不在熱|タイミングIK'),
#     df['Name'].str.contains('不在') & ~df['Name'].str.contains('不在熱'),
#     df['Name'].str.contains('タイミング'),
#     df['Name'].str.contains('済|済み'),
#     df['Name'].str.contains('ik|IK|iK|Ik|ｉｋ|ＩＫ|Ｉｋ|ｉＫ'),
#     df['Name'].str.contains(r'\d{2}/\d{1,2}/\d{1,2}')  # yyyy/mm/dd 形式の日付を検出
# ]

# choices = [6, 12, 7, 2, 1, 16, 5, 13]  # 各条件に対応するピンNo

# np.selectを使って条件に基づいてピンNoを更新
df["pin_no"] = np.select(conditions, choices, default=17)

# 各ピンNoごとの数を集計して表示
pin_counts = df["pin_no"].value_counts().sort_index()
total = pin_counts.sum()
print(pin_counts)
print(f"合計: {total}")

# 'Date'列を追加し、'Name'列から日付を抽出してフォーマット
df["Date"] = df["Name"].apply(extract_and_format_date)

# 'mpid'列を追加し、1から始まる連番を割り振る
df["mpid"] = range(1, len(df) + 1)

# 'Date'列に対して条件に基づいた処理を適用
df["Date"] = df.apply(extract_date_if_missing, axis=1)

# DataFrame全体に適用
df["Date"] = df.apply(extract_and_format_date_correctly, axis=1)

# 'mpid'が7以外かつ'Date'が空のレコードをフィルタリング
filtered_df = df[(df["pin_no"] != 16) & (df["Date"].isna() | (df["Date"] == ""))]

# フィルタリングされたレコードの表示
print(filtered_df)

# 必要に応じてフィルタリングされたレコードからピンNoが-1のレコードを削除して、新しいCSVファイルに出力
filtered_df = filtered_df[filtered_df["pin_no"] != -1]
filtered_df.to_csv(
    "C:\\Users\\14nn0\\works_new\\あおいホーム様\\支店別フォーマットデータ\\3支店データ\\filtered.csv",
    index=False,
    encoding="utf-8-sig",
)

# 'pin_no'が13のレコードをCSVに出力
df[df["pin_no"] == 13].to_csv(
    "C:\\Users\\14nn0\\works_new\\あおいホーム様\\支店別フォーマットデータ\\3支店データ\\pin_no_13.csv",
    index=False,
    encoding="utf-8-sig",
)

# 'pin_no'が17のレコードをCSVに出力
df[df["pin_no"] == 17].to_csv(
    "C:\\Users\\14nn0\\works_new\\あおいホーム様\\支店別フォーマットデータ\\3支店データ\\pin_no_17.csv",
    index=False,
    encoding="utf-8-sig",
)

# 最終的なCSVファイルにデータフレームを出力
df.to_csv(final_csv_path, index=False, encoding="utf-8-sig")
