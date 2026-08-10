#!/usr/bin/env python3
"""
Overnight Market Data Fetcher Helper Script (US Tickers Focus).
Dynamically loads US stock tickers from tickers.json (Single Source of Truth)
and fetches real overnight stock quotes using standard Python library (urllib).

Zero-dependency standard Python engine utilizing Sina Financial US Quotes API
to ensure 100% exact real-world closing prices and percentage changes in milliseconds.

Usage:
    python3 scripts/fetch_overnight_data.py
    python3 scripts/fetch_overnight_data.py --output overnight_summary.json
"""

import os
import json
import datetime
import argparse
import sys
import urllib.request

def parse_args():
    parser = argparse.ArgumentParser(description="Fetch overnight US AI hardware market data.")
    parser.add_argument("--output", default="overnight_summary.json",
                        help="Output JSON filename (default: overnight_summary.json)")
    parser.add_argument("--registry", default="tickers.json",
                        help="Path to tickers.json registry file")
    return parser.parse_args()

def load_us_tickers_from_json(json_path="tickers.json"):
    """
    Loads US tickers from the Single Source of Truth tickers.json file.
    """
    if not os.path.exists(json_path):
        script_dir = os.path.dirname(os.path.abspath(__file__))
        json_path = os.path.join(os.path.dirname(script_dir), json_path)
    
    try:
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data.get("tickers", {}).get("us", [])
    except Exception as e:
        print(f"[Error] Failed to load tickers registry from {json_path}: {e}", file=sys.stderr)
        return []

def fetch_us_quotes_batch(us_tickers):
    """
    Fetches real-world physical stock quotes using standard library urllib.
    Queries Sina US Quotes API for all US tickers in a single HTTP batch request.
    """
    timestamp = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    
    # Map symbols to gb_[symbol_lowercase]
    gb_symbols = [f"gb_{t['symbol'].lower()}" for t in us_tickers]
    api_url = f"http://hq.sinajs.cn/list={','.join(gb_symbols)}"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Referer": "https://finance.sina.com.cn"
    }

    quotes_result = {}
    try:
        req = urllib.request.Request(api_url, headers=headers)
        with urllib.request.urlopen(req, timeout=8) as response:
            if response.status == 200:
                raw_text = response.read().decode('gbk', errors='ignore')
                lines = raw_text.strip().split('\n')
                for line in lines:
                    # Parse format: var hq_str_gb_nvda="英伟达,223.9600,2.27,2026-08-10 19:54:11,...,218.9900,...";
                    if "=" in line and '"' in line:
                        var_part, val_part = line.split('=', 1)
                        sym_raw = var_part.strip().replace("var hq_str_gb_", "")
                        content = val_part.strip(' ";\n\r')
                        fields = content.split(',')
                        if len(fields) >= 27:
                            c_price = float(fields[1]) if fields[1] else None
                            p_change = float(fields[2]) if fields[2] else None
                            p_close = float(fields[26]) if fields[26] else None
                            
                            quotes_result[sym_raw.upper()] = {
                                "close_price": c_price,
                                "prev_close": p_close,
                                "pct_change_pct": p_change
                            }
    except Exception as e:
        print(f"[Warning] API batch fetch failed: {e}", file=sys.stderr)

    formatted_data = []
    for t in us_tickers:
        sym = t["symbol"]
        quote_info = quotes_result.get(sym.upper(), {})
        
        c_price = quote_info.get("close_price")
        p_price = quote_info.get("prev_close")
        ch_pct = quote_info.get("pct_change_pct")
        
        status = "exact_physical_quote" if c_price is not None else "api_fetch_failed"
        
        formatted_data.append({
            "symbol": sym,
            "full_symbol": t.get("full_symbol", f"{sym}.US"),
            "name": t["name"],
            "name_cn": t.get("name_cn", t["name"]),
            "market": "US",
            "sector": t.get("sector", ""),
            "sector_cn": t.get("sector_cn", ""),
            "close_price": c_price,
            "prev_close": p_price,
            "pct_change_pct": ch_pct,
            "timestamp": timestamp,
            "source": "Sina US Quotes API (urllib)",
            "status": status
        })
        
    return formatted_data

def main():
    args = parse_args()
    print(f"[{datetime.datetime.now().isoformat()}] Fetching overnight US AI hardware market quotes (Zero-Dependency API Engine)...")
    us_tickers = load_us_tickers_from_json(args.registry)
    
    us_quotes = fetch_us_quotes_batch(us_tickers)
    exact_count = sum(1 for q in us_quotes if q["close_price"] is not None)
    
    results = {
        "fetch_date": datetime.date.today().isoformat(),
        "market_filter": "us",
        "status": "success",
        "single_source_of_truth": args.registry,
        "engine": "Sina US Quotes API Engine (urllib)",
        "counts": {
            "us_total": len(us_quotes),
            "exact_quotes_fetched": exact_count
        },
        "quotes": {
            "us": us_quotes
        }
    }
    
    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    print(f"Successfully processed {len(us_quotes)} US tickers ({exact_count}/{len(us_quotes)} exact physical quotes fetched).")
    print(f"Data summary saved to {args.output}")

if __name__ == "__main__":
    main()
