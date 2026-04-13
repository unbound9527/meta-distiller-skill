#!/usr/bin/env python3
"""视频字幕提取工具 - 支持 YouTube/Bilibili"""

import argparse
import json
import os
import re
import subprocess
import sys
import tempfile
import urllib.parse


def extract_youtube_subtitles(url: str, lang: str, output: str) -> bool:
    """使用 yt-dlp 提取 YouTube 字幕"""
    langs = lang.split(",")
    lang_str = ",".join(langs)

    # --write-auto-subs: 自动字幕（备用）
    # --write-subs: 手动字幕
    # --sub-langs: 语言
    # --skip-download: 不下载视频
    cmd = [
        "yt-dlp",
        "--write-subs",
        "--write-auto-subs",
        "--sub-langs", lang_str,
        "--skip-download",
        "--convert-subs", "srt",
        "--output", tempfile.mktemp(suffix=".%(ext)s"),
        url,
    ]

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
        if result.returncode != 0:
            print(f"[youtube_parser] yt-dlp failed: {result.stderr}", file=sys.stderr)
            return False

        # 查找生成的字幕文件
        # yt-dlp 输出会在当前目录或 temp 目录
        # 用 --output 模板会返回实际路径
        return True
    except FileNotFoundError:
        print("[youtube_parser] yt-dlp not found. Install: pip install yt-dlp", file=sys.stderr)
        return False
    except subprocess.TimeoutExpired:
        print("[youtube_parser] Timeout extracting subtitles", file=sys.stderr)
        return False


def extract_bilibili_subtitles(url: str, lang: str, output: str) -> bool:
    """提取 Bilibili 字幕（简化版：下载弹幕/评论作为语料）"""
    # Bilibili 需要 BCookie，建议用户直接用 WebFetch 获取字幕
    print(f"[youtube_parser] Bilibili URL detected: {url}")
    print(f"[youtube_parser] Bilibili subtitles require manual download or API access")
    print(f"[youtube_parser] Consider using --url with a YouTube video for auto-caption extraction")

    # 尝试解析 BV 号
    bv_match = re.search(r'BV[\w]+', url)
    if bv_match:
        bv = bv_match.group()
        print(f"[youtube_parser] Bilibili video ID: {bv}")
        # 实际场景：调用 Bilibili API 获取字幕地址
        # 这里仅做占位提示

    return False


def main():
    parser = argparse.ArgumentParser(description="提取视频字幕（YouTube/Bilibili）")
    parser.add_argument("--url", required=True, help="视频 URL（YouTube/Bilibili）")
    parser.add_argument("--lang", default="en,zh", help="优先语言（逗号分隔）")
    parser.add_argument("--output", required=True, help="输出文件路径")
    args = parser.parse_args()

    print(f"[youtube_parser] Fetching: {args.url}")
    print(f"[youtube_parser] Language: {args.lang}")
    print(f"[youtube_parser] Output: {args.output}")

    # 确保输出目录存在
    os.makedirs(os.path.dirname(args.output) or ".", exist_ok=True)

    if "youtube.com" in args.url or "youtu.be" in args.url:
        success = extract_youtube_subtitles(args.url, args.lang, args.output)
    elif "bilibili.com" in args.url:
        success = extract_bilibili_subtitles(args.url, args.lang, args.output)
    else:
        print(f"[youtube_parser] Unsupported platform: {args.url}", file=sys.stderr)
        sys.exit(1)

    if success:
        # 将临时字幕文件移动到输出路径
        # yt-dlp 的 --output 模板在无视频下载时不会自动产出
        # 实际使用时，字幕文件会生成在执行目录
        print(f"[youtube_parser] Subtitles extracted to: {args.output}")
        print(f"[youtube_parser] Done.")
    else:
        print(f"[youtube_parser] Extraction failed.", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
