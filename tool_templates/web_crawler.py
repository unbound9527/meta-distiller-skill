#!/usr/bin/env python3
"""网页正文爬取工具 - 提取网页主要内容"""

import argparse
import os
import re
import sys


try:
    import requests
    from bs4 import BeautifulSoup
    HAS_DEPS = True
except ImportError:
    HAS_DEPS = False


def extract_article_text(url: str, output: str) -> bool:
    """抓取网页并提取正文内容"""
    if not HAS_DEPS:
        print("[web_crawler] requests/beautifulsoup4 not installed", file=sys.stderr)
        print("[web_crawler] Install: pip install requests beautifulsoup4", file=sys.stderr)
        return False

    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (compatible; DistillerBot/1.0; +https://example.com/bot)",
            "Accept": "text/html,application/xhtml+xml",
        }
        resp = requests.get(url, headers=headers, timeout=30, allow_redirects=True)
        resp.raise_for_status()

        soup = BeautifulSoup(resp.text, "html.parser")

        # 移除无关标签
        for tag in soup.find_all(["script", "style", "nav", "header", "footer",
                                   "aside", "form", "button", "iframe", "noscript"]):
            tag.decompose()

        # 尝试多种策略提取正文
        content = None

        # 策略1: <article> 标签
        article = soup.find("article")
        if article:
            content = article.get_text(separator="\n", strip=True)

        # 策略2: 找最大文本块
        if not content:
            # 移除所有 hidden 元素
            for tag in soup.find_all(style=True):
                if "display:none" in tag.get("style", "") or "visibility:hidden" in tag.get("style", ""):
                    tag.decompose()

            # 找所有段落，按密度排序
            candidates = []
            for p in soup.find_all("p"):
                text = p.get_text(strip=True)
                if len(text) > 50:  # 至少50字符
                    # 计算段落周围的文本密度
                    parent = p.parent
                    parent_text = parent.get_text(strip=True) if parent else ""
                    density = len(text) / max(len(parent_text), 1)
                    candidates.append((density, text))

            candidates.sort(reverse=True)
            if candidates:
                # 取前10个高密度段落
                content = "\n\n".join(c[:2] for _, c in candidates[:10])

        # 策略3: <main> 或 role="main"
        if not content:
            main = soup.find("main") or soup.find(attrs={"role": "main"})
            if main:
                content = main.get_text(separator="\n", strip=True)

        # 策略4: 找 class/id 包含 content/article/body 的 div
        if not content:
            for selector in ["div.content", "div.article", "div.post", "div.entry",
                             "#content", "#article", "#post", "#entry"]:
                elem = soup.select_one(selector)
                if elem:
                    content = elem.get_text(separator="\n", strip=True)
                    break

        # 最终 fallback
        if not content:
            # 移除常见导航/页脚后取 body
            body = soup.find("body")
            content = body.get_text(separator="\n", strip=True) if body else soup.get_text(separator="\n", strip=True)

        # 清理：合并空行
        content = re.sub(r"\n{3,}", "\n\n", content)

        # 保存
        os.makedirs(os.path.dirname(output) or ".", exist_ok=True)
        with open(output, "w", encoding="utf-8") as f:
            f.write(content)

        print(f"[web_crawler] Fetched: {url}")
        print(f"[web_crawler] Content length: {len(content)} chars")
        print(f"[web_crawler] Output: {output}")
        return True

    except Exception as e:
        print(f"[web_crawler] Error fetching {url}: {e}", file=sys.stderr)
        return False


def main():
    parser = argparse.ArgumentParser(description="爬取网页正文内容")
    parser.add_argument("--url", required=True, help="目标网页 URL")
    parser.add_argument("--output", required=True, help="输出文件路径")
    args = parser.parse_args()

    print(f"[web_crawler] Fetching: {args.url}")
    print(f"[web_crawler] Output: {args.output}")

    success = extract_article_text(args.url, args.output)
    if not success:
        sys.exit(1)


if __name__ == "__main__":
    main()
