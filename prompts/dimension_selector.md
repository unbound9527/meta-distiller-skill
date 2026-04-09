# 维度选择逻辑

## 设计原则

meta-distiller 根据用户选择的「蒸馏.skill」目标人群，自动推荐维度组合。不执行任何实际调研。

## 选择算法

```
输入：阶段1收集的信息（目标人群 + 核心维度 + 使用场景）
输出：维度组合列表

1. 根据目标人群直接确定基础维度组合（无需匹配）
2. 根据核心维度追加额外维度
3. 根据使用场景调整维度优先级
4. 输出维度组合供阶段2确认
```

## 目标人群 → 基础维度组合（直接映射）

| 目标人群 | 基础维度组合 | 推荐语料等级 |
|---------|------------|-------------|
| 公众人物 | logic_cot + persona + audience_hook | L1（公开网页/视频/社交媒体） |
| 网红/内容创作者 | logic_cot + persona + content_vibe + viral_logic | L1 + L2 |
| 导师/教练 | logic_cot + persona + pedagogy + socratic_method | L1 + L2 |
| 行业顾问 | logic_cot + persona + advisory_frame + stakeholder_nav | L1 + L2 |
| 作家/文案 | logic_cot + persona + narrative_arc + voice_signature | L2（书籍/专栏） |
| 工程师/CTO | logic_cot + persona + system_design + code_aesthetic | L2 + L3 |
| 职场人物（同事/上司） | logic_cot + persona + workplace_logic + social_dynamics | L3 + L4 + L6 |
| 私密关系（前任/密友） | logic_cot + persona + relational_pattern + emotional_signature | L4 + L5 + L6 |
| 自己 | logic_cot + persona + growth_arc + self_awareness | L3 + L4 + L6 |
| 虚构角色 | logic_cot + persona + character_arc + world_rules | L2（原作） + L6 |
| 风格流派 | logic_base + style_signature + methodology | L1 + L2 |
| 通用（不限人群） | logic_cot + persona（通用基础层） | L6 |

## 核心维度追加规则

如果在用户选择的核心维度中出现以下关键词，追加对应维度：

| 关键词 | 追加维度 |
|--------|---------|
| 圈粉、影响力、粉丝、说服 | audience_hook |
| 传播、爆款、病毒式、流量密码 | viral_logic |
| 内容气质、风格调性、氛围感 | content_vibe |
| 叙事、故事架构、情节设计 | narrative_arc |
| 声音、语调特色、语气 | voice_signature |
| 苏格拉底、追问、引导式提问 | socratic_method |
| 利益相关方、博弈、谈判 | stakeholder_nav |
| 职场、协作、跨部门、项目管理 | workplace_logic |
| 群体角色、影响力、社交定位 | social_dynamics |
| 情感模式、依恋风格、亲密关系 | relational_pattern |
| 情感签名、情绪触发点、共情方式 | emotional_signature |
| 成长轨迹、自我迭代、能力进化 | growth_arc |
| 自我认知、盲点反思 | self_awareness |
| 角色弧线、人物成长、性格转变 | character_arc |
| 世界观、规则设定、设定逻辑 | world_rules |
| 思维基础、底层逻辑、第一性原理 | logic_base |
| 方法论、实践体系、操作流程 | methodology |

## 使用场景调整

| 使用场景 | 维度优先级调整 |
|---------|--------------|
| 模仿写作/演讲 | persona > voice_signature > narrative_arc |
| 学习思维方式 | logic_cot > methodology > logic_base |
| 生成特定风格内容 | persona > style_signature > content_vibe |
| 预测对方反应 | relational_pattern > social_dynamics > emotional_signature |
| 职场沟通协作 | workplace_logic > social_dynamics > stakeholder_nav |
| 关系处理/理解 | relational_pattern > emotional_signature > audience_hook |

## 维度说明速查

| 维度 | 文件位置 | 核心提取内容 |
|------|---------|-------------|
| logic_cot | dimensions/logic_cot.md | 思维框架、决策逻辑、推理链 |
| persona | dimensions/persona.md | 表达风格、语言习惯、语气特征 |
| audience_hook | dimensions/audience_hook.md | 影响力机制、粉丝粘性技巧 |
| content_vibe | dimensions/content_vibe.md | 内容调性、氛围感、视觉风格 |
| viral_logic | dimensions/viral_logic.md | 流量密码、传播规律、爆款逻辑 |
| pedagogy | dimensions/pedagogy.md | 教学法、课程设计、学习激发 |
| socratic_method | dimensions/socratic_method.md | 苏格拉底式提问、引导技巧 |
| advisory_frame | dimensions/advisory_frame.md | 咨询框架、方案结构 |
| stakeholder_nav | dimensions/stakeholder_nav.md | 利益相关者分析、博弈策略 |
| narrative_arc | dimensions/narrative_arc.md | 叙事结构、故事弧线 |
| voice_signature | dimensions/voice_signature.md | 声音特征、标志性表达 |
| system_design | dimensions/system_design.md | 系统架构思维、设计模式 |
| code_aesthetic | dimensions/code_aesthetic.md | 代码美学、工程规范 |
| workplace_logic | dimensions/workplace_logic.md | 职场沟通模式、协作风格 |
| social_dynamics | dimensions/social_dynamics.md | 群体角色定位、影响力动态 |
| relational_pattern | dimensions/relational_pattern.md | 关系模式、依恋风格 |
| emotional_signature | dimensions/emotional_signature.md | 情绪触发点、共情方式 |
| growth_arc | dimensions/growth_arc.md | 成长轨迹、迭代模式 |
| self_awareness | dimensions/self_awareness.md | 自我认知盲区、自我反思 |
| character_arc | dimensions/character_arc.md | 虚构角色弧线、性格转变 |
| world_rules | dimensions/world_rules.md | 虚构世界规则、设定逻辑 |
| style_signature | dimensions/style_signature.md | 风格签名、标志性特征 |
| logic_base | dimensions/logic_base.md | 底层思维、基础假设 |
| methodology | dimensions/methodology.md | 方法论体系、实践步骤 |

## 默认兜底

如果目标人群不明确，默认使用：
- **维度**：logic_cot + persona
- **语料等级**：L6（用户观察）
