import os
import hashlib
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')

def file_hash(path, block_size=65536):
	hasher = hashlib.md5()
	with open(path, 'rb') as f:
		for block in iter(lambda: f.read(block_size), b''):
			hasher.update(block)
	return hasher.hexdigest()

def main():
	base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
	data_dir = os.path.join(base_dir, 'data')
	if not os.path.isdir(data_dir):
		logging.error(f'dataディレクトリが見つかりません: {data_dir}')
		return

	deleted_total = 0
	# data直下のXXXX.Tディレクトリのみ処理
	for name in os.listdir(data_dir):
		dir_path = os.path.join(data_dir, name)
		if not (os.path.isdir(dir_path) and name.endswith('.T')):
			continue
		seen = dict()  # {(filename, size, hash): path}
		deleted = 0
		for cur, _dirs, files in os.walk(dir_path):
			for fn in files:
				path = os.path.join(cur, fn)
				try:
					size = os.path.getsize(path)
					h = file_hash(path)
					key = (fn, size, h)
					if key in seen:
						logging.info(f'重複ファイル削除: {path}')
						os.remove(path)
						deleted += 1
					else:
						seen[key] = path
				except Exception as e:
					logging.error(f'ファイル処理失敗: {path} : {e}')
		logging.info(f'{name} ディレクトリの重複削除件数: {deleted}')
		deleted_total += deleted
	logging.info(f'全XXXX.Tディレクトリの重複削除合計: {deleted_total}')

if __name__ == '__main__':
	main()
