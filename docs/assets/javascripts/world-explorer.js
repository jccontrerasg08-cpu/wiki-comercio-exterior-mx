(function () {
  "use strict";

  function createCell(text) {
    const cell = document.createElement("td");
    cell.textContent = text;
    return cell;
  }

  function renderCountries(tableBody, countries) {
    tableBody.replaceChildren();
    for (const country of countries) {
      const row = document.createElement("tr");
      const name = document.createElement("th");
      name.scope = "row";
      const link = document.createElement("a");
      link.href = country.guide_url;
      link.textContent = country.name_es;
      name.append(link);
      row.append(name, createCell(country.iso3), createCell(country.region), createCell(country.official_focus));
      tableBody.append(row);
    }
  }

  async function start(root) {
    const source = root.dataset.source;
    const region = root.querySelector("[data-world-region]");
    const query = root.querySelector("[data-world-query]");
    const tableBody = root.querySelector("[data-world-table]");
    const status = root.querySelector("[data-world-status]");
    const empty = root.querySelector("[data-world-empty]");
    if (!source || !region || !query || !tableBody || !status || !empty) return;

    try {
      const response = await fetch(source, { credentials: "same-origin" });
      if (!response.ok) throw new Error("data-unavailable");
      const data = await response.json();
      const countries = data.country_guides || [];
      const applyFilters = function () {
        const selectedRegion = region.value;
        const phrase = query.value.trim().toLocaleLowerCase("es-MX");
        const visible = countries.filter(function (country) {
          const regionMatches = !selectedRegion || country.region === selectedRegion;
          const textMatches = !phrase || [country.name_es, country.iso3, country.region]
            .join(" ")
            .toLocaleLowerCase("es-MX")
            .includes(phrase);
          return regionMatches && textMatches;
        });
        renderCountries(tableBody, visible);
        empty.hidden = visible.length !== 0;
        empty.textContent = visible.length === 0
          ? "No hay guías que coincidan con estos filtros."
          : "";
        status.textContent = visible.length === 1
          ? "Mostrando 1 guía de país curada."
          : "Mostrando " + visible.length + " guías de país curadas.";
      };
      region.addEventListener("change", applyFilters);
      query.addEventListener("input", applyFilters);
      applyFilters();
    } catch (error) {
      status.textContent = "No se pudo actualizar el filtro. La lista accesible publicada sigue disponible en esta página.";
    }
  }

  function init() {
    document.querySelectorAll("[data-world-explorer]").forEach(start);
  }

  if (typeof document$ !== "undefined") {
    document$.subscribe(init);
  } else if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init, { once: true });
  } else {
    init();
  }
}());
