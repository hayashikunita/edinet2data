import os
import sys
import subprocess
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')

def main():
    if len(sys.argv) < 2:
        print('使い方: python batch_yahoofinance.py yyyymmdd')
        sys.exit(1)
    yyyymmdd = sys.argv[1]
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    day_dir = os.path.join(base_dir, 'data', yyyymmdd)
    if not os.path.isdir(day_dir):
        logging.error(f'対象ディレクトリが見つかりません: {day_dir}')
        sys.exit(1)

    # 指定日付のcompany_code_map.csvから証券コードを取得
    import pandas as pd
    csv_path = os.path.join(day_dir, 'company_code_map.csv')
    if not os.path.exists(csv_path):
        logging.error(f'company_code_map.csvが見つかりません: {csv_path}')
        sys.exit(1)
    df = pd.read_csv(csv_path)
    codes = df['証券コード'].astype(str).unique()
    tickers = [f'{code}.T' for code in codes]
    if not tickers:
        logging.warning('証券コードが見つかりません')
        sys.exit(0)

    for ticker in tickers:
        logging.info(f'Yahoo Finance取得: {ticker}')
        cmd = f'uv run src/scripts/yahoofinance2data.py {ticker}'
        result = subprocess.run(cmd, shell=True)
        if result.returncode != 0:
            logging.error(f'取得失敗: {ticker}')
        else:
            logging.info(f'取得完了: {ticker}')

if __name__ == '__main__':
    main()
