#!/usr/bin/env python3
"""长文本分块处理工具"""

import argparse
import sys

def main():
    parser = argparse.ArgumentParser(description="长文本分块处理")
    parser.add_argument("--file", required=True, help="输入文件路径（PDF/TXT/EPUB）")
    parser.add_argument("--extract-mode", default="first-person-logic",
                        choices=["first-person-logic", "all", "summary"],
                        help="提取模式")
    parser.add_argument("--output", required=True, help="输出文件路径")
    args = parser.parse_args()

    print(f"[corpus_chunker] Processing: {args.file}")
    print(f"[corpus_chunker] Mode: {args.extract_mode}")
    print(f"[corpus_chunker] Output: {args.output}")
    # TODO: 实现文本提取和分块逻辑
    sys.exit(0)

if __name__ == "__main__":
    main()
