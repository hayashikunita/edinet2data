import os
import sys
import zipfile
import logging

# ログ設定
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')

def main(date_str):
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    target_dir = os.path.join(base_dir, 'data', date_str)
    if not os.path.exists(target_dir):
        logging.error(f'ディレクトリが存在しません: {target_dir}')
        return

    for file in os.listdir(target_dir):
        if file.lower().endswith('.zip'):
            zip_path = os.path.join(target_dir, file)
            extract_dir = os.path.join(target_dir, os.path.splitext(file)[0])
            os.makedirs(extract_dir, exist_ok=True)
            try:
                with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                    zip_ref.extractall(extract_dir)
                logging.info(f'解凍完了: {zip_path} → {extract_dir}')
                # 解凍後にZIPファイルを削除
                try:
                    os.remove(zip_path)
                    logging.info(f'ZIPファイル削除: {zip_path}')
                except Exception as e:
                    logging.error(f'ZIPファイル削除失敗: {zip_path} : {e}')
            except Exception as e:
                logging.error(f'解凍失敗: {zip_path} : {e}')

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('使い方: python zip2csv.py yyyymmdd')
    else:
        main(sys.argv[1])