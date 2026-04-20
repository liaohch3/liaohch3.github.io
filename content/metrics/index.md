+++
title = "AI 日常"
description = "最近和 AI 一起写代码时的一些使用记录。"
draft = false
toc = false
comments = false
+++

<p>这页就简单记一下我最近和 AI 一起写代码时的一些使用情况。</p>
<div class="public-metrics">
  <div class="metric-hero">
    <div class="metric-hero-copy">
      <div class="metric-overline">最近在用</div>
      <h2>最近和 AI 一起写代码</h2>
      <p>看几个简单的数字和图，大概就知道我这阵子用了多少、常用什么模型、通常在什么时候写。</p>
    </div>
    <div class="metric-updated" data-usage-field="updated_at">--</div>
  </div>
  <div class="metric-summary-grid">
    <div class="metric-card">
      <span>近 24 小时 token</span>
      <strong data-usage-field="total_tokens">--</strong>
      <em data-usage-field="token_breakdown">--</em>
    </div>
    <div class="metric-card metric-card-models">
      <span>最近在用的模型</span>
      <strong data-usage-field="model_count">--</strong>
      <div class="model-chip-list" id="usage-model-chips"></div>
    </div>
    <div class="metric-card">
      <span>活跃天数</span>
      <strong data-usage-field="active_days">--</strong>
      <em data-usage-field="active_days_copy">--</em>
    </div>
  </div>
  <div class="metric-panel heatmap-card">
    <div class="metric-head">
      <div>
        <div class="metric-overline">Token 墙</div>
        <h3>每天消耗多少 token，一眼看出来</h3>
      </div>
      <div class="metric-caption">最近 18 周</div>
    </div>
    <div class="heatmap-shell">
      <div class="heatmap-weekdays">
        <span></span>
        <span>Mon</span>
        <span></span>
        <span>Wed</span>
        <span></span>
        <span>Fri</span>
        <span></span>
      </div>
      <div class="heatmap-month-block">
        <div class="heatmap-months" id="usage-heatmap-months"></div>
        <div class="heatmap-grid" id="usage-heatmap-grid"></div>
      </div>
    </div>
    <div class="heatmap-legend">
      <span>less</span>
      <i class="legend-swatch heat-l0"></i>
      <i class="legend-swatch heat-l1"></i>
      <i class="legend-swatch heat-l2"></i>
      <i class="legend-swatch heat-l3"></i>
      <i class="legend-swatch heat-l4"></i>
      <span>more</span>
    </div>
  </div>
  <div class="metric-chart-grid">
    <div class="metric-panel chart-panel">
      <div class="metric-overline">最近 7 天</div>
      <h3>最近 7 天 token 趋势</h3>
      <p class="chart-copy">有时候会突然高很多，通常就是那几天在集中写东西或者改东西。</p>
      <svg class="trend-chart" id="usage-trend-chart" viewBox="0 0 640 180" preserveAspectRatio="none"></svg>
      <div class="axis-row" id="usage-trend-axis"></div>
    </div>
    <div class="metric-panel chart-panel">
      <div class="metric-overline">模型分布</div>
      <h3>最近用哪些模型最多</h3>
      <p class="chart-copy">基本就是最近这段时间最常开的几个模型。</p>
      <div class="model-bars" id="usage-model-bars"></div>
    </div>
  </div>
  <div class="metric-panel chart-panel">
    <div class="metric-overline">一天里的节奏</div>
    <h3>一天里通常什么时候最常和 AI 一起写代码</h3>
    <p class="chart-copy">只是看看我平时大概在什么时段用得比较多。</p>
    <div class="hour-bars" id="usage-hour-bars"></div>
  </div>
  <div class="metric-panel metric-detail-panel">
    <div class="metric-head">
      <div>
        <div class="metric-overline">单日下钻</div>
        <h3 id="usage-detail-title">点某一天看细节</h3>
      </div>
      <div class="metric-caption" id="usage-detail-caption">从上面的热力图或者折线里选一天</div>
    </div>
    <p class="chart-copy" id="usage-detail-copy">先看整体，再点某一天，下面会展开那天按小时和按模型的分布。</p>
    <div class="detail-summary-grid" id="usage-detail-summary"></div>
    <div class="metric-chart-grid detail-chart-grid">
      <div class="detail-block">
        <div class="metric-overline">按小时</div>
        <div class="hour-bars" id="usage-day-hour-bars"></div>
      </div>
      <div class="detail-block">
        <div class="metric-overline">按模型</div>
        <div class="model-bars" id="usage-day-model-bars"></div>
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
    selectedDate: null,
  };
  const tooltip = document.getElementById("usage-metric-tooltip");

  const formatInt = (value) => new Intl.NumberFormat("en-US").format(Number(value || 0));
  const formatTime = (value) => {
    if (!value) return "--";
    const dt = new Date(value);
    if (Number.isNaN(dt.getTime())) return value;
    return `Updated ${dt.toLocaleString("zh-CN", { hour12: false })}`;
  };
  const formatDayLabel = (value) => {
    const dt = new Date(`${value}T00:00:00Z`);
    if (Number.isNaN(dt.getTime())) return value;
    return dt.toLocaleDateString("zh-CN", {
      month: "short",
      day: "numeric",
      weekday: "short",
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
  const wireTooltip = (node, getHtml, onClick = null) => {
    node.addEventListener("mouseenter", (event) => showTooltipForEvent(event, getHtml()));
    node.addEventListener("mousemove", (event) => showTooltipForEvent(event, getHtml()));
    node.addEventListener("mouseleave", hideTooltip);
    node.addEventListener("focus", () => showTooltipForNode(node, getHtml()));
    node.addEventListener("blur", hideTooltip);

    if (onClick) {
      node.addEventListener("click", () => onClick());
      node.addEventListener("keydown", (event) => {
        if (event.key === "Enter" || event.key === " ") {
          event.preventDefault();
          onClick();
        }
      });
    }
  };

  const setField = (name, value) => {
    const node = document.querySelector(`[data-usage-field="${name}"]`);
    if (node) node.textContent = value;
  };

  const setText = (id, value) => {
    const node = document.getElementById(id);
    if (node) node.textContent = value;
  };

  const requireJson = async (url) => {
    const response = await fetch(url, { cache: "no-store" });
    if (!response.ok) throw new Error(`${response.status} ${response.statusText}`);
    return response.json();
  };

  const renderModelChips = (models) => {
    const container = document.getElementById("usage-model-chips");
    if (!container) return;
    container.innerHTML = "";
    if (!models.length) {
      container.innerHTML = '<span class="usage-empty">暂时还没有模型数据。</span>';
      return;
    }
    models.forEach((model) => {
      const chip = document.createElement("span");
      chip.className = "model-chip";
      chip.textContent = model;
      container.appendChild(chip);
    });
  };

  const renderHeatmap = (rows) => {
    const monthContainer = document.getElementById("usage-heatmap-months");
    const grid = document.getElementById("usage-heatmap-grid");
    if (!monthContainer || !grid) return;
    monthContainer.innerHTML = "";
    grid.innerHTML = "";

    if (!rows.length) {
      grid.innerHTML = '<div class="usage-empty">暂时还没有每日数据。</div>';
      return;
    }

    const maxTokens = Math.max(...rows.map((row) => Number(row.total_tokens || 0)), 1);
    let lastMonth = "";

    rows.forEach((row) => {
      const date = new Date(`${row.date}T00:00:00Z`);
      if (date.getUTCDay() === 0) {
        const month = date.toLocaleDateString("en-US", { month: "short", timeZone: "UTC" });
        const node = document.createElement("span");
        node.textContent = month === lastMonth ? "" : month;
        lastMonth = month;
        monthContainer.appendChild(node);
      }

      const value = Number(row.total_tokens || 0);
      let level = 0;
      if (value > maxTokens * 0.15) level = 1;
      if (value > maxTokens * 0.35) level = 2;
      if (value > maxTokens * 0.6) level = 3;
      if (value > maxTokens * 0.82) level = 4;

      const cell = document.createElement("button");
      cell.type = "button";
      cell.className = `heat-cell heat-l${level}${row.date === state.selectedDate ? " is-active" : ""}`;
      cell.setAttribute("aria-pressed", row.date === state.selectedDate ? "true" : "false");
      cell.setAttribute("aria-label", `${formatDayLabel(row.date)} ${formatInt(value)} tokens`);
      wireTooltip(
        cell,
        () =>
          tooltipMarkup(formatDayLabel(row.date), [
            ["Total", `${formatInt(value)} tokens`],
            ["Status", value > 0 ? "Active day" : "No activity"],
            ["Action", "Click to drill down"],
          ]),
        () => setSelectedDate(row.date)
      );
      grid.appendChild(cell);
    });
  };

  const renderTrend = (rows) => {
    const svg = document.getElementById("usage-trend-chart");
    const axis = document.getElementById("usage-trend-axis");
    if (!svg || !axis) return;

    if (!rows.length) {
      svg.innerHTML = "";
      axis.innerHTML = "";
      return;
    }

    const recent = rows.slice(-7);
    const width = 640;
    const baseline = 156;
    const paddingX = 18;
    const maxValue = Math.max(...recent.map((item) => Number(item.total_tokens || 0)), 1);
    const step = (width - paddingX * 2) / Math.max(recent.length - 1, 1);

    const points = recent.map((item, index) => {
      const x = paddingX + index * step;
      const y = baseline - (Number(item.total_tokens || 0) / maxValue) * 112;
      return { ...item, x, y };
    });

    const linePath = points.map((point, index) => `${index === 0 ? "M" : "L"} ${point.x} ${point.y}`).join(" ");
    const areaPath = `${linePath} L ${points.at(-1).x} ${baseline} L ${points[0].x} ${baseline} Z`;
    svg.innerHTML = `
      <path class="trend-area" d="${areaPath}"></path>
      <path class="trend-line" d="${linePath}"></path>
      ${points
        .map(
          (point) => `
            <circle
              class="trend-dot${point.date === state.selectedDate ? " is-active" : ""}"
              cx="${point.x}"
              cy="${point.y}"
              r="5"
              tabindex="0"
              role="button"
              data-date="${point.date}"
              data-total="${Number(point.total_tokens || 0)}"
            ></circle>
          `
        )
        .join("")}
    `;
    svg.querySelectorAll(".trend-dot").forEach((dot) => {
      const date = dot.getAttribute("data-date");
      const totalTokens = Number(dot.getAttribute("data-total") || 0);
      wireTooltip(
        dot,
        () =>
          tooltipMarkup(formatDayLabel(date), [
            ["Total", `${formatInt(totalTokens)} tokens`],
            ["Action", "Click to drill down"],
          ]),
        () => setSelectedDate(date)
      );
    });
    axis.innerHTML = recent
      .map(
        (item) => `
          <span
            class="${item.date === state.selectedDate ? "is-active" : ""}"
            tabindex="0"
            role="button"
            data-date="${item.date}"
          >${new Date(`${item.date}T00:00:00Z`).toLocaleDateString("en-US", { weekday: "short", timeZone: "UTC" })}</span>
        `
      )
      .join("");
    axis.querySelectorAll("span[data-date]").forEach((node) => {
      const date = node.getAttribute("data-date");
      wireTooltip(
        node,
        () =>
          tooltipMarkup(formatDayLabel(date), [
            ["Action", "Click to drill down"],
          ]),
        () => setSelectedDate(date)
      );
    });
  };

  const renderBars = (containerId, rows, fillClass, options = {}) => {
    const container = document.getElementById(containerId);
    if (!container) return;
    container.innerHTML = "";
    if (!rows.length) {
      container.innerHTML = '<div class="usage-empty">暂时还没有图表数据。</div>';
      return;
    }

    const maxValue = Math.max(...rows.map((row) => Number(row.total_tokens || 0)), 1);
    const getLabel = options.getLabel || ((row) => row.model || row.hour || "--");
    const getValueText =
      options.getValueText ||
      ((row) => (row.share != null ? `${row.share}%` : formatInt(row.total_tokens)));
    const getWidth =
      options.getWidth ||
      ((row) => (row.share != null ? Number(row.share) : (Number(row.total_tokens || 0) / maxValue) * 100));
    const getTooltip = options.getTooltip || null;
    const rowClass =
      options.rowClass ||
      (containerId.includes("hour-bars") ? "hour-bar-row" : "model-bar-row");

    rows.forEach((row) => {
      const item = document.createElement("div");
      item.className = rowClass;
      const label = getLabel(row);
      const valueText = getValueText(row);
      const width = getWidth(row);
      item.innerHTML = `
        <div class="row-label">${escapeHtml(label)}</div>
        <div class="bar-track"><div class="bar-fill ${fillClass}" style="width:${width}%"></div></div>
        <div class="row-value">${escapeHtml(valueText)}</div>
      `;
      if (getTooltip) {
        item.tabIndex = 0;
        wireTooltip(item, () => getTooltip(row));
      }
      container.appendChild(item);
    });
  };

  const buildDayDetail = (date) => {
    const dailyRow = state.dailyRows.find((row) => row.date === date) || { date, total_tokens: 0 };
    const dayRows = state.hourlyRows.filter((row) => String(row.hour || "").startsWith(date));
    const hourBuckets = new Map();
    const modelBuckets = new Map();

    dayRows.forEach((row) => {
      const hour = String(row.hour).slice(11, 16);
      const hourBucket = hourBuckets.get(hour) || {
        hour,
        total_tokens: 0,
        requests: 0,
        success_requests: 0,
        failed_requests: 0,
      };
      hourBucket.total_tokens += Number(row.total_tokens || 0);
      hourBucket.requests += Number(row.requests || 0);
      hourBucket.success_requests += Number(row.success_requests || 0);
      hourBucket.failed_requests += Number(row.failed_requests || 0);
      hourBuckets.set(hour, hourBucket);

      const model = row.model || "unknown";
      const modelBucket = modelBuckets.get(model) || {
        model,
        total_tokens: 0,
        requests: 0,
        success_requests: 0,
        failed_requests: 0,
      };
      modelBucket.total_tokens += Number(row.total_tokens || 0);
      modelBucket.requests += Number(row.requests || 0);
      modelBucket.success_requests += Number(row.success_requests || 0);
      modelBucket.failed_requests += Number(row.failed_requests || 0);
      modelBuckets.set(model, modelBucket);
    });

    const hourRows = Array.from(hourBuckets.values()).sort((left, right) => left.hour.localeCompare(right.hour));
    const modelRows = Array.from(modelBuckets.values()).sort((left, right) => right.total_tokens - left.total_tokens);
    const busiestHour = hourRows.reduce(
      (best, row) => (row.total_tokens > (best?.total_tokens || -1) ? row : best),
      null
    );
    const topModel = modelRows[0] || null;

    return {
      date,
      totalTokens: Number(dailyRow.total_tokens || sumBy(dayRows, "total_tokens")),
      requests: sumBy(dayRows, "requests"),
      successRequests: sumBy(dayRows, "success_requests"),
      failedRequests: sumBy(dayRows, "failed_requests"),
      activeHours: hourRows.length,
      busiestHour,
      topModel,
      hourRows,
      modelRows,
    };
  };

  const renderDetailSummary = (detail) => {
    const container = document.getElementById("usage-detail-summary");
    if (!container) return;
    if (!detail) {
      container.innerHTML = '<div class="usage-empty">暂时还没有可下钻的数据。</div>';
      return;
    }

    const stats = [
      {
        label: "当天 token",
        value: formatInt(detail.totalTokens),
        copy: detail.requests ? `${formatInt(detail.requests)} requests` : "当天还没有请求记录",
      },
      {
        label: "活跃小时",
        value: detail.activeHours ? String(detail.activeHours) : "--",
        copy: detail.busiestHour
          ? `${detail.busiestHour.hour} 最忙`
          : "当天还没有小时级明细",
      },
      {
        label: "请求状态",
        value: detail.requests ? formatInt(detail.requests) : "--",
        copy: detail.requests
          ? `${formatInt(detail.successRequests)} ok · ${formatInt(detail.failedRequests)} failed`
          : "当天还没有请求记录",
      },
      {
        label: "最常用模型",
        value: detail.topModel ? detail.topModel.model : "--",
        copy: detail.topModel
          ? `${formatInt(detail.topModel.total_tokens)} tokens`
          : "当天还没有模型数据",
      },
    ];

    container.innerHTML = stats
      .map(
        (stat) => `
          <div class="detail-stat">
            <span>${stat.label}</span>
            <strong>${stat.value}</strong>
            <em>${stat.copy}</em>
          </div>
        `
      )
      .join("");
  };

  const renderDetail = (date) => {
    const title = document.getElementById("usage-detail-title");
    const caption = document.getElementById("usage-detail-caption");
    const copy = document.getElementById("usage-detail-copy");

    if (!title || !caption || !copy) return;
    if (!date) {
      title.textContent = "点某一天看细节";
      caption.textContent = "从上面的热力图或者折线里选一天";
      copy.textContent = "先看整体，再点某一天，下面会展开那天按小时和按模型的分布。";
      renderDetailSummary(null);
      renderBars("usage-day-hour-bars", [], "hour-fill");
      renderBars("usage-day-model-bars", [], "model-fill");
      return;
    }

    const detail = buildDayDetail(date);
    title.textContent = `${formatDayLabel(date)} 的明细`;
    caption.textContent = detail.activeHours
      ? `共 ${detail.activeHours} 个活跃小时`
      : "当天还没有小时级明细";
    copy.textContent = detail.activeHours
      ? "上面的热力图和折线负责告诉你哪天最活跃，这里再展开看当天到底是哪些小时和哪些模型贡献了这些 token。"
      : "这一天目前只有日级数据，还没有更细的小时分布可以展开。";

    renderDetailSummary(detail);
    renderBars("usage-day-hour-bars", detail.hourRows, "hour-fill", {
      getValueText: (row) => `${formatInt(row.total_tokens)} tokens`,
      getTooltip: (row) =>
        tooltipMarkup(`${formatDayLabel(date)} ${row.hour}`, [
          ["Total", `${formatInt(row.total_tokens)} tokens`],
          ["Requests", formatInt(row.requests)],
          ["Status", `${formatInt(row.success_requests)} ok · ${formatInt(row.failed_requests)} failed`],
        ]),
    });
    renderBars("usage-day-model-bars", detail.modelRows, "model-fill", {
      getValueText: (row) => `${formatInt(row.total_tokens)} tokens`,
      getTooltip: (row) =>
        tooltipMarkup(`${formatDayLabel(date)} ${row.model}`, [
          ["Total", `${formatInt(row.total_tokens)} tokens`],
          ["Requests", formatInt(row.requests)],
          ["Status", `${formatInt(row.success_requests)} ok · ${formatInt(row.failed_requests)} failed`],
        ]),
    });
  };

  const setSelectedDate = (date) => {
    if (!date || date === state.selectedDate) return;
    state.selectedDate = date;
    renderHeatmap(state.dailyRows);
    renderTrend(state.dailyRows);
    renderDetail(state.selectedDate);
  };

  Promise.all([requireJson(summaryUrl), requireJson(hourlyUrl), requireJson(dailyUrl), requireJson(insightUrl)])
    .then(([summary, hourly, daily, insights]) => {
      const hourlyRows = Array.isArray(hourly.rows) ? hourly.rows : [];
      const dailyRows = Array.isArray(daily.rows) ? daily.rows : [];
      const modelMix = Array.isArray(insights.model_mix) ? insights.model_mix : [];
      const hourMix = Array.isArray(insights.hour_mix) ? insights.hour_mix : [];
      state.summary = summary;
      state.hourlyRows = hourlyRows;
      state.dailyRows = dailyRows;
      state.insights = insights;
      state.selectedDate =
        [...dailyRows].reverse().find((row) => Number(row.total_tokens || 0) > 0)?.date ||
        dailyRows.at(-1)?.date ||
        null;

      setField("total_tokens", formatInt(summary.total_tokens));
      setField("token_breakdown", `Input ${formatInt(summary.input_tokens)} · Output ${formatInt(summary.output_tokens)}`);
      setField("updated_at", formatTime(insights.updated_at || summary.updated_at));

      const models = [...new Set(hourlyRows.map((row) => row.model).filter(Boolean))];
      setField("model_count", models.length ? String(models.length) : "--");
      renderModelChips(models);

      const activeDays = dailyRows.filter((row) => Number(row.total_tokens || 0) > 0).length;
      setField("active_days", String(activeDays));
      setField("active_days_copy", `最近 ${dailyRows.length || 0} 天里，有记录的天数`);

      renderHeatmap(dailyRows);
      renderTrend(dailyRows);
      renderBars("usage-model-bars", modelMix, "model-fill", {
        getTooltip: (row) =>
          tooltipMarkup(row.model || "unknown", [
            ["Total", `${formatInt(row.total_tokens)} tokens`],
            ["Share", `${row.share}%`],
          ]),
      });
      renderBars("usage-hour-bars", hourMix, "hour-fill", {
        getTooltip: (row) =>
          tooltipMarkup(row.hour || "--", [
            ["Total", `${formatInt(row.total_tokens)} tokens`],
          ]),
      });
      renderDetail(state.selectedDate);
    })
    .catch((error) => {
      setField("updated_at", "数据暂时不可用");
      setField("total_tokens", "--");
      setField("token_breakdown", "--");
      setField("model_count", "--");
      setField("active_days", "--");
      setField("active_days_copy", "--");
      renderModelChips([]);
      renderHeatmap([]);
      renderTrend([]);
      renderBars("usage-model-bars", [], "model-fill");
      renderBars("usage-hour-bars", [], "hour-fill");
      renderDetail(null);
    });
})();
</script>
