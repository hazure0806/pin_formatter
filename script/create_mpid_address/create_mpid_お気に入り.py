"""
mpid列に番号を採番するスクリプト
"""

import pandas as pd

# CSVファイルを読み込む
df = pd.read_csv('C:\\Users\\14nn0\\works_new\\あおいホーム様\\script\\お気に入り(♡ピン)\\address_records.csv')


# Date列を追加し、2024-01-01で埋める
df['Date'] = '2024-01-01'

# pin_no列を追加し、14で埋める
df['pin_no'] = 4

# 'mpid'列に番号を採番する
df['mpid'] = range(7442, 7442 + len(df))

# 番号が採番されたCSVファイルを保存する
df.to_csv('C:\\Users\\14nn0\\works_new\\あおいホーム様\\script\\お気に入り(♡ピン)\\update_address_records.csv', index=False)


