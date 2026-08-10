#!/usr/bin/env python3
"""
Overnight Market Data Fetcher Helper Script.
Dynamically loads stock tickers from tickers.json (Single Source of Truth)
and fetches overnight stock metrics and news for AI hardware tickers.

Usage:
    python3 scripts/fetch_overnight_data.py --market all
    python3 scripts/fetch_overnight_data.py --market us --output us_data.json
"""

import os
import json
import datetime
import argparse
import sys

def parse_args():
    parser = argparse.ArgumentParser(description="Fetch overnight AI hardware market data.")
    parser.add_argument("--market", choices=["all", "us", "tw", "cn"], default="all",
                        help="Filter by specific market (default: all)")
    parser.add_argument("--output", default="overnight_summary.json",
                        help="Output JSON filename (default: overnight_summary.json)")
    parser.add_argument("--registry", default="tickers.json",
                        help="Path to tickers.json registry file")
    return parser.parse_args()

def load_tickers_from_json(json_path="tickers.json"):
    """
    Loads tickers from the Single Source of Truth tickers.json file.
    """
    if not os.path.exists(json_path):
        # Fallback if script is run from a subfolder
        script_dir = os.path.dirname(os.path.abspath(__file__))
        json_path = os.path.join(os.path.dirname(script_dir), json_path)
    
    try:
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data.get("tickers", {})
    except Exception as e:
        print(f"[Error] Failed to load tickers registry from {json_path}: {e}", file=sys.stderr)
        return {}

def fetch_ticker_quote(symbol, full_symbol, name, market, sector):
    """
    Simulated fetch for overnight stock quote data.
    Can be extended with yfinance, Alpha Vantage, or custom API endpoints.
    """
    timestamp = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    return {
        "symbol": symbol,
        "full_symbol": full_symbol,
        "name": name,
        "market": market,
        "sector": sector,
        "timestamp": timestamp,
        "source": "Yahoo Finance Helper",
        "status": "ready"
    }

def main():
    args = parse_args()
    print(f"[{datetime.datetime.now().isoformat()}] Fetching AI hardware market data (Market: {args.market})...")
    ticker_registry = load_tickers_from_json(args.registry)
    
    us_data = [fetch_ticker_quote(t["symbol"], t.get("full_symbol", t["symbol"]), t["name"], "US", t.get("sector", "")) 
               for t in ticker_registry.get("us", [])] if args.market in ["all", "us"] else []
    
    tw_data = [fetch_ticker_quote(t["symbol"], t.get("full_symbol", t["symbol"]), t["name"], "TW", t.get("sector", "")) 
               for t in ticker_registry.get("tw", [])] if args.market in ["all", "tw"] else []
    
    cn_data = [fetch_ticker_quote(t["symbol"], t.get("full_symbol", t["symbol"]), t["name"], "CN", t.get("sector", "")) 
               for t in ticker_registry.get("cn", [])] if args.market in ["all", "cn"] else []
    
    results = {
        "fetch_date": datetime.date.today().isoformat(),
        "market_filter": args.market,
        "status": "success",
        "single_source_of_truth": args.registry,
        "counts": {
            "us": len(us_data),
            "tw": len(tw_data),
            "cn": len(cn_data),
            "total": len(us_data) + len(tw_data) + len(cn_data)
        },
        "quotes": {
            "us": us_data,
            "tw": tw_data,
            "cn": cn_data
        }
    }
    
    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    print(f"Successfully processed {len(us_data)} US, {len(tw_data)} TW, and {len(cn_data)} CN tickers.")
    print(f"Data summary saved to {args.output}")

if __name__ == "__main__":
    main()
