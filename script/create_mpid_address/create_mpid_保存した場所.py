"""
mpid列に番号を採番するスクリプト
"""

import pandas as pd

# CSVファイルを読み込む
df = pd.read_csv('C:\\Users\\14nn0\\works_new\\あおいホーム様\\script\\保存した場所(星ピン)\\decoded_non_lat_lon.csv')

# pin_no列を追加し、3で埋める
df['pin_no'] = 14

# 'mpid'列に番号を採番する
df['mpid'] = range(7697, 7697 + len(df))

# 番号が採番されたCSVファイルを保存する
df.to_csv('C:\\Users\\14nn0\\works_new\\あおいホーム様\\script\\保存した場所(星ピン)\\update_address_records.csv', index=False)


