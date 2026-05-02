+++
title = "实验室"
description = "我正在推进的工程、实验和工具链。"
draft = false
toc = false
+++

这里放的是仍在推进中的工程系统。重点不是“展示项目”，而是记录一个系统如何从想法、实现、修正，逐步变成能每天使用的东西。

## 当前重点

### Personal AI telemetry stack

从 `cc/cx` alias 开始捕获 trace，异步入队，原始数据进入私有云存储，用于私有复盘和调试。

- Durable queue and retry-based worker
- Private raw archive in cloud storage
- Allowlist-based export boundary for internal reporting

### claude-tap

一个本地 trace 捕获器，目标不是只支持单一路径，而是在真实命令行工作流里稳定记录请求与响应。

### Usage hub

负责异步上传、聚合和白名单扫描。它让 trace 数据在可控边界内用于复盘，而不是变成对外展示。

### API-first workflows

当 Agent 开始影响真实工程工作时，我更倾向于让它接入真实 API、脚本和文件系统，而不是停留在抽象描述层。
