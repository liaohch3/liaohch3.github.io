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

三步走 — **动态模型注册表 + Skill 语义化引用 + 定时自动更新**

**第一步：TOOLS.md 作为模型注册表。** Agent 每次启动自动加载到上下文，覆盖过时的预训练知识。

**第二步：Skill 文档中用语义描述替代具体模型名。** Agent 执行时读到「最强 Flash 模型」后去 TOOLS.md 查具体名称，通过 `--model` 传入脚本。Skill 文件永不过时。

**第三步：Cron 定时任务自动更新 TOOLS.md。** 每天拉取 OpenRouter API 最新模型列表，写入 TOOLS.md。人不需要手动维护。

![解决方案架构图：踩坑 vs 解决方案对比](/images/model-version-rot/solution.png)

## 修复前后对比

### SKILL.md 修复前

Agent 用预训练知识生成的 SKILL.md，直接硬编码了具体模型版本。以下是 `article-to-podcast/SKILL.md` 的实际片段：

```markdown
## 模型

- 音频转录: `google/gemini-2.0-flash-001`（支持音频输入）
- 翻译/改写: `anthropic/claude-sonnet-4`
- TTS: `gemini-2.5-flash-preview-tts`（Vertex AI）
```

脚本中也是同样的硬编码：

```python
# podcast_pipeline.py — Agent 生成的原始版本
def call_llm(messages, model="google/gemini-2.0-flash-001", timeout=120):
    ...

def translate_faithful(english_text, prev_context=""):
    # 翻译用 claude-sonnet-4，同样是过时版本
    return call_llm([...], model="anthropic/claude-sonnet-4", timeout=120)
```

<p style="background-color: #f8d7da; padding: 12px 16px; border-left: 4px solid #dc3545; border-radius: 4px; font-size: 1.05em;">
❌ <strong>这些过时的模型导致执行性能明显低于预期</strong> — 转录准确率更低、翻译质量更差，但因为不报错、能跑通，很难被发现。
</p>

### SKILL.md 修复后

修复后的 SKILL.md 不再出现任何具体模型名，改为语义化描述。以下是 `article-to-podcast/SKILL.md` 修复后的实际片段：

```markdown
## 模型选择策略（不要硬编码具体版本号！）

执行时根据当前可用模型动态选择，参考 TOOLS.md 里的最新模型列表：

| 用途 | 选择标准 |
|------|---------|
| 音频转录 | Gemini 系列最强 Flash 模型（需支持音频输入） |
| 翻译/改写 | Claude 系列最强性价比模型（Sonnet 级别） |
| TTS 生成 | Gemini 最强 TTS 模型（Vertex AI） |

原则：脚本中的默认模型可能过时，执行前先检查 TOOLS.md 中的
「旗舰选型」表确认当前最优模型，通过 --model 参数覆盖。
如果 TOOLS.md 信息也过时，可通过 OpenRouter Models 查询各家最新模型。
```

<p style="background-color: #d4edda; padding: 12px 16px; border-left: 4px solid #28a745; border-radius: 4px; font-size: 1.05em;">
✅ <strong>关键变化：</strong>表格里只有语义描述（"Gemini 系列最强 Flash 模型"），完全没有具体版本号。Agent 执行时去 TOOLS.md 查最新模型名，TOOLS.md 过时则去 OpenRouter 查。
</p>

### TOOLS.md 模型注册表

Agent 每次启动自动加载到上下文，作为模型选择的唯一真相源：

```markdown
旗舰选型（2026-02-20）
| 场景     | 首选                           | 路径              |
|----------|-------------------------------|-------------------|
| 最强智能 | Gemini 3.1 Pro / Opus 4.6      | Vertex / Anthropic |
| 日常编码 | Sonnet 4.6 ($3/$15)            | Anthropic          |
| 大量文本 | Gemini 2.5 Flash ($0.30/$2.50) | Vertex             |
| 生图     | GPT-5 Image                    | OpenRouter         |
| 音频     | GPT Audio                      | OpenRouter         |
```

### Cron 定时更新任务

每天自动拉取最新模型列表，更新 TOOLS.md，确保 Agent 的模型认知永远是最新的：

```yaml
# OpenClaw cron job 配置
schedule:
  kind: cron
  expr: "0 8 * * *"  # 每天早上 8 点（北京时间）
  tz: Asia/Shanghai
payload:
  kind: agentTurn
  message: "去 OpenRouter API 拉取各家最新模型列表，更新 TOOLS.md 中的旗舰选型表"
sessionTarget: isolated
```

<p style="background-color: #d1ecf1; padding: 12px 16px; border-left: 4px solid #17a2b8; border-radius: 4px; font-size: 1.05em;">
💡 这个 cron job 让 Agent 每天自动检查模型更新。Agent 会调用 OpenRouter API 获取最新模型列表，对比当前 TOOLS.md，有变化就更新。人不需要手动维护。
</p>

## 经验总结

1. **Agent 的预训练知识会过时** — 它"记住"的最新模型可能已经是旧的
2. **旧模型不报错是最大的坑** — 不像依赖库会直接 break，模型退化是无声的
3. **用语义描述 + 动态选择** — Skill 写「最强 Flash 模型」而不是具体版本号
4. **TOOLS.md 作为模型选型的唯一真相源** — 用运行时上下文覆盖过时的预训练知识
5. **定时自动更新 > 人工维护** — 人会忘，cron 不会
