+++
title = 'AI Agent 工具链中的模型版本管理陷阱'
description = '当 AI Agent 用预训练知识中的过时模型名生成代码时，不会报错，但性能在悄悄退化。本文记录了这个"模型版本腐烂"问题的发现与解决方案。'
date = 2026-02-20T21:00:00+08:00
draft = false
tags = ["ai", "agent", "llm"]
+++

## 问题

今天让 OpenClaw（AI Agent）创建一个「播客翻译」Skill，Agent 自动选了 `google/gemini-2.0-flash-001` 做转录、`anthropic/claude-sonnet-4` 做翻译。这两个模型都已过时——当前最新分别是 `gemini-2.5-flash` 和 `claude-sonnet-4.6`。但旧模型仍然能跑通、不报错，性能在悄悄退化。

![问题截图：新建脚本中硬编码的过时模型](/images/model-version-rot/problem.jpg)

## 根因

Agent 的模型认知来源于预训练知识（training data cutoff）。训练数据截止时，`gemini-2.0-flash-001` 和 `claude-sonnet-4` 就是最新的。Agent 写代码时自然用了它"记忆中"的最新版本——但现实世界的模型已经迭代了好几代。

预训练知识是静态的，模型版本是动态的。这个时间差导致 Agent 每次生成代码都可能写入已过时的模型名。

## 解决方案

两步走 — **动态模型注册表 + Skill 语义化引用**

**第一步：** TOOLS.md 作为模型注册表，定时自动更新。设置 cron 每天去 OpenRouter API 拉取各家最新模型列表，写入 TOOLS.md。Agent 每次启动自动加载到上下文，覆盖过时的预训练知识。

**第二步：** Skill 文档中用语义描述替代具体模型名。Agent 执行时读到「最强 Flash 模型」后去 TOOLS.md 查具体名称，通过 `--model` 传入脚本。Skill 文件永不过时。

![解决方案架构图：踩坑 vs 解决方案对比](/images/model-version-rot/solution.png)

## 修复前后对比

**SKILL.md 修复前**（错误 — Agent 用预训练知识中的过时模型）：

```python
# podcast_pipeline.py
def call_llm(messages, model="google/gemini-2.0-flash-001"):
    ...

def translate_faithful(...):
    return call_llm([...], model="anthropic/claude-sonnet-4")
```

```markdown
# SKILL.md 中的描述
# 模型: google/gemini-2.0-flash-001（支持音频输入）
# 模型: anthropic/claude-sonnet-4
```

**SKILL.md 修复后**（正确 — 语义描述，不绑定版本号）：

```markdown
## 模型选择策略（不要硬编码具体版本号！）

| 用途     | 选择标准                    | 示例（会过时）                |
|----------|----------------------------|-------------------------------|
| 音频转录 | Gemini 系列最强 Flash 模型   | google/gemini-2.5-flash      |
| 翻译改写 | Claude 系列最强性价比模型    | anthropic/claude-sonnet-4    |
| TTS 生成 | Gemini 最强 TTS 模型        | gemini-2.5-flash-preview-tts |

原则：执行前先检查 TOOLS.md 确认当前最优模型，通过 --model 参数覆盖。
```

**TOOLS.md 模型注册表**（Agent 每次启动自动加载）：

```markdown
旗舰选型（2026-02-20）
| 场景     | 首选                        | 路径              |
|----------|----------------------------|-------------------|
| 最强智能 | Gemini 3.1 Pro / Opus 4.6   | Vertex / Anthropic |
| 日常编码 | Sonnet 4.6                  | Anthropic          |
| 大量文本 | Gemini 2.5 Flash            | Vertex             |
| 生图     | GPT-5 Image                 | OpenRouter         |
```

## 经验总结

1. **Agent 的预训练知识会过时** — 它"记住"的最新模型可能已经是旧的
2. **旧模型不报错是最大的坑** — 不像依赖库会直接 break，模型退化是无声的
3. **用语义描述 + 动态选择** — Skill 写「最强 Flash 模型」而不是具体版本号
4. **TOOLS.md 作为模型选型的唯一真相源** — 用运行时上下文覆盖过时的预训练知识
5. **定时自动更新 > 人工维护** — 人会忘，cron 不会
