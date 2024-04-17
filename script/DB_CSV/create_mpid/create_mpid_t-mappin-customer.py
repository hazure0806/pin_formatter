"""
mpid列に番号を採番するスクリプト
"""

import pandas as pd

# CSVファイルを読み込む
df = pd.read_csv('C:\\Users\\14nn0\\works_new\\あおいホーム様\\script\\DB_CSV\\t-mappin-customer.csv')

# 'mpid'列に番号を採番する
df['mpid'] = range(1, 1 + len(df))

# 番号が採番されたCSVファイルを保存する
df.to_csv('C:\\Users\\14nn0\\works_new\\あおいホーム様\\script\\DB_CSV\\t-mappin-customer-mpid.csv', index=False)


