import pandas as pd
import numpy as np

# 既存のCSVファイルのパス
existing_csv_path = 'C:\\Users\\14nn0\\works_new\\あおいホーム様\\script\\ラベル\\final_of_last.csv'

# CSVファイルの読み込み
df = pd.read_csv(existing_csv_path, encoding="utf-8-sig")

# 新しいDataFrameの作成（必要な列名を指定）
new_df = pd.DataFrame(
    {
        "mpid": df["mpid"],
        "cid": "651",
        "lat": df["Latitude"],
        "lng": df["Longitude"],
        # "postno": df["postno"],
        "postno": "",
        # "addr": df["addr"],
        "addr": "",
        "istoday": 1,
        "rmflg": 0,
        "rmdt": "",
        "crdt": "2024-02-27 00:00:00",
        "updt": "2024-02-27 00:00:00",
        "bid": 1,
    }
)

# 新しいCSVファイルへの出力パス
# ラベル付きの場所用
new_csv_path = 'C:\\Users\\14nn0\\works_new\\あおいホーム様\\script\\ラベル\\t-mappin.csv'

# 新しいCSVファイルにデータフレームを出力
new_df.to_csv(new_csv_path, index=False, encoding="utf-8-sig")

print(f"新しいCSVファイルが作成されました: {new_csv_path}")
