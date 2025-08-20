#!/usr/bin/env python
"""
edinet2data.py
EDINET v2 documents API 専用。APIキーをスクリプト内に埋め込み、取得結果を pandas DataFrame に整形・保存するツール。
Usage:
  python edinet2data.py --start 2024-08-10 --end 2024-08-15 --out edinet.csv
  python edinet2data.py 7203 2024-05-17 --out out.csv
"""
import argparse
import datetime
import sys
import requests
import pandas as pd
from typing import List, Dict, Any

V2_URL = "https://disclosure.edinet-fsa.go.jp/api/v2/documents.json"
API_KEY = "aaa"  # スクリプト内に埋め込み


def fetch_documents_v2(date: str, sec_code: str = None, timeout: int = 20) -> Dict[str, Any]:
    params = {"date": date, "type": 2}
    if sec_code:
        params["secCode"] = str(sec_code)
    headers = {
        "Subscription-Key": API_KEY,
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) edinet-client/1.0",
        "Accept": "application/json",
    }
    resp = requests.get(V2_URL, params=params, headers=headers, timeout=timeout)
    try:
        resp.raise_for_status()
    except requests.exceptions.HTTPError:
        print(f"HTTP error {resp.status_code}", file=sys.stderr)
        print(resp.text[:2000], file=sys.stderr)
        raise
    print("--- API raw response ---")
    print(resp.json())
    print("------------------------")
    return resp.json()


def extract_items_from_response(resp_json: Dict[str, Any]) -> List[Dict[str, Any]]:
    if isinstance(resp_json, dict):
        for key in ("results", "data", "items", "documents"):
            if key in resp_json and isinstance(resp_json[key], list):
                return resp_json[key]
        for v in resp_json.values():
            if isinstance(v, list):
                return v
    if isinstance(resp_json, list):
        return resp_json
    return []


def items_to_dataframe(items: List[Dict[str, Any]]) -> pd.DataFrame:
    if not items:
        return pd.DataFrame()
    df = pd.json_normalize(items)
    candidates = [
        "docID", "documentId", "docTypeCode", "docTypeName", "docDescription",
        "submitDate", "filerName", "secCode", "filerCode", "formCode",
    ]
    cols = [c for c in candidates if c in df.columns]
    if not cols:
        cols = df.columns.tolist()
    df = df[cols].copy()
    for dcol in ("submitDate", "date", "receivedDate"):
        if dcol in df.columns:
            try:
                df[dcol] = pd.to_datetime(df[dcol], errors="coerce")
            except Exception:
                pass
    if "secCode" in df.columns:
        df["secCode"] = df["secCode"].astype(str).str.extract(r"(\d+)")[0].fillna("")
        df["secCode"] = df["secCode"].apply(lambda s: s.zfill(4) if s.isdigit() else s)
    return df


def summarize_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return pd.DataFrame()
    key = "docTypeName" if "docTypeName" in df.columns else ("docTypeCode" if "docTypeCode" in df.columns else df.columns[0])
    summary = df.groupby(key).size().reset_index(name="count").sort_values("count", ascending=False)
    return summary


def validate_date(date_text: str) -> str:
    try:
        dt = datetime.date.fromisoformat(date_text)
    except Exception as e:
        raise argparse.ArgumentTypeError(f"invalid date: {e}")
    if dt > datetime.date.today():
        raise argparse.ArgumentTypeError("date must not be in the future")
    return date_text


def daterange(start_date, end_date):
    for n in range((end_date - start_date).days + 1):
        yield start_date + datetime.timedelta(n)


def parse_args(argv=None):
    p = argparse.ArgumentParser(description="Fetch EDINET v2 documents and convert to DataFrame")
    p.add_argument("sec_code", nargs="?", help="証券コード（例:7203）。省略可。")
    p.add_argument("date", nargs="?", type=validate_date, help="取得日 yyyy-mm-dd。省略時は昨日。")
    p.add_argument("--out", dest="out", help="出力 CSV パス。省略で標準出力に表示")
    p.add_argument("--start", dest="start", help="開始日 yyyy-mm-dd (範囲指定時)" )
    p.add_argument("--end", dest="end", help="終了日 yyyy-mm-dd (範囲指定時)" )
    return p.parse_args(argv)


def main(argv=None):
    args = parse_args(argv)
    sec_code = args.sec_code
    date = args.date or (datetime.date.today() - datetime.timedelta(days=1)).isoformat()
    start = args.start
    end = args.end

    if start and end:
        try:
            start_date = datetime.date.fromisoformat(start)
            end_date = datetime.date.fromisoformat(end)
        except Exception as e:
            print(f"invalid start/end date: {e}", file=sys.stderr)
            sys.exit(1)
        all_dfs = []
        for d in daterange(start_date, end_date):
            dstr = d.isoformat()
            print(f"Fetching EDINET v2 documents for date={dstr} sec_code={sec_code}")
            try:
                resp = fetch_documents_v2(date=dstr, sec_code=sec_code)
            except Exception as e:
                print(f"Request failed for {dstr}: {e}", file=sys.stderr)
                continue
            items = extract_items_from_response(resp)
            df = items_to_dataframe(items)
            if not df.empty:
                df["_date"] = dstr
                all_dfs.append(df)
        if all_dfs:
            df_all = pd.concat(all_dfs, ignore_index=True)
            print(f"Total rows: {len(df_all)}")
            summary = summarize_dataframe(df_all)
            print("-- summary by document type --")
            print(summary.to_string(index=False))
            if args.out:
                df_all.to_csv(args.out, index=False)
                print(f"Saved CSV to {args.out}")
            else:
                with pd.option_context('display.max_rows', 20, 'display.max_columns', None):
                    print(df_all.head(50).to_string(index=False))
        else:
            print("No data found in the specified date range.")
        return

    print(f"Fetching EDINET v2 documents for date={date} sec_code={sec_code}")
    try:
        resp = fetch_documents_v2(date=date, sec_code=sec_code)
    except Exception as e:
        print(f"Request failed: {e}", file=sys.stderr)
        sys.exit(1)
    items = extract_items_from_response(resp)
    df = items_to_dataframe(items)
    if df.empty:
        print("no items returned for the query")
    else:
        print("result rows:", len(df))
        summary = summarize_dataframe(df)
        print("-- summary by document type --")
        print(summary.to_string(index=False))
        if args.out:
            df.to_csv(args.out, index=False)
            print(f"Saved CSV to {args.out}")
        else:
            with pd.option_context('display.max_rows', 20, 'display.max_columns', None):
                print(df.head(50).to_string(index=False))


if __name__ == "__main__":
    main()