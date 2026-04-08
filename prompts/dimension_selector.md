# 维度选择逻辑

## 选择算法

```
输入：用户描述（核心主题 + 核心能力 + 使用场景）
输出：维度组合列表

1. 提取关键词（来自描述中的名词/动词）
2. 与下方类型关键词匹配表进行匹配
3. 命中最多的类型 → 选取该类型的默认维度组合
4. 如果核心能力描述中有额外指向，追加对应维度
```

## 类型关键词匹配表

| 类型 | 关键词 |
|------|--------|
| influencer / content-creator | 粉丝、流量、爆款、传播、创作内容、网红、博主 |
| celebrity / public-figure | 名人、公众人物、演讲、影响力 |
| mentor / teacher / coach | 教学、指导、传授、学员、学生、成长 |
| consultant / advisor | 咨询、顾问、方案、战略、分析 |
| writer / storyteller | 写作、文笔、叙事、故事、创作 |
| engineer / architect / CTO | 架构、系统设计、代码、工程、技术 |

## 维度追加规则

如果在核心能力描述中出现以下关键词，追加对应维度：

| 关键词 | 追加维度 |
|--------|---------|
| 圈粉、影响力、粉丝 | audience_hook |
| 传播、爆款、病毒式 | viral_logic |
| 内容气质、风格调性 | content_vibe |
| 叙事、故事架构 | narrative_arc |
| 声音、语调特色 | voice_signature |
| 苏格拉底、追问、引导 | socratic_method |
| 利益相关方、博弈、谈判 | stakeholder_nav |

## 默认兜底

如果匹配不上任何类型，默认使用：logic_cot + persona（通用基础层）
