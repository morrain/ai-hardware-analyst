#!/usr/bin/env python3
"""
Taiwan MOPS Monthly Revenue Fetcher.
Fetches official monthly revenue data from TWSE and TPEx Open Data API.
Automatically filters for TW tickers defined in tickers.json.

Examples:
    python3 scripts/fetch_tw_mops_revenue.py --output -
"""

import os
import sys
import json
import argparse
import urllib.request
import time
import datetime
from concurrent.futures import ThreadPoolExecutor

TWSE_URL = "https://openapi.twse.com.tw/v1/opendata/t187ap05_L"
TPEX_URL = "https://www.tpex.org.tw/openapi/v1/mopsfin_t187ap05_O"

def parse_args():
    parser = argparse.ArgumentParser(description="Fetch Taiwan monthly revenue data from TWSE/TPEx OpenData.")
    parser.add_argument("--registry", default="tickers.json", help="Path to tickers.json registry")
    parser.add_argument("--output", default="tw_mops_revenue.json", help="Output JSON filename (use '-' for stdout)")
    return parser.parse_args()

def load_tw_tickers(json_path="tickers.json"):
    if not os.path.exists(json_path):
        script_dir = os.path.dirname(os.path.abspath(__file__))
        json_path = os.path.join(os.path.dirname(script_dir), json_path)
    try:
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data.get("tickers", {}).get("tw", [])
    except Exception as e:
        print(f"[Error] Failed to load TW tickers from {json_path}: {e}", file=sys.stderr)
        return []

def fetch_opendata(url, name="TWSE"):
    for attempt in range(3):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"})
            with urllib.request.urlopen(req, timeout=20) as response:
                if response.status == 200:
                    raw_text = response.read().decode('utf-8', errors='ignore')
                    return json.loads(raw_text)
        except Exception as e:
            if attempt == 2:
                print(f"[Warning] Failed to fetch {name} OpenData: {e}", file=sys.stderr)
            time.sleep(2)
    return []

def safe_float(val, default=None):
    try:
        return float(val)
    except (ValueError, TypeError):
        return default

def convert_minguo_to_ym(minguo_str):
    if not minguo_str or len(minguo_str) < 4:
        return minguo_str
    try:
        year = int(minguo_str[:-2]) + 1911
        month = int(minguo_str[-2:])
        return f"{year}-{month:02d}"
    except ValueError:
        return minguo_str

def main():
    args = parse_args()
    tw_tickers = load_tw_tickers(args.registry)
    if not tw_tickers:
        print("[Error] No TW tickers found in registry.", file=sys.stderr)
        sys.exit(1)
        
    target_symbols = {t["symbol"]: t for t in tw_tickers}
    
    print(f"[{datetime.datetime.now().isoformat()}] Fetching TWSE & TPEx Open Data...", file=sys.stderr)
    
    with ThreadPoolExecutor(max_workers=2) as executor:
        f_twse = executor.submit(fetch_opendata, TWSE_URL, "TWSE")
        f_tpex = executor.submit(fetch_opendata, TPEX_URL, "TPEx")
        twse_data = f_twse.result()
        tpex_data = f_tpex.result()
        
    all_data = twse_data + tpex_data
    
    results = []
    
    for row in all_data:
        sym = row.get("公司代號", "").strip()
        if sym in target_symbols:
            t_info = target_symbols[sym]
            
            # Convert revenue from thousands to billions (NT$ Billion)
            raw_rev = safe_float(row.get("營業收入-當月營收"))
            rev_bn = round(raw_rev / 100000.0, 2) if raw_rev is not None else None
            
            raw_ytd = safe_float(row.get("累計營業收入-當月累計營收"))
            ytd_bn = round(raw_ytd / 100000.0, 2) if raw_ytd is not None else None
            
            data_ym = convert_minguo_to_ym(row.get("資料年月"))
            
            results.append({
                "symbol": sym,
                "full_symbol": t_info.get("full_symbol", f"{sym}.TW"),
                "name": t_info.get("name", row.get("公司名稱")),
                "name_cn": t_info.get("name_cn", row.get("公司名稱")),
                "market": "TW",
                "data_period": data_ym,
                "revenue_bn_ntd": rev_bn,
                "mom_pct": safe_float(row.get("營業收入-上月比較增減(%)")),
                "yoy_pct": safe_float(row.get("營業收入-去年同月增減(%)")),
                "ytd_revenue_bn_ntd": ytd_bn,
                "ytd_yoy_pct": safe_float(row.get("累計營業收入-前期比較增減(%)")),
                "source": "TWSE/TPEx OpenData"
            })
            
    output_data = {
        "fetch_date": datetime.date.today().isoformat(),
        "query_mode": "batch",
        "total_fetched": len(results),
        "source": "mops.twse.com.tw (公开资讯观测站)",
        "unit": "NT$ Billion (亿元新台币)",
        "revenues": results
    }

    if args.output == "-":
        print(json.dumps(output_data, ensure_ascii=False, indent=2))
    else:
        with open(args.output, "w", encoding="utf-8") as f:
            json.dump(output_data, f, ensure_ascii=False, indent=2)
        print(f"Successfully fetched monthly revenue for {len(results)} TW stocks.", file=sys.stderr)

if __name__ == "__main__":
    main()
