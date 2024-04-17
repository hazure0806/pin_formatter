import csv
import re

# 元のCSVファイルパス
csv_file_path = 'C:\\Users\\14nn0\\works_new\\あおいホーム様\\script\\移行対象ファイル\\保存した場所.csv'

# 分けた後のファイル名
csv_lat_lon_path = 'C:\\Users\\14nn0\\works_new\\あおいホーム様\\script\\移行対象ファイル\\lat_lon.csv'
csv_non_lat_lon_path = 'C:\\Users\\14nn0\\works_new\\あおいホーム様\\script\\移行対象ファイル\\non_lat_lon.csv'

# 緯度経度のパターン（簡易的なもの）
lat_lon_pattern = re.compile(r'^-?\d+(\.\d+)?,-?\d+(\.\d+)?$')

with open(csv_file_path, 'r', encoding='utf-8') as csvfile, \
        open(csv_lat_lon_path, 'w', newline='', encoding='utf-8') as lat_lon_file, \
        open(csv_non_lat_lon_path, 'w', newline='', encoding='utf-8') as non_lat_lon_file:
    
    reader = csv.DictReader(csvfile)
    lat_lon_writer = csv.DictWriter(lat_lon_file, fieldnames=reader.fieldnames)
    non_lat_lon_writer = csv.DictWriter(non_lat_lon_file, fieldnames=reader.fieldnames)
    
    # ヘッダーを書き込む
    lat_lon_writer.writeheader()
    non_lat_lon_writer.writeheader()

    for row in reader:
        url = row['URL']
        # URLが緯度経度のパターンに一致するかチェック
        if lat_lon_pattern.match(url):
            # 緯度経度のCSVに書き込む
            lat_lon_writer.writerow(row)
        else:
            # それ以外のCSVに書き込む
            non_lat_lon_writer.writerow(row)
