#!/usr/bin/env python3
"""社交媒体抓取工具"""

import argparse
import sys

def main():
    parser = argparse.ArgumentParser(description="抓取社交媒体内容")
    parser.add_argument("--handle", required=True, help="账号 Handle（如 @username）")
    parser.add_argument("--limit", type=int, default=500, help="抓取条数")
    parser.add_argument("--output", required=True, help="输出文件路径")
    args = parser.parse_args()

    print(f"[social_scraper] Fetching: {args.handle}")
    print(f"[social_scraper] Output: {args.output}")
    # TODO: 实现社交媒体抓取逻辑
    sys.exit(0)

if __name__ == "__main__":
    main()
