"""
行ってみたい.csvから住所を含むレコードを抽出し、新しいCSVファイルに保存するスクリプト
"""

import pandas as pd
import re

# CSVファイルを読み込む
input_csv = 'C:\\Users\\14nn0\\works_new\\あおいホーム様\\script\\移行対象ファイル\\行ってみたい.csv'
output_csv = 'C:\\Users\\14nn0\\works_new\\あおいホーム様\\script\\行ってみたい(緑ピン)\\address_records.csv'
output_csv2 = 'C:\\Users\\14nn0\\works_new\\あおいホーム様\\script\\行ってみたい(緑ピン)\\address_non_records.csv'
output_csv3 = 'C:\\Users\\14nn0\\works_new\\あおいホーム様\\script\\行ってみたい(緑ピン)\\address_url_records.csv'

# CSVファイルの読み込み
df = pd.read_csv(input_csv)

# 住所を含むレコードを判定する関数
def contains_address(title):
    # titleが文字列でない場合（NaNやNoneなど）、Falseを返す
    if not isinstance(title, str):
        return False
    # それ以外の場合、正規表現で検索を実行
    return re.search(r'〒', title) is not None


# タイトル列に住所が含まれているレコードを抽出
address_df = df[df['タイトル'].apply(contains_address)]

# 抽出したレコードを新しいCSVファイルに出力
address_df.to_csv(output_csv, index=False)

# 元のCSVファイルに含まれる住所を含むレコードを削除
df = df[~df['タイトル'].apply(contains_address)]

# URL列が空のレコードを抽出
url_df = df[df['URL'].isnull()]

# URL列が空のレコードを新しいCSVファイルに出力
url_df.to_csv(output_csv3, index=False)

# URL列が空のレコードを削除
df = df[~df['URL'].isnull()]

# URL列が空でないレコードを新しいCSVファイルに出力
df.to_csv(output_csv2, index=False)

print(f'Address records have been extracted and saved to {output_csv}')
