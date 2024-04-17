import pandas as pd

# 既存のCSVからDataFrameを読み込む
df = pd.read_csv(
    "C:\\Users\\14nn0\\works_new\\あおいホーム様\\script\\お気に入り(♡ピン)\\last.csv"
)

# 骨組みは"mpid","csid","csid_org","nm","unm_kana","telno","room","memo","photo_house","status","cs_uid","istoday","power_company","power_rcpno","house_age","denkidai","gusdai","touyudai","family_struct","family_income","crdt","updt"

# 新しいDataFrameの骨組みを作成
new_df = pd.DataFrame(
    columns=[
        "mpid",
        "csid",
        "csid_org",
        "nm",
        "unm_kana",
        "birthdt",
        "telno",
        "telno2",
        "room",
        "memo",
        "photo_house",
        "status",
        "cs_uid",
        "istoday",
        "power_company",
        "power_rcpno",
        "house_age",
        "denkidai",
        "gusdai",
        "touyudai",
        "family_struct",
        "family_income",
        "crdt",
        "updt",
    ]
)

# 必要なデータを新しいDataFrameにコピー
new_df["mpid"] = df["mpid"]
new_df["csid"] = "1"
new_df["csid_org"] = df["mpid"]
new_df["birthdt"] = "NULL"
new_df["cs_uid"] = "2"
new_df["status"] = "0"
new_df["istoday"] = "0"
new_df["crdt"] = "2024-02-27 00:00:00"
new_df["updt"] = "2024-02-27 00:00:00"

# 残りの列は空（NaN）でOKとのことなので、既に新しいDataFrameを作成する際に空で初期化されています。

# 新しいCSVファイルとして保存
# ラベル付きの場所用
new_df.to_csv(
    "C:\\Users\\14nn0\\works_new\\あおいホーム様\\script\\お気に入り(♡ピン)\\t-mappin-customer.csv",
    index=False
)

# お気に入りの場所用
# new_df.to_csv(
#     "C:\\Users\\14nn0\\works_new\\あおいホーム様\\支店別フォーマットデータ\\3支店データ\\お気に入りの場所\\t-mappin-customer.csv",
#     index=False,
# )

print(f"新しいCSVファイルが作成されました: t-customer.csv")
