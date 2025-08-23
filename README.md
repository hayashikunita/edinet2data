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


## キャプチャ例（出力例）
```text
2025-08-23 17:00:26,237 INFO --- EDINETデータ取得・ZIP保存 ---
   seqNumber     docID edinetCode secCode            JCN  ... pdfFlag attachDocFlag englishDocFlag csvFlag legalStatus
0          1  S100VGVM     E26704    None  6010001141324  ...       1             0              0       1           1
...（中略）...
2025-08-23 17:00:28,450 INFO 取得件数: 5
...（中略）...
2025-08-23 17:00:29,421 INFO ZIP保存完了: ...
...（中略）...
2025-08-23 17:00:34,143 INFO --- ZIP解凍・削除 ---
...（中略）...
2025-08-23 17:00:34,656 INFO --- CSVを証券コードディレクトリにコピー ---
...（中略）...
2025-08-23 17:00:36,303 INFO 証券コード・会社名一覧を出力: ...
2025-08-23 17:00:36,463 INFO --- Yahoo Finance財務データ一括取得 ---
Fetching data for 4345.T...
yfinance.Ticker object <4345.T>
[財務データのDataFrame出力例]
Saving data to data\4345.T...
...（中略）...
2025-08-23 17:00:57,269 INFO --- AI財務分析一括処理 ---
分析実行: 4345.T
ChatGPT APIエラー: OPENAI_API_KEYが環境変数に設定されていません
...（各証券コードごとに同様のエラー）...
2025-08-23 17:01:04,858 INFO 全処理完了
```

---
ご質問・改善要望はお気軽にどうぞ。

##　処理結果
(20250820) PS C:<フォルダ>> uv run src\main.py 20250402 
2025-08-23 17:00:26,237 INFO --- EDINETデータ取得・ZIP保存 ---
   seqNumber     docID edinetCode secCode            JCN  ... pdfFlag attachDocFlag englishDocFlag csvFlag legalStatus
0          1  S100VGVM     E26704    None  6010001141324  ...       1             0              0       1           1
1          2  S100VGVQ     E26704    None  6010001141324  ...       1             0              0       1           1
2          3  S100VGVS     E26704    None  6010001141324  ...       1             0              0       1           1
3          4  S100VHLR     E06433    None  3010001034076  ...       1             0              0       1           1
4          5  S100VINX     E10677    None  9010001021473  ...       1             0              0       1           1

[5 rows x 29 columns]
2025-08-23 17:00:28,450 INFO 取得件数: 5
        docID secCode  ...                                    docDescription    submitDateTime
10   S100VIZJ    None  ...   有価証券報告書（内国投資信託受益証券）－第19期(2024/01/23－2025/01/20)  2025-04-02 09:19
36   S100VJGM    None  ...  訂正有価証券報告書（内国投資信託受益証券）－第3期(2023/03/28－2024/03/25)  2025-04-02 11:14
53   S100VJW7    None  ...             訂正有価証券報告書－第30期(2024/01/01－2024/12/31)  2025-04-02 13:13       
59   S100VJS8   92600  ...             訂正有価証券報告書－第78期(2024/01/01－2024/12/31)  2025-04-02 13:44       
110  S100VJZC   39280  ...             訂正有価証券報告書－第19期(2024/01/01－2024/12/31)  2025-04-02 16:12       

[5 rows x 6 columns]
E06264  S100VIZJ        ＪＰモルガン・アセット・マネジメント株式会社    有価証券報告書（内国投資信託受益証券）－第19期(2024/01/23－2025/01/20)    2025-04-02 09:19
2025-08-23 17:00:29,421 INFO ZIP保存完了: C:<フォルダ>\data\20250402\ＪＰモルガン・アセット・マネジメント株式会社_有価証券報告書（内国投資信託受益証券）－第19期(2024_01_23－2025_01_20)_S100VIZJ.zip
E36992  S100VJGM        ＨＣアセットマネジメント株式会社        訂正有価証券報告書（内国投資信託受益証券）－第3期(2023/03/28－2024/03/25) 2025-04-02 11:14
2025-08-23 17:00:30,150 INFO ZIP保存完了: C:<フォルダ>\data\20250402\ＨＣアセットマネジメント株式会社_訂正有価証券報告書（内国投資信託受益証券）－第3期(2023_03_28－2024_03_25)_S100VJGM.zip
E02104  S100VJW7        株式会社ディー・ディー・エス    訂正有価証券報告書－第30期(2024/01/01－2024/12/31)      2025-04-02 13:13
2025-08-23 17:00:30,991 INFO ZIP保存完了: C:<フォルダ>\data\20250402\株式会社ディー・ディー・エス_訂正有価証券報告書－第30期(2024_01_01－2024_12_31)_S100VJW7.zip
E33381  S100VJS8        西本Ｗｉｓｍｅｔｔａｃホールディングス株式会社  訂正有価証券報告書－第78期(2024/01/01－2024/12/31)        2025-04-02 13:44
2025-08-23 17:00:33,213 INFO ZIP保存完了: C:<フォルダ>\data\20250402\西本Ｗｉｓｍｅｔｔａｃホールディングス株式会社_訂正有価証券報告書－第78期(2024_01_01－2024_12_31)_S100VJS8.zip
E31991  S100VJZC        株式会社マイネット      訂正有価証券報告書－第19期(2024/01/01－2024/12/31)      2025-04-02 16:12
2025-08-23 17:00:33,957 INFO ZIP保存完了: C:<フォルダ>\data\20250402\株式会社マイネット_訂正有価証券報告書－第19期(2024_01_01－2024_12_31)_S100VJZC.zip
2025-08-23 17:00:34,143 INFO --- ZIP解凍・削除 ---
2025-08-23 17:00:34,572 INFO 解凍完了: C:<フォルダ>\data\20250402\株式会社ディー・ディー・エス_訂正有価証券報告書－第30期(2024_01_01－2024_12_31)_S100VJW7.zip → C:<フォルダ>\data\20250402\株式会社ディー・ディー・エス_訂正有価証券報告書－第30期(2024_01_01－2024_12_31)_S100VJW7
2025-08-23 17:00:34,574 INFO ZIPファイル削除: C:<フォルダ>\data\20250402\株式会社ディー・ディー・エス_訂正有価証券報告書－第30期(2024_01_01－2024_12_31)_S100VJW7.zip
2025-08-23 17:00:34,583 INFO 解凍完了: C:<フォルダ>\data\20250402\株式会社マイネット_訂正有価証券報告書－第19期(2024_01_01－2024_12_31)_S100VJZC.zip → C:<フォルダ>\data\20250402\株式会社マイネット_訂正有価証券報告書－第19期(2024_01_01－2024_12_31)_S100VJZC
2025-08-23 17:00:34,584 INFO ZIPファイル削除: C:<フォルダ>\data\20250402\株式会社マイネット_訂正有価証券報告書－第19期(2024_01_01－2024_12_31)_S100VJZC.zip
2025-08-23 17:00:34,594 INFO 解凍完了: C:<フォルダ>\data\20250402\西本Ｗｉｓｍｅｔｔａｃホールディングス株式会社_訂正有価証券報告書－第78期(2024_01_01－2024_12_31)_S100VJS8.zip → C:<フォルダ>\data\20250402\西本Ｗｉｓｍｅｔｔａｃホールディングス株式会社_訂正有価証券報告書－第78期(2024_01_01－2024_12_31)_S100VJS8
2025-08-23 17:00:34,596 INFO ZIPファイル削除: C:<フォルダ>\data\20250402\西本Ｗｉｓｍｅｔｔａｃホールディングス株式会社_訂正有価証券報告書－第78期(2024_01_01－2024_12_31)_S100VJS8.zip
2025-08-23 17:00:34,606 INFO 解凍完了: C:<フォルダ>\data\20250402\ＨＣアセットマネジメント株式会社_訂正有価証券報告書（内国投資信託受益証券）－第3期(2023_03_28－2024_03_25)_S100VJGM.zip → C:<フォルダ>\data\20250402\ＨＣアセットマネジメント株式 会社_訂正有価証券報告書（内国投資信託受益証券）－第3期(2023_03_28－2024_03_25)_S100VJGM
2025-08-23 17:00:34,608 INFO ZIPファイル削除: C:<フォルダ>\data\20250402\ＨＣアセットマネジメント株式会社_訂正有価証券報告書（内国投資信託受益証券）－第3期(2023_03_28－2024_03_25)_S100VJGM.zip
2025-08-23 17:00:34,618 INFO 解凍完了: C:<フォルダ>\data\20250402\ＪＰモルガン・アセット・マネジメント株式会社_有価証券報告書（内国投資信託受益証券）－第19期(2024_01_23－2025_01_20)_S100VIZJ.zip → C:<フォルダ>\data\20250402\ＪＰモルガン・アセット・マネジメント株式会社_有価証券報告書（内国投資信託受益証券）－第19期(2024_01_23－2025_01_20)_S100VIZJ
2025-08-23 17:00:34,619 INFO ZIPファイル削除: C:<フォルダ>\data\20250402\ＪＰモルガン・アセット・マネジメント株式会社_有価証券報告書（内国投資信託受益証券）－第19期(2024_01_23－2025_01_20)_S100VIZJ.zip
2025-08-23 17:00:34,656 INFO --- CSVを証券コードディレクトリにコピー ---
2025-08-23 17:00:35,897 INFO 類似度で採用: folder=株式会社ディー・ディー・エス_訂正有価証券報告書－第30期(2024_01_01－2024_12_31)_S100VJW7 company=株式会社ディー・ディー・エス → matched=シーティーエス 類似度=0.67
2025-08-23 17:00:35,905 INFO 株式会社ディー・ディー・エス_訂正有価証券報告書－第30期(2024_01_01－2024_12_31)_S100VJW7 → 4345.T: コピー 2 件, スキップ 0 件
2025-08-23 17:00:35,914 INFO 株式会社マイネット_訂正有価証券報告書－第19期(2024_01_01－2024_12_31)_S100VJZC → 3928.T: コピー 3 件, スキップ 0 件
2025-08-23 17:00:35,925 INFO 西本Ｗｉｓｍｅｔｔａｃホールディングス株式会社_訂正有価証券報告書－第78期(2024_01_01 －2024_12_31)_S100VJS8 → 4319.T: コピー 3 件, スキップ 0 件
2025-08-23 17:00:35,990 INFO 類似度で採用: folder=ＨＣアセットマネジメント株式会社_訂正有価証券報告書（内国投資信 託受益証券）－第3期(2023_03_28－2024_03_25)_S100VJGM company=ＨＣアセットマネジメント株式会社 → matched=sbiグロー バルアセットマネジメント 類似度=0.67
2025-08-23 17:00:35,999 INFO ＨＣアセットマネジメント株式会社_訂正有価証券報告書（内国投資信託受益証券）－第3期(2023_03_28－2024_03_25)_S100VJGM → 4765.T: コピー 4 件, スキップ 0 件
2025-08-23 17:00:36,079 INFO 類似度で採用: folder=ＪＰモルガン・アセット・マネジメント株式会社_有価証券報告書（内 国投資信託受益証券）－第19期(2024_01_23－2025_01_20)_S100VIZJ company=ＪＰモルガン・アセット・マネジメント株式会社 → matched=sbiグローバルアセットマネジメント 類似度=0.65
2025-08-23 17:00:36,088 INFO ＪＰモルガン・アセット・マネジメント株式会社_有価証券報告書（内国投資信託受益証券）－第19期(2024_01_23－2025_01_20)_S100VIZJ → 4765.T: コピー 4 件, スキップ 0 件
2025-08-23 17:00:36,303 INFO 証券コード・会社名一覧を出力: C:<フォルダ>\data\20250402\company_code_map.csv
2025-08-23 17:00:36,463 INFO --- Yahoo Finance財務データ一括取得 ---
2025-08-23 17:00:37,143 INFO Yahoo Finance取得: 4345.T
Fetching data for 4345.T...
yfinance.Ticker object <4345.T>
                                                      2025-03-31    2024-03-31  ...    2022-03-31   2021-03-31
Tax Effect Of Unusual Items                         0.000000e+00  0.000000e+00  ...  6.450098e+06          NaN    
Tax Rate For Calcs                                  3.070000e-01  3.330000e-01  ...  3.225050e-01          NaN    
Normalized EBITDA                                   4.208000e+09  3.795000e+09  ...  3.488000e+09          NaN    
Total Unusual Items                                          NaN  0.000000e+00  ...  2.000000e+07  15000000.00    
Total Unusual Items Excluding Goodwill                       NaN  0.000000e+00  ...  2.000000e+07  15000000.00    
Net Income From Continuing Operation Net Minori...  2.190000e+09  1.858000e+09  ...  1.731000e+09          NaN    
Reconciled Depreciation                             1.002000e+09  9.680000e+08  ...  9.050000e+08          NaN    
Reconciled Cost Of Revenue                          5.745000e+09  5.385000e+09  ...  5.313000e+09          NaN    
EBITDA                                              4.208000e+09  3.795000e+09  ...  3.508000e+09          NaN    
EBIT                                                3.206000e+09  2.827000e+09  ...  2.603000e+09          NaN    
Net Interest Income                                -4.400000e+07 -4.200000e+07  ... -4.800000e+07          NaN    
Interest Expense                                    4.400000e+07  4.200000e+07  ...  4.800000e+07          NaN    
Normalized Income                                   2.190000e+09  1.858000e+09  ...  1.717450e+09          NaN    
Net Income From Continuing And Discontinued Ope...  2.190000e+09  1.858000e+09  ...  1.731000e+09          NaN    
Total Expenses                                      8.743000e+09  8.224000e+09  ...  7.914000e+09          NaN    
Total Operating Income As Reported                  3.077000e+09  2.865000e+09  ...  2.628000e+09          NaN    
Diluted Average Shares                                       NaN  4.237916e+07  ...  4.243168e+07  42679155.00    
Basic Average Shares                                         NaN  4.237916e+07  ...  4.243168e+07  42679155.00    
Diluted EPS                                                  NaN  4.386000e+01  ...  4.080000e+01        34.14    
Basic EPS                                                    NaN  4.386000e+01  ...  4.080000e+01        34.14    
Diluted NI Availto Com Stockholders                 2.190000e+09  1.858000e+09  ...  1.731000e+09          NaN    
Net Income Common Stockholders                      2.190000e+09  1.858000e+09  ...  1.731000e+09          NaN    
Otherunder Preferred Stock Dividend                 0.000000e+00  0.000000e+00  ...  0.000000e+00          NaN    
Net Income                                          2.190000e+09  1.858000e+09  ...  1.731000e+09          NaN    
Net Income Including Noncontrolling Interests       2.190000e+09  1.858000e+09  ...  1.731000e+09          NaN    
Net Income Continuous Operations                    2.191000e+09  1.859000e+09  ...  1.731000e+09          NaN    
Tax Provision                                       9.710000e+08  9.260000e+08  ...  8.240000e+08          NaN    
Pretax Income                                       3.162000e+09  2.785000e+09  ...  2.555000e+09          NaN    
Other Non Operating Income Expenses                 1.100000e+07  4.000000e+06  ...  8.000000e+06          NaN    
Special Income Charges                                       NaN           NaN  ...  3.000000e+06   1000000.00    
Other Special Charges                                        NaN           NaN  ... -3.000000e+06  -1000000.00    
Net Non Operating Interest Income Expense          -4.400000e+07 -4.200000e+07  ... -4.800000e+07          NaN    
Interest Expense Non Operating                      4.400000e+07  4.200000e+07  ...  4.800000e+07          NaN    
Operating Income                                    3.078000e+09  2.865000e+09  ...  2.628000e+09          NaN    
Operating Expense                                   2.998000e+09  2.839000e+09  ...  2.601000e+09          NaN    
Gross Profit                                        6.076000e+09  5.704000e+09  ...  5.229000e+09          NaN    
Cost Of Revenue                                     5.745000e+09  5.385000e+09  ...  5.313000e+09          NaN    
Total Revenue                                       1.182100e+10  1.109000e+10  ...  1.054200e+10          NaN    
Operating Revenue                                   1.182100e+10  1.109000e+10  ...  1.054200e+10          NaN    

[39 rows x 5 columns]
Saving data to data\4345.T...
4345.Tの財務データをdataに保存しました。
2025-08-23 17:00:40,980 INFO 取得完了: 4345.T
2025-08-23 17:00:40,981 INFO Yahoo Finance取得: 3928.T
Fetching data for 3928.T...
yfinance.Ticker object <3928.T>
                                                      2024-12-31    2023-12-31  ...    2021-12-31  2020-12-31
Tax Effect Of Unusual Items                        -6.314549e+06 -2.982267e+07  ... -2.551320e+07         NaN     
Tax Rate For Calcs                                  6.700000e-02  2.320000e-01  ...  3.062000e-01         NaN     
Normalized EBITDA                                   4.638030e+08  3.480390e+08  ...  7.773000e+08         NaN     
Total Unusual Items                                -9.424700e+07 -1.285460e+08  ... -8.332200e+07         NaN     
Total Unusual Items Excluding Goodwill             -9.424700e+07 -1.285460e+08  ... -8.332200e+07         NaN     
Net Income From Continuing Operation Net Minori...  2.456340e+08  1.432780e+08  ...  2.292740e+08         NaN     
Reconciled Depreciation                             6.157300e+07  1.670570e+08  ...  2.082840e+08         NaN     
Reconciled Cost Of Revenue                          5.292561e+09  5.391732e+09  ...  6.278739e+09         NaN     
EBITDA                                              3.695560e+08  2.194930e+08  ...  6.939780e+08         NaN     
EBIT                                                3.079830e+08  5.243600e+07  ...  4.856940e+08         NaN     
Net Interest Income                                -3.059200e+07 -1.513700e+07  ... -2.330300e+07         NaN     
Interest Expense                                    1.905900e+07  1.555300e+07  ...  1.376400e+07         NaN     
Interest Income                                     1.160000e+06  4.160000e+05  ...  9.500000e+04   491000.00     
Normalized Income                                   3.335665e+08  2.420013e+08  ...  2.870828e+08         NaN     
Net Income From Continuing And Discontinued Ope...  2.456340e+08  1.432780e+08  ...  2.292740e+08         NaN     
Total Expenses                                      8.417957e+09  8.549473e+09  ...  9.993573e+09         NaN     
Total Operating Income As Reported                  4.283550e+08  1.685080e+08  ...  5.776110e+08         NaN     
Diluted Average Shares                              8.441031e+06  8.428118e+06  ...  8.668204e+06         NaN     
Basic Average Shares                                         NaN  8.428118e+06  ...  8.651699e+06  8602427.00     
Diluted EPS                                                  NaN  1.700000e+01  ...  2.645000e+01      130.69     
Basic EPS                                                    NaN  1.700000e+01  ...  2.650000e+01      131.34     
Diluted NI Availto Com Stockholders                 2.456340e+08  1.432780e+08  ...  2.292740e+08         NaN     
Net Income Common Stockholders                      2.456340e+08  1.432780e+08  ...  2.292740e+08         NaN     
Otherunder Preferred Stock Dividend                 0.000000e+00  0.000000e+00  ...  0.000000e+00         NaN     
Net Income                                          2.456340e+08  1.432780e+08  ...  2.292740e+08         NaN     
Minority Interests                                 -2.382300e+07 -1.078100e+07  ...           NaN         NaN     
Net Income Including Noncontrolling Interests       2.694570e+08  1.540600e+08  ...  2.292740e+08         NaN     
Net Income Continuous Operations                    2.694580e+08  1.540590e+08  ...  2.292750e+08         NaN     
Tax Provision                                       1.946600e+07 -1.171760e+08  ...  2.426550e+08         NaN     
Pretax Income                                       2.889240e+08  3.688300e+07  ...  4.719300e+08         NaN     
Other Non Operating Income Expenses                -2.316100e+07  7.770000e+06  ... -2.897000e+06         NaN     
Special Income Charges                             -5.491800e+07 -1.304760e+08  ... -7.020000e+07         NaN     
Other Special Charges                               2.397200e+07 -5.572200e+07  ... -7.580000e+06         NaN     
Write Off                                           3.094600e+07  1.861980e+08  ...  7.778000e+07         NaN     
Net Non Operating Interest Income Expense          -3.059200e+07 -1.513700e+07  ... -2.330300e+07         NaN     
Total Other Finance Cost                            1.269300e+07           NaN  ...  9.539000e+06         NaN     
Interest Expense Non Operating                      1.905900e+07  1.555300e+07  ...  1.376400e+07         NaN     
Interest Income Non Operating                       1.160000e+06  4.160000e+05  ...  9.500000e+04   491000.00     
Operating Income                                    4.283550e+08  1.685090e+08  ...  5.776110e+08         NaN     
Operating Expense                                   3.125396e+09  3.157741e+09  ...  3.714834e+09         NaN     
Gross Profit                                        3.553751e+09  3.326250e+09  ...  4.292445e+09         NaN     
Cost Of Revenue                                     5.292561e+09  5.391732e+09  ...  6.278739e+09         NaN     
Total Revenue                                       8.846312e+09  8.717982e+09  ...  1.057118e+10         NaN     
Operating Revenue                                   8.846312e+09  8.717982e+09  ...  1.057118e+10         NaN     

[44 rows x 5 columns]
Saving data to data\3928.T...
3928.Tの財務データをdataに保存しました。
2025-08-23 17:00:48,014 INFO 取得完了: 3928.T
2025-08-23 17:00:48,015 INFO Yahoo Finance取得: 4319.T
Fetching data for 4319.T...
yfinance.Ticker object <4319.T>
                                                      2025-03-31    2024-03-31    2023-03-31    2022-03-31
Tax Effect Of Unusual Items                        -2.853022e+06  4.190689e+06  1.119637e+06  1.147180e+08        
Tax Rate For Calcs                                  3.129000e-01  3.525140e-01  2.804000e-01  3.710000e-01        
Normalized EBITDA                                   1.115973e+09  9.292200e+07  7.482280e+08  8.643390e+08        
Total Unusual Items                                -9.118000e+06  1.188800e+07  3.993000e+06  3.092130e+08        
Total Unusual Items Excluding Goodwill             -9.118000e+06  1.188800e+07  3.993000e+06  3.092130e+08        
Net Income From Continuing Operation Net Minori...  4.674820e+08 -2.197660e+08  2.147400e+08  4.449870e+08        
Reconciled Depreciation                             3.833390e+08  4.088760e+08  4.175920e+08  4.276220e+08        
Reconciled Cost Of Revenue                          1.148886e+10  1.201297e+10  1.197934e+10  1.265740e+10        
EBITDA                                              1.106855e+09  1.048100e+08  7.522210e+08  1.173552e+09        
EBIT                                                7.235160e+08 -3.040660e+08  3.346290e+08  7.459300e+08        
Net Interest Income                                -3.348600e+07 -2.591100e+07 -2.553500e+07 -2.021500e+07        
Interest Expense                                    4.115400e+07  3.309200e+07  3.430000e+07  3.554800e+07        
Interest Income                                     7.668000e+06  7.181000e+06  8.765000e+06  1.533300e+07        
Normalized Income                                   4.737470e+08 -2.274633e+08  2.118666e+08  2.504920e+08        
Net Income From Continuing And Discontinued Ope...  4.674820e+08 -2.197660e+08  2.147400e+08  4.449870e+08        
Total Expenses                                      1.847100e+10  1.930891e+10  1.939270e+10  2.005852e+10        
Total Operating Income As Reported                  7.259400e+08 -3.074120e+08  3.190410e+08  4.132950e+08        
Diluted Average Shares                              1.813351e+07  1.813251e+07  1.836603e+07  1.850393e+07        
Basic Average Shares                                1.813351e+07  1.813251e+07  1.836603e+07  1.850393e+07        
Diluted EPS                                         2.578000e+01 -1.212000e+01  1.169000e+01  2.405000e+01        
Basic EPS                                           2.578000e+01 -1.212000e+01  1.169000e+01  2.405000e+01        
Diluted NI Availto Com Stockholders                 4.674820e+08 -2.197660e+08  2.147400e+08  4.449870e+08        
Net Income Common Stockholders                      4.674820e+08 -2.197660e+08  2.147400e+08  4.449870e+08        
Otherunder Preferred Stock Dividend                 0.000000e+00  0.000000e+00  0.000000e+00  0.000000e+00        
Net Income                                          4.674820e+08 -2.197660e+08  2.147400e+08  4.449870e+08        
Minority Interests                                 -1.342000e+06 -1.461000e+06 -1.346000e+06 -1.783000e+06        
Net Income Including Noncontrolling Interests       4.688240e+08 -2.183040e+08  2.160870e+08  4.467710e+08        
Net Income Continuous Operations                    4.688240e+08 -2.183050e+08  2.160880e+08  4.467710e+08        
Tax Provision                                       2.135380e+08 -1.188530e+08  8.424100e+07  2.636110e+08        
Pretax Income                                       6.823620e+08 -3.371580e+08  3.003290e+08  7.103820e+08        
Other Non Operating Income Expenses                 1.050000e+06 -7.813000e+06  4.270000e+06  4.849000e+06        
Special Income Charges                             -7.593000e+06 -1.391200e+07  8.006000e+06  2.679420e+08        
Other Special Charges                              -2.934800e+07  1.391200e+07 -2.344700e+07 -2.832490e+08        
Write Off                                           3.694100e+07  0.000000e+00  1.544100e+07  1.530700e+07        
Net Non Operating Interest Income Expense          -3.348600e+07 -2.591100e+07 -2.553500e+07 -2.021500e+07        
Interest Expense Non Operating                      4.115400e+07  3.309200e+07  3.430000e+07  3.554800e+07        
Interest Income Non Operating                       7.668000e+06  7.181000e+06  8.765000e+06  1.533300e+07        
Operating Income                                    7.259400e+08 -3.074130e+08  3.190410e+08  4.132950e+08        
Operating Expense                                   6.982140e+09  7.295940e+09  7.413355e+09  7.401118e+09        
Gross Profit                                        7.708080e+09  6.988527e+09  7.732396e+09  7.814413e+09        
Cost Of Revenue                                     1.148886e+10  1.201297e+10  1.197934e+10  1.265740e+10        
Total Revenue                                       1.919694e+10  1.900150e+10  1.971174e+10  2.047182e+10        
Operating Revenue                                   1.919694e+10  1.900150e+10  1.971174e+10  2.047182e+10        
Saving data to data\4319.T...
4319.Tの財務データをdataに保存しました。
2025-08-23 17:00:52,535 INFO 取得完了: 4319.T
2025-08-23 17:00:52,536 INFO Yahoo Finance取得: 4765.T
Fetching data for 4765.T...
yfinance.Ticker object <4765.T>
                                                      2025-03-31    2024-03-31  ...    2022-03-31  2021-03-31
Tax Effect Of Unusual Items                         1.694401e+07  4.670747e+07  ...  3.116419e+07         NaN     
Tax Rate For Calcs                                  3.488000e-01  3.540000e-01  ...  3.077150e-01         NaN     
Normalized EBITDA                                   2.764029e+09  2.484670e+09  ...  2.590187e+09         NaN     
Total Unusual Items                                 4.857800e+07  1.319420e+08  ...  1.012760e+08         NaN     
Total Unusual Items Excluding Goodwill              4.857800e+07  1.319420e+08  ...  1.012760e+08         NaN     
Net Income From Continuing Operation Net Minori...  1.646935e+09  1.589278e+09  ...  1.454134e+09         NaN     
Reconciled Depreciation                             5.433320e+08  5.052870e+08  ...  5.616580e+08         NaN     
Reconciled Cost Of Revenue                          5.870993e+09  4.917169e+09  ...  3.654398e+09         NaN     
EBITDA                                              2.812607e+09  2.616612e+09  ...  2.691463e+09         NaN     
EBIT                                                2.269275e+09  2.111325e+09  ...  2.129805e+09         NaN     
Net Interest Income                                 1.197520e+08  7.030900e+07  ...  1.877940e+08         NaN     
Interest Expense                                             NaN           NaN  ...  0.000000e+00  16447000.0     
Interest Income                                     1.211360e+08  7.800600e+07  ...  1.970720e+08         NaN     
Normalized Income                                   1.615301e+09  1.504043e+09  ...  1.384022e+09         NaN     
Net Income From Continuing And Discontinued Ope...  1.646935e+09  1.589278e+09  ...  1.454134e+09         NaN     
Total Expenses                                      9.299715e+09  8.026270e+09  ...  5.993481e+09         NaN     
Total Operating Income As Reported                  2.269274e+09  2.111325e+09  ...  2.129805e+09         NaN     
Diluted Average Shares                              8.965351e+07  8.968838e+07  ...  8.967343e+07         NaN     
Basic Average Shares                                8.965351e+07  8.968838e+07  ...  8.967343e+07         NaN     
Diluted EPS                                         1.837000e+01  1.772000e+01  ...  1.622000e+01         NaN     
Basic EPS                                           1.837000e+01  1.772000e+01  ...  1.622000e+01         NaN     
Diluted NI Availto Com Stockholders                 1.646935e+09  1.589278e+09  ...  1.454134e+09         NaN     
Net Income Common Stockholders                      1.646935e+09  1.589278e+09  ...  1.454134e+09         NaN     
Otherunder Preferred Stock Dividend                 0.000000e+00  0.000000e+00  ...  0.000000e+00         NaN     
Net Income                                          1.646935e+09  1.589278e+09  ...  1.454134e+09         NaN     
Minority Interests                                 -2.338900e+07 -3.237200e+07  ... -2.613820e+08         NaN     
Net Income Including Noncontrolling Interests       1.670325e+09  1.621651e+09  ...  1.715516e+09         NaN     
Net Income Continuous Operations                    1.670325e+09  1.621651e+09  ...  1.715517e+09         NaN     
Tax Provision                                       8.946460e+08  8.884590e+08  ...  7.625350e+08         NaN     
Pretax Income                                       2.564971e+09  2.510110e+09  ...  2.478052e+09         NaN     
Other Non Operating Income Expenses                 4.179000e+06  1.571400e+07  ...  4.277000e+06         NaN     
Special Income Charges                                       NaN  0.000000e+00  ... -1.897730e+08         0.0     
Other Special Charges                                        NaN           NaN  ...  1.393650e+08         NaN     
Write Off                                                    NaN  0.000000e+00  ...  5.040800e+07         NaN     
Restructuring And Mergern Acquisition                        NaN  0.000000e+00  ...  0.000000e+00         NaN     
Net Non Operating Interest Income Expense           1.197520e+08  7.030900e+07  ...  1.877940e+08         NaN     
Total Other Finance Cost                            1.384000e+06  7.697000e+06  ...  9.278000e+06         NaN     
Interest Expense Non Operating                               NaN           NaN  ...  0.000000e+00  16447000.0     
Interest Income Non Operating                       1.211360e+08  7.800600e+07  ...  1.970720e+08         NaN     
Operating Income                                    2.269275e+09  2.111325e+09  ...  2.129805e+09         NaN     
Operating Expense                                   3.428722e+09  3.109101e+09  ...  2.339083e+09         NaN     
Gross Profit                                        5.697997e+09  5.220426e+09  ...  4.468888e+09         NaN     
Cost Of Revenue                                     5.870993e+09  4.917169e+09  ...  3.654398e+09         NaN     
Total Revenue                                       1.156899e+10  1.013760e+10  ...  8.123286e+09         NaN     
Operating Revenue                                   1.156899e+10  1.013760e+10  ...  8.123286e+09         NaN      

[45 rows x 5 columns]
Saving data to data\4765.T...
4765.Tの財務データをdataに保存しました。
2025-08-23 17:00:57,120 INFO 取得完了: 4765.T
2025-08-23 17:00:57,269 INFO --- AI財務分析一括処理 ---
分析実行: 4345.T
ChatGPT APIエラー: OPENAI_API_KEYが環境変数に設定されていません
分析実行: 3928.T
ChatGPT APIエラー: OPENAI_API_KEYが環境変数に設定されていません
分析実行: 4319.T
ChatGPT APIエラー: OPENAI_API_KEYが環境変数に設定されていません
分析実行: 4765.T
ChatGPT APIエラー: OPENAI_API_KEYが環境変数に設定されていません
2025-08-23 17:01:04,858 INFO 全処理完了
