import pandas as pd

# 既存のCSVからDataFrameを読み込む
df = pd.read_csv(
    'C:\\Users\\14nn0\\works_new\\あおいホーム様\\script\\行ってみたい(緑ピン)\\last.csv'
)

# 新しいDataFrameの骨組みを作成
new_df = pd.DataFrame(
    columns=[
        "mpid",
        "vidt",
        "vitm",
        "csid",
        "cid",
        "uid",
        "pno",
        "lbnm",
        "memo",
        "is_revisit",
        "is_nextapp",
        "appdt",
        "apptm",
        "appuid",
        "svydt",
        "svytm",
        "svyuid",
        "oppdt",
        "opptm",
        "pnm",
        "style",
        "result",
        "rmflg",
        "crdt",
        "updt",
    ]
)

# 必要なデータを新しいDataFrameにコピー
new_df["mpid"] = df["mpid"]
new_df["uid"] = "2"
new_df["memo"] = df["Name"]
new_df["pno"] = df["pin_no"]
new_df["appdt"] = "2024/02/27"
new_df["apptm"] = "00:00:00"
new_df["svydt"] = "2024/02/27"
new_df["svytm"] = "00:00:00"
new_df["oppdt"] = df["Date"]
new_df["cid"] = "651"
new_df["csid"] = "1"
new_df["rmflg"] = "0"
new_df["crdt"] = "2024-02-27 00:00:00"
new_df["updt"] = "2024-02-27 00:00:00"

# 残りの列は空（NaN）でOKとのことなので、既に新しいDataFrameを作成する際に空で初期化されています。

# new_df['oppdt'] がNanの場合はNULLに変換
new_df["oppdt"] = new_df["oppdt"].fillna("NULL")

# 新しいCSVファイルとして保存
new_df.to_csv(
    "C:\\Users\\14nn0\\works_new\\あおいホーム様\\script\\行ってみたい(緑ピン)\\t-visit.csv",
    index=False,
)
