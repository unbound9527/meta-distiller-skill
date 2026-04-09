# 工具推荐生成提示词

## 使用方式

根据「蒸馏.skill」的目标人群和用户选择的维度，生成推荐工具清单，供组装到蒸馏.skill 的 tools/ 目录。

---

## 推荐算法

```
输入：目标人群 + 用户选择的维度 + 语料来源列表
输出：工具清单（哪些工具需要调用，以什么参数）

1. 根据目标人群确定必须工具
2. 根据语料来源追加对应工具
3. 去重，输出完整工具清单
```

## 目标人群 → 必须工具

| 目标人群 | 必须工具 |
|---------|---------|
| 公众人物 | web_crawler, youtube_parser, social_scraper |
| 网红/内容创作者 | web_crawler, social_scraper, youtube_parser |
| 导师/教练 | corpus_chunker, web_crawler |
| 行业顾问 | web_crawler, corpus_chunker |
| 作家/文案 | corpus_chunker, web_crawler |
| 工程师/CTO | web_crawler（文档站点） |
| 职场人物 | web_crawler, corpus_chunker, email_parser |
| 私密关系 | observation_guide, chat_export_parser |
| 虚构角色 | web_crawler, corpus_chunker |
| 通用 | web_crawler, corpus_chunker |

## 语料来源 → 工具映射

| 来源类型 | 对应工具 |
|---------|---------|
| 网页 URL | web_crawler |
| YouTube/Bilibili 链接 | youtube_parser |
| Twitter/X Handle | social_scraper |
| PDF/TXT/EPUB 文件 | corpus_chunker |

## 输出格式

```markdown
## 推荐工具清单

| 工具 | 调用参数 | 用途 |
|------|---------|------|
| web_crawler | --url {url} --output {path} | 抓取网页 |
| youtube_parser | --url {url} --lang {lang} --output {path} | 提取字幕 |
| ... | ... | ... |

这些工具将从 `\$\{META_DISTILLER_DIR\}/tool_templates/` 组装到「蒸馏.skill」的 `tools/` 目录中。
```
