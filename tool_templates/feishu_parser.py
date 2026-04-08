#!/usr/bin/env python3
"""
feishu_parser.py
飞书文档/多维表格解析工具，用于 L3 级语料收集
"""

import json
import re
from typing import List, Dict, Optional, Iterator, Any
from pathlib import Path
from dataclasses import dataclass


@dataclass
class FeishuBlock:
    """飞书文档块"""
    block_id: str
    block_type: str
    content: str
    children: List['FeishuBlock'] = None

    def __post_init__(self):
        if self.children is None:
            self.children = []


class FeishuDocParser:
    """飞书文档解析器

    支持格式：
    1. 飞书文档导出的 Markdown 格式
    2. 飞书文档导出 JSON 格式
    3. 飞书多维表格 CSV 导出
    """

    def parse_markdown(self, content: str) -> Iterator[FeishuBlock]:
        """解析飞书导出的 Markdown 格式

        飞书导出的 Markdown 通常保留以下结构：
        # 标题
        ## 二级标题
        段落文字
        - 列表项
        > 引用
        代码块
        """
        lines = content.split('\n')
        current_block = None
        code_block_content = []

        for line in lines:
            # 跳过空行
            if not line.strip():
                continue

            # 标题
            heading_match = re.match(r'^(#{1,6})\s+(.+)$', line)
            if heading_match:
                if current_block:
                    yield current_block
                yield FeishuBlock(
                    block_id=f"heading_{len(lines)}",
                    block_type="heading",
                    content=heading_match.group(2),
                )
                continue

            # 代码块
            if line.startswith('```'):
                if current_block and current_block.block_type == "code":
                    # 结束代码块
                    current_block.content = '\n'.join(code_block_content)
                    code_block_content = []
                    yield current_block
                    current_block = None
                else:
                    # 开始代码块
                    if current_block:
                        yield current_block
                    current_block = FeishuBlock(
                        block_id=f"code_{len(lines)}",
                        block_type="code",
                        content=""
                    )
                continue

            if current_block and current_block.block_type == "code":
                code_block_content.append(line)
                continue

            # 列表
            list_match = re.match(r'^[\-\*\+]\s+(.+)$', line)
            if list_match:
                if current_block:
                    yield current_block
                yield FeishuBlock(
                    block_id=f"list_{len(lines)}",
                    block_type="list_item",
                    content=list_match.group(1)
                )
                continue

            # 引用
            if line.startswith('>'):
                if current_block:
                    yield current_block
                yield FeishuBlock(
                    block_id=f"quote_{len(lines)}",
                    block_type="quote",
                    content=line[1:].strip()
                )
                continue

            # 段落
            if current_block:
                current_block.content += '\n' + line
            else:
                current_block = FeishuBlock(
                    block_id=f"para_{len(lines)}",
                    block_type="paragraph",
                    content=line
                )

        if current_block:
            yield current_block

    def parse_json(self, content: str) -> Iterator[FeishuBlock]:
        """解析飞书文档 JSON 格式

        期望格式：
        {
            "blocks": [
                {"block_id": "xxx", "block_type": "text", "content": "..."},
                ...
            ]
        }
        """
        try:
            data = json.loads(content)
            blocks = data.get('blocks', data) if isinstance(data, dict) else data

            for item in blocks:
                block_type = item.get('type', item.get('block_type', 'text'))
                content = item.get('text', item.get('content', ''))

                # 处理嵌套的内容
                if isinstance(content, list):
                    content = ' '.join(
                        c.get('text', '') if isinstance(c, dict) else str(c)
                        for c in content
                    )

                yield FeishuBlock(
                    block_id=item.get('block_id', ''),
                    block_type=block_type,
                    content=str(content)
                )
        except json.JSONDecodeError:
            # JSON 解析失败，尝试作为普通文本处理
            yield FeishuBlock(
                block_id="fallback",
                block_type="paragraph",
                content=content
            )

    def parse_csv(self, content: str) -> List[Dict[str, str]]:
        """解析飞书多维表格 CSV 导出"""
        lines = content.strip().split('\n')
        if not lines:
            return []

        # 第一行是表头
        headers = [h.strip() for h in lines[0].split(',')]
        result = []

        for line in lines[1:]:
            values = [v.strip() for v in line.split(',')]
            if len(values) == len(headers):
                result.append(dict(zip(headers, values)))

        return result


def extract_text_only(blocks: Iterator[FeishuBlock]) -> str:
    """从解析的块中提取纯文本"""
    texts = []
    for block in blocks:
        if block.content:
            texts.append(block.content)
    return '\n'.join(texts)


def feishu_to_markdown(blocks: Iterator[FeishuBlock]) -> str:
    """将解析的块转换为 Markdown 格式"""
    md_lines = []

    for block in blocks:
        if block.block_type == "heading":
            level = len(block.content.split()[0]) if block.content.startswith('#') else 1
            md_lines.append(f"{'#' * min(level, 6)} {block.content}")
        elif block.block_type == "code":
            md_lines.append(f"```\n{block.content}\n```")
        elif block.block_type == "list_item":
            md_lines.append(f"- {block.content}")
        elif block.block_type == "quote":
            md_lines.append(f"> {block.content}")
        else:
            md_lines.append(block.content)
        md_lines.append("")  # 空行分隔

    return '\n'.join(md_lines)


def parse_feishu_export(file_path: str, encoding: str = 'utf-8') -> List[FeishuBlock]:
    """自动检测并解析飞书导出文件

    Args:
        file_path: 文件路径
        encoding: 文件编码

    Returns:
        解析后的块列表
    """
    path = Path(file_path)

    # 读取文件
    try:
        content = path.read_text(encoding=encoding)
    except UnicodeDecodeError:
        try:
            content = path.read_text(encoding='gbk')
        except UnicodeDecodeError:
            content = path.read_text(encoding='utf-8-sig')

    # 根据文件扩展名选择解析器
    suffix = path.suffix.lower()

    if suffix == '.json':
        parser = FeishuDocParser()
        return list(parser.parse_json(content))
    elif suffix == '.csv':
        return [FeishuBlock(
            block_id="csv_table",
            block_type="table",
            content=content  # CSV 内容作为整体存储
        )]
    else:
        # 默认为 Markdown
        parser = FeishuDocParser()
        return list(parser.parse_markdown(content))


# 便捷函数
def extract_from_feishu(file_path: str) -> str:
    """从飞书文档快速提取纯文本"""
    blocks = parse_feishu_export(file_path)
    return extract_text_only(iter(blocks))


def extract_from_feishu_csv(file_path: str) -> List[Dict[str, str]]:
    """从飞书多维表格 CSV 提取"""
    path = Path(file_path)

    try:
        content = path.read_text(encoding='utf-8')
    except UnicodeDecodeError:
        content = path.read_text(encoding='utf-8-sig')

    parser = FeishuDocParser()
    return parser.parse_csv(content)


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        file_path = sys.argv[1]
        blocks = parse_feishu_export(file_path)

        print(f"共解析 {len(blocks)} 个块")
        print("\n前5个块:")
        for block in blocks[:5]:
            print(f"  [{block.block_type}] {block.content[:50]}...")
    else:
        # 测试 Markdown 解析
        test_md = """# 标题1
这是第一段文字。

## 二级标题
- 列表项1
- 列表项2

> 这是一段引用

```
代码块内容
```
"""
        parser = FeishuDocParser()
        blocks = list(parser.parse_markdown(test_md))
        for block in blocks:
            print(f"[{block.block_type}] {block.content[:30]}...")
