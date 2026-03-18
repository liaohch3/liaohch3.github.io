---
title: "GPT-5.4 / mini / nano 速度实测：4x 差距从哪来？"
date: 2026-03-18
draft: false
tags: ["AI", "GPT", "Benchmark", "LLM", "OpenAI"]
description: "亲手跑了 9 种 input/output 组合场景，用真实 API usage 数据对比三款模型的速度，并和官方公开数据做了对照。"
---

GPT-5.4 mini 和 nano 昨天正式发布（2026-03-17），OpenAI 说 mini 比上一代快 2x 以上，是"最强小模型"。

正好手边有 API，就系统地跑了一遍速度测试，用真实 `usage` 字段拿 token 数，而不是估算。把结果记录下来。

## 测试设置

**模型：** `gpt-5.4-nano` / `gpt-5.4-mini` / `gpt-5.4`（均通过 OpenRouter 调用）

**测试维度：**
- Input 长度：短（~25 tok）/ 中（~600 tok）/ 长（~2400 tok）
- Output 长度：短（max 100 tok）/ 中（max 600 tok）/ 长（max 2000 tok）

**指标：**
- TTFT（首 token 延迟）
- 总耗时
- 生成速度（tok/s）—— 用 API 返回的 `completion_tokens` 除以生成时间，真实值

每个场景跑 2 次取平均，streaming 模式。

## 实测数据

| 场景 | 模型 | in tok | out tok | TTFT | 总耗时 | tok/s |
|------|------|-------:|--------:|-----:|------:|------:|
| short/short | nano | 25 | 81 | 0.85s | 1.36s | **158** |
| short/short | mini | 25 | 75 | 1.01s | 1.37s | **205** |
| short/short | gpt-5.4 | 25 | 78 | 0.89s | 2.13s | **63** |
| short/medium | nano | 25 | 310 | 0.91s | 2.20s | **239** |
| short/medium | mini | 25 | 355 | 0.78s | 2.40s | **220** |
| short/medium | gpt-5.4 | 25 | 399 | 0.99s | 9.45s | **47** |
| short/long | nano | 36 | 2000 | 0.75s | 10.61s | **203** |
| short/long | mini | 36 | 2000 | 0.92s | 10.04s | **219** |
| short/long | gpt-5.4 | 36 | 2000 | 1.08s | 40.62s | **51** |
| medium/short | nano | 600 | 100 | 0.78s | 1.21s | **232** |
| medium/short | mini | 600 | 100 | 0.99s | 1.53s | **185** |
| medium/short | gpt-5.4 | 600 | 100 | 1.20s | 3.08s | **53** |
| medium/medium | nano | 600 | 494 | 0.88s | 3.03s | **229** |
| medium/medium | mini | 600 | 458 | 1.15s | 3.49s | **196** |
| medium/medium | gpt-5.4 | 600 | 466 | 1.21s | 10.11s | **52** |
| medium/long | nano | 611 | 2000 | 0.75s | 10.10s | **214** |
| medium/long | mini | 611 | 2000 | 0.82s | 9.77s | **223** |
| medium/long | gpt-5.4 | 611 | 2000 | 1.04s | 35.22s | **59** |
| long/short | nano | 2420 | 100 | 0.92s | 1.35s | **234** |
| long/short | mini | 2420 | 100 | 1.02s | 1.58s | **180** |
| long/short | gpt-5.4 | 2420 | 100 | 1.07s | 2.76s | **59** |
| long/medium | nano | 2420 | 600 | 0.81s | 3.53s | **221** |
| long/medium | mini | 2420 | 561 | 1.35s | 4.10s | **204** |
| long/medium | gpt-5.4 | 2420 | 560 | 1.46s | 12.02s | **53** |
| long/long | nano | 2431 | 2000 | 1.01s | 10.84s | **204** |
| long/long | mini | 2431 | 2000 | 0.87s | 10.12s | **216** |
| long/long | gpt-5.4 | 2431 | 2000 | 1.03s | 38.04s | **54** |

## 几个值得关注的点

**1. 速度差距是真实的，不是 token 数造成的**

三款模型在 long output 场景下全部输出了 2000 tok（达到 max_tokens 上限），medium out 也在同一量级（310–494 tok），输出量相同，速度却差了 4x。

**2. TTFT 差异不大**

三款模型首 token 延迟都在 0.75–1.5s，没有本质差距。速度的差距主要体现在 decode 阶段（生成 token 的速度），不是排队时间。

**3. Input 长度对速度没影响**

25 tok input 和 2400 tok input 时，各模型的生成速度几乎一样——prefill 阶段不是瓶颈。

**4. nano 和 mini 速度非常接近**

nano 平均约 **200–234 tok/s**，mini 约 **185–223 tok/s**，差距在 10–15% 之间，远小于和 gpt-5.4 的差距。gpt-5.4 稳定在 **47–63 tok/s**，约是 nano 的 1/4。

## 和公开数据的对比

OpenAI 官方说 GPT-5.4 mini 比 GPT-5 mini 快 **2x 以上**。我没跑 GPT-5 mini，但从能力/价格的改变可以侧面对比：

| 模型 | Input 价格 | Output 价格 | 涨幅 |
|------|--------:|--------:|------|
| GPT-5 mini | $0.25/M | $2.00/M | — |
| GPT-5.4 mini | $0.75/M | $4.50/M | 3x / 2.25x |
| GPT-5 nano | $0.05/M | $0.40/M | — |
| GPT-5.4 nano | $0.20/M | $1.25/M | 4x / 3.125x |

能力方面，公开 benchmark 数据（来源：The Decoder / OpenAI）：

| Benchmark | gpt-5.4 | mini | nano | GPT-5 mini |
|-----------|--------:|-----:|-----:|----------:|
| SWE-Bench Pro | 57.7% | 54.4% | 52.4% | 45.7% |
| Terminal-Bench 2.0 | 75.1% | 60.0% | 46.3% | 38.2% |
| GPQA Diamond | 93.0% | 88.0% | 82.8% | 81.6% |
| OSWorld-Verified | 75.0% | 72.1% | 39.0% | 42.0% |
| Toolathlon | 54.6% | 42.9% | 35.5% | 26.9% |

mini 在大多数指标上逼近 gpt-5.4，nano 在编码和工具调用上表现尚可，但在 computer use（OSWorld-Verified 39%）上甚至不如 GPT-5 mini（42%）。

## 怎么选

**nano（$0.20/$1.25）：** 分类、数据抽取、排名、简单 subagent，速度和成本都最优，但别指望它做复杂任务。

**mini（$0.75/$4.50）：** 能力接近旗舰，速度是旗舰的 4x，适合 Agent 架构里的 worker 角色——搜索、文件扫描、并行子任务。OSWorld-Verified 72.1% 对比旗舰 75%，computer use 场景可以直接替换。

**gpt-5.4（$2.50/$15）：** 保留给真正需要深度推理和长上下文检索的任务。OpenAI MRCR 128K-256K 场景，旗舰 79.3% vs mini 33.6%，差距巨大。

---

价格涨了 3-4x，但能力也是真实的提升。对于构建 multi-agent 系统的开发者来说，用 gpt-5.4 做规划、mini/nano 做执行，这个组合的性价比目前挺高。
