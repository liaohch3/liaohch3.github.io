+++
title = "实验室"
description = "我正在推进的工程、实验和工具链。"
draft = false
toc = false
+++

这里放的是仍在推进中的工程系统。重点不是“展示项目”，而是记录一个系统如何从想法、实现、修正，逐步变成能每天使用的东西。

## 当前重点

### Personal AI telemetry stack

从 `cc/cx` alias 开始捕获 trace，异步入队，原始数据进入私有云存储，经过白名单过滤后的聚合指标再发布到公开页面。

- Durable queue and retry-based worker
- Private raw archive in cloud storage
- Public metrics generated from allowlisted payloads only
- Homepage consumes static snapshots instead of direct warehouse queries

### claude-tap

一个本地 trace 捕获器，目标不是只支持单一路径，而是在真实命令行工作流里稳定记录请求与响应。

### Usage hub

负责异步上传、聚合、白名单扫描和公开快照。它让 metrics 成为一个受约束的副产品，而不是泄露风险。

### API-first workflows

当 Agent 开始影响真实工程工作时，我更倾向于让它接入真实 API、脚本和文件系统，而不是停留在抽象描述层。
