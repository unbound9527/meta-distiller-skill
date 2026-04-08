#!/usr/bin/env python3
"""视频字幕提取工具"""

import argparse
import sys

def main():
    parser = argparse.ArgumentParser(description="提取视频字幕")
    parser.add_argument("--url", required=True, help="视频 URL（YouTube/Bilibili）")
    parser.add_argument("--lang", default="en,zh", help="优先语言（逗号分隔）")
    parser.add_argument("--output", required=True, help="输出文件路径")
    args = parser.parse_args()

    print(f"[youtube_parser] Fetching: {args.url}")
    print(f"[youtube_parser] Output: {args.output}")
    # TODO: 实现字幕下载和提取逻辑
    sys.exit(0)

if __name__ == "__main__":
    main()
