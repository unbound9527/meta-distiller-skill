#!/usr/bin/env python3
"""
image_ocr.py
图片文字提取工具，用于 L5 级语料收集
支持截图、朋友圈截图、照片等
"""

import base64
import os
import json
from typing import Optional, List, Dict
from pathlib import Path


# 提示词模板：指导 AI 从截图中提取信息
SCREENSHOT_EXTRACTION_PROMPT = """
你是一个信息提取专家。请从以下截图中提取文字内容。

**提取原则：**
1. 完整提取所有可见文字，保持原有格式
2. 标注图片类型（如：聊天截图、朋友圈截图、文章截图等）
3. 识别并标注说话人/用户名（如果可见）
4. 注意提取可能的水印、时间戳等信息
5. 如果图片质量差或文字模糊，标注"文字模糊/不可识别"

**输出格式：**
```
## 图片类型
[类型描述]

## 时间戳（如果可见）
[时间信息]

## 说话人/用户名（如果可见）
[用户名]

## 提取文字内容
[完整文字内容]

## 备注
[其他需要注意的信息]
```

**截图内容：
```
{image_content}
```
"""


def encode_image_to_base64(image_path: str) -> str:
    """将图片转换为 base64 编码"""
    with open(image_path, 'rb') as f:
        return base64.b64encode(f.read()).decode('utf-8')


def image_to_text_prompt(image_path: str, image_description: str = "") -> str:
    """生成图片转文字的提示词

    Args:
        image_path: 图片路径
        image_description: 图片内容的文字描述（当无法直接读取图片时使用）

    Returns:
        格式化的问题字符串
    """
    prompt = SCREENSHOT_EXTRACTION_PROMPT.format(image_content=image_description or "[图片文件]")

    # 如果是实际文件，可以在这里添加 base64 编码
    if Path(image_path).exists():
        try:
            b64 = encode_image_to_base64(image_path)
            prompt = f"![image](data:image/png;base64,{b64})\n\n{prompt}"
        except Exception:
            pass

    return prompt


def batch_image_prompt(image_paths: List[str], batch_name: str = "批量图片") -> str:
    """生成批量图片处理的提示词

    Args:
        image_paths: 图片路径列表
        batch_name: 批次名称

    Returns:
        批量处理的提示词
    """
    result = f"## {batch_name}\n\n请依次提取以下 {len(image_paths)} 张图片的文字内容：\n\n"

    for i, path in enumerate(image_paths, 1):
        result += f"### 图片 {i}: {Path(path).name}\n"
        result += image_to_text_prompt(path)
        result += "\n---\n\n"

    return result


def extract_from_text_description(
    description: str,
    image_type: str = "未指定"
) -> str:
    """从文字描述生成模拟 OCR 结果

    当用户无法提供图片文件，只能描述截图内容时使用。
    将用户的描述转换为标准化的提取格式。

    Args:
        description: 用户对截图内容的文字描述
        image_type: 图片类型（聊天截图/朋友圈/文章等）

    Returns:
        格式化后的提取结果
    """
    return f"""## 图片类型
{image_type}

## 提取文字内容
{description}

## 备注
由用户描述生成，如有具体截图建议提供原图以获得更准确的分析。
"""


def format_conversation_screenshot(
    screenshot_content: str,
    participants: Optional[List[str]] = None
) -> str:
    """格式化聊天截图提取结果

    Args:
        screenshot_content: 截图中的文字内容
        participants: 聊天参与者列表

    Returns:
        格式化后的聊天记录
    """
    participant_str = ", ".join(participants) if participants else "未知"
    return f"""## 聊天截图提取

**参与者**: {participant_str}

**内容**:
{screenshot_content}
"""


def format_moment_screenshot(
    screenshot_content: str,
    username: str = "",
    timestamp: str = ""
) -> str:
    """格式化朋友圈截图提取结果

    Args:
        screenshot_content: 截图中的文字内容
        username: 用户名
        timestamp: 发布时间

    Returns:
        格式化后的朋友圈内容
    """
    return f"""## 朋友圈截图提取

**用户名**: {username or "未知"}
**发布时间**: {timestamp or "未知"}

**内容**:
{screenshot_content}
"""


def format_article_screenshot(
    screenshot_content: str,
    title: str = "",
    author: str = ""
) -> str:
    """格式化文章截图提取结果

    Args:
        screenshot_content: 截图中的文字内容
        title: 文章标题
        author: 作者

    Returns:
        格式化后的文章内容
    """
    return f"""## 文章截图提取

**标题**: {title or "未知"}
**作者**: {author or "未知"}

**内容**:
{screenshot_content}
"""


class ImageOCRProcessor:
    """图片 OCR 处理器"""

    def __init__(self, use_mcp_vision: bool = False):
        """
        Args:
            use_mcp_vision: 是否使用 MCP 视觉能力（如 chrome-devtools-mcp）
        """
        self.use_mcp_vision = use_mcp_vision

    def process_image(self, image_path: str) -> str:
        """处理单张图片"""
        if not Path(image_path).exists():
            return f"[文件不存在: {image_path}]"

        if self.use_mcp_vision:
            # 使用 MCP 视觉能力（需配合 chrome-devtools-mcp 等 MCP 服务器）
            return "[MCP 视觉模式：需要配置 MCP 服务器以自动提取图片文字]"
        else:
            # 返回提示用户上传或描述
            return image_to_text_prompt(image_path)

    def process_batch(self, image_paths: List[str]) -> str:
        """批量处理图片"""
        return batch_image_prompt(image_paths)


# 便捷函数
def ocr_screenshot(image_path: str) -> str:
    """快速 OCR 截图"""
    processor = ImageOCRProcessor()
    return processor.process_image(image_path)


def ocr_from_description(description: str, image_type: str = "截图") -> str:
    """从文字描述快速提取"""
    return extract_from_text_description(description, image_type)


if __name__ == "__main__":
    # 测试
    print(image_to_text_prompt("test.png", "一张微信聊天截图"))
    print("---")
    print(extract_from_text_description(
        "张三: 今天的会议几点？\n李四: 下午3点",
        "微信聊天截图"
    ))
