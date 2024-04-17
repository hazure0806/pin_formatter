"""
mpid列に番号を採番するスクリプト
"""

import pandas as pd

# CSVファイルを読み込む
df = pd.read_csv('C:\\Users\\14nn0\\works_new\\あおいホーム様\\script\\行ってみたい(緑ピン)\\address_non_records.csv')


# Date列を追加し、2024-01-01で埋める
df['Date'] = '2024-01-01'

# pin_no列を追加し、3で埋める
df['pin_no'] = 3

# 'mpid'列に番号を採番する
df['mpid'] = range(5272, 5272 + len(df))

# 番号が採番されたCSVファイルを保存する
df.to_csv('C:\\Users\\14nn0\\works_new\\あおいホーム様\\script\\行ってみたい(緑ピン)\\update_address_non_records.csv', index=False)


