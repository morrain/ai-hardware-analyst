#!/usr/bin/env python3
"""
CN Stock Official Announcement Fetcher Helper Script.
Directly queries Cninfo (巨潮资讯网 - China CSRC Designated Official Disclosure Portal)
to fetch official announcements, PDF download links, and release timestamps for A-share companies.

Supports single stock lookup or batch lookup for CN tickers defined in tickers.json.

Usage:
    python3 scripts/fetch_cn_announcements.py --stock 300476 --keyword 业绩预告
    python3 scripts/fetch_cn_announcements.py --batch --days 2 --output cn_today_announcements.json
"""

import os
import json
import datetime
import argparse
import sys
import urllib.request
import urllib.parse
from concurrent.futures import ThreadPoolExecutor

def parse_args():
    parser = argparse.ArgumentParser(description="Fetch official A-share company announcements from Cninfo.")
    parser.add_argument("--stock", default="", help="Stock code (e.g. 300476, 300308, 002851)")
    parser.add_argument("--keyword", default="", help="Announcement search keyword (e.g. 业绩预告, 半年报, 合同)")
    parser.add_argument("--pageSize", type=int, default=5, help="Number of announcements to fetch (default: 5)")
    parser.add_argument("--days", type=int, default=2, help="Filter announcements published within N days (default: 2)")
    parser.add_argument("--batch", action="store_true", help="Batch query all CN tickers defined in tickers.json")
    parser.add_argument("--registry", default="tickers.json", help="Path to tickers.json registry")
    parser.add_argument("--output", default="cn_announcements.json", help="Output JSON filename")
    return parser.parse_args()

def load_cn_tickers_from_json(json_path="tickers.json"):
    if not os.path.exists(json_path):
        script_dir = os.path.dirname(os.path.abspath(__file__))
        json_path = os.path.join(os.path.dirname(script_dir), json_path)
    try:
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data.get("tickers", {}).get("cn", [])
    except Exception as e:
        print(f"[Error] Failed to load CN tickers from {json_path}: {e}", file=sys.stderr)
        return []

def fetch_cninfo_announcements(stock_code="", keyword="", page_size=5, days_filter=None):
    url = "http://www.cninfo.com.cn/new/hisAnnouncement/query"
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Referer": "http://www.cninfo.com.cn/new/commonUrl?url=disclosure/list/notice",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"
    }

    search_term = keyword
    if stock_code and not keyword:
        search_term = stock_code
    elif stock_code and keyword:
        search_term = f"{stock_code} {keyword}"

    params = {
        "pageNum": 1,
        "pageSize": page_size,
        "column": "szse",
        "tabName": "fulltext",
        "plate": "",
        "stock": "",
        "searchkey": search_term,
        "secid": "",
        "category": "",
        "trade": "",
        "seDate": ""
    }

    data = urllib.parse.urlencode(params).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers=headers)

    announcements_list = []
    now_dt = datetime.datetime.now()

    try:
        with urllib.request.urlopen(req, timeout=8) as response:
            if response.status == 200:
                raw_text = response.read().decode("utf-8", errors="ignore")
                json_res = json.loads(raw_text)
                anns = json_res.get("announcements") or []
                
                for a in anns:
                    sec_code = a.get("secCode")
                    sec_name = a.get("secName")
                    raw_title = a.get("announcementTitle") or ""
                    clean_title = raw_title.replace("<em>", "").replace("</em>", "").strip()
                    adj_path = a.get("adjunctUrl")
                    
                    pdf_url = f"http://static.cninfo.com.cn/{adj_path}" if adj_path else ""
                    time_stamp = a.get("announcementTime")
                    pub_date = ""
                    pub_dt = None
                    if time_stamp:
                        pub_dt = datetime.datetime.fromtimestamp(time_stamp / 1000.0)
                        pub_date = pub_dt.strftime("%Y-%m-%d")

                    # Check days filter if specified
                    if days_filter is not None and pub_dt is not None:
                        delta_days = (now_dt.date() - pub_dt.date()).days
                        if delta_days > days_filter:
                            continue

                    announcements_list.append({
                        "stock_code": sec_code,
                        "stock_name": sec_name,
                        "title": clean_title,
                        "pub_date": pub_date,
                        "announcement_id": a.get("announcementId"),
                        "pdf_url": pdf_url,
                        "source": "Cninfo Official Disclosure Portal (cninfo.com.cn)"
                    })
    except Exception as e:
        print(f"[Warning] Failed to fetch Cninfo for stock '{stock_code}': {e}", file=sys.stderr)

    return announcements_list

def main():
    args = parse_args()
    results_list = []

    if args.batch:
        cn_tickers = load_cn_tickers_from_json(args.registry)
        print(f"[{datetime.datetime.now().isoformat()}] Batch querying Cninfo for {len(cn_tickers)} CN tickers (Days filter <= {args.days}d)...")
        
        def fetch_single(ticker_info):
            code = ticker_info["symbol"]
            return fetch_cninfo_announcements(stock_code=code, keyword="", page_size=5, days_filter=args.days)

        with ThreadPoolExecutor(max_workers=8) as executor:
            batch_results = list(executor.map(fetch_single, cn_tickers))
            for res in batch_results:
                results_list.extend(res)
    else:
        print(f"[{datetime.datetime.now().isoformat()}] Querying Cninfo for stock='{args.stock}', keyword='{args.keyword}'...")
        results_list = fetch_cninfo_announcements(args.stock, args.keyword, args.pageSize, days_filter=args.days if args.stock else None)

    output_data = {
        "fetch_date": datetime.date.today().isoformat(),
        "query_mode": "batch" if args.batch else "single",
        "days_filter": args.days,
        "total_fetched": len(results_list),
        "source": "cninfo.com.cn (中国证监会指定法定信息披露平台)",
        "announcements": results_list
    }

    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(output_data, f, ensure_ascii=False, indent=2)

    print(f"Successfully fetched {len(results_list)} official announcements from Cninfo.")
    print(f"Results saved to {args.output}")

if __name__ == "__main__":
    main()
