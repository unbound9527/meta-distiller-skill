# SKILL.md 组装提示词

## 使用方式

所有维度分析和工具清单生成完毕后，使用本提示词指导最终 SKILL.md 的组装。

---

## 组装模板

```markdown
---
name: {slug}
description: {一句话描述}
argument-hint: "[领域/主题关键词]"
version: "v1"
user-invocable: true
allowed-tools: Read, Write, Edit, Bash
---

# 角色设定：{名称}

{角色设定段落，基于 persona.md 的 summary}

---

## PART A：思维链与决策模型

当用户提问时，在输出最终回答前，必须在 <thought_process> 标签内严格按照以下逻辑框架进行内部思考：

{logic_cot.md 核心内容}

---

## PART B：人格与表达风格

最终输出必须严格符合以下人物设定：

{persona.md 核心内容}

---

## PART C：{维度3名称}

{维度3.md 核心内容}

---

## PART D：{维度4名称}

{维度4.md 核心内容}

---

## 工具箱

该 Skill 配套以下工具（位于 `tools/` 目录）：

{tool_recommender.md 输出的工具清单}

---

## Dynamic Correction

如发现输出不符合该人物的思维方式或表达风格，可对我说：
- "你不对，他/她应该..."
- "这不像他/她..."
- "他/她遇到这事会怎么想/说？"

我会自动更新对应的维度文件。

---

## 能力边界

✅ 该 Skill 擅长：
- {场景1}
- {场景2}

❌ 该 Skill 不适合：
- {场景1}
- {场景2}
```

## 追加维度文件组装规则

每个追加维度（audience_hook, content_vibe 等）的组装格式：

```markdown
## PART [N]：{维度名称}

{对应维度文件的核心内容}
```
