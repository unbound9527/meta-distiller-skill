#!/usr/bin/env python3
"""
chat_export_parser.py
解析微信/钉钉等聊天记录导出文件，用于 L4 级语料收集
"""

import re
import json
from typing import List, Dict, Optional, Iterator
from dataclasses import dataclass
from pathlib import Path


@dataclass
class Message:
    """单条消息"""
    timestamp: str
    sender: str
    content: str
    is_image: bool = False
    is_file: bool = False

    def to_dict(self) -> Dict:
        return {
            "timestamp": self.timestamp,
            "sender": self.sender,
            "content": self.content,
            "is_image": self.is_image,
            "is_file": self.is_file
        }


class ChatExportParser:
    """聊天记录解析器基类"""

    def parse(self, content: str) -> Iterator[Message]:
        """解析内容，返回消息迭代器"""
        raise NotImplementedError

    def extract_speakers(self, messages: List[Message]) -> List[str]:
        """提取所有说话人"""
        return list(set(msg.sender for msg in messages if msg.sender != "系统消息"))

    def extract_conversations(self, messages: List[Message]) -> Dict[str, List[Message]]:
        """按说话人分组消息"""
        conversations = {}
        for msg in messages:
            if msg.sender not in conversations:
                conversations[msg.sender] = []
            conversations[msg.sender].append(msg)
        return conversations


class WeChatParser(ChatExportParser):
    """微信聊天记录解析器

    支持格式：
    2023-01-01 12:00:00  张三  你好啊
    [2023-01-01 12:00:01] 李四: 你好
    """

    def parse(self, content: str) -> Iterator[Message]:
        # 常见微信格式的正则表达式
        patterns = [
            # 格式1: 2023-01-01 12:00:00  张三  你好啊
            r'(\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2})\s+([^\s]+)\s+(.+)',
            # 格式2: [2023-01-01 12:00:01] 李四: 你好
            r'\[(\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2})\]\s*([^:]+):\s*(.+)',
            # 格式3: 2023/1/1 12:00 张三: 你好
            r'(\d{4}/\d{1,2}/\d{1,2}\s+\d{2}:\d{2})\s*([^:]+):\s*(.+)',
        ]

        for line in content.split('\n'):
            line = line.strip()
            if not line:
                continue

            for pattern in patterns:
                match = re.match(pattern, line)
                if match:
                    groups = match.groups()
                    if len(groups) == 3:
                        timestamp, sender, msg_content = groups
                        is_image = '[图片]' in msg_content or '[Image]' in msg_content
                        is_file = '[文件]' in msg_content or '[File]' in msg_content
                        yield Message(
                            timestamp=timestamp.strip(),
                            sender=sender.strip(),
                            content=msg_content.strip(),
                            is_image=is_image,
                            is_file=is_file
                        )
                    break


class DingTalkParser(ChatExportParser):
    """钉钉聊天记录解析器

    支持格式：
    [2023-01-01 12:00:01] 张三: 你好
    """

    def parse(self, content: str) -> Iterator[Message]:
        pattern = r'\[(\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2})\]\s*([^:]+):\s*(.+)'

        for line in content.split('\n'):
            line = line.strip()
            if not line:
                continue

            match = re.match(pattern, line)
            if match:
                timestamp, sender, msg_content = match.groups()
                is_image = '图片' in msg_content or '[图片]' in msg_content
                is_file = '文件' in msg_content or '[文件]' in msg_content
                yield Message(
                    timestamp=timestamp.strip(),
                    sender=sender.strip(),
                    content=msg_content.strip(),
                    is_image=is_image,
                    is_file=is_file
                )


class JSONChatParser(ChatExportParser):
    """JSON 格式聊天记录解析器

    期望格式:
    {"timestamp": "2023-01-01 12:00:00", "sender": "张三", "content": "你好"}
    """

    def parse(self, content: str) -> Iterator[Message]:
        # 尝试解析为 JSON 数组或多个 JSON 对象
        try:
            # 单个数组
            data = json.loads(content)
            if isinstance(data, list):
                for item in data:
                    yield self._json_to_message(item)
            elif isinstance(data, dict):
                yield self._json_to_message(data)
        except json.JSONDecodeError:
            # 尝试 JSONL 格式（每行一个 JSON）
            for line in content.split('\n'):
                line = line.strip()
                if line:
                    try:
                        yield self._json_to_message(json.loads(line))
                    except json.JSONDecodeError:
                        continue

    def _json_to_message(self, item: Dict) -> Message:
        return Message(
            timestamp=item.get('timestamp', item.get('time', '')),
            sender=item.get('sender', item.get('name', '未知')),
            content=item.get('content', item.get('message', '')),
            is_image=item.get('is_image', False),
            is_file=item.get('is_file', False)
        )


def auto_detect_parser(content: str) -> ChatExportParser:
    """根据内容自动检测聊天格式"""
    # 尝试 JSON 格式
    try:
        json.loads(content)
        return JSONChatParser()
    except json.JSONDecodeError:
        pass

    # 检测钉钉格式
    if '[2023-' in content and ']:' in content:
        return DingTalkParser()

    # 默认使用微信格式
    return WeChatParser()


def parse_chat_export(file_path: str, encoding: str = 'utf-8') -> List[Message]:
    """解析聊天记录文件，自动检测格式"""
    path = Path(file_path)

    # 读取文件
    try:
        content = path.read_text(encoding=encoding)
    except UnicodeDecodeError:
        try:
            content = path.read_text(encoding='gbk')
        except UnicodeDecodeError:
            content = path.read_text(encoding='utf-8-sig')

    # 自动检测格式
    parser = auto_detect_parser(content)
    return list(parser.parse(content))


def extract_text_only(messages: List[Message]) -> str:
    """仅提取文本消息，用于后续分析"""
    text_messages = []
    for msg in messages:
        if not msg.is_image and not msg.is_file and msg.content:
            text_messages.append(f"[{msg.timestamp}] {msg.sender}: {msg.content}")
    return '\n'.join(text_messages)


def group_by_date(messages: List[Message]) -> Dict[str, List[Message]]:
    """按日期分组消息"""
    groups = {}
    for msg in messages:
        # 提取日期部分
        date = msg.timestamp.split(' ')[0] if msg.timestamp else '未知'
        if date not in groups:
            groups[date] = []
        groups[date].append(msg)
    return groups


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        file_path = sys.argv[1]
        messages = parse_chat_export(file_path)

        print(f"共解析 {len(messages)} 条消息")
        print(f"说话人: {set(msg.sender for msg in messages)}")
        print("\n前10条消息:")
        for msg in messages[:10]:
            print(f"  [{msg.timestamp}] {msg.sender}: {msg.content[:50]}...")
    else:
        # 测试
        test_content = """
[2023-01-01 10:00:01] 张三: 你好
[2023-01-01 10:00:02] 李四: 你好，请问有什么事吗？
[2023-01-01 10:01:01] 张三: 想请教一下项目的问题
[2023-01-01 10:01:05] 李四: 好的，请说
        """
        parser = auto_detect_parser(test_content)
        messages = list(parser.parse(test_content))
        for msg in messages:
            print(f"{msg.sender}: {msg.content}")
