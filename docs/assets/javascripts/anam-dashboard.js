(() => {
  const formatNumber = (value, digits = 0) => new Intl.NumberFormat("es-MX", {
    maximumFractionDigits: digits,
    minimumFractionDigits: digits,
  }).format(value);

  const renderBars = (items, suffix) => {
    const maximum = Math.max(...items.map((item) => item.value));
    const rows = items.map((item) => {
      const width = maximum ? (item.value / maximum) * 100 : 0;
      return `<li class="anam-dashboard__bar-row"><span>${item.label || item.name}</span><strong>${formatNumber(item.value, suffix === "%" ? 1 : 0)} ${suffix}</strong><span class="anam-dashboard__bar" aria-hidden="true"><span style="width:${width}%"></span></span></li>`;
    }).join("");
    return `<ul class="anam-dashboard__bars">${rows}</ul>`;
  };

  const renderRanking = (items) => {
    const body = items.map((item) => `<tr><td>${item.rank}</td><td>${item.name}</td><td>${formatNumber(item.value)} MDP</td></tr>`).join("");
    return `<div class="anam-dashboard__table-wrap"><table><thead><tr><th>Posición</th><th>Aduana</th><th>Recaudación Q2</th></tr></thead><tbody>${body}</tbody></table></div>`;
  };

  const renderSeries = (items) => {
    const rows = items.map((item) => ({ label: item.label, value: item.value }));
    return `${renderBars(rows, "MDP")}<p class="anam-dashboard__caption">Serie mensual de recaudación publicada para enero-junio de 2026.</p>`;
  };

  const metricSummary = (data, metric) => {
    const key = {
      recaudacion: "recaudacion_q2_mdp",
      pedimentos: "pedimentos_q2_millones",
      operaciones: "operaciones_q2_millones",
    }[metric];
    const indicator = data.indicators[key];
    const unit = indicator.unit === "MDP" ? "MDP" : indicator.unit;
    const digits = indicator.unit === "millones" ? 2 : 0;
    const comparison = indicator.comparison_value === null
      ? indicator.comparison_label
      : `${indicator.comparison_value > 0 ? "+" : ""}${formatNumber(indicator.comparison_value, 1)}% ${indicator.comparison_label}`;
    return `<section class="anam-dashboard__metric"><p>${indicator.label}</p><strong>${formatNumber(indicator.value, digits)} <span>${unit}</span></strong><small>${comparison}</small></section>`;
  };

  const render = (root, data) => {
    const metric = root.querySelector("[data-dashboard-metric]").value;
    const view = root.querySelector("[data-dashboard-view]").value;
    const output = root.querySelector("[data-dashboard-output]");
    const status = root.querySelector("[data-dashboard-status]");
    let body = "";

    if (view === "serie" && metric === "recaudacion") {
      body = renderSeries(data.series.recaudacion_mensual_mdp);
    } else if (view === "ranking" && metric === "recaudacion") {
      body = renderRanking(data.rankings.recaudacion_aduanas_q2_mdp);
    } else if (view === "composicion") {
      const items = metric === "recaudacion"
        ? data.breakdowns.recaudacion_por_tipo_aduana_q2_pct
        : metric === "pedimentos"
          ? data.breakdowns.pedimentos_por_tipo_aduana_q2_pct
          : data.breakdowns.operaciones_por_tipo_aduana_q2_pct;
      body = `${renderBars(items, "%")}<p class="anam-dashboard__caption">Participaciones reportadas por ANAM para Q2 2026; no se recalculan desde otras métricas.</p>`;
    } else {
      body = `<p class="anam-dashboard__empty">Esta vista no está publicada con la granularidad seleccionada. Consulta el informe fuente para el detalle disponible.</p>`;
    }

    output.innerHTML = `${metricSummary(data, metric)}<div class="anam-dashboard__result">${body}</div>`;
    const labels = { recaudacion: "recaudación", pedimentos: "pedimentos", operaciones: "operaciones" };
    status.textContent = `Mostrando ${labels[metric]} para ${data.scope.period_label}.`;
  };

  const initialize = (root) => {
    if (root.dataset.loaded === "true") return;
    root.dataset.loaded = "true";
    const source = root.dataset.source;
    const status = root.querySelector("[data-dashboard-status]");
    status.textContent = "Cargando datos documentados por ANAM.";
    fetch(source)
      .then((response) => {
        if (!response.ok) throw new Error(`HTTP ${response.status}`);
        return response.json();
      })
      .then((data) => {
        root.querySelectorAll("select").forEach((control) => {
          control.addEventListener("change", () => render(root, data));
        });
        render(root, data);
      })
      .catch(() => {
        status.textContent = "No fue posible cargar la vista interactiva. Usa la tabla y la fuente primaria disponibles en esta página.";
      });
  };

  const boot = () => document.querySelectorAll("[data-anam-dashboard]").forEach(initialize);
  if (typeof document$ !== "undefined") {
    document$.subscribe(boot);
  } else {
    document.addEventListener("DOMContentLoaded", boot);
  }
})();
