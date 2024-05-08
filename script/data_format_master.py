"""
ラベル付きの場所データを処理して、データを整形するスクリプト

※data.jsonは3支店分のデータをまとめてあるJSONファイル（下関、北区、南区）
"""

import json
import pandas as pd
import numpy as np
import re

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


# YYYY/MM/DD、YY/MM/DD、YYMMDD 形式の日付を識別し、YYYY/MM/DD形式に変換する関数
def extract_and_format_date(name):
    # YYYY/MM/DD 形式を直接検出
    yyyy_mm_dd_pattern = re.compile(r"\b(\d{4})/(\d{1,2})/(\d{1,2})\b")
    # YY/MM/DD 形式を検出
    yy_mm_dd_pattern = re.compile(r"\b(\d{2})/(\d{1,2})/(\d{1,2})\b")
    # YYMMDD 形式（スペースなし）を検出
    yymmdd_pattern = re.compile(r"(\d{2})(\d{2})(\d{2})")

    match = yyyy_mm_dd_pattern.search(name)
    if match:
        year, month, day = match.groups()
    else:
        match = yy_mm_dd_pattern.search(name)
        if match:
            year, month, day = match.groups()
            # 年を2000年代として解釈
            year = f"20{year}"
            # 日付フォーマットの誤解釈を防ぐための確認
            if int(month) > 12:
                month, day = day, month  # 月と日を交換

    if not match:
        match = yymmdd_pattern.search(name)
        if match:
            year, month, day = match.groups()
            year = f"20{year}"

    if match:
        # 月と日を2桁に整形
        month = month.zfill(2)
        day = day.zfill(2)
        return f"{year}/{month}/{day}"
    return name  # 変換できない場合は元の文字列を返す


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

def format_date_in_text(text):
    # YYYY/MM/DD や YY/MM/DD 形式の日付を識別する正規表現
    date_pattern = re.compile(r'(\d{2,4}/\d{1,2}/\d{1,2})')

    # 日付の前後にスペースを挿入
    formatted_text = re.sub(date_pattern, r' \1 ', text)

    # 連続するスペースを一つに縮小
    formatted_text = re.sub(r'\s+', ' ', formatted_text).strip()

    return formatted_text


# 処理の実行
df = json_to_dataframe(json_file_path)

# 'Name_Copy'列を追加し、'Name'列の値をコピー
df["Name_Copy"] = df["Name"]

df["Name_Copy"] = df["Name_Copy"].apply(format_date_in_text)

# 他の条件に基づいてピンNoを割り当てる処理
conditions = [
    df["Name_Copy"].str.contains("もうすぐ完成"),
    df["Name_Copy"].str.contains("棟中|棟契約|棟成約"),
    df["Name_Copy"].str.contains("もうすぐ"),
    df["Name_Copy"].str.contains("タイミングIK"),
    df["Name_Copy"].str.contains("タイミング"),
    df["Name_Copy"].str.contains("不在熱い"),
    df["Name_Copy"].str.contains("ik|IK|iK|Ik|ｉｋ|ＩＫ|Ｉｋ|ｉＫ"),
    df["Name_Copy"].str.contains("済み|設置済み|設置済|済"),
    df["Name_Copy"].str.contains("再訪不可|危険"),
    df["Name_Copy"].str.contains("不在") & ~df["Name_Copy"].str.contains("不在熱い"),
    df["Name_Copy"].str.contains("浮"),
    df["Name_Copy"].str.contains("顧客"),
    df["Name_Copy"].str.contains("商談外し|APキャン|アポキャン"),
    df["Name_Copy"].str.contains("アポ|AP"),
    df["Name_Copy"].str.contains("断"),
    df["Name_Copy"].str.contains(r"\b\d{2,4}/\d{1,2}/\d{1,2}\b$"),
    df["Name_Copy"].str.contains(r"\d{2}/\d{1,2}/\d{1,2}.*(建設中|土間)"),
]

choices = [13, 12, 12, 1, 1, 7, 5, 16, 6, 2, 9, 8, 10, 4, 3, 13, 13]  # 各条件に対応するピンNo

# np.selectを使って条件に基づいてピンNoを更新
df["pin_no"] = np.select(conditions, choices, default=17)

# 各ピンNoごとの数を集計して表示
pin_counts = df["pin_no"].value_counts().sort_index()
total = pin_counts.sum()
print(pin_counts)
print(f"合計: {total}")

# 'Date'列を追加し、'Name'列から日付を抽出してフォーマット
df["Date"] = df["Name_Copy"].apply(extract_and_format_date)

# 'mpid'列を追加し、1から始まる連番を割り振る
df["mpid"] = range(1, len(df) + 1)

# 'Date'列に対して条件に基づいた処理を適用
df["Date"] = df.apply(extract_date_if_missing, axis=1)

# DataFrame全体に適用
df["Date"] = df.apply(extract_and_format_date_correctly, axis=1)

# 最終的なCSVファイルにデータフレームを出力
df.to_csv(final_csv_path, index=False, encoding="utf-8-sig")
