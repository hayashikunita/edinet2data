# edinet2data

---

## プロジェクト概要
EDINET API・JPX公式データ・Yahoo Finance・ChatGPTを活用し、証券コードごとの財務データを自動取得・整理・AI分析するPythonプロジェクトです。

**決算財務諸表の速報をAIで即時分析できる点が最大の特徴です。**

---

## ワークフロー
1. **EDINET API** から財務データを取得しZIP保存
2. **ZIPファイル** を一括解凍・CSV化
3. **JPX公式CSV** で証券コードをマッピング
4. **証券コードごとにディレクトリ整理**
5. **Yahoo Finance** から追加財務データ一括取得
6. **ChatGPT** で複数CSVを統合しAI財務分析
7. すべての処理を `main.py` で日付指定して一括実行

```
┌─────────────┐      ┌─────────────┐      ┌─────────────┐
│ EDINET API │→ZIP→│ 解凍・CSV化 │→JPX→│ コード付与 │→...
└─────────────┘      └─────────────┘      └─────────────┘
	   ↓
   Yahoo Finance取得
	   ↓
   ChatGPT財務分析
```

---

## 主な機能
- EDINET/JPXデータの自動取得・整理
- 決算発表直後の財務諸表（速報）を即座にAI分析
- 証券コードごとのディレクトリ構成
- Yahoo Finance財務データ一括取得
- ChatGPTによるAI財務分析（複数CSVを統合して要約）
- 一連の処理を `main.py` で日付指定して一括実行

---

## ディレクトリ構成例
```
edinet2data/
├─ data/
│   ├─ <yyyymmdd>/
│   │   └─ company_code_map.csv
│   ├─ 7203.T/
│   │   ├─ financials.csv
│   │   ├─ balance_sheet.csv
│   │   └─ ...
│   └─ ...
├─ src/
│   ├─ main.py
│   └─ scripts/
│       ├─ edinet2data2zipdata.py
│       ├─ zipdata2allcsv.py
│       ├─ yyyymmddallcsv2tickersymbol2data.py
│       ├─ batch_yahoofinance.py
│       ├─ yyyymmddaifinanceanalysisfortickersymbol.py
│       └─ ...
└─ README.md
```

---

## 依存パッケージ
- Python 3.8+
- pandas
- requests
- openai
- yfinance
- uvicorn（uvコマンド用）
- dotenv（APIキー管理）

---

## 実行例
```bash
python src/main.py 20250401
```
指定日付（yyyymmdd）のデータ取得からAI分析まで自動で完了します。

---

## AI活用ポイント
- ChatGPT APIを使い、複数CSVを統合した財務分析を自動要約
- 決算発表直後の財務諸表（速報）をAIで即時レポート化
- 企業ごとの財務状況を一括でレポート化

---

## 今後の拡張案
- 画面キャプチャや出力例の追加
- Web UI化（Streamlit等）
- 分析レポートのPDF自動生成
- 他AIモデルへの対応

---

## キャプチャ例
（今後、画面キャプチャや出力例を追加予定です）

---
ご質問・改善要望はお気軽にどうぞ。