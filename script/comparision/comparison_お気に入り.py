"""
緯度と経度が一致する場合、
一致した場所をマージし、ラベル付きの場所から削除するスクリプト
"""

import pandas as pd

# CSVファイルの読み込み
address_non_records_df = pd.read_csv(
    "C:\\Users\\14nn0\\works_new\\あおいホーム様\\script\\お気に入り(♡ピン)\\update_address_non_records.csv"
)
updated_with_date_filtered_df = pd.read_csv(
    "C:\\Users\\14nn0\\works_new\\あおいホーム様\\script\\ラベル\\updated_with_date_filtered.csv"
)


# 一致する緯度と経度を持つレコードをマージ（完全一致）
matches = pd.merge(address_non_records_df, updated_with_date_filtered_df, on=['Latitude', 'Longitude'], how='inner')

# マッチしたレコードがある場合、address_non_recordsから削除
if not matches.empty:
    for index, row in matches.iterrows():
        # address_non_recordsからマッチしたレコードを削除
        address_non_records_df.drop(index, inplace=True)
        
        # updated_with_date_filteredの対応するレコードのpin_noを4に更新
        updated_index = updated_with_date_filtered_df[(updated_with_date_filtered_df['Latitude'] == row['Latitude']) & (updated_with_date_filtered_df['Longitude'] == row['Longitude'])].index
        updated_with_date_filtered_df.loc[updated_index, 'pin_no'] = 4

# 結果を新しいCSVファイルに保存
address_non_records_df.to_csv('C:\\Users\\14nn0\\works_new\\あおいホーム様\\\script\\お気に入り(♡ピン)\\last.csv', index=False)
updated_with_date_filtered_df.to_csv('C:\\Users\\14nn0\\works_new\\あおいホーム様\\script\\ラベル\\last.csv', index=False)