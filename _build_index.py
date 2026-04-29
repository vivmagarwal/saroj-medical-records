#!/usr/bin/env python3
"""Build all_reports.html — a clickable, searchable, filter-able index of
all 188 per-report markdowns, grouped by date, newest first.
"""
import os
import re
import json
import html
from collections import defaultdict
from datetime import datetime

MD_DIR = "report_md"


def parse_md(path: str) -> dict:
    with open(path) as fh:
        text = fh.read()
    rec = {"md_path": path}
    m = re.search(r"^# (.+)$", text, re.MULTILINE)
    rec["title"] = m.group(1).strip() if m else os.path.basename(path)
    m = re.search(r"\*\*Date performed\*\*:\s*(\S+)", text)
    rec["date"] = m.group(1).strip() if m else None
    m = re.search(r"\*\*Category\*\*:\s*(\S+)", text)
    rec["category"] = m.group(1).strip() if m else "Other"
    m = re.search(r"\*\*Source PDF\*\*:\s*\[`?\.\./report_pdf/([^`)]+)`?\]", text)
    rec["pdf"] = m.group(1).strip() if m else None
    m = re.search(
        r"## Summary \(extracted\)\s*\n(.*?)\n## Verbatim text from PDF",
        text,
        re.DOTALL,
    )
    summary = (m.group(1).strip() if m else "")
    summary = re.sub(r"\s+", " ", summary)
    rec["summary"] = summary
    return rec


def fmt_long_date(iso: str) -> str:
    try:
        return datetime.strptime(iso, "%Y-%m-%d").strftime("%A, %d %B %Y")
    except (ValueError, TypeError):
        return iso or "(unknown)"


def truncate(s: str, n: int = 280) -> str:
    if len(s) <= n:
        return s
    return s[: n - 1].rstrip() + "…"


CAT_COLOR = {
    "XRay": "#5b8def",
    "USG": "#7c5cff",
    "CT": "#9c5cff",
    "ECHO": "#a02020",
    "ECG": "#c0392b",
    "Holter": "#d35400",
    "Lab-Haem": "#c81d65",
    "Lab-Biochem": "#0a805e",
    "Lab-Micro": "#777028",
    "Lab-Serol": "#7a4f8b",
    "Lab-ClinPath": "#6b4e1f",
    "Summary-Discharge": "#2c3e50",
    "Summary-Daycare": "#34495e",
    "Consent": "#666",
}


def main() -> None:
    files = sorted(f for f in os.listdir(MD_DIR) if f.endswith(".md"))
    records = [parse_md(os.path.join(MD_DIR, f)) for f in files]
    by_date = defaultdict(list)
    for r in records:
        by_date[r["date"] or "(unknown)"].append(r)
    dates = sorted(by_date.keys(), reverse=True)

    # Build category options for the filter pills
    cats = sorted({r["category"] for r in records})

    # Build the HTML
    css = """
:root { --ink:#1a1a1a; --muted:#555; --line:#d8dee6; --bg:#f7f9fc; }
* { box-sizing: border-box; }
body { font-family: -apple-system,BlinkMacSystemFont,"Segoe UI","Helvetica Neue",Arial,sans-serif;
  background: var(--bg); color: var(--ink); margin: 0;
  padding: 28px 16px 48px; line-height: 1.45; }
.wrap { max-width: 1080px; margin: 0 auto; }
header { border-bottom: 2px solid var(--ink); padding-bottom: 12px; margin-bottom: 18px; }
header a.back { font-size: 13px; color: var(--muted); text-decoration: none; }
header a.back:hover { color: var(--ink); }
h1 { font-size: 24px; margin: 6px 0 0; }
.sub { color: var(--muted); margin: 4px 0 0; font-size: 14px; }
.toolbar { display: flex; gap: 10px; flex-wrap: wrap; align-items: center;
  position: sticky; top: 0; background: var(--bg); padding: 12px 0 12px;
  z-index: 10; border-bottom: 1px solid var(--line); margin-bottom: 14px; }
.toolbar input[type=search] { flex: 1 1 240px; padding: 8px 12px;
  border: 1px solid var(--line); border-radius: 6px; font-size: 14px;
  background: white; }
.toolbar input[type=search]:focus { outline: 2px solid #4a90e2; outline-offset: -1px; }
.pills { display: flex; gap: 6px; flex-wrap: wrap; }
.pill { padding: 4px 10px; border-radius: 999px; font-size: 12px;
  background: white; border: 1px solid var(--line); cursor: pointer;
  user-select: none; color: var(--ink); }
.pill.active { background: var(--ink); color: white; border-color: var(--ink); }
.pill:hover:not(.active) { border-color: var(--ink); }
.count { font-size: 13px; color: var(--muted); margin-left: auto; white-space: nowrap; }
.day { margin-top: 22px; }
.day h2 { font-size: 15px; margin: 0 0 8px; padding-bottom: 4px;
  border-bottom: 1px solid var(--line); color: var(--ink);
  position: sticky; top: 60px; background: var(--bg); z-index: 5;
  padding-top: 6px; }
.day .iso { color: var(--muted); font-weight: 400; font-size: 13px; margin-left: 6px; }
.entry { background: white; border: 1px solid var(--line); border-radius: 6px;
  padding: 10px 14px; margin-bottom: 8px; }
.entry .row1 { display: flex; gap: 8px; align-items: baseline; flex-wrap: wrap; }
.entry .badge { font-size: 11px; padding: 1px 8px; border-radius: 3px;
  color: white; font-weight: 600; letter-spacing: 0.2px; flex: none; }
.entry .title { font-weight: 600; font-size: 14.5px; flex: 1 1 auto; min-width: 0; }
.entry .links { font-size: 12px; flex: none; }
.entry .links a { color: #2a5db0; text-decoration: none; margin-left: 8px;
  border-bottom: 1px dotted #6688aa; }
.entry .links a:hover { color: #0a4d8c; border-bottom-color: #0a4d8c; }
.entry .summary { color: #333; font-size: 13px; margin: 5px 0 0;
  display: -webkit-box; -webkit-line-clamp: 3; -webkit-box-orient: vertical;
  overflow: hidden; }
.entry .summary.expanded { -webkit-line-clamp: unset; overflow: visible; }
.entry .more { font-size: 12px; color: #2a5db0; cursor: pointer; user-select: none;
  display: inline-block; margin-top: 3px; }
.entry .more:hover { text-decoration: underline; }
.empty { padding: 40px; text-align: center; color: var(--muted); display: none; }
@media (max-width: 720px) {
  body { padding: 16px 10px; }
  .toolbar { position: static; }
  .day h2 { position: static; }
}
"""

    parts: list[str] = []
    parts.append("<!DOCTYPE html>")
    parts.append('<html lang="en"><head><meta charset="UTF-8">')
    parts.append('<meta name="viewport" content="width=device-width,initial-scale=1">')
    parts.append("<title>All 188 Reports — Saroj Agarwal</title>")
    parts.append(f"<style>{css}</style>")
    parts.append("</head><body><div class='wrap'>")

    parts.append('<header>')
    parts.append('<a class="back" href="./index.html">← Back to hub</a>')
    parts.append('<h1>All 188 Reports — Saroj Agarwal</h1>')
    parts.append(f'<p class="sub">Date range: {dates[-1]} → {dates[0]} · '
                 f'Click any report to open its PDF in a new tab.</p>')
    parts.append('</header>')

    # Toolbar — search + category pills + count
    parts.append('<div class="toolbar">')
    parts.append('<input type="search" id="q" placeholder="Search title or summary…" autocomplete="off">')
    parts.append('<div class="pills" id="pills">')
    parts.append('<span class="pill active" data-cat="*">All</span>')
    for c in cats:
        parts.append(f'<span class="pill" data-cat="{html.escape(c)}">{html.escape(c)}</span>')
    parts.append('</div>')
    parts.append(f'<span class="count" id="count">{len(records)} reports</span>')
    parts.append('</div>')

    # Per-day groups
    for d in dates:
        items = sorted(by_date[d], key=lambda r: (r["category"] or "", r["title"]))
        parts.append(f'<section class="day" data-day="{html.escape(d)}">')
        parts.append(f'<h2>{html.escape(fmt_long_date(d))} '
                     f'<span class="iso">({html.escape(d)} · {len(items)} report'
                     f"{'s' if len(items) != 1 else ''})</span></h2>")
        for r in items:
            cat = r["category"]
            color = CAT_COLOR.get(cat, "#666")
            pdf = r["pdf"] or ""
            md = r["md_path"]
            title = html.escape(r["title"])
            summary = html.escape(r["summary"])
            full = summary  # we just truncate via CSS line-clamp
            parts.append(f'<article class="entry" data-cat="{html.escape(cat)}" data-text="{html.escape((r["title"] + " " + r["summary"]).lower())}">')
            parts.append('<div class="row1">')
            parts.append(f'<span class="badge" style="background:{color}">{html.escape(cat)}</span>')
            parts.append(f'<span class="title">{title}</span>')
            parts.append('<span class="links">')
            if pdf:
                parts.append(f'<a target="_blank" rel="noopener" href="./report_pdf/{html.escape(pdf)}">PDF</a>')
            parts.append(f'<a target="_blank" rel="noopener" href="./{html.escape(md)}">MD</a>')
            parts.append('</span>')
            parts.append('</div>')
            if full:
                parts.append(f'<p class="summary">{full}</p>')
                if len(r["summary"]) > 280:
                    parts.append('<span class="more">show more</span>')
            parts.append('</article>')
        parts.append('</section>')

    parts.append('<div class="empty" id="empty">No reports match this filter.</div>')

    # JS for search + category filter + show-more
    js = """
const q = document.getElementById('q');
const pills = document.querySelectorAll('#pills .pill');
const count = document.getElementById('count');
const empty = document.getElementById('empty');
const days = document.querySelectorAll('.day');
const entries = document.querySelectorAll('.entry');
let activeCat = '*';
function apply() {
  const term = (q.value || '').trim().toLowerCase();
  let shown = 0;
  entries.forEach(el => {
    const matchCat = activeCat === '*' || el.dataset.cat === activeCat;
    const matchText = !term || el.dataset.text.indexOf(term) !== -1;
    const visible = matchCat && matchText;
    el.style.display = visible ? '' : 'none';
    if (visible) shown++;
  });
  // Hide day groups with no visible entries
  days.forEach(d => {
    const anyVisible = Array.from(d.querySelectorAll('.entry')).some(e => e.style.display !== 'none');
    d.style.display = anyVisible ? '' : 'none';
  });
  count.textContent = shown + ' / ' + entries.length + ' reports';
  empty.style.display = shown === 0 ? 'block' : 'none';
}
q.addEventListener('input', apply);
pills.forEach(p => p.addEventListener('click', () => {
  pills.forEach(x => x.classList.remove('active'));
  p.classList.add('active');
  activeCat = p.dataset.cat;
  apply();
}));
document.addEventListener('click', (e) => {
  if (e.target.classList.contains('more')) {
    const s = e.target.previousElementSibling;
    s.classList.toggle('expanded');
    e.target.textContent = s.classList.contains('expanded') ? 'show less' : 'show more';
  }
});
"""
    parts.append(f"<script>{js}</script>")
    parts.append("</div></body></html>")

    with open("all_reports.html", "w") as fh:
        fh.write("\n".join(parts))
    print(f"Wrote all_reports.html — {len(records)} reports across {len(dates)} dates.")


if __name__ == "__main__":
    main()
