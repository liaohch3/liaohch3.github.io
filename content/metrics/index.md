+++
title = "AI 日常"
description = "最近和 AI 一起写代码时的一些使用记录。"
draft = false
toc = false
comments = false
+++

这页就简单记一下我最近和 AI 一起写代码时的一些使用情况。

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
</div>

<script>
(() => {
  const summaryUrl = "/data/ai-usage-summary.json";
  const hourlyUrl = "/data/ai-usage-hourly.json";
  const dailyUrl = "/data/ai-usage-daily.json";
  const insightUrl = "/data/ai-usage-insights.json";

  const formatInt = (value) => new Intl.NumberFormat("en-US").format(Number(value || 0));
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

    rows.forEach((row, index) => {
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

      const cell = document.createElement("div");
      cell.className = `heat-cell heat-l${level}`;
      cell.title = `${row.date}: ${formatInt(value)} tokens`;
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
      ${points.map((point) => `<circle class="trend-dot" cx="${point.x}" cy="${point.y}" r="4"></circle>`).join("")}
    `;
    axis.innerHTML = recent
      .map((item) => `<span>${new Date(`${item.date}T00:00:00Z`).toLocaleDateString("en-US", { weekday: "short", timeZone: "UTC" })}</span>`)
      .join("");
  };

  const renderBars = (containerId, rows, fillClass) => {
    const container = document.getElementById(containerId);
    if (!container) return;
    container.innerHTML = "";
    if (!rows.length) {
      container.innerHTML = '<div class="usage-empty">暂时还没有图表数据。</div>';
      return;
    }

    const maxValue = Math.max(...rows.map((row) => Number(row.total_tokens || 0)), 1);
    rows.forEach((row) => {
      const item = document.createElement("div");
      item.className = containerId === "usage-hour-bars" ? "hour-bar-row" : "model-bar-row";
      const label = row.model || row.hour || "--";
      const share = row.share != null ? `${row.share}%` : formatInt(row.total_tokens);
      const width = row.share != null ? Number(row.share) : (Number(row.total_tokens || 0) / maxValue) * 100;
      item.innerHTML = `
        <div class="row-label">${label}</div>
        <div class="bar-track"><div class="bar-fill ${fillClass}" style="width:${width}%"></div></div>
        <div class="row-value">${share}</div>
      `;
      container.appendChild(item);
    });
  };

  Promise.all([requireJson(summaryUrl), requireJson(hourlyUrl), requireJson(dailyUrl), requireJson(insightUrl)])
    .then(([summary, hourly, daily, insights]) => {
      const hourlyRows = Array.isArray(hourly.rows) ? hourly.rows : [];
      const dailyRows = Array.isArray(daily.rows) ? daily.rows : [];
      const modelMix = Array.isArray(insights.model_mix) ? insights.model_mix : [];
      const hourMix = Array.isArray(insights.hour_mix) ? insights.hour_mix : [];

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
      renderBars("usage-model-bars", modelMix, "model-fill");
      renderBars("usage-hour-bars", hourMix, "hour-fill");
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
    });
})();
</script>
