#!/usr/bin/env python3
"""
CN Stock Official Announcement Fetcher Helper Script.
Directly queries Cninfo (巨潮资讯网 - China CSRC Designated Official Disclosure Portal)
to fetch official announcements, PDF download links, and release timestamps for A-share companies.

Zero-dependency standard Python engine utilizing Cninfo Official API.

Usage:
    python3 scripts/fetch_cn_announcements.py --stock 300476 --keyword 业绩预告
    python3 scripts/fetch_cn_announcements.py --stock 300308 --pageSize 5
"""

import os
import json
import datetime
import argparse
import sys
import urllib.request
import urllib.parse

def parse_args():
    parser = argparse.ArgumentParser(description="Fetch official A-share company announcements from Cninfo.")
    parser.add_argument("--stock", default="", help="Stock code (e.g. 300476, 300308, 002851)")
    parser.add_argument("--keyword", default="", help="Announcement search keyword (e.g. 业绩预告, 半年报, 合同)")
    parser.add_argument("--pageSize", type=int, default=5, help="Number of announcements to fetch (default: 5)")
    parser.add_argument("--output", default="cn_announcements.json", help="Output JSON filename")
    return parser.parse_args()

def fetch_cninfo_announcements(stock_code="", keyword="", page_size=5):
    """
    Queries Cninfo official JSON API gateway using urllib.
    Returns list of announcements with titles, timestamps, and direct PDF URLs.
    """
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
                    if time_stamp:
                        pub_date = datetime.datetime.fromtimestamp(time_stamp / 1000.0).strftime("%Y-%m-%d")

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
        print(f"[Error] Failed to fetch Cninfo announcements: {e}", file=sys.stderr)

    return announcements_list

def main():
    args = parse_args()
    print(f"[{datetime.datetime.now().isoformat()}] Querying Cninfo for stock='{args.stock}', keyword='{args.keyword}'...")
    
    results_list = fetch_cninfo_announcements(args.stock, args.keyword, args.pageSize)
    
    output_data = {
        "fetch_date": datetime.date.today().isoformat(),
        "query": {
            "stock": args.stock,
            "keyword": args.keyword,
            "pageSize": args.pageSize
        },
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
