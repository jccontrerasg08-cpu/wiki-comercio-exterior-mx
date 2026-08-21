(() => {
  const formatNumber = (value, digits = 0) => new Intl.NumberFormat("es-MX", {
    maximumFractionDigits: digits,
    minimumFractionDigits: digits,
  }).format(value);

  const finiteNumber = (value) => Number.isFinite(Number(value)) ? Number(value) : 0;

  const element = (tag, className) => {
    const node = document.createElement(tag);
    if (className) node.className = className;
    return node;
  };

  const textElement = (tag, text, className) => {
    const node = element(tag, className);
    node.textContent = text;
    return node;
  };

  const renderBars = (items, suffix) => {
    const values = items.map((item) => finiteNumber(item.value));
    const maximum = Math.max(...values, 0);
    const list = element("ul", "anam-dashboard__bars");

    items.forEach((item, index) => {
      const value = values[index];
      const width = maximum ? Math.min((value / maximum) * 100, 100) : 0;
      const row = element("li", "anam-dashboard__bar-row");
      const label = textElement("span", item.label || item.name || "");
      const amount = textElement(
        "strong",
        `${formatNumber(value, suffix === "%" ? 1 : 0)} ${suffix}`,
      );
      const track = element("span", "anam-dashboard__bar");
      track.setAttribute("aria-hidden", "true");
      const fill = document.createElement("span");
      fill.style.width = `${width}%`;
      track.append(fill);
      row.append(label, amount, track);
      list.append(row);
    });

    return list;
  };

  const renderRanking = (items) => {
    const wrapper = element("div", "anam-dashboard__table-wrap");
    const table = document.createElement("table");
    const head = document.createElement("thead");
    const headerRow = document.createElement("tr");
    ["Posición", "Aduana", "Recaudación Q2"].forEach((label) => {
      headerRow.append(textElement("th", label));
    });
    head.append(headerRow);
    const body = document.createElement("tbody");

    items.forEach((item) => {
      const row = document.createElement("tr");
      row.append(
        textElement("td", String(item.rank ?? "")),
        textElement("td", item.name || ""),
        textElement("td", `${formatNumber(finiteNumber(item.value))} MDP`),
      );
      body.append(row);
    });

    table.append(head, body);
    wrapper.append(table);
    return wrapper;
  };

  const renderSeries = (items) => {
    const fragment = document.createDocumentFragment();
    fragment.append(renderBars(items, "MDP"));
    fragment.append(textElement(
      "p",
      "Serie mensual de recaudación publicada para enero-junio de 2026.",
      "anam-dashboard__caption",
    ));
    return fragment;
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
    const summary = element("section", "anam-dashboard__metric");
    const value = document.createElement("strong");
    value.append(document.createTextNode(`${formatNumber(finiteNumber(indicator.value), digits)} `));
    value.append(textElement("span", unit));
    summary.append(
      textElement("p", indicator.label || ""),
      value,
      textElement("small", comparison || ""),
    );
    return summary;
  };

  const render = (root, data) => {
    const metric = root.querySelector("[data-dashboard-metric]").value;
    const view = root.querySelector("[data-dashboard-view]").value;
    const output = root.querySelector("[data-dashboard-output]");
    const status = root.querySelector("[data-dashboard-status]");
    const result = element("div", "anam-dashboard__result");

    if (view === "serie" && metric === "recaudacion") {
      result.append(renderSeries(data.series.recaudacion_mensual_mdp));
    } else if (view === "ranking" && metric === "recaudacion") {
      result.append(renderRanking(data.rankings.recaudacion_aduanas_q2_mdp));
    } else if (view === "composicion") {
      const items = metric === "recaudacion"
        ? data.breakdowns.recaudacion_por_tipo_aduana_q2_pct
        : metric === "pedimentos"
          ? data.breakdowns.pedimentos_por_tipo_aduana_q2_pct
          : data.breakdowns.operaciones_por_tipo_aduana_q2_pct;
      result.append(renderBars(items, "%"));
      result.append(textElement(
        "p",
        "Participaciones reportadas por ANAM para Q2 2026; no se recalculan desde otras métricas.",
        "anam-dashboard__caption",
      ));
    } else {
      result.append(textElement(
        "p",
        "Esta vista no está publicada con la granularidad seleccionada. Consulta el informe fuente para el detalle disponible.",
        "anam-dashboard__empty",
      ));
    }

    output.replaceChildren(metricSummary(data, metric), result);
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
        const output = root.querySelector("[data-dashboard-output]");
        const fallback = root.querySelector("[data-dashboard-fallback]");
        if (output && fallback instanceof HTMLTemplateElement) {
          output.replaceChildren(fallback.content.cloneNode(true));
        }
        status.textContent = "No fue posible cargar la vista interactiva. Se muestra el Resumen publicado de ANAM y la fuente primaria disponibles en esta página.";
      });
  };

  const boot = () => document.querySelectorAll("[data-anam-dashboard]").forEach(initialize);
  if (typeof document$ !== "undefined") {
    document$.subscribe(boot);
  } else {
    document.addEventListener("DOMContentLoaded", boot);
  }
})();
