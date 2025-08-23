import os
import sys
import csv
import pandas as pd
import shutil
import logging
import argparse
import unicodedata
import difflib
from typing import Optional, Dict, Tuple


logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')


def normalize_name(name: str) -> str:
	"""会社名の比較用に正規化 (全角→半角、空白/記号除去、大小無視、(株)/株式会社の前後除去)"""
	if name is None:
		return ''
	s = unicodedata.normalize('NFKC', str(name))
	# 先頭/末尾の 株式会社 / (株) / （株） を除去
	for mark in ['株式会社', '(株)', '（株）']:
		if s.startswith(mark):
			s = s[len(mark):]
		if s.endswith(mark):
			s = s[:-len(mark)]
	# 空白類・アンダースコア・中点などを除去
	remove_chars = [' ', '\t', '\n', '\r', '_', '･', '・', '　']
	for ch in remove_chars:
		s = s.replace(ch, '')
	# ドットやスラッシュ等の記号も広く除去
	for ch in ['.', '．', '-', '−', '/', '／']:
		s = s.replace(ch, '')
	return s.lower()


def normalize_code(code: str) -> Optional[str]:
	"""コード文字列から最初の4桁の数字を抽出（全角数字にも対応）。"""
	if not code:
		return None
	s = unicodedata.normalize('NFKC', str(code))
	digits = ''.join(ch for ch in s if ch.isdigit())
	if len(digits) >= 4:
		return digits[:4]
	return None


def load_company_code_map(xls_path: str) -> Dict[str, str]:
	"""会社名→4桁証券コードのマッピングをExcelから読み込む。
	列名は自動判定（証券コード・会社名）。"""
	if not os.path.exists(xls_path):
		raise FileNotFoundError(f"マッピングExcelが見つかりません: {xls_path}")

	# Excel読み込み（JPX公式は1枚目のシート）
	df = pd.read_excel(xls_path, sheet_name=0)
	headers = [str(h).strip() for h in df.columns]

	name_keys = [
		'company', 'Company', 'company_name', 'CompanyName', 'name', 'Name', 'filerName', 'issuerName',
		'発行体名', '提出者名', '銘柄名', '企業名', '会社名', '上場会社名', '上場銘柄名', '正式名称', '正式名', 'Company Name'
	]
	code_keys = [
		'code', 'Code', 'secCode', '証券コード', '銘柄コード', 'コード', 'Local Code', '証券コード(4桁)'
	]

	def find_key(candidates):
		for c in candidates:
			for h in headers:
				if c == h or c in h:
					return h
		return None

	name_col = find_key(name_keys)
	code_col = find_key(code_keys)
	if not name_col or not code_col:
		raise ValueError(f"Excelの列名が解釈できません。ヘッダー: {headers}")

	mapping: Dict[str, str] = {}
	for _, row in df.iterrows():
		company = str(row.get(name_col, '')).strip()
		code_raw = str(row.get(code_col, '')).strip()
		code = normalize_code(code_raw)
		if company and code:
			mapping[normalize_name(company)] = code

	return mapping


def parse_company_from_folder(folder_name: str) -> str:
	"""ZIP展開フォルダ名は '{filerName}_{docDescription}_{submitDateTime}_{docID}' 形式（sanitize済み）
	先頭要素が会社名想定なので、それを返す。"""
	# アンダースコアで分割して先頭要素
	if not folder_name:
		return ''
	return folder_name.split('_', 1)[0]


def resolve_code(company2code: Dict[str, str], extracted_company: str) -> Tuple[Optional[str], Optional[str]]:
	"""厳密一致→部分一致（片方が他方を包含）の順でコード解決"""
	key = normalize_name(extracted_company)
	if key in company2code:
		return company2code[key], key
	# 部分一致（3文字以上）
	for k, v in company2code.items():
		if len(k) >= 3 and (k in key or key in k):
			return v, k
	return None, None

def resolve_code_with_similarity(company2code: Dict[str, str], extracted_company: str, threshold: float = 0.5) -> Tuple[Optional[str], Optional[str], float]:
	"""厳密一致→部分一致→類似度でコード解決。類似度は0.0〜1.0"""
	code, matched_key = resolve_code(company2code, extracted_company)
	if code:
		return code, matched_key, 1.0
	# 類似度判定
	key = normalize_name(extracted_company)
	best_ratio = 0.0
	best_code = None
	best_name = None
	for k, v in company2code.items():
		ratio = difflib.SequenceMatcher(None, key, k).ratio()
		if ratio > best_ratio:
			best_ratio = ratio
			best_code = v
			best_name = k
	if best_ratio >= threshold:
		return best_code, best_name, best_ratio
	return None, None, best_ratio


def find_csvs_recursively(root_dir: str):
	for cur, _dirs, files in os.walk(root_dir):
		for fn in files:
			if fn.lower().endswith('.csv'):
				yield os.path.join(cur, fn)


def copy_csvs_to_ticker_dir(src_folder: str, ticker_dir: str) -> Tuple[int, int]:
	os.makedirs(ticker_dir, exist_ok=True)
	copied, skipped = 0, 0
	for csv_path in find_csvs_recursively(src_folder):
		dst_path = os.path.join(ticker_dir, os.path.basename(csv_path))
		if os.path.exists(dst_path):
			logging.info(f"既存CSVのためスキップ: {dst_path}")
			skipped += 1
			continue
		try:
			shutil.copy2(csv_path, dst_path)
			copied += 1
		except Exception as e:
			logging.error(f"コピー失敗: {csv_path} → {dst_path}: {e}")
	return copied, skipped


def main():

	parser = argparse.ArgumentParser(description='data/yyyymmdd配下の各フォルダから会社名→証券コードを割当て、data/<code>.T にCSVをコピーする')
	parser.add_argument('date', help='対象日 yyyymmdd 例: 20240517')
	args = parser.parse_args()

	base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
	day_dir = os.path.join(base_dir, 'data', args.date)
	if not os.path.isdir(day_dir):
		logging.error(f'対象ディレクトリが見つかりません: {day_dir}')
		sys.exit(1)

	# マッピングExcelは固定パス
	map_xls = os.path.join(base_dir, 'src', 'scripts', 'samples', 'data_j.xls')
	try:
		company2code = load_company_code_map(map_xls)
	except Exception as e:
		logging.error(f'マッピングExcel読込失敗: {e}')
		sys.exit(1)

	unmatched_log = []  # (folder, extracted_company)

	# yyyymmdd配下の直下フォルダを処理
	for name in os.listdir(day_dir):
		src_path = os.path.join(day_dir, name)
		if not os.path.isdir(src_path):
			continue

		extracted_company = parse_company_from_folder(name)
		code, matched_key, ratio = resolve_code_with_similarity(company2code, extracted_company, threshold=0.5)
		if not code:
			logging.warning(f'証券コード不明のためスキップ: folder={name} company={extracted_company} 類似度最大={ratio:.2f}')
			unmatched_log.append((name, extracted_company))
			continue

		if ratio < 1.0:
			logging.info(f'類似度で採用: folder={name} company={extracted_company} → matched={matched_key} 類似度={ratio:.2f}')

		ticker = f'{code}.T'
		ticker_dir = os.path.join(base_dir, 'data', ticker)
		copied, skipped = copy_csvs_to_ticker_dir(src_path, ticker_dir)
		logging.info(f'{name} → {ticker}: コピー {copied} 件, スキップ {skipped} 件')

	# 未一致ログを残す
	if unmatched_log:
		out_path = os.path.join(day_dir, 'unmatched_companies.csv')
		try:
			with open(out_path, 'w', encoding='utf-8-sig', newline='') as f:
				w = csv.writer(f)
				w.writerow(['folder_name', 'parsed_company'])
				w.writerows(unmatched_log)
			logging.info(f'未一致の会社名を出力: {out_path}')
		except Exception as e:
			logging.error(f'未一致ログ出力失敗: {e}')

	# 会社名と証券コードのペアをCSVにまとめて保存（gettickersymbol2csv.py形式）
	company_code_rows = []
	for name in os.listdir(day_dir):
		src_path = os.path.join(day_dir, name)
		if not os.path.isdir(src_path):
			continue
		extracted_company = parse_company_from_folder(name)
		code, matched_key, ratio = resolve_code_with_similarity(company2code, extracted_company, threshold=0.5)
		if code:
			company_code_rows.append([code, extracted_company])
	out_path2 = os.path.join(day_dir, 'company_code_map.csv')
	try:
		with open(out_path2, 'w', encoding='utf-8-sig', newline='') as f:
			w = csv.writer(f)
			w.writerow(['証券コード', '会社名'])
			w.writerows(company_code_rows)
		logging.info(f'証券コード・会社名一覧を出力: {out_path2}')
	except Exception as e:
		logging.error(f'証券コード・会社名CSV出力失敗: {e}')


if __name__ == '__main__':
	main()

