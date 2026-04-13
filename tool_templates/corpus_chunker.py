#!/usr/bin/env python3
"""长文本分块处理工具 - 专为蒸馏.skill 语料处理设计"""

import argparse
import json
import os
import re
import sys


try:
    import markdown
    HAS_MARKDOWN = True
except ImportError:
    HAS_MARKDOWN = False


def chunk_text_plain(text: str, max_chars: int = 2000, overlap: int = 200) -> list[dict]:
    """按字符数分块，保留 overlap"""
    chunks = []
    start = 0
    total = len(text)

    while start < total:
        end = start + max_chars
        chunk_text = text[start:end]

        # 尝试在句号/换行处断开
        if end < total:
            # 找最后一个句号或换行
            last_period = max(chunk_text.rfind("。"), chunk_text.rfind("."))
            last_newline = chunk_text.rfind("\n")
            cut = max(last_period, last_newline)
            if cut > max_chars * 0.6:  # 确保不在太短处切断
                end = start + cut + 1
                chunk_text = text[start:end]

        chunks.append({
            "text": chunk_text.strip(),
            "start": start,
            "end": end,
            "length": len(chunk_text),
        })
        start = end - overlap if end < total else total

    return chunks


def chunk_by_first_person(text: str, max_chars: int = 2000) -> list[dict]:
    """按第一人称逻辑分块（观点/论断 为单位）"""
    chunks = []

    # 识别第一人称陈述的特征
    # 1. 引号内内容
    # 2. 段落以 "我认为"、"我相信"、"我的观点是" 开头
    # 3. 长段落按自然段落分割

    # 先按自然段落分割
    paragraphs = [p.strip() for p in re.split(r"\n{2,}", text) if p.strip()]

    current_chunk = []
    current_len = 0

    first_person_markers = [
        "我认为", "我相信", "我的观点", "我要说", "我想说",
        "我的方法是", "我的原则", "我的理念", "我相信",
        "i think", "i believe", "i want to", "my view", "my approach",
    ]

    for para in paragraphs:
        para_len = len(para)
        is_first_person = any(marker in para.lower() for marker in first_person_markers)

        # 如果这个段落本身很长，超出 max_chars，需要进一步分块
        if para_len > max_chars:
            if current_chunk:
                chunks.append({"text": "\n\n".join(current_chunk), "type": "mixed", "first_person": False})
                current_chunk = []
                current_len = 0

            sub_chunks = chunk_text_plain(para, max_chars, overlap=100)
            for sc in sub_chunks:
                chunks.append({
                    **sc,
                    "type": "first_person" if is_first_person else "general",
                    "first_person": is_first_person,
                })
            continue

        # 累积到当前 chunk
        if current_len + para_len + 2 > max_chars:
            if current_chunk:
                combined = "\n\n".join(current_chunk)
                chunks.append({
                    "text": combined,
                    "type": "first_person" if any(
                        any(m in c.lower() for m in first_person_markers) for c in current_chunk
                    ) else "mixed",
                    "first_person": any(
                        any(m in c.lower() for m in first_person_markers) for c in current_chunk
                    ),
                })
            current_chunk = [para]
            current_len = para_len
        else:
            current_chunk.append(para)
            current_len += para_len + 2

    # 处理最后一块
    if current_chunk:
        combined = "\n\n".join(current_chunk)
        chunks.append({
            "text": combined,
            "type": "first_person",
            "first_person": any(
                any(m in c.lower() for m in first_person_markers)
                for c in current_chunk
            ),
        })

    return chunks


def extract_text_from_file(filepath: str) -> str:
    """根据文件类型提取文本"""
    ext = os.path.splitext(filepath)[1].lower()

    if ext == ".txt":
        with open(filepath, encoding="utf-8") as f:
            return f.read()

    if ext in (".md", ".markdown"):
        if HAS_MARKDOWN:
            with open(filepath, encoding="utf-8") as f:
                md = markdown.Markdown(extensions=["extra"])
                html = md.convert(f.read())
                # 简单去除 HTML 标签
                text = re.sub(r"<[^>]+>", "", html)
                return text
        else:
            with open(filepath, encoding="utf-8") as f:
                return f.read()

    if ext == ".json":
        with open(filepath, encoding="utf-8") as f:
            data = json.load(f)
            # 尝试提取文本字段
            if isinstance(data, dict):
                for key in ["text", "content", "body", "tweets"]:
                    if key in data:
                        if isinstance(data[key], list):
                            return "\n\n".join(str(i) for i in data[key])
                        return str(data[key])
            if isinstance(data, list):
                return "\n\n".join(str(i) for i in data)
            return str(data)

    # 纯文本 fallback
    with open(filepath, encoding="utf-8") as f:
        return f.read()


def main():
    parser = argparse.ArgumentParser(description="长文本分块处理")
    parser.add_argument("--file", required=True, help="输入文件路径（支持 TXT/MD/JSON）")
    parser.add_argument("--extract-mode", default="first-person-logic",
                        choices=["first-person-logic", "all", "summary"],
                        help="提取模式")
    parser.add_argument("--output", required=True, help="输出文件路径")
    parser.add_argument("--max-chars", type=int, default=2000, help="单块最大字符数")
    args = parser.parse_args()

    print(f"[corpus_chunker] Processing: {args.file}")
    print(f"[corpus_chunker] Mode: {args.extract_mode}")
    print(f"[corpus_chunker] Output: {args.output}")

    if not os.path.exists(args.file):
        print(f"[corpus_chunker] File not found: {args.file}", file=sys.stderr)
        sys.exit(1)

    # 提取文本
    text = extract_text_from_file(args.file)
    print(f"[corpus_chunker] Extracted {len(text)} chars")

    # 分块
    if args.extract_mode == "first-person-logic":
        chunks = chunk_by_first_person(text, args.max_chars)
    elif args.extract_mode == "summary":
        # 提取摘要模式：取头尾+高密度段落
        lines = text.split("\n")
        chunks = [{"text": "\n".join(lines[:5]), "type": "summary_head"}]
        if len(lines) > 10:
            chunks.append({"text": "\n".join(lines[-5:]), "type": "summary_tail"})
        # 取中间高信息量段落
        for i, line in enumerate(lines[5:-5]):
            if len(line) > 100 and (i % 3 == 0):
                chunks.append({"text": line, "type": "summary_mid"})
    else:  # all
        chunks = chunk_text_plain(text, args.max_chars)

    # 写入输出
    os.makedirs(os.path.dirname(args.output) or ".", exist_ok=True)
    result = {
        "source": args.file,
        "mode": args.extract_mode,
        "total_chars": len(text),
        "total_chunks": len(chunks),
        "chunks": chunks,
    }

    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    print(f"[corpus_chunker] Created {len(chunks)} chunks")
    print(f"[corpus_chunker] Output: {args.output}")


if __name__ == "__main__":
    main()
