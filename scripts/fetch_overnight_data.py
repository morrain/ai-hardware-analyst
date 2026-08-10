#!/usr/bin/env python3
"""
Daily Market Briefing Quotes Fetcher Helper Script (US & TW Tickers Focus).
Dynamically loads US and TW stock tickers from tickers.json (Single Source of Truth)
and fetches real stock quotes & volume using standard Python library (urllib).

High-Performance Hybrid Engine:
- US Tickers: Sina US Quotes Batch API (Zero 429 errors, millisecond response)
- TW Tickers: Yahoo v8 Chart API with automatic .TW / .TWO market suffix matching

Usage:
    python3 scripts/fetch_overnight_data.py --market all
    python3 scripts/fetch_overnight_data.py --output overnight_summary.json
"""

import os
import json
import datetime
import argparse
import sys
import time
import urllib.request
import urllib.parse

def parse_args():
    parser = argparse.ArgumentParser(description="Fetch daily market quotes & volume for US & TW AI hardware tickers.")
    parser.add_argument("--market", choices=["all", "us", "tw"], default="all",
                        help="Filter by specific market (default: all)")
    parser.add_argument("--output", default="overnight_summary.json",
                        help="Output JSON filename (default: overnight_summary.json)")
    parser.add_argument("--registry", default="tickers.json",
                        help="Path to tickers.json registry file")
    return parser.parse_args()

def load_tickers_from_json(json_path="tickers.json"):
    """
    Loads US and TW tickers from the Single Source of Truth tickers.json file.
    """
    if not os.path.exists(json_path):
        script_dir = os.path.dirname(os.path.abspath(__file__))
        json_path = os.path.join(os.path.dirname(script_dir), json_path)
    
    try:
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data.get("tickers", {})
    except Exception as e:
        print(f"[Error] Failed to load tickers registry from {json_path}: {e}", file=sys.stderr)
        return {}

def format_volume_str(vol, market):
    """
    Formats raw volume numbers into human-readable strings (e.g. 105.67M for US, 1.99万张 for TW).
    """
    if not vol:
        return "N/A"
    try:
        vol = float(vol)
        if market == "US":
            if vol >= 1e6:
                return f"{vol / 1e6:.2f}M"
            elif vol >= 1e3:
                return f"{vol / 1e3:.1f}K"
            return str(int(vol))
        elif market == "TW":
            lots = vol / 1000.0
            if lots >= 10000:
                return f"{lots / 10000.0:.2f}万张"
            elif lots >= 1:
                return f"{int(lots)}张"
            return f"{int(vol)}股"
    except Exception:
        pass
    return str(vol)

def fetch_us_quotes_sina_batch(us_tickers):
    """
    Fetches US quotes via Sina US Batch API (fast, reliable, zero 429 rate limit).
    """
    timestamp = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    if not us_tickers:
        return []

    gb_syms = [f"gb_{t['symbol'].lower()}" for t in us_tickers]
    api_url = f"http://hq.sinajs.cn/list={','.join(gb_syms)}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
        "Referer": "https://finance.sina.com.cn"
    }

    quotes_map = {}
    try:
        req = urllib.request.Request(api_url, headers=headers)
        with urllib.request.urlopen(req, timeout=8) as response:
            if response.status == 200:
                text = response.read().decode('gbk', errors='ignore')
                for line in text.strip().split('\n'):
                    if '=' in line and '"' in line:
                        sym_raw = line.split('=')[0].replace('var hq_str_gb_', '').upper()
                        fields = line.split('=')[1].strip(' ";\n\r').split(',')
                        if len(fields) >= 27:
                            cp = float(fields[1]) if fields[1] else None
                            ch_pct = float(fields[2]) if fields[2] else None
                            vol = float(fields[10]) if fields[10] else None
                            pp = float(fields[26]) if fields[26] else None
                            
                            quotes_map[sym_raw] = {
                                "close_price": round(cp, 2) if cp else None,
                                "prev_close": round(pp, 2) if pp else None,
                                "pct_change_pct": round(ch_pct, 2) if ch_pct is not None else None,
                                "volume_raw": vol,
                                "volume_str": format_volume_str(vol, "US")
                            }
    except Exception as e:
        print(f"[Warning] Sina US Batch fetch error: {e}", file=sys.stderr)

    formatted = []
    for t in us_tickers:
        sym = t["symbol"]
        info = quotes_map.get(sym.upper(), {})
        cp = info.get("close_price")
        pp = info.get("prev_close")
        pct = info.get("pct_change_pct")
        vol_str = info.get("volume_str", "N/A")
        
        status = "exact_physical_quote" if cp is not None else "api_fetch_failed"
        formatted.append({
            "symbol": sym,
            "full_symbol": t.get("full_symbol", f"{sym}.US"),
            "name": t["name"],
            "name_cn": t.get("name_cn", t["name"]),
            "market": "US",
            "sector": t.get("sector", ""),
            "sector_cn": t.get("sector_cn", ""),
            "close_price": cp,
            "prev_close": pp,
            "pct_change_pct": pct,
            "volume_raw": info.get("volume_raw"),
            "volume_str": vol_str,
            "timestamp": timestamp,
            "source": "Sina US Batch API Engine",
            "status": status
        })
    return formatted

def fetch_single_tw_quote(t):
    """
    Fetches single TW stock quote trying .TW then .TWO suffixes.
    """
    sym = t["symbol"]
    timestamp = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"}

    close_p, prev_p, pct_p, raw_vol = None, None, None, None
    vol_str = "N/A"
    status = "api_fetch_failed"

    suffixes = [".TW", ".TWO"]
    # Check if listed in OTC (.TWO)
    otc_symbols = ["6223", "6510", "6515", "3324", "3017", "6805", "5274", "6274"]
    if sym in otc_symbols:
        suffixes = [".TWO", ".TW"]

    for suf in suffixes:
        url = f"https://query1.finance.yahoo.com/v8/finance/chart/{sym}{suf}?interval=1d"
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=5) as response:
                if response.status == 200:
                    data = json.loads(response.read().decode('utf-8'))
                    result_list = data.get("chart", {}).get("result", [])
                    if result_list:
                        meta = result_list[0].get("meta", {})
                        close_p = meta.get("regularMarketPrice")
                        prev_p = meta.get("chartPreviousClose") or meta.get("previousClose")
                        raw_vol = meta.get("regularMarketVolume")
                        if close_p is not None and prev_p is not None and prev_p > 0:
                            close_p = round(close_p, 2)
                            prev_p = round(prev_p, 2)
                            pct_p = round(((close_p - prev_p) / prev_p) * 100, 2)
                            vol_str = format_volume_str(raw_vol, "TW")
                            status = "exact_physical_quote"
                            break
        except Exception:
            pass

    return {
        "symbol": sym,
        "full_symbol": t.get("full_symbol", f"{sym}.TW"),
        "name": t["name"],
        "name_cn": t.get("name_cn", t["name"]),
        "market": "TW",
        "sector": t.get("sector", ""),
        "sector_cn": t.get("sector_cn", ""),
        "close_price": close_p,
        "prev_close": prev_p,
        "pct_change_pct": pct_p,
        "volume_raw": raw_vol,
        "volume_str": vol_str,
        "timestamp": timestamp,
        "source": "Yahoo v8 TW Engine",
        "status": status
    }

def main():
    args = parse_args()
    print(f"[{datetime.datetime.now().isoformat()}] Fetching daily market quotes & volume (Market: {args.market})...")
    ticker_registry = load_tickers_from_json(args.registry)
    
    us_tickers = ticker_registry.get("us", []) if args.market in ["all", "us"] else []
    tw_tickers = ticker_registry.get("tw", []) if args.market in ["all", "tw"] else []
    
    # 1. Fetch US in single batch via Sina
    us_quotes = fetch_us_quotes_sina_batch(us_tickers)
    
    # 2. Fetch TW smoothly with slight delay
    tw_quotes = []
    for t in tw_tickers:
        tw_quotes.append(fetch_single_tw_quote(t))
        time.sleep(0.08)  # smooth rate limiting
    
    us_exact = sum(1 for q in us_quotes if q["close_price"] is not None)
    tw_exact = sum(1 for q in tw_quotes if q["close_price"] is not None)
    
    results = {
        "fetch_date": datetime.date.today().isoformat(),
        "market_filter": args.market,
        "status": "success",
        "single_source_of_truth": args.registry,
        "engine": "Hybrid Sina US & Yahoo TW Engine",
        "counts": {
            "us_total": len(us_quotes),
            "us_exact_fetched": us_exact,
            "tw_total": len(tw_quotes),
            "tw_exact_fetched": tw_exact,
            "total_quotes": len(us_quotes) + len(tw_quotes)
        },
        "quotes": {
            "us": us_quotes,
            "tw": tw_quotes
        }
    }
    
    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    print(f"Successfully processed {len(us_quotes)} US quotes ({us_exact}/{len(us_quotes)} exact) and {len(tw_quotes)} TW quotes ({tw_exact}/{len(tw_quotes)} exact).")
    print(f"Data summary saved to {args.output}")

if __name__ == "__main__":
    main()
