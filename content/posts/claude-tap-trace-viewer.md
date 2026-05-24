+++
title = 'claude-tap：把 Claude Code / Codex 的真实请求抓出来'
description = '我做 Agent 开发时经常需要研究 Claude Code / Codex 的上下文工程，于是做了 claude-tap：抓取真实请求，生成本地 HTML trace viewer。'
date = 2026-05-03T23:42:53+08:00
draft = false
tags = ["AI", "Agent", "Claude Code", "Codex", "claude-tap"]

[decision_record]
claim = "研究 Agent harness 时，先抓真实请求比从终端表现反推更可靠。"
assumption = "Claude Code / Codex 发给模型的上下文包含提示词、工具、历史、结果和 token 信息，肉眼看到的交互只是压缩后的表面。"
uncertainty = "本地 trace viewer 适合研发复盘，但还不是生产监控、权限审计或团队级指标系统。"
follow_up = "继续补强 diff、token 分布和敏感字段遮罩，让 trace 能用于安全的团队内复盘。"
follow_up_status = "进行中"
rejected_approach = [
  "只复制终端输出做问题复盘。",
  "默认把 trace 上传到云端再分析。"
]

[[decision_record.evidence]]
title = "claude-tap trace viewer"
url = "https://github.com/liaohch3/claude-tap"
source = "本地工具"
role = "证据"
section_anchor = "claude-tap-做什么"
section_label = "工具边界"
note = "真实请求、JSONL trace 和自包含 HTML 是这篇笔记的核心工件。"

[[decision_record.evidence]]
title = "连续请求 diff 截图"
url = "/images/claude-tap/diff-view.jpg"
source = "本文截图"
role = "证据"
section_anchor = "对比连续请求"
section_label = "diff"
note = "用连续调用差异检查上下文如何增长、回灌和复用。"

[[decision_record.experiment]]
result = "已验证"
note = "Claude Code 与 Codex 两种客户端都可通过本地 proxy 记录请求。"
+++

今天发了一条推文介绍 [claude-tap](https://github.com/liaohch3/claude-tap)。这里把背景和截图整理成一篇博客，方便以后回看。

我的主业是 Agent 开发，日常经常需要研究 Claude Code / Codex 这类工具的上下文工程：system prompt 怎么写，messages 怎么组织，tools 怎么传，tool results 怎么回灌，token 又花在了哪里。

以前社区里有一个 `claude-trace`，但它已经不太适配最新的 Claude Code。所以我重新做了一个工具：`claude-tap`。

## claude-tap 做什么

一句话：**把 Claude Code / Codex 的真实请求抓出来，生成本地 HTML trace viewer。**

它会在本地启动一个 proxy，把客户端发给上游模型服务的请求记录下来，最后生成 JSONL trace 和一个自包含的 HTML 页面。这个页面可以直接打开，不依赖服务端。

<img src="/images/claude-tap/github-overview.jpg" alt="claude-tap GitHub 项目首页" loading="lazy">

它主要解决的是一个很具体的问题：不要只猜 Agent harness 怎么设计，而是直接看真实请求。

## 看见完整上下文

Claude Code / Codex 真正发给模型的内容，通常比我们肉眼在终端里看到的复杂很多。除了用户消息，还有 system prompt、developer instructions、工具定义、历史消息、continuation 信息、token usage 等。

这些东西如果只靠猜，很容易误判。trace viewer 能把每次 LLM call 展开看：

<img src="/images/claude-tap/trace-overview.jpg" alt="在 trace viewer 中查看 Codex 请求上下文" loading="lazy">

对我来说，最有价值的是能看到这些细节：

- system prompt / instructions
- messages / input
- tools schema
- tool calls 和 tool results
- token usage
- WebSocket / SSE 事件

这对于研究一个 Agent 工具为什么这样行动、为什么上下文变大、为什么某次调用结果不稳定，都很有帮助。

## 看见工具调用和结果

Agent 工具链里，LLM call 本身只是一部分。很多行为真正发生在工具调用阶段。

比如 Codex 调用 `exec_command` 时，模型到底生成了什么参数，工具返回了什么结果，下一轮又如何把结果喂回模型，这些都可以在 viewer 里展开看。

<img src="/images/claude-tap/tool-calls.jpg" alt="查看工具调用和工具结果" loading="lazy">

这类信息平时散落在终端输出和内部状态里，直接读很麻烦。放进 trace viewer 后，就比较适合复盘和对比。

## 对比连续请求

另一个我常用的功能是 diff。

Agent 在连续几轮调用中，新增了哪些消息，工具结果如何进入上下文，`previous_response_id`、metadata、prompt cache 等字段怎么变化，都可以直接对比。

<img src="/images/claude-tap/diff-view.jpg" alt="对比连续请求的差异" loading="lazy">

这对调试上下文工程很有用。尤其是在改 prompt、改 tool schema、改 harness 逻辑之后，可以直接看新旧请求差异，而不是只看最终回答。

## 为什么是本地 HTML

我做这个工具时有一个很明确的边界：数据默认留在本地。

trace 里会包含 system prompt、上下文、工具结果，有些项目里还会出现路径、日志、内部配置等信息。把它做成一个本地 HTML viewer，比较适合个人研究、团队内部复盘和问题定位。

它不是一个生产监控平台，也不想先把数据上传到某个云服务。它更像一个开发者工具：需要的时候打开，用完之后 trace 文件还在你自己的机器上。

## 试用

项目地址：

https://github.com/liaohch3/claude-tap

安装：

```bash
uv tool install claude-tap
```

追踪 Claude Code：

```bash
claude-tap
```

追踪 Codex：

```bash
claude-tap --tap-client codex
```

如果你也在研究 Agent、Claude Code、Codex、上下文工程，欢迎试用、提 issue 或 star。

原推文：

https://x.com/liaohch3/status/2050964318070673581
