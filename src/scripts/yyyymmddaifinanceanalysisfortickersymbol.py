import os
import pandas as pd
import subprocess
import sys

def main():
    # 対象日付（引数で受け取る）
    if len(sys.argv) > 1:
        date = sys.argv[1]
    else:
        date = "20250820"
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    csv_path = os.path.join(base_dir, "data", date, "company_code_map.csv")
    data_dir = os.path.join(base_dir, "data")
    script_path = os.path.join(base_dir, "src", "scripts", "aifinanceanalysisfortickersymbol.py")

    # 証券コード一覧を取得
    df = pd.read_csv(csv_path)
    codes = df["証券コード"].astype(str).unique()

    for code in codes:
        ticker = f"{code}.T"
        ticker_dir = os.path.join(data_dir, ticker)
        if os.path.isdir(ticker_dir):
            print(f"分析実行: {ticker}")
            # powershell用コマンド
            cmd = [sys.executable, script_path, ticker]
            try:
                subprocess.run(cmd, check=True)
            except Exception as e:
                print(f"{ticker} の分析失敗: {e}")
        else:
            print(f"ディレクトリなし: {ticker_dir}")

if __name__ == "__main__":
    main()
