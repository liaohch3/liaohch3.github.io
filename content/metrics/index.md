+++
title = "AI 日常"
description = "最近 30 天和 AI 一起写代码的一些公开记录。"
draft = false
toc = false
comments = false
+++

<div class="public-metrics public-metrics-refined">
  <div class="metric-hero metric-hero-refined">
    <div class="metric-hero-copy">
      <div class="metric-overline">AI 日常</div>
      <h2>最近 30 天的 AI 写码节奏</h2>
      <p>只看哪天开工、强度多高、通常在哪个时段打开。</p>
    </div>
    <div class="metric-updated">
      <div data-usage-field="updated_at">--</div>
      <div class="metric-updated-subtle" data-usage-field="window_copy">--</div>
    </div>
  </div>

  <div class="metric-summary-grid metric-summary-grid-refined">
    <div class="metric-card">
      <span>近 30 天 token</span>
      <strong data-usage-field="total_tokens">--</strong>
      <em data-usage-field="token_breakdown">--</em>
    </div>
    <div class="metric-card">
      <span>活跃天数</span>
      <strong data-usage-field="active_days">--</strong>
      <em data-usage-field="active_days_copy">--</em>
    </div>
    <div class="metric-card">
      <span>请求数</span>
      <strong data-usage-field="requests_total">--</strong>
      <em data-usage-field="requests_copy">--</em>
    </div>
    <div class="metric-card metric-card-models">
      <span>主力模型</span>
      <strong data-usage-field="primary_model">--</strong>
      <em data-usage-field="primary_model_copy">--</em>
      <div class="model-chip-list" id="usage-model-chips"></div>
    </div>
  </div>

  <div class="metric-panel activity-panel activity-panel-refined">
    <div class="metric-head">
      <div>
        <div class="metric-overline">30 天节奏</div>
        <h3>最近哪几天在写</h3>
      </div>
      <div class="metric-caption" id="usage-activity-headline">hover 看当天卡片，click 锁定</div>
    </div>
    <div class="activity-layout">
      <div class="activity-spotlight" id="usage-activity-spotlight"></div>
      <div class="activity-chart-shell">
        <div class="activity-summary" id="usage-activity-summary"></div>
        <div class="activity-sequence-wrap">
          <div class="activity-sequence" id="usage-activity-sequence"></div>
        </div>
        <div class="activity-axis" id="usage-activity-axis"></div>
      </div>
    </div>
  </div>

  <div class="metric-secondary-grid">
    <div class="metric-panel chart-panel signal-panel">
      <div class="metric-overline">总量信号</div>
      <h3>输入输出 / 请求层</h3>
      <div class="signal-layout">
        <div class="signal-block">
          <div class="signal-title">Token 结构</div>
          <div class="split-bar" id="usage-token-split"></div>
          <div class="composition-list" id="usage-composition-list"></div>
        </div>
        <div class="signal-block">
          <div class="signal-title">请求质量</div>
          <div class="health-grid" id="usage-health-grid"></div>
          <div class="signal-pills" id="usage-signal-pills"></div>
        </div>
      </div>
    </div>
    <div class="metric-panel chart-panel side-panel">
      <div class="metric-overline">模型</div>
      <h3>主力模型</h3>
      <div class="rank-list" id="usage-model-bars"></div>
    </div>
    <div class="metric-panel chart-panel side-panel">
      <div class="metric-overline">时段</div>
      <h3>打开时段</h3>
      <div class="rhythm-chart" id="usage-hour-rhythm"></div>
      <div class="rhythm-axis">
        <span>00:00</span>
        <span>06:00</span>
        <span>12:00</span>
        <span>18:00</span>
        <span>23:00</span>
      </div>
    </div>
  </div>

  <div class="metric-tooltip" id="usage-metric-tooltip" hidden></div>
</div>

<script>
(() => {
  const summaryUrl = "/data/ai-usage-summary.json";
  const hourlyUrl = "/data/ai-usage-hourly.json";
  const dailyUrl = "/data/ai-usage-daily.json";
  const insightUrl = "/data/ai-usage-insights.json";

  const state = {
    summary: null,
    hourlyRows: [],
    dailyRows: [],
    insights: null,
    dailyByDate: new Map(),
    hourlyByDate: new Map(),
    defaultDate: null,
    hoverDate: null,
    lockedDate: null,
    activityNodes: new Map(),
  };

  const tooltip = document.getElementById("usage-metric-tooltip");

  const formatInt = (value) => new Intl.NumberFormat("en-US").format(Number(value || 0));
  const formatPercent = (value, total) => {
    if (!total) return "0%";
    return `${Math.round((Number(value || 0) / Number(total)) * 100)}%`;
  };
  const formatTime = (value) => {
    if (!value) return "--";
    const dt = new Date(value);
    if (Number.isNaN(dt.getTime())) return value;
    return `Updated ${dt.toLocaleString("zh-CN", { hour12: false })}`;
  };
  const formatLatency = (value) => {
    const ms = Number(value || 0);
    if (!ms) return "--";
    if (ms >= 1000) return `${(ms / 1000).toFixed(ms >= 10000 ? 1 : 2)}s`;
    return `${Math.round(ms)}ms`;
  };
  const formatDayLabel = (value) => {
    const dt = new Date(`${value}T00:00:00Z`);
    if (Number.isNaN(dt.getTime())) return value;
    return dt.toLocaleDateString("zh-CN", {
      month: "numeric",
      day: "numeric",
      weekday: "short",
      timeZone: "UTC",
    });
  };
  const formatDayTick = (value) => {
    const dt = new Date(`${value}T00:00:00Z`);
    if (Number.isNaN(dt.getTime())) return value;
    return dt.toLocaleDateString("zh-CN", {
      month: "numeric",
      day: "numeric",
      timeZone: "UTC",
    });
  };
  const escapeHtml = (value) =>
    String(value ?? "").replace(/[&<>"']/g, (char) => ({
      "&": "&amp;",
      "<": "&lt;",
      ">": "&gt;",
      '"': "&quot;",
      "'": "&#39;",
    }[char]));
  const sumBy = (rows, key) => rows.reduce((total, row) => total + Number(row[key] || 0), 0);
  const unique = (items) => [...new Set(items.filter(Boolean))];
  const focusDate = () => state.hoverDate || state.lockedDate || state.defaultDate;

  const tooltipMarkup = (title, rows) => `
    <div class="metric-tooltip-title">${escapeHtml(title)}</div>
    ${rows
      .map(
        ([label, value]) => `
          <div class="metric-tooltip-row">
            <span>${escapeHtml(label)}</span>
            <strong>${escapeHtml(value)}</strong>
          </div>
        `
      )
      .join("")}
  `;

  const showTooltipAtPoint = (clientX, clientY, html) => {
    if (!tooltip) return;
    tooltip.hidden = false;
    tooltip.innerHTML = html;

    const padding = 14;
    const { innerWidth, innerHeight } = window;
    const rect = tooltip.getBoundingClientRect();
    let left = clientX + padding;
    let top = clientY + padding;

    if (left + rect.width > innerWidth - 12) left = clientX - rect.width - padding;
    if (top + rect.height > innerHeight - 12) top = clientY - rect.height - padding;

    tooltip.style.left = `${Math.max(12, left)}px`;
    tooltip.style.top = `${Math.max(12, top)}px`;
  };

  const showTooltipForEvent = (event, html) => showTooltipAtPoint(event.clientX, event.clientY, html);
  const showTooltipForNode = (node, html) => {
    const rect = node.getBoundingClientRect();
    showTooltipAtPoint(rect.left + rect.width / 2, rect.top + rect.height / 2, html);
  };
  const hideTooltip = () => {
    if (!tooltip) return;
    tooltip.hidden = true;
    tooltip.innerHTML = "";
  };

  const setField = (name, value) => {
    const node = document.querySelector(`[data-usage-field="${name}"]`);
    if (node) node.textContent = value;
  };

  const requireJson = async (url) => {
    const response = await fetch(url, { cache: "no-store" });
    if (!response.ok) throw new Error(`${response.status} ${response.statusText}`);
    return response.json();
  };

  const renderModelChips = (rows) => {
    const container = document.getElementById("usage-model-chips");
    if (!container) return;
    container.innerHTML = "";
    if (!rows.length) {
      container.innerHTML = '<span class="usage-empty">暂时还没有模型数据。</span>';
      return;
    }

    rows.slice(0, 3).forEach((row) => {
      const chip = document.createElement("span");
      chip.className = "model-chip";
      chip.textContent = `${row.model} ${row.share}%`;
      container.appendChild(chip);
    });
  };

  const buildSplitBar = (segments, total, compact = false) => `
    <div class="split-track ${compact ? "split-track-compact" : ""}">
      ${segments
        .map((segment) => {
          const width = total ? (Number(segment.value || 0) / total) * 100 : 0;
          return `<span class="split-segment ${segment.className}" style="width:${width}%"></span>`;
        })
        .join("")}
    </div>
    <div class="split-legend ${compact ? "split-legend-compact" : ""}">
      ${segments
        .map(
          (segment) => `
            <div class="split-legend-item">
              <i class="split-dot ${segment.className}"></i>
              <span>${escapeHtml(segment.label)}</span>
              <strong>${escapeHtml(formatInt(segment.value))}</strong>
            </div>
          `
        )
        .join("")}
    </div>
  `;

  const buildDayDetail = (date) => {
    const daily = state.dailyByDate.get(date) || {
      date,
      input_tokens: 0,
      cache_read_input_tokens: 0,
      cache_creation_input_tokens: 0,
      output_tokens: 0,
      total_tokens: 0,
      tool_calls: 0,
    };
    const hours = state.hourlyByDate.get(date) || [];
    const requests = sumBy(hours, "requests");
    const successRequests = sumBy(hours, "success_requests");
    const failedRequests = sumBy(hours, "failed_requests");
    const activeHours = hours.filter((row) => Number(row.total_tokens || 0) > 0).length;
    const models = unique(hours.map((row) => row.model));
    const peakHourRow = hours.reduce((best, row) => {
      if (!best || Number(row.total_tokens || 0) > Number(best.total_tokens || 0)) return row;
      return best;
    }, null);

    return {
      date,
      totalTokens: Number(daily.total_tokens || 0),
      inputTokens: Number(daily.input_tokens || 0),
      outputTokens: Number(daily.output_tokens || 0),
      cacheReadTokens: Number(daily.cache_read_input_tokens || 0),
      cacheWriteTokens: Number(daily.cache_creation_input_tokens || 0),
      toolCalls: Number(daily.tool_calls || 0),
      requests,
      successRequests,
      failedRequests,
      activeHours,
      models,
      peakHour: peakHourRow ? String(peakHourRow.hour).slice(11, 16) : "--",
      shareOfWindow: Number(state.summary?.total_tokens || 0)
        ? Math.round((Number(daily.total_tokens || 0) / Number(state.summary.total_tokens || 0)) * 100)
        : 0,
      successRate: requests ? Math.round((successRequests / requests) * 100) : 0,
    };
  };

  const buildDayTooltip = (detail) =>
    tooltipMarkup(formatDayLabel(detail.date), [
      ["Total", `${formatInt(detail.totalTokens)} tokens`],
      ["Requests", formatInt(detail.requests)],
      ["Success", detail.requests ? `${detail.successRate}%` : "--"],
      ["Peak hour", detail.peakHour],
    ]);

  const wireDateNode = (node, date) => {
    const tooltipHtml = () => buildDayTooltip(buildDayDetail(date));

    node.addEventListener("mouseenter", (event) => {
      state.hoverDate = date;
      renderInteractiveState();
      showTooltipForEvent(event, tooltipHtml());
    });
    node.addEventListener("mousemove", (event) => showTooltipForEvent(event, tooltipHtml()));
    node.addEventListener("mouseleave", () => {
      if (state.hoverDate === date) {
        state.hoverDate = null;
        renderInteractiveState();
      }
      hideTooltip();
    });
    node.addEventListener("focus", () => {
      state.hoverDate = date;
      renderInteractiveState();
      showTooltipForNode(node, tooltipHtml());
    });
    node.addEventListener("blur", () => {
      if (state.hoverDate === date) {
        state.hoverDate = null;
        renderInteractiveState();
      }
      hideTooltip();
    });
    node.addEventListener("click", () => {
      state.lockedDate = state.lockedDate === date ? null : date;
      renderInteractiveState();
    });
    node.addEventListener("keydown", (event) => {
      if (event.key === "Enter" || event.key === " ") {
        event.preventDefault();
        state.lockedDate = state.lockedDate === date ? null : date;
        renderInteractiveState();
      }
    });
  };

  const renderOverview = () => {
    const summary = state.summary || {};
    const activeDays = state.dailyRows.filter((row) => Number(row.total_tokens || 0) > 0).length;
    const quietDays = Math.max(state.dailyRows.length - activeDays, 0);
    const modelMix = state.insights?.model_mix || [];
    const primaryModel = modelMix[0] || null;
    const requests = Number(summary.requests || 0);
    const successRequests = Number(summary.success_requests || 0);
    const failedRequests = Number(summary.failed_requests || 0);

    setField("updated_at", formatTime(summary.updated_at));
    setField("window_copy", `${activeDays} 天有记录 · ${quietDays} 天留白`);
    setField("total_tokens", formatInt(summary.total_tokens));
    setField(
      "token_breakdown",
      `输入 ${formatInt(summary.input_tokens)} · 输出 ${formatInt(summary.output_tokens)}`
    );
    setField("active_days", formatInt(activeDays));
    setField("active_days_copy", `最近 30 天里有记录的天数`);
    setField(
      "requests_total",
      formatInt(requests)
    );
    setField(
      "requests_copy",
      requests ? `${formatInt(successRequests)} 成功 · ${formatInt(failedRequests)} 失败` : "最近 30 天没有请求"
    );
    setField("primary_model", primaryModel ? primaryModel.model : "--");
    setField(
      "primary_model_copy",
      primaryModel ? `${primaryModel.share}% 的 token 来自 ${primaryModel.model}` : "暂时还没有模型数据"
    );
    renderModelChips(modelMix);
  };

  const renderActivitySummary = () => {
    const container = document.getElementById("usage-activity-summary");
    const axis = document.getElementById("usage-activity-axis");
    const rows = state.dailyRows;
    if (!container || !axis) return;

    if (!rows.length) {
      container.innerHTML = '<div class="usage-empty">暂时还没有每日数据。</div>';
      axis.innerHTML = "";
      return;
    }

    const activeRows = rows.filter((row) => Number(row.total_tokens || 0) > 0);
    const biggestDay = activeRows.reduce((best, row) => {
      if (!best || Number(row.total_tokens || 0) > Number(best.total_tokens || 0)) return row;
      return best;
    }, null);
    const latestActive = [...activeRows].reverse()[0] || rows.at(-1);

    container.innerHTML = [
      ["活跃天数", `${activeRows.length}/${rows.length}`],
      ["最大单日", biggestDay ? formatInt(biggestDay.total_tokens) : "--"],
      ["最近活跃", latestActive ? formatDayTick(latestActive.date) : "--"],
    ]
      .map(
        ([label, value]) => `
          <div class="activity-pill">
            <span>${escapeHtml(label)}</span>
            <strong>${escapeHtml(value)}</strong>
          </div>
        `
      )
      .join("");

    const tickIndexes = unique([0, 5, 11, 17, 23, rows.length - 1]).sort((a, b) => a - b);
    axis.innerHTML = tickIndexes
      .map((index) => `<span>${escapeHtml(formatDayTick(rows[index].date))}</span>`)
      .join("");
  };

  const renderActivitySequence = () => {
    const container = document.getElementById("usage-activity-sequence");
    if (!container) return;
    container.innerHTML = "";
    state.activityNodes = new Map();

    if (!state.dailyRows.length) {
      container.innerHTML = '<div class="usage-empty">暂时还没有每日数据。</div>';
      return;
    }

    const maxValue = Math.max(...state.dailyRows.map((row) => Number(row.total_tokens || 0)), 0);
    state.dailyRows.forEach((row) => {
      const total = Number(row.total_tokens || 0);
      const height = maxValue ? Math.max(total > 0 ? 14 : 6, (total / maxValue) * 100) : 6;
      const button = document.createElement("button");
      button.type = "button";
      button.className = `activity-day ${total > 0 ? "is-active" : "is-idle"}`;
      button.dataset.date = row.date;
      button.setAttribute("aria-label", `${formatDayLabel(row.date)} ${formatInt(total)} tokens`);
      button.style.setProperty("--activity-height", `${height}%`);
      button.innerHTML = `
        <span class="activity-day-frame">
          <span class="activity-day-fill"></span>
        </span>
      `;
      wireDateNode(button, row.date);
      state.activityNodes.set(row.date, button);
      container.appendChild(button);
    });
  };

  const renderSpotlight = (date) => {
    const container = document.getElementById("usage-activity-spotlight");
    const headline = document.getElementById("usage-activity-headline");
    if (!container || !headline) return;

    const detail = buildDayDetail(date);
    const mode = state.hoverDate ? "hover" : state.lockedDate ? "locked" : "default";
    const modeCopy =
      mode === "hover"
        ? "当前 hover"
        : mode === "locked"
          ? "已锁定"
          : "默认焦点";
    const splitMarkup = buildSplitBar(
      [
        { label: "输入", value: detail.inputTokens, className: "split-input" },
        { label: "输出", value: detail.outputTokens, className: "split-output" },
      ],
      Math.max(detail.totalTokens, 1),
      true
    );
    const leadCopy = detail.totalTokens
      ? `这一天占最近 30 天公开 token 的 ${detail.shareOfWindow}%，峰值出现在 ${detail.peakHour}。`
      : "这一天没有公开记录。最近 30 天里，留白天本身也是节奏的一部分。";
    const footerItems = [
      `输入 ${formatInt(detail.inputTokens)}`,
      `输出 ${formatInt(detail.outputTokens)}`,
      `Peak ${detail.peakHour}`,
    ];
    if (detail.failedRequests > 0) footerItems.push(`失败 ${formatInt(detail.failedRequests)}`);
    if (detail.toolCalls > 0) footerItems.push(`工具 ${formatInt(detail.toolCalls)}`);
    if (detail.cacheReadTokens > 0) footerItems.push(`Cache read ${formatInt(detail.cacheReadTokens)}`);
    if (detail.cacheWriteTokens > 0) footerItems.push(`Cache write ${formatInt(detail.cacheWriteTokens)}`);

    headline.textContent = state.lockedDate
      ? `已锁定 ${formatDayTick(state.lockedDate)} · 再点一次取消`
      : "hover 看当天卡片，click 锁定";

    container.innerHTML = `
      <div class="spotlight-mode">${escapeHtml(modeCopy)}</div>
      <h4>${escapeHtml(formatDayLabel(detail.date))}</h4>
      <p class="spotlight-copy">${escapeHtml(leadCopy)}</p>

      <div class="spotlight-stat-grid">
        <div class="spotlight-stat">
          <span>Total</span>
          <strong>${escapeHtml(formatInt(detail.totalTokens))}</strong>
        </div>
        <div class="spotlight-stat">
          <span>Requests</span>
          <strong>${escapeHtml(formatInt(detail.requests))}</strong>
        </div>
        <div class="spotlight-stat">
          <span>Success</span>
          <strong>${escapeHtml(detail.requests ? `${detail.successRate}%` : "--")}</strong>
        </div>
        <div class="spotlight-stat">
          <span>Active hours</span>
          <strong>${escapeHtml(formatInt(detail.activeHours))}</strong>
        </div>
      </div>

      <div class="spotlight-structure">${splitMarkup}</div>

      <div class="spotlight-footer">
        ${footerItems.map((item) => `<span>${escapeHtml(item)}</span>`).join("")}
      </div>
    `;
  };

  const renderTokenStructure = () => {
    const split = document.getElementById("usage-token-split");
    const list = document.getElementById("usage-composition-list");
    const summary = state.summary || {};
    if (!split || !list) return;

    const totalTokens = Number(summary.total_tokens || 0);
    const tokenSegments = [
      { label: "输入", value: Number(summary.input_tokens || 0), className: "split-input" },
      { label: "输出", value: Number(summary.output_tokens || 0), className: "split-output" },
    ];
    split.innerHTML = buildSplitBar(tokenSegments, Math.max(totalTokens, 1));

    list.innerHTML = tokenSegments
      .map((item) => {
        const width = totalTokens ? (Number(item.value || 0) / totalTokens) * 100 : 0;
        return `
          <div class="composition-row">
            <div class="composition-meta">
              <span>${escapeHtml(item.label)}</span>
              <strong>${escapeHtml(formatInt(item.value))}</strong>
            </div>
            <div class="bar-track">
              <div class="bar-fill ${item.className}" style="width:${width}%"></div>
            </div>
            <em>占总 token ${escapeHtml(formatPercent(item.value, totalTokens))}</em>
          </div>
        `;
      })
      .join("");
  };

  const renderHealth = () => {
    const healthGrid = document.getElementById("usage-health-grid");
    const signalPills = document.getElementById("usage-signal-pills");
    const summary = state.summary || {};
    if (!healthGrid || !signalPills) return;

    const requests = Number(summary.requests || 0);
    const successRate = requests
      ? Math.round((Number(summary.success_requests || 0) / requests) * 100)
      : 0;

    healthGrid.innerHTML = [
      ["Requests", formatInt(summary.requests)],
      ["Success rate", requests ? `${successRate}%` : "--"],
      ["Failures", formatInt(summary.failed_requests)],
      ["Avg latency", formatLatency(summary.avg_latency_ms)],
    ]
      .map(
        ([label, value]) => `
          <div class="micro-card">
            <span>${escapeHtml(label)}</span>
            <strong>${escapeHtml(value)}</strong>
          </div>
        `
      )
      .join("");

    const pills = [];
    const toolCalls = Number(summary.tool_calls || 0);
    const cacheRead = Number(summary.cache_read_input_tokens || 0);
    const cacheWrite = Number(summary.cache_creation_input_tokens || 0);

    if (toolCalls > 0) pills.push(`Tool calls ${formatInt(toolCalls)}`);
    if (cacheRead > 0) pills.push(`Cache read ${formatInt(cacheRead)}`);
    if (cacheWrite > 0) pills.push(`Cache write ${formatInt(cacheWrite)}`);

    signalPills.innerHTML = pills.map((item) => `<span>${escapeHtml(item)}</span>`).join("");
    signalPills.hidden = pills.length === 0;
  };

  const renderModelBars = () => {
    const container = document.getElementById("usage-model-bars");
    const rows = state.insights?.model_mix || [];
    if (!container) return;
    container.innerHTML = "";

    if (!rows.length) {
      container.innerHTML = '<div class="usage-empty">暂时还没有模型数据。</div>';
      return;
    }

    const maxValue = Math.max(...rows.map((row) => Number(row.total_tokens || 0)), 1);
    rows.forEach((row) => {
      const item = document.createElement("div");
      item.className = "rank-row";
      item.tabIndex = 0;
      item.innerHTML = `
        <div class="rank-meta">
          <span>${escapeHtml(row.model)}</span>
          <strong>${escapeHtml(`${row.share}%`)}</strong>
        </div>
        <div class="bar-track">
          <div class="bar-fill rank-fill" style="width:${(Number(row.total_tokens || 0) / maxValue) * 100}%"></div>
        </div>
        <div class="rank-value">${escapeHtml(formatInt(row.total_tokens))}</div>
      `;
      const tooltipHtml = () =>
        tooltipMarkup(row.model, [
          ["Total", `${formatInt(row.total_tokens)} tokens`],
          ["Share", `${row.share}%`],
        ]);
      item.addEventListener("mouseenter", (event) => showTooltipForEvent(event, tooltipHtml()));
      item.addEventListener("mousemove", (event) => showTooltipForEvent(event, tooltipHtml()));
      item.addEventListener("mouseleave", hideTooltip);
      item.addEventListener("focus", () => showTooltipForNode(item, tooltipHtml()));
      item.addEventListener("blur", hideTooltip);
      container.appendChild(item);
    });
  };

  const renderHourRhythm = () => {
    const container = document.getElementById("usage-hour-rhythm");
    if (!container) return;
    container.innerHTML = "";

    const totals = new Map((state.insights?.hour_mix || []).map((row) => [row.hour, Number(row.total_tokens || 0)]));
    const rows = Array.from({ length: 24 }, (_, hour) => ({
      hour: `${String(hour).padStart(2, "0")}:00`,
      total_tokens: totals.get(`${String(hour).padStart(2, "0")}:00`) || 0,
    }));

    if (!rows.length) {
      container.innerHTML = '<div class="usage-empty">暂时还没有按小时的分布数据。</div>';
      return;
    }

    const maxValue = Math.max(...rows.map((row) => row.total_tokens), 0);
    rows.forEach((row) => {
      const button = document.createElement("button");
      button.type = "button";
      button.className = `rhythm-bin ${row.total_tokens > 0 ? "is-active" : "is-idle"}`;
      const height = maxValue ? Math.max(row.total_tokens > 0 ? 20 : 6, (row.total_tokens / maxValue) * 132) : 6;
      button.style.setProperty("--rhythm-height-px", `${height}px`);
      button.setAttribute("aria-label", `${row.hour} ${formatInt(row.total_tokens)} tokens`);
      button.innerHTML = '<span class="rhythm-fill"></span>';
      const tooltipHtml = () =>
        tooltipMarkup(row.hour, [["Total", `${formatInt(row.total_tokens)} tokens`]]);
      button.addEventListener("mouseenter", (event) => showTooltipForEvent(event, tooltipHtml()));
      button.addEventListener("mousemove", (event) => showTooltipForEvent(event, tooltipHtml()));
      button.addEventListener("mouseleave", hideTooltip);
      button.addEventListener("focus", () => showTooltipForNode(button, tooltipHtml()));
      button.addEventListener("blur", hideTooltip);
      container.appendChild(button);
    });
  };

  const renderInteractiveState = () => {
    const date = focusDate();
    if (!date) return;
    renderSpotlight(date);

    state.activityNodes.forEach((node, nodeDate) => {
      node.classList.toggle("is-focus", nodeDate === date);
      node.classList.toggle("is-locked", nodeDate === state.lockedDate);
    });
  };

  const renderErrorState = (message) => {
    console.error(message);
    setField("updated_at", "Data unavailable");
    setField("window_copy", "请稍后重试");
    [
      "usage-activity-spotlight",
      "usage-activity-summary",
      "usage-activity-sequence",
      "usage-token-split",
      "usage-composition-list",
      "usage-health-grid",
      "usage-signal-pills",
      "usage-model-bars",
      "usage-hour-rhythm",
    ].forEach((id) => {
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
      state.hourlyRows = Array.isArray(hourly?.rows) ? hourly.rows : [];
      state.dailyRows = Array.isArray(daily?.rows) ? daily.rows : [];
      state.insights = insights || { model_mix: [], hour_mix: [] };
      state.dailyByDate = new Map(state.dailyRows.map((row) => [row.date, row]));
      state.hourlyByDate = state.hourlyRows.reduce((map, row) => {
        const key = String(row.hour || "").slice(0, 10);
        if (!map.has(key)) map.set(key, []);
        map.get(key).push(row);
        return map;
      }, new Map());

      const latestActive = [...state.dailyRows]
        .reverse()
        .find((row) => Number(row.total_tokens || 0) > 0);
      state.defaultDate = (latestActive || state.dailyRows.at(-1) || {}).date || null;

      renderOverview();
      renderActivitySummary();
      renderActivitySequence();
      renderTokenStructure();
      renderHealth();
      renderModelBars();
      renderHourRhythm();
      renderInteractiveState();
    } catch (error) {
      renderErrorState("暂时拉不到公开数据。");
    }
  };

  load();
})();
</script>
