(() => {
  const toggle = document.getElementById("toggle-menu");
  const menu = document.getElementById("main-menu");

  if (toggle && menu) {
    const syncMenuState = () => {
      const open = document.body.classList.contains("show-menu");
      toggle.setAttribute("aria-expanded", String(open));
      menu.setAttribute("aria-modal", open ? "true" : "false");
      menu.setAttribute("role", open ? "dialog" : "navigation");
    };

    toggle.addEventListener("click", () => window.setTimeout(syncMenuState, 0));
    document.addEventListener("keydown", (event) => {
      if (event.key !== "Escape" || !document.body.classList.contains("show-menu")) return;
      toggle.click();
      toggle.focus();
    });
    menu.addEventListener("click", (event) => {
      const link = event.target.closest("a");
      if (link && document.body.classList.contains("show-menu")) toggle.click();
    });
    syncMenuState();
  }

  window.addEventListener("load", () => {
    window.setTimeout(() => {
      document.querySelectorAll(".article-content div.highlight").forEach((highlight, index) => {
        if (highlight.closest(".code-frame")) return;

        const code = highlight.querySelector("code");
        const copy = highlight.querySelector(".copyCodeButton");
        const frame = document.createElement("div");
        const tools = document.createElement("div");
        const label = document.createElement("span");
        const languageClass = Array.from(code?.classList || [])
          .find((name) => name.startsWith("language-") || name.startsWith("lang-"));
        const language = code?.dataset.lang
          || languageClass?.replace(/^lang(uage)?-/, "")
          || highlight.querySelector("[data-lang]")?.dataset.lang
          || `代码 ${String(index + 1).padStart(2, "0")}`;

        frame.className = "code-frame";
        tools.className = "code-frame__tools";
        label.textContent = language;

        highlight.parentNode.insertBefore(frame, highlight);
        frame.appendChild(tools);
        tools.appendChild(label);
        if (copy) {
          copy.setAttribute("aria-label", "复制代码块");
          tools.appendChild(copy);
        }
        frame.appendChild(highlight);
      });

      const evidenceDetails = Array.from(document.querySelectorAll(".claim-ledger__checks"));
      const syncEvidenceDensity = () => {
        const compact = window.matchMedia("(max-width: 389px)").matches;
        evidenceDetails.forEach((details) => {
          if (compact) details.removeAttribute("open");
          else details.setAttribute("open", "");
        });
      };
      if (evidenceDetails.length > 0) {
        syncEvidenceDensity();
        window.addEventListener("resize", syncEvidenceDensity, { passive: true });
      }

      document.querySelectorAll("[data-claim-ledger-json]").forEach((node) => {
        let payload;
        try {
          payload = JSON.parse(node.textContent || "{}");
        } catch {
          return;
        }

        const evidence = Array.isArray(payload.evidence) ? payload.evidence : [];
        const grouped = evidence.reduce((acc, item) => {
          const anchor = item.section_anchor || "article-content";
          acc[anchor] = acc[anchor] || [];
          acc[anchor].push(item);
          return acc;
        }, {});

        Object.entries(grouped).forEach(([anchor, items]) => {
          const heading = document.getElementById(anchor);
          if (!heading || heading.dataset.claimNoteAttached === "true") return;

          const note = document.createElement("aside");
          note.className = "section-claim-note";
          note.setAttribute("aria-label", "本节证据和复核点");

          const rail = document.createElement("div");
          rail.className = "section-claim-note__rail";
          rail.textContent = "evidence";
          note.appendChild(rail);

          const list = document.createElement("div");
          list.className = "section-claim-note__items";

          items.slice(0, 3).forEach((item) => {
            const link = document.createElement("a");
            const target = item.url || "#claim-ledger";
            link.href = target;
            if (/^https?:\/\//.test(target)) {
              link.target = "_blank";
              link.rel = "noopener noreferrer";
            }

            const meta = document.createElement("span");
            meta.textContent = `${item.role || "证据"} · ${item.source || item.section_label || "来源"}`;

            const title = document.createElement("strong");
            title.textContent = item.title || "未命名来源";

            const detail = document.createElement("em");
            detail.textContent = item.note || "用于核对本节判断。";

            link.append(meta, title, detail);
            list.appendChild(link);
          });

          if (payload.uncertainty || payload.followUp) {
            const compact = document.createElement("details");
            compact.className = "section-claim-note__details";
            const summary = document.createElement("summary");
            summary.textContent = "复核点";
            compact.appendChild(summary);

            if (payload.uncertainty) {
              const uncertainty = document.createElement("p");
              uncertainty.textContent = `不确定：${payload.uncertainty}`;
              compact.appendChild(uncertainty);
            }

            if (payload.followUp) {
              const follow = document.createElement("p");
              follow.textContent = `后续：${payload.followUp}`;
              compact.appendChild(follow);
            }

            list.appendChild(compact);
          }

          note.appendChild(list);
          heading.insertAdjacentElement("afterend", note);
          heading.dataset.claimNoteAttached = "true";
        });

        const links = Array.from(document.querySelectorAll("[data-claim-ledger-link]"));
        if ("IntersectionObserver" in window && links.length > 0) {
          const byAnchor = new Map(links.map((link) => [link.dataset.claimLedgerLink, link]));
          const observer = new IntersectionObserver((entries) => {
            entries.forEach((entry) => {
              const link = byAnchor.get(entry.target.id);
              if (!link) return;
              link.classList.toggle("is-active", entry.isIntersecting);
            });
          }, { rootMargin: "-18% 0px -68% 0px", threshold: 0.01 });

          Object.keys(grouped).forEach((anchor) => {
            const heading = document.getElementById(anchor);
            if (heading) observer.observe(heading);
          });
        }
      });
    }, 50);
  });
})();
