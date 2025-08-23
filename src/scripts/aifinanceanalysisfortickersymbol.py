import os
import pandas as pd
import openai
import argparse

def read_all_csv_files(ticker_dir):
	"""指定ディレクトリ内のすべてのCSVファイルをDataFrame化"""
	data = {}
	encodings = ["utf-8", "utf-8-sig", "shift_jis", "cp932", "latin1"]
	for fname in os.listdir(ticker_dir):
		if fname.lower().endswith('.csv'):
			path = os.path.join(ticker_dir, fname)
			for enc in encodings:
				try:
					df = pd.read_csv(path, encoding=enc, on_bad_lines='skip')
					data[fname] = df
					break
				except Exception as e:
					last_error = e
			else:
				print(f"{path} の読み込み失敗: {last_error}")
	return data

def analyze_with_gpt(prompt, model="gpt-3.5-turbo"):
	api_key = os.getenv("OPENAI_API_KEY")
	if not api_key:
		raise RuntimeError("OPENAI_API_KEYが環境変数に設定されていません")
	openai.api_key = api_key
	response = openai.ChatCompletion.create(
		model=model,
		messages=[{"role": "system", "content": "あなたは財務分析の専門家です。"},
				  {"role": "user", "content": prompt}]
	)
	return response.choices[0].message.content

def main():
		parser = argparse.ArgumentParser(description="指定ティッカーのCSVをChatGPTで財務分析")
		parser.add_argument("ticker", type=str, nargs="?", default="2168.T", help="ティッカー名（例: 7203.T）")
		args = parser.parse_args()

		ticker_dir = os.path.join("data", args.ticker)
		if not os.path.isdir(ticker_dir):
			print(f"{ticker_dir} ディレクトリが存在しません")
			return

		data = read_all_csv_files(ticker_dir)

		# すべてのCSVのプレビューをまとめて1つのプロンプトに
		prompt_parts = []
		for fname, df in data.items():
			csv_preview = df.head(10).to_csv()
			prompt_parts.append(f"--- {fname} ---\n{csv_preview}")
		prompt = f"以下は{args.ticker}の複数財務データです。各CSVの内容を総合して財務分析を日本語で要約してください。\n\n" + '\n\n'.join(prompt_parts)
		try:
			result = analyze_with_gpt(prompt)
			print(result)
		except Exception as e:
			print(f"ChatGPT APIエラー: {e}")

if __name__ == "__main__":
	main()
