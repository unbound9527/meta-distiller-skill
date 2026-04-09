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

## 数字分身对话示例

> 通过 `celebrity-distiller` 蒸馏出的马斯克数字分身，可以直接以第一人称对话：

```
你：如何度过创业历程中那些难熬的日子？

马斯克：难熬的日子？

让我问你：什么叫"难熬"？

如果你的理由只是"赚钱"——那你会在某个谷底放弃，因为钱不是足够强的理由。

但如果你的理由是"我要解决某个根本问题"——你会一直找方法，直到解决它。

第四，极端地拆分任务。
当你面对一个看起来无法逾越的障碍时，把它拆到不能再拆。然后逐个击破。

SpaceX的火箭成本问题是：猎鹰9号的成本是Ariane 5的三分之一。怎么做到的？不是什么魔法，是把火箭拆成4000个零件，一个一个问：为什么是这个成本？能不能用更便宜的材料？能不能自己造？

最后：别停下来。

停滞才会死。往前走，哪怕慢一点。

那些最难熬的日子，回头看，都是燃料。

我当时没有"度过"它们——我是踩着它们走过去的。
```

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

## 蒸馏案例

### celebrity-distiller（名人蒸馏）
> 蒸馏名人的思维框架和表达习惯，生成可对话的数字分身

**子案例：**
| 名称 | 说明 |
|------|------|
| elon-musk | 马斯克数字分身 — 包含完整的三维分析框架与第一人称对话能力 |

### 更多蒸馏案例
> 更多蒸馏.skill 案例持续添加中...

## 项目结构

```
meta-distiller-skill/
├── SKILL.md                    # 工厂母机 Skill 定义
├── dimensions/                 # 维度定义（12个）
│   ├── logic_base.md          # 逻辑基础
│   ├── logic_cot.md           # 思维框架
│   ├── growth_arc.md          # 成长轨迹
│   ├── self_awareness.md      # 自我认知
│   ├── methodology.md         # 方法论
│   ├── relational_pattern.md  # 关系模式
│   ├── social_dynamics.md     # 社交动态
│   ├── style_signature.md     # 风格签名
│   ├── workplace_logic.md     # 职场逻辑
│   ├── world_rules.md         # 世界规则
│   ├── character_arc.md       # 角色弧线
│   └── emotional_signature.md # 情感签名
├── prompts/                   # 提示词模板
│   ├── agent_swarm.md         # Subagent 工作流编排
│   ├── dimension_selector.md  # 维度选择器
│   ├── extraction_framework.md # 语料提取框架
│   ├── intake_template.md     # 运行时问题模板
│   └── skill_assembler.md     # Skill 组装模板
├── tool_templates/            # 工具模板
│   ├── chat_export_parser.py  # 聊天记录解析
│   ├── dingtalk_parser.py     # 钉钉记录解析
│   ├── feishu_parser.py       # 飞书记录解析
│   ├── image_ocr.py           # 图片 OCR
│   └── observation_guide.py   # 观察指南
├── examples/                  # 蒸馏案例
│   └── celebrity-distiller/    # 蒸馏.skill 案例
│       ├── SKILL.md           # 蒸馏.skill 模板
│       ├── meta.json          # 元数据
│       └── elon-musk/         # 子案例：马斯克数字分身
│           ├── SKILL.md
│           ├── meta.json
│           └── references/
└── LICENSE
```

## 使用示例

### 构建新的蒸馏.skill

```
你：我想造一个能蒸馏职场人物的 skill
meta-distiller：好的，请回答几个问题...

（多轮对话后）
meta-distiller：✅ 蒸馏.skill 构建完成！
```

### 使用蒸馏.skill（案例：celebrity-distiller）

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

### 维度体系（12个维度）

| 维度 | 说明 |
|------|------|
| logic_base | 逻辑基础 |
| logic_cot | 思维框架（第一性原理、推理模式）|
| growth_arc | 成长轨迹 |
| self_awareness | 自我认知 |
| methodology | 方法论 |
| relational_pattern | 关系模式 |
| social_dynamics | 社交动态 |
| style_signature | 风格签名 |
| workplace_logic | 职场逻辑 |
| world_rules | 世界规则 |
| character_arc | 角色弧线 |
| emotional_signature | 情感签名 |

## 开发指南

### 贡献新的蒸馏案例

1. Fork 本仓库
2. 在 `examples/` 创建新的蒸馏案例（如 `examples/{person-slug}/`）
3. 包含 SKILL.md、meta.json 和 references/analysis/ 分析结果
4. 提交 Pull Request

### 添加新的维度

在 `dimensions/` 添加新的维度定义文件。

## License

MIT License - 详见 [LICENSE](LICENSE)
