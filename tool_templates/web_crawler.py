#!/usr/bin/env python3
"""网页正文爬取工具"""

import argparse
import sys

def main():
    parser = argparse.ArgumentParser(description="爬取网页正文内容")
    parser.add_argument("--url", required=True, help="目标网页 URL")
    parser.add_argument("--output", required=True, help="输出文件路径")
    args = parser.parse_args()

    # 实现：使用 requests + BeautifulSoup 抓取并清洗正文
    # 提取 <article> 或主要内容区块，去除广告/导航/脚本
    print(f"[web_crawler] Fetching: {args.url}")
    print(f"[web_crawler] Output: {args.output}")
    # TODO: 实现实际爬取逻辑
    sys.exit(0)

if __name__ == "__main__":
    main()
