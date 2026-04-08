# 工具推荐生成提示词

## 使用方式

根据 Skill 类型和用户提供的语料来源，生成推荐工具清单。

---

## 推荐算法

```
输入：Skill 类型 + 语料来源列表
输出：工具清单（哪些工具需要调用，以什么参数）

1. 根据 Skill 类型确定必须工具
2. 根据语料来源追加对应工具
3. 去重，输出完整工具清单
```

## 类型 → 工具映射

| Skill 类型 | 必须工具 |
|-----------|---------|
| influencer / content-creator | web_crawler, social_scraper, youtube_parser |
| celebrity / public-figure | web_crawler, youtube_parser, social_scraper |
| mentor / teacher / coach | corpus_chunker, web_crawler |
| consultant / advisor | web_crawler, corpus_chunker |
| writer / storyteller | corpus_chunker, web_crawler |
| engineer / architect | web_crawler（文档站点） |

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

这些工具将从 `${META_DISTILLER_DIR}/tool_templates/` 组装到目标 Skill 的 `tools/` 目录中。
```
