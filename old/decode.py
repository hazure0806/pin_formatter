from urllib.parse import unquote
import csv

# C:\Users\14nn0\works_new\あおいホーム様\script\移行対象ファイル\non_lat_lon.csv を読み込む
# 元のCSVファイルパス
csv_file_path = 'C:\\Users\\14nn0\\works_new\\あおいホーム様\\script\\移行対象ファイル\\non_lat_lon.csv'

# 出力先のCSVファイルパス
decoded_csv_file_path = 'C:\\Users\\14nn0\\works_new\\あおいホーム様\\script\\移行対象ファイル\\decoded_non_lat_lon.csv'

# URLカラムのデコード後の値を格納するリスト
decoded_urls = []

# CSVファイルを開く
with open(csv_file_path, 'r', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    
    # 各行のURLカラムをデコードし、リストに格納
    for row in reader:
        url = row['URL']
        decoded_url = unquote(url)
        decoded_urls.append(decoded_url)

# デコード後の値をCSVに書き込む
with open(decoded_csv_file_path, 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['Date', 'URL']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    
    # ヘッダーを書き込む
    writer.writeheader()
    
    # デコード後の値を書き込む
    for decoded_url in decoded_urls:
        writer.writerow({'Date': '', 'URL': decoded_url})