"""Offline-first intelligence primitives for the legacy SNICE document index.

The module deliberately separates physical files from logical datasets. It does
not decide legal validity: transport/discovery metadata can identify versions,
backfills and likely anomalies, while legal currentness remains governed by the
repository's source and temporal-instrument layers.
"""

from __future__ import annotations

import calendar
import html
from dataclasses import asdict, dataclass, replace
from datetime import date, datetime, timedelta
import re
from statistics import median
import unicodedata
from urllib.parse import unquote, urljoin, urlparse


_DATE_SUFFIX_RE = re.compile(
    r"_(?P<filename_date>\d{8})-(?P<source_date>\d{8})(?P<tail>.*)$",
    re.IGNORECASE,
)
_INDEX_ROW_RE = re.compile(
    r'<a\s+[^>]*href=["\'](?P<href>[^"\']+)["\'][^>]*>.*?</a>'
    r"\s+(?P<day>\d{2}-[A-Za-z]{3}-\d{4})"
    r"\s+(?P<time>\d{2}:\d{2})"
    r"\s+(?P<size>\d+(?:\.\d+)?[KMGTP]?|-)",
    re.IGNORECASE | re.DOTALL,
)
_YEAR_RE = re.compile(r"(?<!\d)(?:19|20)\d{2}(?!\d)")

_MONTH_ALIASES: tuple[tuple[str, int], ...] = (
    ("SEPTIEMBRE", 9),
    ("DICIEMBRE", 12),
    ("NOVIEMBRE", 11),
    ("OCTUBRE", 10),
    ("FEBRERO", 2),
    ("AGOSTO", 8),
    ("ENERO", 1),
    ("MARZO", 3),
    ("ABRIL", 4),
    ("JUNIO", 6),
    ("JULIO", 7),
    ("MAYO", 5),
    ("SEPT", 9),
    ("ENE", 1),
    ("FEB", 2),
    ("MAR", 3),
    ("ABR", 4),
    ("MAY", 5),
    ("JUN", 6),
    ("JUL", 7),
    ("AGO", 8),
    ("SEP", 9),
    ("OCT", 10),
    ("NOV", 11),
    ("DIC", 12),
)

# These are collection-normalization aliases, not legal synonyms.
_FAMILY_ALIASES: tuple[tuple[str, str], ...] = (
    ("NOVALIDADOS", "NOVALIDADOS"),
    ("NO-VALIDADOS", "NOVALIDADOS"),
    ("NO_VALIDADOS", "NOVALIDADOS"),
    ("VALIDADOS", "VALIDADOS"),
    ("AVISODISPONIBILIDAD", "AVISODISPONIBILIDAD"),
    ("AVISO-DISPONIBILIDAD", "AVISODISPONIBILIDAD"),
    ("SIDERURGICO", "SIDERURGICO"),
    ("TEXITL", "TEXTIL"),
    ("TEXTIL", "TEXTIL"),
    ("CALZADO", "CALZADO"),
    ("IMMEX", "IMMEX"),
    ("PROSEC", "PROSEC"),
    ("ACUSE", "ACUSE"),
    ("LIGIE", "LIGIE"),
    ("TIGIE", "LIGIE"),
    ("NICO", "NICO"),
    ("LICITACION", "LICITACION"),
    ("BOLETIN", "BOLETIN"),
    ("OFICIO", "OFICIO"),
    ("CUPOS", "CUPOS"),
    ("CUPO", "CUPOS"),
    ("NOMS", "NOMS"),
    ("NOM", "NOMS"),
    ("CSA", "CSA"),
    ("TUV", "TUV"),
    ("ULUSA", "UL"),
    ("UL", "UL"),
)

_CATEGORY_MARKERS = (
    "PERMISO-AUTOMATICO-IMPORTACION",
    "AVISO-AUTOMATICO-IMPORTACION",
    "PERMISO-PREVIO-IMPORTACION",
    "PERMISO-PREVIO-EXPORTACION",
    "CUPOS-DEMANDA-EXPORTACION",
    "LICITACION-ACTUALIDAD",
    "IMPORTACION-EXPORTACION",
    "DIRECTORIO",
    "ETIQUETADO",
    "ACTUALIDAD",
    "ACUSE",
    "LIGIE",
    "NOMS",
)

_COMPANIONS: dict[str, tuple[str, ...]] = {
    "IMMEX": ("PROSEC",),
    "PROSEC": ("IMMEX",),
    "SIDERURGICO": ("TEXTIL", "CALZADO"),
    "TEXTIL": ("SIDERURGICO", "CALZADO"),
    "CALZADO": ("SIDERURGICO", "TEXTIL"),
}


@dataclass(frozen=True, slots=True)
class ParsedSniceFilename:
    filename: str
    normalized_name: str
    family: str
    category: str
    filename_date: date
    source_date: date
    extension: str
    period_year: int | None
    period_month: int | None
    logical_dataset_id: str


@dataclass(frozen=True, slots=True)
class SniceDocument:
    filename: str
    normalized_name: str
    family: str
    category: str
    filename_date: date
    source_date: date
    extension: str
    period_year: int | None
    period_month: int | None
    logical_dataset_id: str
    source_url: str
    last_modified: datetime
    discovered_at: datetime
    bytes: int
    sha256: str | None = None
    version: int = 1
    is_replacement: bool = False
    is_backfill: bool = False
    is_anomaly: bool = False


@dataclass(frozen=True, slots=True)
class UnparsedSniceEntry:
    filename: str
    source_url: str
    last_modified: datetime
    bytes: int
    reason: str


@dataclass(frozen=True, slots=True)
class SniceIndexSnapshot:
    documents: tuple[SniceDocument, ...]
    unparsed_entries: tuple[UnparsedSniceEntry, ...]
    index_entry_count: int


@dataclass(frozen=True, slots=True)
class SniceSeries:
    logical_dataset_id: str
    family: str
    category: str
    period_year: int | None
    period_month: int | None
    documents: tuple[SniceDocument, ...]


@dataclass(frozen=True, slots=True)
class RowDiff:
    rows_added: int
    rows_removed: int
    rows_modified: int
    added_keys: tuple[tuple[object, ...], ...]
    removed_keys: tuple[tuple[object, ...], ...]
    modified_keys: tuple[tuple[object, ...], ...]


def _fold(value: str) -> str:
    decomposed = unicodedata.normalize("NFKD", value)
    plain = "".join(ch for ch in decomposed if not unicodedata.combining(ch))
    folded = plain.upper().replace("\\", "-").replace("/", "-")
    folded = re.sub(r"[^A-Z0-9]+", "-", folded)
    return re.sub(r"-+", "-", folded).strip("-")


def _date_yyyymmdd(raw: str) -> date:
    return datetime.strptime(raw, "%Y%m%d").date()


def _extension(filename: str) -> str:
    suffix = filename.rsplit(".", 1)[-1] if "." in filename else ""
    return re.sub(r"[^A-Za-z0-9].*$", "", suffix).lower()


def _family(semantic: str) -> str:
    folded = _fold(semantic)
    for alias, canonical in _FAMILY_ALIASES:
        alias_folded = _fold(alias)
        if folded == alias_folded or folded.startswith(alias_folded + "-"):
            return canonical
    first = folded.split("-", 1)[0]
    return first or "UNKNOWN"


def _period(semantic: str) -> tuple[int | None, int | None]:
    folded = _fold(semantic)
    for month_name, month_number in _MONTH_ALIASES:
        pattern = re.compile(
            rf"(?:^|-){re.escape(month_name)}(?:-|)?(?P<year>(?:19|20)\d{{2}})(?:-|$)"
        )
        match = pattern.search(folded)
        if match:
            return int(match.group("year")), month_number
    parts = folded.split("-")
    for index, part in enumerate(parts[:-1]):
        month_number = next(
            (number for name, number in _MONTH_ALIASES if part == name), None
        )
        if month_number is not None and _YEAR_RE.fullmatch(parts[index + 1]):
            return int(parts[index + 1]), month_number
    return None, None


def _category(semantic: str, family: str) -> str:
    folded = _fold(semantic)
    for marker in _CATEGORY_MARKERS:
        if marker in folded:
            return marker
    if family == "ACUSE":
        return "ACUSE"
    return family


def _logical_dataset_id(
    semantic: str,
    *,
    family: str,
    category: str,
    period_year: int | None,
    period_month: int | None,
    source_date: date,
) -> str:
    family_key = family.casefold()
    category_key = category.casefold()
    if family == "ACUSE":
        folio = re.search(r"ACUSE\D*(\d+)", _fold(semantic))
        if folio:
            return f"{family_key}:{category_key}:{folio.group(1)}"
    if period_year is not None and period_month is not None:
        return f"{family_key}:{category_key}:{period_year:04d}-{period_month:02d}"
    return f"{family_key}:{category_key}:{source_date.isoformat()}"


def parse_snice_filename(filename: str) -> ParsedSniceFilename:
    """Normalize one SNICE filename without assuming its upload date is its period."""

    clean = unquote(html.unescape(filename)).strip()
    match = _DATE_SUFFIX_RE.search(clean)
    if not match:
        raise ValueError(f"SNICE filename has no terminal date pair: {filename}")
    semantic = clean[: match.start()]
    filename_date = _date_yyyymmdd(match.group("filename_date"))
    source_date = _date_yyyymmdd(match.group("source_date"))
    family = _family(semantic)
    period_year, period_month = _period(semantic)
    category = _category(semantic, family)
    extension = _extension(clean)
    logical_dataset_id = _logical_dataset_id(
        semantic,
        family=family,
        category=category,
        period_year=period_year,
        period_month=period_month,
        source_date=source_date,
    )
    return ParsedSniceFilename(
        filename=clean,
        normalized_name=_fold(clean),
        family=family,
        category=category,
        filename_date=filename_date,
        source_date=source_date,
        extension=extension,
        period_year=period_year,
        period_month=period_month,
        logical_dataset_id=logical_dataset_id,
    )


def _parse_size(raw: str) -> int:
    value = raw.strip().upper()
    if value == "-":
        return 0
    match = re.fullmatch(r"(?P<number>\d+(?:\.\d+)?)(?P<unit>[KMGTP]?)", value)
    if not match:
        raise ValueError(f"unrecognized Apache index size: {raw}")
    exponent = {"": 0, "K": 1, "M": 2, "G": 3, "T": 4, "P": 5}[match.group("unit")]
    return int(float(match.group("number")) * (1024**exponent))


def parse_index_snapshot(
    index_html: str,
    *,
    base_url: str,
    discovered_at: datetime,
) -> SniceIndexSnapshot:
    """Parse every file-shaped autoindex row and preserve parse failures."""

    parsed_base = urlparse(base_url)
    if parsed_base.scheme not in {"https", "http"} or not parsed_base.hostname:
        raise ValueError("base_url must be an absolute HTTP(S) URL")

    documents: list[SniceDocument] = []
    unparsed: list[UnparsedSniceEntry] = []
    entry_count = 0
    for row in _INDEX_ROW_RE.finditer(index_html):
        href = html.unescape(row.group("href")).strip()
        if href.startswith("?") or (href.startswith("/") and href.rstrip("/") == ""):
            continue
        filename = unquote(urlparse(href).path.rsplit("/", 1)[-1])
        if not filename:
            continue
        entry_count += 1
        source_url = urljoin(base_url, href)
        last_modified = datetime.strptime(
            f"{row.group('day')} {row.group('time')}", "%d-%b-%Y %H:%M"
        )
        size = _parse_size(row.group("size"))
        try:
            parsed = parse_snice_filename(filename)
        except ValueError as exc:
            unparsed.append(
                UnparsedSniceEntry(
                    filename=filename,
                    source_url=source_url,
                    last_modified=last_modified,
                    bytes=size,
                    reason=str(exc),
                )
            )
            continue
        documents.append(
            SniceDocument(
                **asdict(parsed),
                source_url=source_url,
                last_modified=last_modified,
                discovered_at=discovered_at,
                bytes=size,
            )
        )

    return SniceIndexSnapshot(
        documents=tuple(documents),
        unparsed_entries=tuple(unparsed),
        index_entry_count=entry_count,
    )


def parse_index_html(
    index_html: str,
    *,
    base_url: str,
    discovered_at: datetime,
) -> list[SniceDocument]:
    """Compatibility wrapper returning only successfully normalized documents."""

    return list(
        parse_index_snapshot(
            index_html,
            base_url=base_url,
            discovered_at=discovered_at,
        ).documents
    )


def _period_end(year: int, month: int) -> date:
    return date(year, month, calendar.monthrange(year, month)[1])


def _is_backfill(document: SniceDocument) -> bool:
    if document.period_year is None or document.period_month is None:
        return False
    return document.last_modified.date() > (
        _period_end(document.period_year, document.period_month) + timedelta(days=90)
    )


def build_series(documents: list[SniceDocument]) -> list[SniceSeries]:
    """Group physical documents into deterministic logical version histories."""

    grouped: dict[str, list[SniceDocument]] = {}
    for document in documents:
        grouped.setdefault(document.logical_dataset_id, []).append(document)
    series: list[SniceSeries] = []
    for logical_dataset_id, members in grouped.items():
        ordered = sorted(members, key=lambda item: (item.last_modified, item.filename))
        versioned = tuple(
            replace(
                item,
                version=index,
                is_replacement=index > 1,
                is_backfill=_is_backfill(item),
            )
            for index, item in enumerate(ordered, start=1)
        )
        first = versioned[0]
        series.append(
            SniceSeries(
                logical_dataset_id=logical_dataset_id,
                family=first.family,
                category=first.category,
                period_year=first.period_year,
                period_month=first.period_month,
                documents=versioned,
            )
        )
    return sorted(series, key=lambda item: item.logical_dataset_id)


def detect_missing_companions(documents: list[SniceDocument]) -> list[dict[str, object]]:
    """Flag expected monthly companion families without treating absence as invalidity."""

    present = {
        (doc.family, doc.period_year, doc.period_month)
        for doc in documents
        if doc.period_year is not None and doc.period_month is not None
    }
    findings: list[dict[str, object]] = []
    for family, year, month in sorted(
        present, key=lambda item: (item[1] or 0, item[2] or 0, item[0])
    ):
        for companion in _COMPANIONS.get(family, ()):
            if (companion, year, month) not in present:
                findings.append(
                    {
                        "family": family,
                        "missing_family": companion,
                        "period_year": year,
                        "period_month": month,
                    }
                )
    return findings


def detect_size_anomaly(current_bytes: int, baseline_bytes: list[int]) -> bool:
    """Use median/MAD plus a proportional floor to avoid noisy small samples."""

    clean = [int(value) for value in baseline_bytes if int(value) >= 0]
    if len(clean) < 3:
        return False
    center = float(median(clean))
    if center <= 0:
        return current_bytes > 0
    mad = float(median(abs(value - center) for value in clean))
    threshold = max(6.0 * mad, 0.25 * center)
    return abs(float(current_bytes) - center) > threshold


def _row_index(
    rows: list[dict[str, object]], key_fields: tuple[str, ...]
) -> dict[tuple[object, ...], dict[str, object]]:
    index: dict[tuple[object, ...], dict[str, object]] = {}
    for row in rows:
        key = tuple(row.get(field) for field in key_fields)
        if key in index:
            raise ValueError(f"duplicate snapshot key: {key!r}")
        index[key] = dict(row)
    return index


def diff_rows(
    previous: list[dict[str, object]],
    current: list[dict[str, object]],
    *,
    key_fields: tuple[str, ...],
) -> RowDiff:
    """Return deterministic CDC counts for normalized snapshot rows."""

    if not key_fields:
        raise ValueError("key_fields must not be empty")
    old = _row_index(previous, key_fields)
    new = _row_index(current, key_fields)
    old_keys = set(old)
    new_keys = set(new)
    added = tuple(sorted(new_keys - old_keys, key=repr))
    removed = tuple(sorted(old_keys - new_keys, key=repr))
    modified = tuple(
        sorted(
            (key for key in old_keys & new_keys if old[key] != new[key]),
            key=repr,
        )
    )
    return RowDiff(
        rows_added=len(added),
        rows_removed=len(removed),
        rows_modified=len(modified),
        added_keys=added,
        removed_keys=removed,
        modified_keys=modified,
    )
