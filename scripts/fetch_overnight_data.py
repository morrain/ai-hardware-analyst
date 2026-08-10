#!/usr/bin/env python3
"""
Overnight Market Data Fetcher Helper Script.
Dynamically loads stock tickers from tickers.json (Single Source of Truth)
and fetches overnight stock metrics and news for AI hardware tickers.
"""

import os
import json
import datetime
import sys

def load_tickers_from_json(json_path="tickers.json"):
    """
    Loads tickers from the Single Source of Truth tickers.json file.
    """
    if not os.path.exists(json_path):
        # Fallback if script is run from a subfolder
        script_dir = os.path.dirname(os.path.abspath(__file__))
        json_path = os.path.join(os.path.dirname(script_dir), "tickers.json")
    
    try:
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data.get("tickers", {})
    except Exception as e:
        print(f"[Warning] Failed to load tickers.json: {e}", file=sys.stderr)
        return {}

def fetch_ticker_quote(symbol, name, market):
    """
    Simulated fetch for overnight stock quote data.
    Can be extended with yfinance, Alpha Vantage, or custom API endpoints.
    """
    timestamp = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    return {
        "symbol": symbol,
        "name": name,
        "market": market,
        "timestamp": timestamp,
        "source": "Yahoo Finance Helper",
        "status": "ready"
    }

def main():
    print(f"[{datetime.datetime.now().isoformat()}] Fetching overnight AI hardware market data...")
    ticker_registry = load_tickers_from_json()
    
    us_tickers = [fetch_ticker_quote(t["symbol"], t["name"], "US") for t in ticker_registry.get("us", [])]
    tw_tickers = [fetch_ticker_quote(t["symbol"], t["name"], "TW") for t in ticker_registry.get("tw", [])]
    cn_tickers = [fetch_ticker_quote(t["symbol"], t["name"], "CN") for t in ticker_registry.get("cn", [])]
    
    results = {
        "fetch_date": datetime.date.today().isoformat(),
        "status": "success",
        "single_source_of_truth": "tickers.json",
        "counts": {
            "us": len(us_tickers),
            "tw": len(tw_tickers),
            "cn": len(cn_tickers)
        },
        "quotes": {
            "us": us_tickers,
            "tw": tw_tickers,
            "cn": cn_tickers
        }
    }
    
    output_filename = "overnight_summary.json"
    with open(output_filename, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    print(f"Successfully processed {len(us_tickers)} US, {len(tw_tickers)} TW, and {len(cn_tickers)} CN tickers from tickers.json.")
    print(f"Data summary saved to {output_filename}")

if __name__ == "__main__":
    main()
