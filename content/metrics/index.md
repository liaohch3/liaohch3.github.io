+++
title = "AI 日常"
description = "最近 30 天和 AI 一起写代码的公开指标。"
draft = false
toc = false
comments = false
+++

<style>
.usage-dashboard {
  display: grid;
  gap: 18px;
  margin: 24px 0 32px;
}

.usage-policy {
  display: grid;
  gap: 10px;
  margin-top: 10px;
}

.usage-policy-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 12px;
}

.usage-policy-card {
  border: 1px solid var(--card-separator-color);
  border-radius: 18px;
  padding: 12px 14px;
  background: color-mix(in srgb, var(--accent-color) 4%, var(--card-background));
}

.usage-policy-title {
  margin: 0 0 8px;
  color: var(--card-text-color-tertiary);
  font-family: var(--code-font-family);
  text-transform: uppercase;
  font-size: 1.1rem;
  letter-spacing: 0.08em;
}

.usage-policy-list {
  margin: 0;
  padding-left: 18px;
  color: var(--card-text-color-secondary);
}

.usage-policy-list li {
  margin-bottom: 8px;
}

.usage-hero {
  display: flex;
  justify-content: space-between;
  gap: 20px;
  align-items: flex-start;
  padding: 24px 24px 20px;
  border: 1px solid var(--card-separator-color);
  border-radius: var(--card-border-radius);
  background: linear-gradient(180deg, rgba(255, 251, 244, 0.98), var(--card-background));
}

.usage-hero-copy {
  max-width: 760px;
}

.usage-hero h2 {
  margin: 6px 0 12px;
  font-size: clamp(3rem, 7vw, 5.5rem);
  line-height: 0.98;
  letter-spacing: -0.06em;
}

.usage-overline,
.usage-hero-copy .usage-subtitle {
  color: var(--card-text-color-tertiary);
  font-family: var(--code-font-family);
  font-size: 1.2rem;
  text-transform: uppercase;
  letter-spacing: 0.08em;
}

.usage-subtitle {
  margin: 0;
  color: var(--card-text-color-secondary);
}

.usage-boundary {
  display: grid;
  gap: 10px;
  margin-top: 12px;
  color: var(--card-text-color-secondary);
  font-size: 1.35rem;
}

.usage-boundary p {
  margin: 0;
}

.usage-meta {
  white-space: nowrap;
  display: grid;
  gap: 4px;
  text-align: right;
  font-family: var(--code-font-family);
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: var(--card-text-color-tertiary);
}

.usage-kpi-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(190px, 1fr));
  gap: 16px;
}

.usage-kpi-card {
  padding: 18px;
  border-radius: 24px;
  border: 1px solid var(--card-separator-color);
  background: radial-gradient(circle at top right, rgba(216, 191, 144, 0.12), transparent 42%),
    linear-gradient(180deg, rgba(255, 251, 244, 0.95), rgba(255, 255, 255, 0.96));
}

.usage-kpi-label {
  color: var(--card-text-color-tertiary);
  font-family: var(--code-font-family);
  text-transform: uppercase;
  letter-spacing: 0.08em;
  font-size: 1.1rem;
}

.usage-kpi-value {
  display: block;
  margin-top: 12px;
  color: var(--card-text-color-main);
  font-size: clamp(2.8rem, 4vw, 3.6rem);
  line-height: 1.02;
}

.usage-kpi-copy {
  margin-top: 9px;
  color: var(--card-text-color-secondary);
  font-size: 1.3rem;
  line-height: 1.6;
}

.usage-main-grid {
  display: grid;
  grid-template-columns: minmax(0, 1.45fr) minmax(270px, 1fr);
  gap: 16px;
  align-items: stretch;
}

.usage-panel {
  padding: 18px;
  border-radius: 24px;
  border: 1px solid var(--card-separator-color);
  background: linear-gradient(180deg, rgba(255, 252, 246, 0.95), var(--card-background));
}

.usage-panel h3 {
  margin: 0 0 10px;
  font-size: clamp(2rem, 3.2vw, 3rem);
  letter-spacing: -0.04em;
  line-height: 1.08;
}

.usage-panel-sub {
  color: var(--card-text-color-tertiary);
  font-family: var(--code-font-family);
  font-size: 1.15rem;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  margin-bottom: 14px;
}

.usage-panel-headline {
  margin-top: 0;
}

.usage-spotlight {
  padding: 14px;
  border-radius: 18px;
  margin-bottom: 12px;
  border: 1px solid color-mix(in srgb, var(--accent-color) 10%, var(--card-separator-color));
  background: linear-gradient(180deg, rgba(238, 245, 225, 0.55), rgba(255, 255, 255, 0.95));
}

.usage-spotlight-mode {
  color: var(--card-text-color-tertiary);
  font-family: var(--code-font-family);
  text-transform: uppercase;
  font-size: 1.1rem;
  letter-spacing: 0.08em;
}

.usage-spotlight-title {
  margin: 6px 0 8px;
  font-size: clamp(2.4rem, 3vw, 2.9rem);
  line-height: 1.05;
}

.usage-spotlight-summary {
  margin-top: 8px;
  color: var(--card-text-color-secondary);
  line-height: 1.7;
  max-width: 38ch;
}

.usage-spotlight-stats {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(110px, 1fr));
  margin-top: 14px;
  gap: 8px;
}

.usage-stat {
  padding: 8px 10px;
  border-radius: 12px;
  border: 1px solid var(--card-separator-color);
  background: var(--card-background);
}

.usage-stat strong {
  display: block;
  margin-top: 4px;
  color: var(--card-text-color-main);
  font-size: 1.8rem;
  line-height: 1;
}

.usage-stat span {
  color: var(--card-text-color-tertiary);
  font-family: var(--code-font-family);
  text-transform: uppercase;
  font-size: 1.05rem;
}

.usage-day-shell {
  padding: 14px 4px 10px;
  border-radius: 18px;
  border: 1px solid var(--card-separator-color);
  background: linear-gradient(180deg, rgba(247, 244, 236, 0.75), var(--card-background));
}

.usage-day-summary {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-bottom: 12px;
}

.usage-day-pill {
  padding: 8px 12px;
  border-radius: 999px;
  border: 1px solid var(--card-separator-color);
  font-size: 1.15rem;
  color: var(--card-text-color-secondary);
  line-height: 1.35;
}

.usage-day-pill strong {
  display: inline;
  color: var(--card-text-color-main);
}

.usage-day-bars {
  position: relative;
  display: grid;
  grid-template-columns: repeat(var(--usage-day-columns, 30), minmax(9px, 1fr));
  gap: 8px;
  align-items: end;
  min-height: 180px;
}

.usage-day-bar {
  appearance: none;
  width: 100%;
  border: none;
  border-radius: 16px;
  background: transparent;
  padding: 0;
  cursor: pointer;
  display: flex;
  align-items: end;
  min-height: 24px;
}

.usage-day-bar-frame {
  position: relative;
  width: 100%;
  min-height: 100%;
  border-radius: 14px;
  background: linear-gradient(180deg, rgba(236, 233, 225, 0.6), rgba(236, 232, 223, 0.95));
  padding-top: 2px;
  transition: transform 0.15s ease, box-shadow 0.15s ease, background 0.15s ease;
}

.usage-day-bar-fill {
  display: block;
  width: 100%;
  min-height: 6px;
  max-height: 100%;
  border-radius: 10px 10px 5px 5px;
  background: linear-gradient(180deg, #9fd373, #239a3b);
  height: var(--day-bar-height, 8px);
}

.usage-day-bar.is-idle .usage-day-bar-fill {
  background: linear-gradient(180deg, #e7e2d8, #d1c8b8);
}

.usage-day-bar:hover .usage-day-bar-frame,
.usage-day-bar:focus-visible .usage-day-bar-frame,
.usage-day-bar.is-focus .usage-day-bar-frame {
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(36, 122, 61, 0.16);
}

.usage-day-bar.is-locked .usage-day-bar-frame {
  box-shadow: inset 0 0 0 2px rgba(35, 154, 59, 0.3);
}

.usage-axis {
  margin-top: 8px;
  display: flex;
  justify-content: space-between;
  color: var(--card-text-color-tertiary);
  font-family: var(--code-font-family);
  font-size: 1.1rem;
}

.usage-drill {
  margin-top: 14px;
}

.usage-hour-grid,
.usage-mix {
  display: grid;
  gap: 8px;
  margin-top: 10px;
}

.usage-hour-grid {
  grid-template-columns: repeat(24, minmax(6px, 1fr));
  align-items: end;
}

.usage-hour-bar,
.usage-origin-bar {
  appearance: none;
  border: none;
  padding: 0;
  background: transparent;
  width: 100%;
  display: flex;
  align-items: end;
  min-height: 90px;
  cursor: pointer;
}

.usage-hour-fill {
  width: 100%;
  border-radius: 999px 999px 5px 5px;
  background: linear-gradient(180deg, #78b893, #1f6f57);
  height: var(--hour-bar-height, 8px);
}

.usage-hour-bar.is-idle .usage-hour-fill,
.usage-origin-bar.is-idle .usage-origin-fill {
  background: linear-gradient(180deg, #e9e4db, #cfc6b7);
}

.usage-hour-bar:hover .usage-hour-fill,
.usage-hour-bar:focus-visible .usage-hour-fill {
  box-shadow: 0 0 0 2px rgba(31, 111, 87, 0.18);
}

.usage-hour-axes {
  margin-top: 6px;
  display: flex;
  justify-content: space-between;
  color: var(--card-text-color-tertiary);
  font-family: var(--code-font-family);
  font-size: 1rem;
  letter-spacing: 0.04em;
}

.usage-health {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 8px;
  margin-top: 6px;
}

.usage-health-card {
  padding: 10px;
  border-radius: 12px;
  border: 1px solid var(--card-separator-color);
  background: var(--card-background);
}

.usage-health-card span {
  color: var(--card-text-color-tertiary);
  font-family: var(--code-font-family);
  font-size: 1.05rem;
  text-transform: uppercase;
}

.usage-health-card strong {
  display: block;
  margin-top: 6px;
  color: var(--card-text-color-main);
  font-size: clamp(1.6rem, 2vw, 2rem);
}

.usage-rank-list {
  margin-top: 10px;
  display: grid;
  gap: 10px;
}

.usage-rank-item {
  display: grid;
  grid-template-columns: 1fr auto;
  gap: 10px;
  align-items: center;
  padding: 10px;
  border-radius: 14px;
  border: 1px solid var(--card-separator-color);
  background: var(--card-background);
}

.usage-rank-meta {
  display: grid;
  gap: 2px;
}

.usage-rank-value {
  font-size: 1.3rem;
  color: var(--card-text-color-main);
}

.usage-rank-share {
  color: var(--card-text-color-tertiary);
  font-family: var(--code-font-family);
  font-size: 1.02rem;
}

.usage-rank-track {
  height: 8px;
  border-radius: 999px;
  background: #ece8df;
  overflow: hidden;
  margin-top: 5px;
}

.usage-rank-fill {
  height: 100%;
  background: linear-gradient(90deg, #9fd373, #23743a);
}

.usage-origin-grid {
  margin-top: 10px;
  display: grid;
  gap: 14px;
}

.usage-origin-block h4 {
  margin: 0 0 8px;
  color: var(--card-text-color-tertiary);
  font-family: var(--code-font-family);
  font-size: 1.2rem;
  text-transform: uppercase;
}

.usage-origin-row {
  display: grid;
  gap: 6px;
  margin-bottom: 8px;
}

.usage-origin-head {
  display: flex;
  justify-content: space-between;
  gap: 8px;
  font-size: 1.2rem;
}

.usage-origin-name {
  color: var(--card-text-color-main);
}

.usage-origin-name strong {
  color: var(--card-text-color-secondary);
}

.usage-origin-bar {
  position: relative;
  width: 100%;
  display: block;
  height: 12px;
  border-radius: 999px;
  background: #ece8df;
  overflow: hidden;
}

.usage-origin-fill {
  position: absolute;
  inset: 0 auto 0 0;
  width: 0;
  border-radius: 999px;
  background: linear-gradient(90deg, #f0c07c, #af6b25);
}

.usage-tooltip {
  position: fixed;
  z-index: 999;
  min-width: 220px;
  max-width: 280px;
  border-radius: 16px;
  padding: 12px 14px;
  border: 1px solid rgba(255, 255, 255, 0.1);
  background: rgba(24, 21, 17, 0.94);
  color: #fffdf7;
  box-shadow: 0 18px 50px rgba(0, 0, 0, 0.24);
  pointer-events: none;
}

.usage-tooltip-title {
  margin-bottom: 8px;
  color: rgba(255, 253, 247, 0.76);
  font-family: var(--code-font-family);
  font-size: 1.15rem;
  text-transform: uppercase;
  letter-spacing: 0.08em;
}

.usage-tooltip-row {
  display: flex;
  justify-content: space-between;
  gap: 16px;
  font-size: 1.3rem;
}

.usage-tooltip-row + .usage-tooltip-row {
  margin-top: 6px;
}

.usage-empty {
  padding: 12px;
  border-radius: 12px;
  border: 1px dashed var(--card-separator-color);
  color: var(--card-text-color-secondary);
  text-align: center;
}

@media (max-width: 1200px) {
  .usage-main-grid {
    grid-template-columns: 1fr;
  }

  .usage-hero,
  .usage-kpi-grid {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 768px) {
  .usage-hero {
    flex-direction: column;
  }

  .usage-meta {
    white-space: normal;
    text-align: left;
  }

  .usage-day-bars {
    grid-template-columns: repeat(var(--usage-day-columns, 30), minmax(7px, 1fr));
    gap: 6px;
  }

  .usage-main-grid {
    gap: 10px;
  }

  .usage-kpi-grid,
  .usage-spotlight-stats,
  .usage-health {
    grid-template-columns: 1fr;
  }

  .usage-policy-grid {
    grid-template-columns: 1fr;
  }
}
</style>

<div class="usage-dashboard">
  <div class="usage-hero">
  <div class="usage-hero-copy">
      <div class="usage-overline">AI 日常 · 对外指标页</div>
      <h2>最近 30 天公开节奏与质量</h2>
      <p class="usage-subtitle">本页为对外展示的运行级汇总指标：只保留聚合后的 token、请求、成功率、模型和时段分布，不暴露任何输入内容、仓库信息与执行细节。</p>
      <div class="usage-boundary">
        <p><strong>展示边界（本页）</strong></p>
        <div class="usage-policy">
          <div class="usage-policy-grid">
            <div class="usage-policy-card">
              <div class="usage-policy-title">适合公开</div>
              <ul class="usage-policy-list">
                <li>近 30 天汇总 token、请求与成功率</li>
                <li>模型偏好与时段偏好</li>
                <li>来源、客户端与平均延迟</li>
              </ul>
            </div>
            <div class="usage-policy-card">
              <div class="usage-policy-title">不适合公开</div>
              <ul class="usage-policy-list">
                <li>Prompt 文本、命令参数、工具入参</li>
                <li>仓库路径与代码片段</li>
                <li>逐条工具调用记录</li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    </div>
    <div class="usage-meta">
      <div id="usage-updated">--</div>
      <div id="usage-window">--</div>
      <div id="usage-stale" class="usage-empty" hidden></div>
    </div>
  </div>
  <div class="usage-kpi-grid">
    <div class="usage-kpi-card">
      <div class="usage-kpi-label">总 token</div>
      <strong class="usage-kpi-value" id="kpi-total-tokens">--</strong>
      <div class="usage-kpi-copy" id="kpi-token-breakdown">--</div>
    </div>
    <div class="usage-kpi-card">
      <div class="usage-kpi-label">请求数</div>
      <strong class="usage-kpi-value" id="kpi-requests">--</strong>
      <div class="usage-kpi-copy" id="kpi-success-rate">--</div>
    </div>
    <div class="usage-kpi-card">
      <div class="usage-kpi-label">请求延迟</div>
      <strong class="usage-kpi-value" id="kpi-avg-latency">--</strong>
      <div class="usage-kpi-copy" id="kpi-failures">--</div>
    </div>
    <div class="usage-kpi-card">
      <div class="usage-kpi-label">活跃节奏</div>
      <strong class="usage-kpi-value" id="kpi-active-days">--</strong>
      <div class="usage-kpi-copy" id="kpi-peak-day">--</div>
    </div>
    <div class="usage-kpi-card">
      <div class="usage-kpi-label">平均每请求 token</div>
      <strong class="usage-kpi-value" id="kpi-avg-tokens-per-request">--</strong>
      <div class="usage-kpi-copy" id="kpi-latency-note">--</div>
    </div>
  </div>
  <div class="usage-main-grid">
    <div class="usage-panel">
      <h3>30 天活动节奏</h3>
      <div class="usage-panel-sub" id="day-caption">悬停看当天详情，点击锁定</div>
      <div class="usage-spotlight" id="day-spotlight"></div>
      <div class="usage-day-shell">
        <div class="usage-day-summary" id="day-summary"></div>
        <div class="usage-day-bars" id="day-bars"></div>
      </div>
      <div class="usage-axis" id="day-axis"></div>
      <div class="usage-drill">
        <h4>选中日期的下钻（按小时）</h4>
        <div class="usage-hour-grid" id="day-hour-chart"></div>
        <div class="usage-hour-axes">
          <span>00</span>
          <span>06</span>
          <span>12</span>
          <span>18</span>
          <span>23</span>
        </div>
      </div>
    </div>
    <div class="usage-panel">
      <h3>模型偏好</h3>
      <div class="usage-panel-sub">近 30 天 token Top 6</div>
      <div class="usage-rank-list" id="model-list"></div>
    </div>
    <div class="usage-panel">
      <h3>时段偏好</h3>
      <div class="usage-panel-sub">近 30 天整体时间分布</div>
      <div class="usage-hour-grid" id="hour-rhythm"></div>
      <div class="usage-hour-axes">
        <span>00</span>
        <span>06</span>
        <span>12</span>
        <span>18</span>
        <span>23</span>
      </div>
    </div>
    <div class="usage-panel">
      <h3>请求质量</h3>
      <div class="usage-health" id="health-grid"></div>
    </div>
    <div class="usage-panel">
      <h3>来源与客户端</h3>
      <div class="usage-origin-grid" id="origin-grid"></div>
    </div>
  </div>
  <div class="usage-tooltip" id="usage-tooltip" hidden></div>
</div>

<script>
(() => {
  const summaryUrl = "/data/ai-usage-summary.json";
  const hourlyUrl = "/data/ai-usage-hourly.json";
  const dailyUrl = "/data/ai-usage-daily.json";
  const insightUrl = "/data/ai-usage-insights.json";
  const VISIBLE_DAYS = 30;

  const state = {
    summary: null,
    hourlyRows: [],
    dailyRows: [],
    allDailyRows: [],
    allHourlyRows: [],
    insights: null,
    dailyByDate: new Map(),
    hourlyByDate: new Map(),
    defaultDate: null,
    hoverDate: null,
    lockedDate: null,
    windowTrimmed: false,
    dayNodes: new Map(),
  };

  const tooltip = document.getElementById("usage-tooltip");

  const escapeHtml = (value) =>
    String(value ?? "").replace(/[&<>"']/g, (char) => ({
      "&": "&amp;",
      "<": "&lt;",
      ">": "&gt;",
      '"': "&quot;",
      "'": "&#39;",
    }[char]));

  const formatInt = (value) => new Intl.NumberFormat("zh-CN").format(Number(value || 0));

  const formatPercent = (value, total) => {
    const denominator = Number(total || 0);
    if (!denominator) return "0%";
    return `${Math.round((Number(value || 0) / denominator) * 100)}%`;
  };

  const formatLatency = (value) => {
    const ms = Number(value || 0);
    if (!ms) return "--";
    if (ms >= 1000) return `${(ms / 1000).toFixed(ms >= 10000 ? 1 : 2)}s`;
    return `${Math.round(ms)}ms`;
  };

  const formatDateShort = (value) => {
    const dt = new Date(`${value}T00:00:00Z`);
    if (Number.isNaN(dt.getTime())) return value;
    return dt.toLocaleDateString("zh-CN", { month: "numeric", day: "numeric", timeZone: "UTC" });
  };

  const formatDateWeekday = (value) => {
    const dt = new Date(`${value}T00:00:00Z`);
    if (Number.isNaN(dt.getTime())) return value;
    return dt.toLocaleDateString("zh-CN", {
      month: "numeric",
      day: "numeric",
      weekday: "short",
      timeZone: "UTC",
    });
  };

  const toLocaleTs = (value) => {
    if (!value) return "--";
    const dt = new Date(value);
    if (Number.isNaN(dt.getTime())) return value;
    return dt.toLocaleString("zh-CN", { hour12: false });
  };

  const sumBy = (rows, key) => rows.reduce((total, row) => total + Number(row[key] || 0), 0);

  const weightedAverage = (rows, valueKey, weightKey) => {
    const total = rows.reduce(
      (acc, row) => {
        const weight = Number(row[weightKey] || 0);
        acc.weight += weight;
        acc.total += Number(row[valueKey] || 0) * weight;
        return acc;
      },
      { weight: 0, total: 0 }
    );
    return total.weight ? total.total / total.weight : 0;
  };

  const setText = (id, value) => {
    const node = document.getElementById(id);
    if (node) node.textContent = value;
  };

  const buildDateMap = (rows) =>
    rows.reduce((acc, row) => {
      const key = String(row.hour || "").slice(0, 10);
      if (!acc.has(key)) acc.set(key, []);
      acc.get(key).push(row);
      return acc;
    }, new Map());

  const aggregateBy = (rows, key, metric) => {
    const out = new Map();
    rows.forEach((row) => {
      const k = String(row[key] || "unknown");
      const v = Number(row[metric] || 0);
      out.set(k, (out.get(k) || 0) + v);
    });
    return out;
  };

  const mapToSortedList = (map) =>
    [...map.entries()].sort((a, b) => Number(b[1]) - Number(a[1])).map(([name, value]) => ({ name, value }));

  const tooltipMarkup = (title, rows) => `
    <div class="usage-tooltip-title">${escapeHtml(title)}</div>
    ${rows
      .map(
        ([label, value]) => `
          <div class="usage-tooltip-row">
            <span>${escapeHtml(label)}</span>
            <strong>${escapeHtml(value)}</strong>
          </div>
        `
      )
      .join("")}
  `;

  const showTooltip = (x, y, html) => {
    if (!tooltip) return;
    tooltip.hidden = false;
    tooltip.innerHTML = html;
    const padding = 12;
    tooltip.style.left = `${Math.max(12, x + padding)}px`;
    tooltip.style.top = `${Math.max(12, y + padding)}px`;
    const rect = tooltip.getBoundingClientRect();
    if (rect.right > window.innerWidth - 12) tooltip.style.left = `${window.innerWidth - rect.width - 12}px`;
    if (rect.bottom > window.innerHeight - 12) tooltip.style.top = `${y - rect.height - padding}px`;
  };

  const hideTooltip = () => {
    if (!tooltip) return;
    tooltip.hidden = true;
    tooltip.innerHTML = "";
  };

  const requireJson = async (url) => {
    const response = await fetch(url, { cache: "no-store" });
    if (!response.ok) throw new Error(`${response.status} ${response.statusText}`);
    return response.json();
  };

  const getFocusDate = () => state.hoverDate || state.lockedDate || state.defaultDate;

  const buildDayDetail = (date) => {
    const daily = state.dailyByDate.get(date) || { date, total_tokens: 0, input_tokens: 0, output_tokens: 0, tool_calls: 0, cache_read_input_tokens: 0, cache_creation_input_tokens: 0 };
    const hourly = state.hourlyByDate.get(date) || [];
    const requests = sumBy(hourly, "requests");
    const successRequests = sumBy(hourly, "success_requests");
    const failedRequests = sumBy(hourly, "failed_requests");
    const avgLatency = weightedAverage(hourly, "avg_latency_ms", "requests");
    const peakRow = hourly.reduce((best, row) => {
      if (!best || Number(row.total_tokens || 0) > Number(best.total_tokens || 0)) return row;
      return best;
    }, null);
    const modelMap = aggregateBy(hourly, "model", "total_tokens");
    const sourceMap = aggregateBy(hourly, "source", "total_tokens");
    const activeHours = hourly.filter((row) => Number(row.total_tokens || 0) > 0).length;

    return {
      date,
      totalTokens: Number(daily.total_tokens || 0),
      inputTokens: Number(daily.input_tokens || 0),
      outputTokens: Number(daily.output_tokens || 0),
      cacheRead: Number(daily.cache_read_input_tokens || 0),
      cacheWrite: Number(daily.cache_creation_input_tokens || 0),
      toolCalls: Number(daily.tool_calls || 0),
      requests,
      successRequests,
      failedRequests,
      avgLatency,
      shareOfWindow:
        Number(state.summary?.total_tokens || 0)
          ? Math.round((Number(daily.total_tokens || 0) / Number(state.summary.total_tokens || 0)) * 100)
          : 0,
      successRate: requests ? Math.round((successRequests / requests) * 100) : 0,
      peakHour: peakRow ? String(peakRow.hour || "").slice(11, 16) : "--",
      modelMix: mapToSortedList(modelMap),
      sourceMix: mapToSortedList(sourceMap),
      activeHours,
    };
  };

  const renderTop = () => {
    const summary = state.summary || {};
    const requests = Number(summary.requests || 0);
    const success = Number(summary.success_requests || 0);
    const failed = Number(summary.failed_requests || 0);
    const activeRows = state.dailyRows.filter((row) => Number(row.total_tokens || 0) > 0);
    const activeDays = activeRows.length;
    const quietDays = Math.max(state.dailyRows.length - activeDays, 0);
    const avgLatency = Number(summary.avg_latency_ms || 0);
    const updated = summary.updated_at;
    const avgTokensPerRequest = requests ? Number(summary.total_tokens || 0) / requests : 0;
    const effectiveWindow = Math.max(state.dailyRows.length, 1);
    const peakDateRow = [...state.dailyRows]
      .filter((row) => Number(row.total_tokens || 0) > 0)
      .reduce((best, row) => {
        if (!best || Number(row.total_tokens || 0) > Number(best.total_tokens || 0)) return row;
        return best;
      }, null);
    const modelRows = state.insights?.model_mix || [];
    const primaryModel = modelRows[0];
    const modelText = primaryModel ? `${primaryModel.model} (${primaryModel.share}%)` : "--";

    const staleHours = updated ? (Date.now() - new Date(updated).getTime()) / (1000 * 60 * 60) : null;
    const staleNode = document.getElementById("usage-stale");
    if (staleNode) {
      if (staleHours !== null && Number.isFinite(staleHours) && staleHours > 2) {
        staleNode.hidden = false;
        staleNode.textContent = `更新告警：超过 2 小时未刷新（${Math.round(staleHours)} 小时）`;
      } else if (staleNode) {
        staleNode.hidden = true;
        staleNode.textContent = "";
      }
    }

    setText("usage-updated", `数据更新时间：${toLocaleTs(updated)}`);
    setText("kpi-total-tokens", formatInt(summary.total_tokens || 0));
    setText(
      "kpi-token-breakdown",
      `输入 ${formatInt(summary.input_tokens || 0)} · 输出 ${formatInt(summary.output_tokens || 0)} · Cache 读取 ${formatInt(summary.cache_read_input_tokens || 0)}`
    );
    setText("kpi-requests", formatInt(requests));
    setText("kpi-success-rate", `成功率 ${requests ? `${Math.round((success / requests) * 100)}%` : "—"}`);
    setText("kpi-avg-latency", formatLatency(avgLatency));
    setText("kpi-failures", `失败 ${formatInt(failed)}；工具调用 ${formatInt(summary.tool_calls || 0)}`);
    setText("kpi-active-days", `${activeDays}/${effectiveWindow} 天`);
    setText("kpi-peak-day", `主力模型 ${modelText} · ${quietDays} 天留白`);
    setText("kpi-avg-tokens-per-request", formatInt(Math.round(avgTokensPerRequest)));
    setText("kpi-latency-note", `峰值日 ${formatInt((peakDateRow?.total_tokens || 0))}`);

    if (state.windowTrimmed) {
      setText("kpi-latency-note", `仅展示最近 ${state.dailyRows.length} 天（共 ${state.allDailyRows.length} 天）`);
    }
  };

  const renderModelChart = () => {
    const container = document.getElementById("model-list");
    if (!container) return;
    const rows = state.insights?.model_mix || [];
    container.innerHTML = "";
    if (!rows.length) {
      container.innerHTML = '<div class="usage-empty">暂无模型数据</div>';
      return;
    }

    rows.forEach((row, idx) => {
      const item = document.createElement("button");
      item.type = "button";
      item.className = "usage-rank-item";
      item.setAttribute("aria-label", `${row.model} ${row.share}%，${formatInt(row.total_tokens)} Token`);
      const width = Math.min(Math.max(Number(row.total_tokens || 0) / Math.max(rows[0].total_tokens || 1, 1), 0), 1);
      const tooltipHtml = tooltipMarkup(row.model, [
        ["Token", `${formatInt(row.total_tokens)}`],
        ["占比", `${row.share}%`],
        ["排序", `${idx + 1} / ${rows.length}`],
      ]);
      item.innerHTML = `
        <div class="usage-rank-meta">
          <span>${escapeHtml(row.model)}</span>
          <strong class="usage-rank-value">${escapeHtml(formatInt(row.total_tokens))}</strong>
        </div>
        <strong class="usage-rank-share">${escapeHtml(`${row.share}%`)}</strong>
        <div class="usage-rank-track"><div class="usage-rank-fill" style="width:${Math.round(width * 100)}%"></div></div>
      `;
      item.addEventListener("mouseenter", (event) => showTooltip(event.clientX, event.clientY, tooltipHtml));
      item.addEventListener("mousemove", (event) => showTooltip(event.clientX, event.clientY, tooltipHtml));
      item.addEventListener("mouseleave", hideTooltip);
      item.addEventListener("focus", () => showTooltip(item.getBoundingClientRect().left, item.getBoundingClientRect().top, tooltipHtml));
      item.addEventListener("blur", hideTooltip);
      container.appendChild(item);
    });
  };

  const renderHealth = () => {
    const summary = state.summary || {};
    const requests = Number(summary.requests || 0);
    const success = Number(summary.success_requests || 0);
    const failed = Number(summary.failed_requests || 0);
    const avgLatency = Number(summary.avg_latency_ms || 0);
    const toolCalls = Number(summary.tool_calls || 0);
    const cacheWrite = Number(summary.cache_creation_input_tokens || 0);
    const container = document.getElementById("health-grid");
    if (!container) return;

    const rows = [
      ["请求总量", formatInt(requests)],
      ["成功率", requests ? `${Math.round((success / requests) * 100)}%` : "--"],
      ["失败率", requests ? `${Math.round((failed / requests) * 100)}%` : "--"],
      ["平均延迟", formatLatency(avgLatency)],
      ["工具调用", formatInt(toolCalls)],
      ["Cache 写入", formatInt(cacheWrite)],
    ];

    container.innerHTML = rows
      .map(
        ([label, value]) => `
          <div class="usage-health-card">
            <span>${escapeHtml(label)}</span>
            <strong>${escapeHtml(value)}</strong>
          </div>
        `
      )
      .join("");
  };

  const renderOriginClient = () => {
    const container = document.getElementById("origin-grid");
    if (!container) return;
    container.innerHTML = "";
    const sourceMap = aggregateBy(state.hourlyRows, "source", "total_tokens");
    const clientMap = aggregateBy(state.hourlyRows, "client", "total_tokens");
    const sourceRows = mapToSortedList(sourceMap);
    const clientRows = mapToSortedList(clientMap);
    const totalSource = sourceRows.reduce((total, row) => total + row.value, 0) || 1;
    const totalClient = clientRows.reduce((total, row) => total + row.value, 0) || 1;

    const renderGroup = (title, rows, total, barClass) => {
      const group = document.createElement("div");
      group.className = "usage-origin-block";
      group.innerHTML = `
        <h4>${escapeHtml(title)}</h4>
      `;

      rows.forEach((entry) => {
        const percent = Math.round((entry.value / total) * 100);
        const row = document.createElement("div");
        row.className = "usage-origin-row";
        row.innerHTML = `
          <div class="usage-origin-head">
            <span class="usage-origin-name">${escapeHtml(entry.name)} <strong>${escapeHtml(percent)}%</strong></span>
            <span>${escapeHtml(formatInt(entry.value))}</span>
          </div>
          <span class="usage-origin-bar"><span class="usage-origin-fill ${barClass}" style="width:${percent}%"></span></span>
        `;
        const tooltipHtml = tooltipMarkup(`${title} · ${entry.name}`, [["Token", `${formatInt(entry.value)}`], ["占比", `${percent}%`]]);
        row.addEventListener("mouseenter", (event) => showTooltip(event.clientX, event.clientY, tooltipHtml));
        row.addEventListener("mousemove", (event) => showTooltip(event.clientX, event.clientY, tooltipHtml));
        row.addEventListener("mouseleave", hideTooltip);
        group.appendChild(row);
      });
      container.appendChild(group);
    };

    if (!sourceRows.length && !clientRows.length) {
      container.innerHTML = '<div class="usage-empty">暂无来源/客户端数据</div>';
      return;
    }

    renderGroup("来源", sourceRows, totalSource);
    renderGroup("客户端", clientRows, totalClient, "usage-origin-fill");
  };

  const renderHourRhythm = () => {
    const container = document.getElementById("hour-rhythm");
    if (!container) return;
    container.innerHTML = "";

    const totalMap = new Map(
      (state.insights?.hour_mix || []).map((row) => [row.hour, Number(row.total_tokens || 0)])
    );
    const rows = Array.from({ length: 24 }, (_, hour) => {
      const key = `${String(hour).padStart(2, "0")}:00`;
      return { hour, total_tokens: totalMap.get(key) || 0 };
    });
    const maxValue = Math.max(...rows.map((row) => Number(row.total_tokens || 0)), 0);
    if (!maxValue) {
      container.innerHTML = '<div class="usage-empty">暂时还没有按小时聚合数据</div>';
      return;
    }

    rows.forEach((row) => {
      const button = document.createElement("button");
      button.type = "button";
      button.className = `usage-hour-bar ${row.total_tokens > 0 ? "is-active" : "is-idle"}`;
      button.style.setProperty("--hour-bar-height", `${maxValue ? Math.max((row.total_tokens / maxValue) * 120, 6) : 6}px`);
      button.setAttribute("aria-label", `${String(row.hour).padStart(2, "0")}:00 ${formatInt(row.total_tokens)} Token`);
      button.innerHTML = '<span class="usage-hour-fill"></span>';
      const tooltipRows = [
        [`${String(row.hour).padStart(2, "0")}:00`, formatInt(row.total_tokens)],
        ["指标", "时间片总 Token"],
      ];
      const tooltipHtml = tooltipMarkup(`${String(row.hour).padStart(2, "0")}:00`, tooltipRows);
      button.addEventListener("mouseenter", (event) => showTooltip(event.clientX, event.clientY, tooltipHtml));
      button.addEventListener("mousemove", (event) => showTooltip(event.clientX, event.clientY, tooltipHtml));
      button.addEventListener("mouseleave", hideTooltip);
      button.addEventListener("focus", () => showTooltip(button.getBoundingClientRect().left, button.getBoundingClientRect().top, tooltipHtml));
      button.addEventListener("blur", hideTooltip);
      container.appendChild(button);
    });
  };

  const renderDayBars = () => {
    const summary = document.getElementById("day-summary");
    const chart = document.getElementById("day-bars");
    const axis = document.getElementById("day-axis");
    if (!chart || !axis) return;

    if (!state.dailyRows.length) {
      summary.innerHTML = '<div class="usage-empty">暂无每日数据</div>';
      chart.innerHTML = "";
      axis.innerHTML = "";
      return;
    }

    const activeRows = state.dailyRows.filter((row) => Number(row.total_tokens || 0) > 0);
    const biggest = activeRows.reduce((best, row) => {
      if (!best || Number(row.total_tokens || 0) > Number(best.total_tokens || 0)) return row;
      return best;
    }, null);
    const latest = [...activeRows].reverse()[0] || state.dailyRows.at(-1);
    summary.innerHTML = `
      <div class="usage-day-pill"><span>活跃天数</span> <strong>${activeRows.length}/${state.dailyRows.length}</strong></div>
      <div class="usage-day-pill"><span>最大单日</span> <strong>${formatInt(biggest ? biggest.total_tokens : 0)} tokens</strong></div>
      <div class="usage-day-pill"><span>最近有数据</span> <strong>${latest ? formatDateShort(latest.date) : "--"}</strong></div>
    `;

    chart.innerHTML = "";
    chart.style.setProperty("--usage-day-columns", String(state.dailyRows.length || 1));
    state.dayNodes.clear();
    const maxValue = Math.max(...state.dailyRows.map((row) => Number(row.total_tokens || 0)), 0);
    const maxDate = state.dailyRows[state.dailyRows.length - 1]?.date;
    const firstDate = state.dailyRows[0]?.date;
    state.dailyRows.forEach((row, index) => {
      const total = Number(row.total_tokens || 0);
      const height = maxValue ? Math.max((total / maxValue) * 110, 8) : 8;
      const button = document.createElement("button");
      button.type = "button";
      button.className = `usage-day-bar ${total > 0 ? "is-active" : "is-idle"}`;
      button.dataset.date = row.date;
      button.style.setProperty("--day-bar-height", `${Math.round(height)}px`);
      button.setAttribute("aria-label", `${formatDateWeekday(row.date)} ${formatInt(total)} Token`);
      button.innerHTML = `
        <span class="usage-day-bar-frame">
          <span class="usage-day-bar-fill" style="height:${Math.round(height)}px"></span>
        </span>
      `;

      const tooltipRows = [
        ["Token", `${formatInt(total)}`],
        ["日期", formatDateWeekday(row.date)],
        ["窗口位次", `${index + 1}/${state.dailyRows.length}`],
      ];
      if (firstDate && maxDate) {
        tooltipRows.push(["窗口", `${formatDateShort(firstDate)} ~ ${formatDateShort(maxDate)}`]);
      }
      const tooltipHtml = tooltipMarkup(formatDateWeekday(row.date), tooltipRows);

      button.addEventListener("mouseenter", (event) => {
        state.hoverDate = row.date;
        renderInteractiveState();
        showTooltip(event.clientX, event.clientY, tooltipHtml);
      });
      button.addEventListener("mousemove", (event) => showTooltip(event.clientX, event.clientY, tooltipHtml));
      button.addEventListener("mouseleave", () => {
        if (state.hoverDate === row.date) {
          state.hoverDate = null;
          renderInteractiveState();
        }
        hideTooltip();
      });
      button.addEventListener("focus", () => {
        state.hoverDate = row.date;
        renderInteractiveState();
        showTooltip(button.getBoundingClientRect().left, button.getBoundingClientRect().top, tooltipHtml);
      });
      button.addEventListener("blur", () => {
        if (state.hoverDate === row.date) {
          state.hoverDate = null;
          renderInteractiveState();
        }
        hideTooltip();
      });
      button.addEventListener("click", () => {
        state.lockedDate = state.lockedDate === row.date ? null : row.date;
        renderInteractiveState();
      });
      button.addEventListener("keydown", (event) => {
        if (event.key === "Enter" || event.key === " ") {
          event.preventDefault();
          state.lockedDate = state.lockedDate === row.date ? null : row.date;
          renderInteractiveState();
        }
      });

      state.dayNodes.set(row.date, button);
      chart.appendChild(button);
    });

    const tickIndexes = [0, Math.floor((state.dailyRows.length - 1) * 0.25), Math.floor((state.dailyRows.length - 1) * 0.5), Math.floor((state.dailyRows.length - 1) * 0.75), state.dailyRows.length - 1]
      .map((idx) => Math.min(Math.max(idx, 0), state.dailyRows.length - 1));
    const uniqueIndexes = [...new Set(tickIndexes)];
    axis.innerHTML = uniqueIndexes.map((idx) => `<span>${escapeHtml(formatDateShort(state.dailyRows[idx].date))}</span>`).join("");
  };

  const renderDayDrilldown = () => {
    const date = getFocusDate();
    const container = document.getElementById("day-hour-chart");
    const detail = buildDayDetail(date);
    if (!container) return;
    container.innerHTML = "";
    const rowHours = state.hourlyByDate.get(date) || [];
    const hourMap = new Map();
    const requestMap = new Map();
    const latencyMap = new Map();
    const latencyWeightMap = new Map();
    for (let hour = 0; hour < 24; hour++) hourMap.set(String(hour).padStart(2, "0"), 0);
    rowHours.forEach((row) => {
      const hour = String(row.hour || "").slice(11, 13);
      const current = hourMap.get(hour) || 0;
      hourMap.set(hour, current + Number(row.total_tokens || 0));
      const currentReq = requestMap.get(hour) || 0;
      requestMap.set(hour, currentReq + Number(row.requests || 0));
      const requestWeight = Number(row.requests || 0);
      if (requestWeight > 0) {
        latencyMap.set(hour, (latencyMap.get(hour) || 0) + Number(row.avg_latency_ms || 0) * requestWeight);
        latencyWeightMap.set(hour, (latencyWeightMap.get(hour) || 0) + requestWeight);
      }
    });

    const rows = Array.from({ length: 24 }, (_, hour) => {
      const key = String(hour).padStart(2, "0");
      return {
        hour: key,
        total_tokens: hourMap.get(key) || 0,
        requests: requestMap.get(key) || 0,
        avg_latency_ms: latencyWeightMap.get(key) ? latencyMap.get(key) / latencyWeightMap.get(key) : 0,
      };
    });
    const maxValue = Math.max(...rows.map((row) => row.total_tokens), 0);
    if (!rowHours.length || !maxValue) {
      container.innerHTML = '<div class="usage-empty">当日暂无明细数据</div>';
      return;
    }

    rows.forEach((row) => {
      const button = document.createElement("button");
      button.type = "button";
      button.className = `usage-hour-bar ${row.total_tokens > 0 ? "is-active" : "is-idle"}`;
      button.style.setProperty("--hour-bar-height", `${maxValue ? Math.max((row.total_tokens / maxValue) * 72, 6) : 6}px`);
      button.setAttribute("aria-label", `${row.hour}:00 ${formatInt(row.total_tokens)} Token`);
      button.innerHTML = '<span class="usage-hour-fill"></span>';
      const tooltipHtml = tooltipMarkup(`${row.hour}:00`, [
        ["日期", formatDateWeekday(date)],
        ["Token", formatInt(row.total_tokens)],
        ["请求", formatInt(row.requests)],
        ["平均延迟", formatLatency(row.avg_latency_ms)],
      ]);
      button.addEventListener("mouseenter", (event) => showTooltip(event.clientX, event.clientY, tooltipHtml));
      button.addEventListener("mousemove", (event) => showTooltip(event.clientX, event.clientY, tooltipHtml));
      button.addEventListener("mouseleave", hideTooltip);
      container.appendChild(button);
    });
  };

  const renderSpotlight = () => {
    const spot = document.getElementById("day-spotlight");
    const caption = document.getElementById("day-caption");
    if (!spot) return;

    const date = getFocusDate();
    const detail = buildDayDetail(date);
    if (!date || !detail) {
      spot.innerHTML = '<div class="usage-empty">暂无可视化焦点</div>';
      return;
    }

    const mode = state.hoverDate ? "hover" : state.lockedDate ? "locked" : "default";
    const modeCopy = mode === "hover" ? "悬停中" : mode === "locked" ? "已锁定" : "默认焦点";
    if (caption) {
      caption.textContent = state.lockedDate ? `已锁定 ${formatDateShort(date)}，再点一次取消` : "悬停看当天详情，点击锁定";
    }

    const footerBits = [
      `请求 ${formatInt(detail.requests)}`,
      `成功 ${detail.requests ? `${detail.successRate}%` : "--"}`,
      `失败 ${formatInt(detail.failedRequests)}`,
      `活跃小时 ${formatInt(detail.activeHours)}`,
      `工具调用 ${formatInt(detail.toolCalls)}`,
    ];
      footerBits.push(`平均延迟 ${formatLatency(detail.avgLatency)}`);
    if (detail.cacheRead) footerBits.push(`Cache 读取 ${formatInt(detail.cacheRead)}`);
    if (detail.cacheWrite) footerBits.push(`Cache 写入 ${formatInt(detail.cacheWrite)}`);
    const topModel = detail.modelMix[0];

    spot.innerHTML = `
      <div class="usage-spotlight-mode">${modeCopy}</div>
      <h4 class="usage-spotlight-title">${escapeHtml(formatDateWeekday(detail.date))}</h4>
      <p class="usage-spotlight-summary">这一天占近 ${state.dailyRows.length} 天公开 token 的 ${detail.shareOfWindow}%，主模型 ${escapeHtml(topModel ? `${topModel.name} (${formatPercent(topModel.value, detail.totalTokens || 1)})` : "--")}。</p>
      <div class="usage-spotlight-stats">
        <div class="usage-stat"><span>总 token</span><strong>${escapeHtml(formatInt(detail.totalTokens))}</strong></div>
        <div class="usage-stat"><span>输入</span><strong>${escapeHtml(formatInt(detail.inputTokens))}</strong></div>
        <div class="usage-stat"><span>输出</span><strong>${escapeHtml(formatInt(detail.outputTokens))}</strong></div>
        <div class="usage-stat"><span>峰值小时</span><strong>${escapeHtml(detail.peakHour)}</strong></div>
        <div class="usage-stat"><span>主模型</span><strong>${escapeHtml(topModel ? `${topModel.name}` : "--")}</strong></div>
      </div>
      <div style="margin-top:10px; display:flex; flex-wrap:wrap; gap:6px;">
        ${footerBits.map((item) => `<span class="usage-day-pill">${escapeHtml(item)}</span>`).join("")}
      </div>
    `;
    renderDayDrilldown();
  };

  const renderInteractiveState = () => {
    const date = getFocusDate();
    if (!date) return;
    renderSpotlight();

    state.dayNodes.forEach((node, nodeDate) => {
      node.classList.toggle("is-focus", nodeDate === date);
      node.classList.toggle("is-locked", nodeDate === state.lockedDate);
      if (nodeDate === date) {
        node.setAttribute("aria-current", "true");
      } else {
        node.removeAttribute("aria-current");
      }
    });
  };

  const renderAll = () => {
    renderTop();
    renderModelChart();
    renderHealth();
    renderOriginClient();
    renderHourRhythm();
    renderDayBars();
    renderInteractiveState();
  };

  const renderError = (message) => {
    const ids = [
      "usage-updated",
      "usage-window",
      "kpi-total-tokens",
      "kpi-token-breakdown",
      "kpi-requests",
      "kpi-success-rate",
      "kpi-avg-latency",
      "kpi-failures",
      "kpi-active-days",
      "kpi-peak-day",
      "kpi-avg-tokens-per-request",
      "kpi-latency-note",
      "day-spotlight",
      "day-summary",
      "day-bars",
      "day-hour-chart",
      "model-list",
      "health-grid",
      "origin-grid",
      "hour-rhythm",
    ];
    ids.forEach((id) => {
      const node = document.getElementById(id);
      if (node) node.innerHTML = `<div class="usage-empty">${escapeHtml(message)}</div>`;
    });
  };

  const load = async () => {
    try {
      const [summary, hourly, daily, insights] = await Promise.all([
        requireJson(summaryUrl),
        requireJson(hourlyUrl),
        requireJson(dailyUrl),
        requireJson(insightUrl),
      ]);

      state.summary = summary || {};
      state.allDailyRows = Array.isArray(daily?.rows) ? daily.rows : [];
      state.allHourlyRows = Array.isArray(hourly?.rows) ? hourly.rows : [];
      state.windowTrimmed = state.allDailyRows.length > VISIBLE_DAYS;

      state.dailyRows = state.allDailyRows.slice(-VISIBLE_DAYS);
      const visibleDateSet = new Set(state.dailyRows.map((row) => row.date));
      state.hourlyRows = state.allHourlyRows.filter((row) => visibleDateSet.has(String(row.hour || "").slice(0, 10)));
      state.insights = insights || { model_mix: [], hour_mix: [] };
      state.dailyByDate = new Map(state.dailyRows.map((row) => [row.date, row]));
      state.hourlyByDate = buildDateMap(state.hourlyRows);

      if (state.allDailyRows.length) {
        const trimmedWindowNotice = state.windowTrimmed
          ? `仅展示最近 ${VISIBLE_DAYS} 天（共 ${state.allDailyRows.length} 天数据）`
          : `展示窗口：最近 ${state.dailyRows.length} 天`;
        setText("usage-window", trimmedWindowNotice);
      }

      const latestActive = [...state.dailyRows].reverse().find((row) => Number(row.total_tokens || 0) > 0);
      state.defaultDate = (latestActive || state.dailyRows.at(-1) || {}).date || null;

      renderAll();
    } catch (error) {
      console.error(error);
      renderError("暂时拉不到公开数据。");
    }
  };

  load();
})();
</script>
