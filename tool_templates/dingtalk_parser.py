#!/usr/bin/env python3
"""
dingtalk_parser.py
钉钉文档/聊天记录解析工具，用于 L3/L4 级语料收集
"""

import json
import re
from typing import List, Dict, Optional, Iterator
from pathlib import Path
from dataclasses import dataclass


@dataclass
class DingTalkMessage:
    """钉钉消息"""
    msg_id: str
    create_time: str
    sender_nickname: str
    content: str
    msg_type: str = "text"


class DingTalkParser:
    """钉钉解析器

    支持格式：
    1. 钉钉导出的 JSON 格式
    2. 钉钉导出的 Markdown 格式
    3. 钉钉聊天记录文本格式
    """

    def parse_json(self, content: str) -> Iterator[DingTalkMessage]:
        """解析钉钉 JSON 格式

        钉钉导出的 JSON 通常是消息数组：
        [
            {"msgId": "xxx", "createTime": 1234567890, "senderNick": "张三", "content": "你好"},
            ...
        ]
        """
        try:
            data = json.loads(content)
            if isinstance(data, list):
                for item in data:
                    yield self._json_to_message(item)
            elif isinstance(data, dict) and 'messages' in data:
                for item in data['messages']:
                    yield self._json_to_message(item)
        except json.JSONDecodeError:
            pass

    def _json_to_message(self, item: Dict) -> DingTalkMessage:
        """将 JSON 项转换为消息对象"""
        return DingTalkMessage(
            msg_id=item.get('msgId', item.get('msg_id', '')),
            create_time=str(item.get('createTime', item.get('create_time', ''))),
            sender_nickname=item.get('senderNick', item.get('sender_nickname', item.get('sender', '未知'))),
            content=item.get('text', item.get('content', '')),
            msg_type=item.get('msgType', item.get('msg_type', 'text'))
        )

    def parse_markdown(self, content: str) -> Iterator[str]:
        """解析钉钉导出的 Markdown 格式

        钉钉导出的 Markdown 通常保留文档结构
        """
        blocks = content.split('\n\n')
        for block in blocks:
            block = block.strip()
            if block:
                # 移除可能的标题标记用于纯文本
                clean_block = re.sub(r'^#+\s+', '', block)
                yield clean_block

    def parse_text_format(self, content: str) -> Iterator[DingTalkMessage]:
        """解析钉钉文本格式的聊天记录

        常见格式：
        [2023-01-01 12:00:01] 张三: 你好
        [2023-01-01 12:00:02] 李四: 你好
        """
        pattern = r'\[(\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2})\]\s*([^:]+):\s*(.+)'

        for line in content.split('\n'):
            line = line.strip()
            if not line:
                continue

            match = re.match(pattern, line)
            if match:
                create_time, sender, content = match.groups()
                yield DingTalkMessage(
                    msg_id="",
                    create_time=create_time,
                    sender_nickname=sender.strip(),
                    content=content.strip(),
                    msg_type="text"
                )

    def parse_eml(self, content: str) -> Iterator[DingTalkMessage]:
        """解析钉钉邮件导出格式（如果有）"""
        # 钉钉邮件导出通常是标准 EML 格式
        # 这里简化处理，只提取正文
        lines = content.split('\n')
        in_body = False
        body_lines = []
        sender = "未知"
        date = ""

        for line in lines:
            if line.startswith('From:'):
                sender = line[5:].strip()
            elif line.startswith('Date:'):
                date = line[5:].strip()
            elif line.strip() == '':
                in_body = True
            elif in_body:
                body_lines.append(line)

        if body_lines:
            yield DingTalkMessage(
                msg_id="",
                create_time=date,
                sender_nickname=sender,
                content='\n'.join(body_lines),
                msg_type="email"
            )


class DingTalkDocParser:
    """钉钉文档解析器

    用于解析钉钉云文档、知识库等导出内容
    """

    def parse_markdown(self, content: str) -> Iterator[str]:
        """解析 Markdown 格式的钉钉文档"""
        lines = content.split('\n')

        for line in lines:
            # 跳过空行
            if not line.strip():
                continue

            # 处理代码块
            if line.startswith('```'):
                continue

            # 移除 Markdown 标记，保留内容
            cleaned = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', line)  # 链接
            cleaned = re.sub(r'[*_]{1,2}([^*_]+)[*_]{1,2}', r'\1', cleaned)  # 粗体斜体
            cleaned = re.sub(r'#{1,6}\s+', '', cleaned)  # 标题标记

            if cleaned.strip():
                yield cleaned.strip()

    def parse_json(self, content: str) -> Iterator[str]:
        """解析 JSON 格式的钉钉文档"""
        try:
            data = json.loads(content)

            # 递归提取所有文本内容
            def extract_text(obj):
                if isinstance(obj, str):
                    yield obj
                elif isinstance(obj, dict):
                    for value in obj.values():
                        yield from extract_text(value)
                elif isinstance(obj, list):
                    for item in obj:
                        yield from extract_text(item)

            for text in extract_text(data):
                if text.strip():
                    yield text.strip()
        except json.JSONDecodeError:
            pass


def extract_conversation_text(messages: Iterator[DingTalkMessage]) -> str:
    """从消息中提取对话文本

    Args:
        messages: 消息迭代器

    Returns:
        格式化对话文本
    """
    result = []
    for msg in messages:
        result.append(f"[{msg.create_time}] {msg.sender_nickname}: {msg.content}")
    return '\n'.join(result)


def group_by_sender(messages: List[DingTalkMessage]) -> Dict[str, List[DingTalkMessage]]:
    """按发送者分组消息

    Args:
        messages: 消息列表

    Returns:
        发送者到消息的映射
    """
    groups = {}
    for msg in messages:
        if msg.sender_nickname not in groups:
            groups[msg.sender_nickname] = []
        groups[msg.sender_nickname].append(msg)
    return groups


def parse_dingtalk_export(file_path: str, encoding: str = 'utf-8') -> List[DingTalkMessage]:
    """自动检测并解析钉钉导出文件

    Args:
        file_path: 文件路径
        encoding: 文件编码

    Returns:
        解析后的消息列表
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

    suffix = path.suffix.lower()

    # 根据文件类型选择解析器
    if suffix == '.json':
        parser = DingTalkParser()
        return list(parser.parse_json(content))
    elif suffix == '.eml':
        parser = DingTalkParser()
        return list(parser.parse_eml(content))
    else:
        # 默认为文本格式
        parser = DingTalkParser()
        return list(parser.parse_text_format(content))


def parse_dingtalk_doc(file_path: str, encoding: str = 'utf-8') -> List[str]:
    """解析钉钉文档文件

    Args:
        file_path: 文件路径
        encoding: 文件编码

    Returns:
        解析后的文本块列表
    """
    path = Path(file_path)

    try:
        content = path.read_text(encoding=encoding)
    except UnicodeDecodeError:
        content = path.read_text(encoding='utf-8-sig')

    suffix = path.suffix.lower()

    if suffix == '.json':
        parser = DingTalkDocParser()
        return list(parser.parse_json(content))
    else:
        parser = DingTalkDocParser()
        return list(parser.parse_markdown(content))


# 便捷函数
def extract_dingtalk_chat(file_path: str) -> str:
    """从钉钉聊天记录快速提取对话文本"""
    messages = parse_dingtalk_export(file_path)
    return extract_conversation_text(iter(messages))


def extract_dingtalk_doc(file_path: str) -> str:
    """从钉钉文档快速提取文本"""
    blocks = parse_dingtalk_doc(file_path)
    return '\n'.join(blocks)


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        file_path = sys.argv[1]
        messages = parse_dingtalk_export(file_path)

        print(f"共解析 {len(messages)} 条消息")
        print(f"发送者: {set(msg.sender_nickname for msg in messages)}")
        print("\n前5条消息:")
        for msg in messages[:5]:
            print(f"  [{msg.create_time}] {msg.sender_nickname}: {msg.content[:30]}...")
    else:
        # 测试
        test_content = """
[2023-01-01 10:00:01] 张三: 项目进度如何？
[2023-01-01 10:00:02] 李四: 基本上完成了
[2023-01-01 10:01:01] 张三: 有什么问题吗？
[2023-01-01 10:01:03] 李四: 遇到了点技术难题
        """
        parser = DingTalkParser()
        messages = list(parser.parse_text_format(test_content))
        for msg in messages:
            print(f"{msg.sender_nickname}: {msg.content}")
