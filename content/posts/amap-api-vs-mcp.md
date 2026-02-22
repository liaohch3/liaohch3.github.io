---
title: "我给 OpenClaw🦞 装了高德 API，方便找合适的租房位置"
date: 2026-02-22
draft: false
tags: ["AI", "Agent", "MCP", "高德地图", "OpenClaw"]
description: "给 OpenClaw 接入高德地图 API 做租房通勤规划，发现直接调 API + 文件系统比 MCP 好用得多。"
---

今天想通过 OpenClaw 找深圳地图上适合租房的位置。需求是两个人在不同地方上班，一个开车一个坐地铁，要找一个对两边通勤都合理的片区。但发现 Agent 自己无法准确输出通勤时间——全靠估算，数据不靠谱。所以就想给 Agent 接上高德地图 API，让它基于真实行程数据来回答。

## 没有 API 时：AI 靠猜

没接地图 API 之前，AI 会自信地输出完整的通勤方案表格——哪个片区开车多少分钟、地铁多少分钟——看起来很专业，但全是根据「大约每站 2.5-3 分钟」估算的：

![AI 幻觉输出的通勤数据](/images/amap-api/hallucination.jpg)

问它数据来源，才老实交代：

> 「说实话，我手头没有高德/百度地图 API key，刚才的通勤时间是根据地铁线路站数 + 路网距离估算的，不是 API 返回的精确数据。」

设置好 API Key 后，AI 立刻开始调真实接口，结果打脸了：

![设置 API 后的对话](/images/amap-api/api-setup.jpg)

> 「高德 API 的真实数据出来了，跟我之前的估算差距很大，尤其地铁时间被低估了不少。」

典型案例：家到公司，AI 估算 28 分钟，高德实测 **41 分钟**（含步行+换乘），**误差 46%**。这种误差在租房决策中是致命的。

## 高德 API 能力测试

注册高德开放平台（个人认证，免费），拿到 Web 服务 Key：

![高德开放平台控制台](/images/amap-api/console.jpg)

个人认证开发者的免费配额：

![配额说明](/images/amap-api/quota.jpg)

用深圳 5 个随机地标做了 14 项 API 全面测试，全部通过：

![测试地标地图](/images/amap-api/test-map.png)

![测试报告](/images/amap-api/test-report.jpg)

高德 API 提供的核心能力：地理编码（地址⇄坐标互转）、路径规划（驾车/公交/步行/骑行）、距离批量测量、POI 关键字搜索、周边搜索、行政区域查询、天气预报、静态地图生成。个人认证每天 5000 次路径规划调用，免费够用。

## 实战：从估算到精确

有了 API 后，Agent 自动组合多个接口完成一次完整的租房通勤分析：地理编码（地铁站名→坐标）→ 驾车规划（到工作地点）→ 公交规划（地铁换乘方案）→ 批量测距（10+ 个站同时算）→ 周边搜索（附近小区/餐厅）。最终生成了 16 个地铁站的通勤排名表，每个数据都是 API 实测。

## 为什么不需要 MCP

高德很早就封装过 MCP（Model Context Protocol）。但实际用下来，有文件系统的 Agent 完全不需要 MCP，原因有三：

**1. API 的可组合性。** MCP 把每个能力封装成独立 tool，调用方式固定。Agent 直接调 HTTP API + 写脚本，想怎么组合怎么组合，不受 tool schema 约束。

```python
for station in stations:
    coords = geocode(station)
    drive = route_drive(coords, work)
    transit = route_transit(coords, work2)
    pois = search_around(coords, "小区")
```

**2. 渐进式上下文加载。** MCP 需要把所有 tool 的 schema（名称、描述、参数定义）预加载到上下文中，高德十几个 API 对应十几个 tool 定义，光 schema 就占了大量 context——即使这次只用路径规划，天气、POI、地理编码的 schema 也全在上下文里白白占着。而 Agent 直接调 API + 文件系统，按需加载：这次只要路径规划就只读路径规划的脚本，不需要把所有能力的定义塞进上下文。

**3. 文件系统 = 天然的中间层。** Agent 把脚本存到文件系统下次复用，MCP 没有这个能力。文件系统给了 Agent 持久化的工具链，脚本可以不断迭代优化。

## 结论

给 AI Agent 一个 API Key，比装十个 MCP 工具有用得多。14 种高德能力全部通过 curl + Python 脚本调用，零 MCP 插件。上下文更省，组合更灵活，脚本可复用。

目前还有一块短板：租房房源数据。贝壳、链家、自如全部没有公开 API，房源信息只能手动查。下一步计划通过 Agent 接管浏览器（Playwright）来自动化房源采集，与高德通勤数据交叉分析，实现「找房→算通勤→决策」全流程自动化。
