

import requests
import pandas as pd
import os
import logging
from dotenv import load_dotenv
import argparse



# .envファイルをルート直下から読み込む
load_dotenv(dotenv_path=os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), '.env'))

# ログ設定
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')

# APIのエンドポイント
# url = 'https://disclosure.edinet-fsa.go.jp/api/v2/documents.json'
url = 'https://disclosure.edinet-fsa.go.jp/api/v2/documents.json'


# APIキーは環境変数から取得
api_key = os.environ.get('EDINET_API_KEY')
if not api_key:
    logging.error('EDINET_API_KEY 環境変数が設定されていません。')
    raise SystemExit(1)


# コマンドライン引数で日付指定（yyyymmdd形式）
parser = argparse.ArgumentParser(description='EDINET APIから指定日付のZIPデータを取得')
parser.add_argument('date', help='取得日 yyyymmdd 例: 20250821')
args = parser.parse_args()

# yyyymmdd→yyyy-mm-ddに変換
input_date = args.date
if len(input_date) == 8 and input_date.isdigit():
    date_str = f'{input_date[:4]}-{input_date[4:6]}-{input_date[6:]}'
else:
    logging.error('日付はyyyymmdd形式で指定してください')
    raise SystemExit(1)

params = {
    'date': date_str,
    'type': 2,  # 2は有価証券報告書などの決算書類
    'Subscription-Key': api_key
}


try:
    response = requests.get(url, params=params, timeout=10)
    response.raise_for_status()
except requests.RequestException as e:
    logging.error(f'APIリクエスト失敗: {e}')
    raise SystemExit(1)

# レスポンスのJSONデータを取得
try:
    data = response.json()
except Exception as e:
    logging.error(f'JSONデータの取得失敗: {e}')
    raise SystemExit(1)

# データフレームに変換
try:
    documents = data.get('results', [])
    df = pd.DataFrame(documents)
    print(df.head())
    # 特定のカラムだけを選択
    df_filtered = df[['docID', 'secCode','edinetCode', 'filerName', 'docDescription', 'submitDateTime']]
    # 決算情報のみをフィルタリング
    df_financial = df_filtered[df_filtered['docDescription'].str.contains('有価証券報告書', na=False)]
    logging.info(f'取得件数: {len(df_financial)}')
    print(df_financial.head())

    # 保存先ディレクトリの作成とCSV保存
    save_date = params['date'].replace('-', '')  # yyyymmdd形式
    save_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'data', save_date)
    os.makedirs(save_dir, exist_ok=True)
    save_path = os.path.join(save_dir, 'edinet_financial.csv')
    # df_financial.to_csv(save_path, index=False, encoding='utf-8-sig')

    import urllib.request
    import sys
    import re

    def sanitize_filename(filename):
        """ファイル名を安全な形式に変換"""
        # Windows で使用できない文字を除去・置換
        filename = re.sub(r'[<>:"/\\|?*]', '_', filename)
        # 連続するスペースやドットを単一に
        filename = re.sub(r'[\s\.]+', '_', filename)
        # 長すぎるファイル名を制限
        if len(filename) > 200:
            filename = filename[:200]
        return filename

    # ドキュメントのダウンロード
    for index, doc in df_financial.iterrows():
        docID = doc['docID']
        url = f'https://api.edinet-fsa.go.jp/api/v2/documents/{docID}?type=5&Subscription-Key={api_key}'
        
        print(doc['edinetCode'], doc['docID'], doc['filerName'], doc['docDescription'], doc['submitDateTime'], sep='\t')

        try:
            # ZIPファイルのダウンロード
            with urllib.request.urlopen(url) as res:
                content = res.read()
            # ファイル名を安全な形式に変換
            raw_filename = f'{doc["filerName"]}_{doc["docDescription"]}_{docID}'
            output_filename = sanitize_filename(raw_filename)
            output_path = os.path.join(save_dir, f'{output_filename}.zip')
            if os.path.exists(output_path):
                logging.info(f'既存ファイルのため保存スキップ: {output_path}')
            else:
                with open(output_path, 'wb') as file_out:
                    file_out.write(content)
                logging.info(f'ZIP保存完了: {output_path}')

        except urllib.error.HTTPError as e:
            if e.code >= 400:
                sys.stderr.write(e.reason + '\n')
            else:
                raise e

except Exception as e:
    logging.error(f'データ処理失敗: {e}')
    raise SystemExit(1)


