<div align="center">

# Meta Distiller Skill

> ### 「蒸馏.skill」 之母 — 产出任何人物蒸馏类skill的skill

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

</div>

用这个skill工厂你能得到名人.skill、网红.skill、教师.skill...
meta-distiller（skill工厂）
└── 产出：「蒸馏.skill」
    └── 用户激活「蒸馏.skill」
        └── 运行时问：蒸馏谁？
            └── 产出：马斯克 lens、乔布斯 lens...

## 数字分身对话示例

> 先看效果——用此skill构建的名人.skill `celebrity-distiller` ，进而蒸馏出的马斯克数字分身，可以直接以第一人称对话：

```
我 -> 如何度过创业历程中那些难熬的日子？

马斯克 -> 难熬的日子？

让我问你：什么叫“难熬”？
你是指资金快断链的时候？是指团队有人要离开的时候？是指外界都在嘲笑你的时候？

我告诉你真相——2008 年 SpaceX 第三次火箭发射失败的时候，特斯拉几乎破产，
整个媒体都在说我是骗子，SpaceX 是骗局。那是我人生中最黑暗的时期。
但我从来没有“熬过去”这种想法。

为什么？

因为“熬”意味着你在忍耐什么，你在等待什么结束。这是类比推理者的思维。

我不是在熬。我是在房间里计算，下一步怎么走。

让我用第一性原理来拆解这个问题：

第一，问正确的问题。
不是“这件事有多难”，而是“这件事最基本的障碍是什么？是技术？是资金？是人？”

2008 年，SpaceX 最基本的问题不是舆论，是火箭第三级冷却管路的设计缺陷。
找到它，修好它，第四次发射成功了。

第二，把情绪清掉。
情绪是噪音。恐惧、焦虑、绝望——这些情绪会干扰你的计算能力。
我不是没有感受过，我是学会在感受的同时继续计算。

我曾经连续几个月每天工作 20 个小时。
不是因为我精力无限，是因为问题太多太紧迫，没时间睡觉。

第三，找到那个让你不放弃的理由。
对我来说，是使命。不是“我想成功”，是“这件事必须做成，对人类重要”。

如果你创业的理由只是“我想变得有钱”——那你会在某个谷底放弃，因为钱不是足够强的理由。

但如果你的理由是“我要解决某个根本问题”——你会一直找方法，直到解决它。

第四，极端地拆分任务。
当你面对一个看起来无法逾越的障碍时，把它拆到不能再拆。然后逐个击破。

SpaceX 的火箭成本问题是：猎鹰 9 号的成本是 Ariane 5 的三分之一。怎么做到的？
不是什么魔法，是把火箭拆成 4000 个零件，一个一个问：为什么是这个成本？能不能用更便宜的材料？能不能自己造？

最后：别停下来。

停滞才会死。往前走，哪怕慢一点。

那些最难熬的日子，回头看，都是燃料。

我当时没有“度过”它们——我是踩着它们走过去的。
```

## 是什么

**一个 Skill 工厂——帮你构建能蒸馏任何人的 Skill 模板**

Meta Distiller 是一个**蒸馏.skill 工厂母机**。

它的作用很简单：通过对话引导你构建一个**蒸馏.skill**。

蒸馏.skill 是什么？是一个可以反复使用的 Skill 模板。一旦构建完成，你输入任意一个具体的人名，它就会自动采集语料、分析维度，产出这个人对应的数字分身 Lens。

### 蒸馏.skill 能做什么？

- 输入人名 → 自动采集语料 → 生成数字分身
- 以**第一人称**和这个牛人对话
- 用**他的框架**分析问题、模仿**他的风格**输出

## 核心概念

### 蒸馏.skill

一个"蒸馏.skill"是一个**Skill 模板**。运行时它会：

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
