# Meta Distiller Skill

> 蒸馏.skill 工厂母机 — 通过对话引导构建「蒸馏.skill」

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## 是什么

Meta Distiller 是一个**蒸馏.skill 工厂**。

它的作用：通过多轮对话，引导你构建一个可以**反复蒸馏任何具体人**的 Skill 模板。

蒸馏出来的 skill 有什么用？

- 生成名人的**数字分身**（以第一人称对话）
- 学习牛人的**思维框架**和**表达风格**
- 构建可激活的**个人 Lens**

## 核心概念

### 蒸馏.skill

一个"蒸馏.skill"本质上是一个**Skill 模板**。当你指定要蒸馏的具体人物时，它会：

1. **采集语料** — 搜索该人物的访谈、文章、演讲
2. **维度分析** — 分析思维框架、表达风格、说服影响力
3. **组装 Lens** — 生成可激活的 SKILL.md

### Lens（数字分身）

蒸馏产出的 Lens 是一个**完整的 Claude Code Skill**，可以：

- 以**第一人称**与该人物对话
- 用他的思维方式分析问题
- 模仿他的表达风格输出内容

## 快速开始

### 1. 克隆本仓库到 Claude Code skills 目录

```bash
# 克隆到你的 Claude Code skills 目录
git clone https://github.com/unbound9527/meta-distiller-skill.git ~/.claude/skills/meta-distiller-skill
```

### 2. 激活 meta-distiller-skill

在 Claude Code 中输入：

```
/meta-distiller
```

### 3. 开始构建蒸馏.skill

按照引导对话，完成 6 个阶段的配置。

## 内置蒸馏.skill

| 名称 | 触发词 | 说明 |
|------|--------|------|
| celebrity-distiller | `/celebrity-distiller` | 蒸馏名人的思维框架和表达习惯 |

## 项目结构

```
meta-distiller-skill/
├── SKILL.md                    # 工厂母机 Skill 定义
├── meta.json                   # 元数据
├── dimensions/                  # 维度定义（17个）
│   ├── logic_cot.md           # 思维框架
│   ├── persona.md              # 表达风格
│   └── ...
├── prompts/                    # 提示词模板
│   ├── agent_swarm.md
│   ├── dimension_selector.md
│   └── ...
├── tool_templates/             # 工具模板
│   ├── corpus_collector.py
│   ├── corpus_chunker.py
│   └── ...
├── examples/                   # 示例
│   └── elon-musk/            # 马斯克数字分身示例
└── docs/                       # 设计文档
```

## 使用示例

### 构建新的蒸馏.skill

```
你：我想造一个能蒸馏职场人物的 skill
meta-distiller：好的，请回答几个问题...

（多轮对话后）
meta-distiller：✅ 蒸馏.skill 构建完成！
```

### 使用蒸馏.skill

```
你：/celebrity-distiller
蒸馏谁？马斯克
激活 subagent...
✅ 蒸馏完成！马斯克数字分身已生成
```

### 与数字分身对话

```
你：/elon-musk
马斯克：我是埃隆·马斯克。问我任何问题。
```

## 架构说明

### 蒸馏流程

```
用户对话
    ↓
meta-distiller-skill（工厂）
    ↓
celebrity-distiller（蒸馏.skill）
    ↓
采集 → 分析 → 组装
    ↓
lens/{person}/SKILL.md（数字分身）
```

### 维度体系

| 维度 | 说明 |
|------|------|
| logic_cot | 思维框架（第一性原理、推理模式）|
| persona | 表达风格（语言特征、叙事策略）|
| influence_pattern | 说服影响力（受众定位、影响策略）|

## 开发指南

### 贡献新的蒸馏.skill

1. Fork 本仓库
2. 在 `distilled_skills/` 创建你的蒸馏.skill
3. 添加测试和文档
4. 提交 Pull Request

### 添加新的维度

在 `dimensions/` 添加新的维度定义文件。

## License

MIT License - 详见 [LICENSE](LICENSE)
