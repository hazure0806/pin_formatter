import json
import csv

# JSONファイルのパス
json_file_path = r'C:\Users\14nn0\works_new\あおいホーム様\script\移行対象ファイル\保存した場所.json'

# JSONファイルを読み込む
with open(json_file_path, 'r', encoding='utf-8') as jsonfile:
    data = json.load(jsonfile)

# CSVファイルのパスを設定（JSONファイルと同じフォルダに保存）
csv_file_path = json_file_path.replace('保存した場所.json', '保存した場所.csv')

# CSVファイルを開き、書き込み
with open(csv_file_path, 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['Date', 'URL']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    # ヘッダー（カラム名）を書き込む
    writer.writeheader()

    # 各フィーチャーに対して、必要な情報をCSVに書き込む
    for feature in data['features']:
        date = feature['properties']['date']
        url = feature['properties']['google_maps_url']
        writer.writerow({'Date': date, 'URL': url})
