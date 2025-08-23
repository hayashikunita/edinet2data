import sys
import subprocess
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')

def run_step(cmd, desc):
	logging.info(f'--- {desc} ---')
	result = subprocess.run(cmd, shell=True)
	if result.returncode != 0:
		logging.error(f'失敗: {desc}')
		sys.exit(result.returncode)

def main():
	if len(sys.argv) < 2:
		print('使い方: python main.py yyyymmdd')
		sys.exit(1)
	yyyymmdd = sys.argv[1]

	# 1. EDINETデータ取得・ZIP保存
	run_step(f'uv run src/scripts/edinet2data2zipdata.py {yyyymmdd}', 'EDINETデータ取得・ZIP保存')

	# 2. ZIP解凍（全ZIPを解凍して削除）
	run_step(f'uv run src/scripts/zipdata2allcsv.py {yyyymmdd}', 'ZIP解凍・削除')

	# 3. CSVを証券コードディレクトリにコピー
	run_step(f'uv run src/scripts/yyyymmddallcsv2tickersymbol2data.py {yyyymmdd}', 'CSVを証券コードディレクトリにコピー')


	# 4. Yahoo Finance財務データ一括取得
	run_step(f'python src/scripts/batch_yahoofinance.py {yyyymmdd}', 'Yahoo Finance財務データ一括取得')

	# 5. AI財務分析一括処理
	run_step(f'python src/scripts/yyyymmddaifinanceanalysisfortickersymbol.py {yyyymmdd}', 'AI財務分析一括処理')

	logging.info('全処理完了')

if __name__ == '__main__':
	main()
