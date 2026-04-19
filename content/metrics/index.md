+++
title = "指标"
description = "公开的 AI 工作流技术指标，只展示脱敏后的安全聚合。"
draft = false
toc = false
comments = false
+++

这是公开可见的 AI 工作流信号页。它只展示脱敏后的聚合数据，不展示 prompt、response、文件路径、原始 trace 或任何未列入白名单的字段。

<div class="public-metrics">
  <div class="metric-hero">
    <div class="metric-hero-copy">
      <div class="metric-overline">Public usage snapshot</div>
      <h2>公开信号，不是原始数据</h2>
      <p>数据来源于私有原始 trace 的公开快照层。上传前、发布前、导出前都过白名单扫描。</p>
    </div>
    <div class="metric-updated" data-usage-field="updated_at">--</div>
  </div>

  <div class="metric-grid">
    <div class="metric-card">
      <span>24h tokens</span>
      <strong data-usage-field="total_tokens">--</strong>
    </div>
    <div class="metric-card">
      <span>24h requests</span>
      <strong data-usage-field="requests">--</strong>
    </div>
    <div class="metric-card">
      <span>success rate</span>
      <strong data-usage-field="success_rate">--</strong>
    </div>
    <div class="metric-card">
      <span>avg latency</span>
      <strong data-usage-field="avg_latency_ms">--</strong>
    </div>
  </div>

  <div class="metric-bars-head">
    <span>Hourly token buckets</span>
    <span id="usage-model-line">loading</span>
  </div>
  <div class="metric-bars" id="usage-bars"></div>
  <div class="metric-status" id="usage-dashboard-status">Loading public metrics...</div>
</div>

## 安全边界

- Upload-side scan：上传到 usage API 前，事件会先过 schema allowlist，只允许非敏感指标字段通过。
- Publish-side scan：公开 BigQuery 行和 summary 在写出前再次校验，字段不匹配就直接失败。
- Homepage JSON scan：站点导出脚本只允许白名单字段落到 `static/data/*.json`，防止 UI 层误暴露额外信息。

<script>
(() => {
  const summaryUrl = "/data/ai-usage-summary.json";
  const hourlyUrl = "/data/ai-usage-hourly.json";

  const formatInt = (value) => new Intl.NumberFormat("en-US").format(Number(value || 0));
  const formatRate = (success, requests) => {
    if (!requests) return "--";
    return `${((success / requests) * 100).toFixed(1)}%`;
  };
  const formatLatency = (value) => `${Math.round(Number(value || 0))} ms`;
  const formatTime = (value) => {
    if (!value) return "--";
    const dt = new Date(value);
    if (Number.isNaN(dt.getTime())) return value;
    return `Updated ${dt.toLocaleString("zh-CN", { hour12: false })}`;
  };

  const setField = (name, value) => {
    const node = document.querySelector(`[data-usage-field="${name}"]`);
    if (node) node.textContent = value;
  };

  const setText = (id, value) => {
    const node = document.getElementById(id);
    if (node) node.textContent = value;
  };

  const renderBars = (rows) => {
    const container = document.getElementById("usage-bars");
    if (!container) return;
    container.innerHTML = "";

    if (!rows.length) {
      container.innerHTML = '<div class="usage-empty">No public usage data yet.</div>';
      return;
    }

    const maxTokens = Math.max(...rows.map((row) => Number(row.total_tokens || 0)), 1);
    rows.forEach((row) => {
      const column = document.createElement("div");
      column.className = "metric-bar-column";

      const value = document.createElement("div");
      value.className = "metric-bar-value";
      value.textContent = formatInt(row.total_tokens);

      const bar = document.createElement("div");
      bar.className = "metric-bar-shape";
      bar.style.height = `${Math.max(20, (Number(row.total_tokens || 0) / maxTokens) * 148)}px`;
      bar.title = `${row.hour}: ${formatInt(row.total_tokens)} tokens`;

      const label = document.createElement("div");
      label.className = "metric-bar-label";
      label.textContent = String(row.hour || "").slice(11, 16);

      column.appendChild(value);
      column.appendChild(bar);
      column.appendChild(label);
      container.appendChild(column);
    });
  };

  const requireJson = async (url) => {
    const response = await fetch(url, { cache: "no-store" });
    if (!response.ok) throw new Error(`${response.status} ${response.statusText}`);
    return response.json();
  };

  Promise.all([requireJson(summaryUrl), requireJson(hourlyUrl)])
    .then(([summary, hourly]) => {
      const rows = Array.isArray(hourly.rows) ? hourly.rows : [];
      setField("requests", formatInt(summary.requests));
      setField("total_tokens", formatInt(summary.total_tokens));
      setField("success_rate", formatRate(summary.success_requests, summary.requests));
      setField("avg_latency_ms", formatLatency(summary.avg_latency_ms));
      setField("updated_at", formatTime(summary.updated_at));

      const modelLine = [...new Set(rows.map((row) => row.model).filter(Boolean))];
      setText("usage-model-line", modelLine.join(", ") || "recent hours");
      renderBars(rows);

      const status = document.getElementById("usage-dashboard-status");
      if (status) {
        status.textContent = `Window ${summary.window_hours}h · Allowlisted public aggregates only`;
      }
    })
    .catch((error) => {
      setText("usage-model-line", "unavailable");
      const status = document.getElementById("usage-dashboard-status");
      if (status) {
        status.textContent = `Public metrics unavailable: ${error.message}`;
      }
      renderBars([]);
    });
})();
</script>
