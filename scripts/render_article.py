#!/usr/bin/env python3
"""Render an article content file (content/articles/<slug>.json) into a
self-contained HTML page under articles/, following docs/master-prompt-v1.md.

Usage:
  python3 scripts/render_article.py content/articles/<slug>.json [...]
  python3 scripts/render_article.py --all            # render every content file
  python3 scripts/render_article.py --all --update-metadata

No dependencies beyond the Python 3 standard library. Body strings in content
files may contain a small amount of trusted inline HTML (<em>, <code>, <strong>, <a>).
"""
import html
import json
import math
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BASE_URL = "https://iggym.github.io/awesome-ai-architecture/"
SITE = "Awesome AI Architecture"
FONTS = ("https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;700"
         "&family=Inter:wght@400;500&family=IBM+Plex+Mono:wght@400;500&display=swap")
WORDS_PER_MINUTE = 230

e = html.escape


def attr(s):
    return html.escape(str(s), quote=True)


def mon_year(iso):
    months = "Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec".split()
    y, m, _ = iso.split("-")
    return f"{months[int(m) - 1]} {y}"


def ext_link(name, url):
    return (f'<a href="{attr(url)}" target="_blank" rel="noopener noreferrer">{e(name)}</a>')


def strip_url(url):
    return re.sub(r"^https?://(www\.)?", "", url).rstrip("/")


CSS = """
:root{
  --cream:#FAF6EE; --ink:#1F2421; --teal:#1F7A6C; --coral:#C4502B; --muted:#6F6A5E;
  --surface:#FFFFFF; --border:rgba(31,36,33,0.14); --soft:#4B4738; --teal-soft:rgba(31,122,108,0.10);
  --display:'Space Grotesk',sans-serif; --body:'Inter',sans-serif; --mono:'IBM Plex Mono',monospace;
}
@media (prefers-color-scheme: dark){
  :root{ --cream:#121412; --ink:#E9E6DF; --teal:#4FB8A6; --coral:#F08A63; --muted:#A39F94;
    --surface:#1A1D1B; --border:rgba(233,230,223,0.14); --soft:#CFCAC0; --teal-soft:rgba(79,184,166,0.14); }
}
*{box-sizing:border-box}
html{scroll-behavior:smooth}
@media (prefers-reduced-motion: reduce){ html{scroll-behavior:auto} *{animation-duration:.001ms!important;transition-duration:.001ms!important} }
body{margin:0;background:var(--cream);color:var(--ink);font-family:var(--body);line-height:1.65;font-size:16px}
a{color:var(--teal)}
a:focus-visible,button:focus-visible{outline:2px solid var(--coral);outline-offset:2px}
code{font-family:var(--mono);font-size:.88em;background:var(--teal-soft);padding:1px 5px;border-radius:4px}
.topbar{position:sticky;top:0;z-index:20;background:var(--cream);border-bottom:1px solid var(--border);padding:12px 16px;display:flex;gap:16px;align-items:center;justify-content:space-between}
.topbar a.home{font-family:var(--display);font-weight:700;font-size:14px;text-decoration:none;color:var(--ink);white-space:nowrap}
.toc{display:flex;gap:14px;overflow-x:auto;font-family:var(--mono);font-size:12px;scrollbar-width:none}
.toc a{color:var(--muted);text-decoration:none;white-space:nowrap}
.toc a:hover{color:var(--teal)}
header.hero,.wrap{max-width:760px;margin:0 auto;padding:0 16px}
header.hero{padding-top:56px}
.meta-line{font-family:var(--mono);font-size:11.5px;letter-spacing:.08em;text-transform:uppercase;color:var(--teal);margin-bottom:14px}
h1{font-family:var(--display);font-weight:700;font-size:clamp(2rem,5vw,3rem);line-height:1.12;margin:0 0 16px;letter-spacing:-.01em}
.standfirst{font-size:1.12rem;color:var(--soft);margin:0 0 8px}
.tags{display:flex;gap:6px;flex-wrap:wrap;margin:18px 0 0;padding:0;list-style:none}
.tags li{font-family:var(--mono);font-size:10.5px;color:var(--teal);border:1px solid var(--border);padding:3px 9px;border-radius:20px}
section{margin:52px 0}
h2{font-family:var(--display);font-weight:700;font-size:1.5rem;line-height:1.25;margin:0 0 14px}
h3{font-family:var(--display);font-weight:700;font-size:1.1rem;margin:0 0 6px}
p{margin:0 0 14px}
.callout{background:var(--surface);border:1px solid var(--border);border-left:4px solid var(--coral);border-radius:8px;padding:20px 22px}
.callout h2{font-size:1.2rem}
.callout ul{margin:0 0 14px;padding-left:20px}
.callout li{margin-bottom:8px}
.bar{font-weight:500}
.chips{display:flex;gap:8px;flex-wrap:wrap;margin:0 0 8px}
.chip{font-family:var(--mono);font-size:11.5px;padding:6px 14px;border-radius:20px;border:1px solid var(--border);background:var(--surface);color:var(--ink);cursor:pointer}
.chip:hover{border-color:var(--teal)}
.chip[aria-pressed="true"]{background:var(--teal);border-color:var(--teal);color:var(--cream)}
.search{font-family:var(--mono);font-size:12.5px;border:1px solid var(--border);background:var(--surface);color:var(--ink);padding:7px 12px;border-radius:20px;width:100%;max-width:300px;margin-top:8px}
.cards{display:grid;gap:14px;margin-top:18px}
.card{background:var(--surface);border:1px solid var(--border);border-radius:8px;padding:18px 20px;transition:border-color .2s ease}
.card:hover{border-color:var(--teal)}
.card[hidden]{display:none}
.card .label{font-family:var(--mono);font-size:10.5px;color:var(--muted);text-transform:uppercase;letter-spacing:.06em;margin-bottom:6px}
.card h3 a{color:var(--ink);text-decoration:none;border-bottom:1px solid var(--teal)}
.card p{font-size:14.5px;color:var(--soft);margin:6px 0 0}
.card .limit{font-size:13.5px;color:var(--muted)}
.card .limit strong{color:var(--coral);font-weight:500}
.strip{display:grid;grid-template-columns:1fr 1fr;gap:12px;margin:28px 0 0}
.strip div{background:var(--surface);border:1px solid var(--border);border-radius:8px;padding:14px 16px;font-size:14px}
.strip .k{font-family:var(--mono);font-size:10.5px;text-transform:uppercase;letter-spacing:.06em;display:block;margin-bottom:4px}
.strip .legacy .k{color:var(--muted)} .strip .modern{border-color:var(--teal)} .strip .modern .k{color:var(--teal)}
.matrix{list-style:none;padding:0;margin:0}
.matrix li{border-top:1px solid var(--border);padding:12px 0}
.matrix li strong{font-family:var(--display)}
.move{background:var(--teal);color:var(--cream);border-radius:8px;padding:20px 22px}
.move h2{color:var(--cream)}
.stack{display:grid;gap:10px;margin-top:16px}
.layer{background:var(--surface);border:1px solid var(--border);border-radius:8px;padding:12px 14px}
.layer[hidden]{display:none}
.layer .lname{font-family:var(--mono);font-size:11px;text-transform:uppercase;letter-spacing:.06em;color:var(--teal);margin-bottom:8px}
.layer .ltools{display:flex;gap:8px;flex-wrap:wrap}
.layer .ltools span{font-family:var(--display);font-size:13.5px;border:1px solid var(--border);border-radius:6px;padding:4px 10px}
.table-wrap{overflow-x:auto;border:1px solid var(--border);border-radius:8px;background:var(--surface)}
table{border-collapse:collapse;width:100%;font-size:13.5px;min-width:620px}
th,td{text-align:left;padding:10px 12px;border-bottom:1px solid var(--border);vertical-align:top}
th{font-family:var(--mono);font-size:11px;text-transform:uppercase;letter-spacing:.05em;color:var(--muted)}
tr:last-child td{border-bottom:0}
.reframe{font-family:var(--display);font-weight:700;font-size:1.35rem;line-height:1.35;border-left:4px solid var(--teal);padding-left:18px;margin:0 0 18px}
.share-actions{display:flex;gap:8px;flex-wrap:wrap}
.btn{font-family:var(--mono);font-size:12px;padding:8px 14px;border-radius:20px;border:1px solid var(--teal);background:var(--surface);color:var(--teal);cursor:pointer;text-decoration:none}
.btn.primary{background:var(--teal);color:var(--cream)}
.toast{font-family:var(--mono);font-size:12px;color:var(--teal);margin-left:6px;opacity:0;transition:opacity .2s ease}
.toast.show{opacity:1}
.evidence{list-style:none;padding:0;margin:0;font-family:var(--mono);font-size:12px;color:var(--soft)}
.evidence li{border-top:1px solid var(--border);padding:10px 0;overflow-wrap:anywhere}
.evidence strong{font-family:var(--display);font-size:14px;color:var(--ink)}
.related{list-style:none;padding:0;margin:0;display:grid;gap:8px}
.related a{font-family:var(--display);text-decoration:none}
footer{border-top:1px solid var(--border);margin-top:64px;padding:28px 16px;text-align:center;font-family:var(--mono);font-size:12px}
footer a{margin:0 10px;text-decoration:none}
@media (max-width:560px){ .strip{grid-template-columns:1fr} .toc{display:none} }
"""

JS = """
(function(){
  var chips = document.querySelectorAll('[data-filter]');
  var cards = document.querySelectorAll('[data-mode]');
  var search = document.getElementById('tool-search');
  var active = '';
  function apply(){
    var q = search ? search.value.trim().toLowerCase() : '';
    cards.forEach(function(c){
      var okMode = !active || c.getAttribute('data-mode') === active;
      var okQ = !q || c.textContent.toLowerCase().indexOf(q) !== -1;
      c.hidden = !(okMode && okQ);
    });
    document.querySelectorAll('[data-mode-section]').forEach(function(s){
      s.hidden = !!active && s.getAttribute('data-mode-section') !== active;
    });
  }
  chips.forEach(function(chip){
    chip.addEventListener('click', function(){
      active = chip.getAttribute('data-filter');
      chips.forEach(function(c){ c.setAttribute('aria-pressed', String(c === chip)); });
      apply();
    });
  });
  if (search) search.addEventListener('input', apply);

  var copyBtn = document.getElementById('copy-share');
  var toast = document.getElementById('copy-toast');
  if (copyBtn) copyBtn.addEventListener('click', function(){
    var text = copyBtn.getAttribute('data-text');
    function done(){ toast.classList.add('show'); setTimeout(function(){ toast.classList.remove('show'); }, 1800); }
    if (navigator.clipboard && navigator.clipboard.writeText) { navigator.clipboard.writeText(text).then(done, function(){}); }
    else { var t = document.createElement('textarea'); t.value = text; document.body.appendChild(t); t.select();
      try { document.execCommand('copy'); done(); } catch (err) {} document.body.removeChild(t); }
  });
})();
"""


def head(a, url, title_tag):
    ld = {
        "@context": "https://schema.org",
        "@type": "TechArticle",
        "headline": a["title"],
        "description": a["description"],
        "datePublished": a["date"],
        "dateModified": a.get("date_modified", a["date"]),
        "author": {"@type": "Person", "name": "iggym", "url": "https://github.com/iggym"},
        "publisher": {"@type": "Organization", "name": SITE, "url": BASE_URL},
        "url": url,
        "mainEntityOfPage": url,
        "keywords": ", ".join(a["tags"]),
        "isPartOf": {"@type": "WebSite", "name": SITE, "url": BASE_URL},
    }
    tags_meta = "\n".join(f'<meta property="article:tag" content="{attr(t)}">' for t in a["tags"])
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{e(title_tag)}</title>
<meta name="description" content="{attr(a['description'])}">
<meta name="author" content="iggym">
<link rel="canonical" href="{attr(url)}">
<meta property="og:type" content="article">
<meta property="og:site_name" content="{SITE}">
<meta property="og:title" content="{attr(a['title'])}">
<meta property="og:description" content="{attr(a['description'])}">
<meta property="og:url" content="{attr(url)}">
<meta property="article:published_time" content="{attr(a['date'])}">
{tags_meta}
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{attr(a['title'])}">
<meta name="twitter:description" content="{attr(a['description'])}">
<meta name="color-scheme" content="light dark">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="{FONTS}" rel="stylesheet">
<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>
<style>{CSS}</style>
</head>
<body>
"""


def topbar(nav):
    links = "".join(f'<a href="#{attr(i)}">{e(t)}</a>' for i, t in nav)
    return (f'<nav class="topbar" aria-label="Article sections">'
            f'<a class="home" href="../">← {SITE}</a><div class="toc">{links}</div></nav>\n')


def exclusions_block(a):
    x = a["exclusions"]
    items = "".join(f"<li><strong>{e(i['name'])}.</strong> {i['reason']}</li>" for i in x["items"])
    intro = f"<p>{x['intro']}</p>" if x.get("intro") else ""
    heading = "Exclusion Criteria — Read First" if a["format"] == "reference" else "What Got Cut"
    return (f'<section id="preamble" class="callout"><h2>{heading}</h2>{intro}'
            f'<ul>{items}</ul><p class="bar"><strong>Inclusion bar:</strong> {x["bar"]}</p></section>')


def tool_card(t, mode_key, mode_label):
    limit = f'<p class="limit"><strong>Limit:</strong> {t["limit"]}</p>' if t.get("limit") else ""
    org = f' <span class="label" style="display:inline">· {e(t["org"])}</span>' if t.get("org") else ""
    return (f'<article class="card" data-mode="{attr(mode_key)}">'
            f'<div class="label">{e(mode_label)}</div>'
            f'<h3>{ext_link(t["name"], t["url"])}{org}</h3>'
            f'<p>{t["fit"]}</p>{limit}</article>')


def share_block(a, url):
    text = f'{a["hook"]} — {url}'
    tw = ("https://twitter.com/intent/tweet?text=" + _q(a["hook"]) + "&url=" + _q(url))
    li = "https://www.linkedin.com/sharing/share-offsite/?url=" + _q(url)
    return (f'<section id="share"><h2>Bold Reframe</h2><p class="reframe">{e(a["hook"])}</p>'
            f'<div class="share-actions">'
            f'<button type="button" class="btn primary" id="copy-share" data-text="{attr(text)}">Copy Text &amp; Link</button>'
            f'<a class="btn" href="{attr(tw)}" target="_blank" rel="noopener noreferrer">Share on X</a>'
            f'<a class="btn" href="{attr(li)}" target="_blank" rel="noopener noreferrer">Share on LinkedIn</a>'
            f'<span class="toast" id="copy-toast" role="status" aria-live="polite">Copied to clipboard</span>'
            f'</div></section>')


def _q(s):
    from urllib.parse import quote
    return quote(s, safe="")


def evidence_block(a):
    rows = "".join(
        f'<li><strong>{e(r["name"])}</strong> — {ext_link(strip_url(r["url"]), r["url"])}'
        f' · query: "{e(r["query"])}" · {e(r["signal"])}</li>' for r in a["evidence"])
    note = (f'<p>Verified {e(a["research_window"][0])} → {e(a["research_window"][1])}. '
            f'Release dates are from each project\'s package registry (PyPI) unless noted.</p>')
    return f'<section id="evidence"><h2>Evidence Log &amp; Citations</h2>{note}<ul class="evidence">{rows}</ul></section>'


def missing_block(a):
    return (f'<section id="missing"><h2>What\'s Still Missing (as of {mon_year(a["date"])})</h2>'
            f'<p>{a["missing"]}</p></section>')


def related_block(a, all_meta):
    by_slug = {m.get("slug"): m for m in all_meta}
    items = []
    for s in a.get("related", []):
        m = by_slug.get(s)
        if m:
            href = "./" + m["path"].split("/", 1)[1]
            items.append(f'<li><a href="{attr(href)}">{e(m["title"])}</a></li>')
    if not items:
        return ""
    return f'<section id="related"><h2>Related on {SITE}</h2><ul class="related">{"".join(items)}</ul></section>'


def footer():
    return ('<footer><a href="../">← Back to awesome-ai-architecture</a>'
            '<a href="#top">↑ Scroll to top</a></footer>\n')


def render_reference(a, all_meta):
    url = f'{BASE_URL}articles/{a["slug"]}.html'
    modes = a["failure_modes"]
    nav = [("preamble", "Exclusions")] + [(f'cat-{m["key"]}', m["short"]) for m in modes] + \
          ([("choose", "How to Choose")] if a.get("choose") else []) + [("share", "Share"), ("evidence", "Evidence")]
    win = a["research_window"]
    out = [head(a, url, f'{a["title"]} — {SITE}'), topbar(nav), '<main id="top">']
    out.append(f'<header class="hero"><div class="meta-line">Reference · {e(a["date"])} · Window: '
               f'{e(win[0])} → {e(win[1])} · {a["reading_time_minutes"]} min</div>'
               f'<h1>{e(a["title"])}</h1><p class="standfirst">{a["standfirst"]}</p>'
               f'<ul class="tags">{"".join(f"<li>{e(t)}</li>" for t in a["tags"])}</ul></header>')
    out.append('<div class="wrap">')
    out.append(exclusions_block(a))
    chips = '<button type="button" class="chip" data-filter="" aria-pressed="true">All Tools</button>' + "".join(
        f'<button type="button" class="chip" data-filter="{attr(m["key"])}" aria-pressed="false">{e(m["short"])}</button>'
        for m in modes)
    out.append(f'<section aria-label="Filter tools" style="margin-bottom:0"><div class="chips">{chips}</div>'
               f'<label class="sr" for="tool-search" style="position:absolute;left:-9999px">Filter tools</label>'
               f'<input class="search" id="tool-search" type="search" placeholder="filter tools by keyword…"></section>')
    for m in modes:
        cards = "".join(tool_card(t, m["key"], m["short"]) for t in m["tools"])
        out.append(f'<section id="cat-{attr(m["key"])}" data-mode-section="{attr(m["key"])}">'
                   f'<h2>{e(m["title"])}</h2><p>{m["body"]}</p><div class="cards">{cards}</div></section>')
    if a.get("choose"):
        out.append('<section id="choose"><h2>How to Choose</h2>' + "".join(f"<p>{p}</p>" for p in a["choose"]) + '</section>')
    out.append(share_block(a, url))
    out.append(evidence_block(a))
    out.append(missing_block(a))
    out.append(related_block(a, all_meta))
    out.append('</div></main>')
    out.append(footer())
    out.append(f'<script>{JS}</script>\n</body>\n</html>\n')
    return "".join(out)


def render_essay(a, all_meta):
    url = f'{BASE_URL}articles/{a["slug"]}.html'
    nav = [("problem", "The Problem"), ("preamble", "What Got Cut"), ("taxonomy", "Taxonomy"),
           ("land", "Where to Land"), ("move", "One Move"), ("stack", "Stack"),
           ("compare", "Compare"), ("evidence", "Evidence")]
    out = [head(a, url, f'{a["title"]} — {SITE}'), topbar(nav), '<main id="top">']
    win = a["research_window"]
    mat = a["maturity"]
    out.append(f'<header class="hero"><div class="meta-line">Essay · {e(a["eyebrow"])} · {e(a["date"])} · '
               f'{a["reading_time_minutes"]} min</div><h1>{e(a["title"])}</h1>'
               f'<p class="standfirst">{a["standfirst"]}</p>'
               f'<div class="strip"><div class="legacy"><span class="k">Legacy</span>{mat["legacy"]}</div>'
               f'<div class="modern"><span class="k">Modern</span>{mat["modern"]}</div></div>'
               f'<ul class="tags">{"".join(f"<li>{e(t)}</li>" for t in a["tags"])}</ul></header>')
    out.append('<div class="wrap">')
    out.append('<section id="problem"><h2>The Real Problem</h2>' + "".join(f"<p>{p}</p>" for p in a["problem"]) + '</section>')
    out.append(exclusions_block(a))
    tax = ['<section id="taxonomy"><h2>' + e(a.get("taxonomy_title", "The Taxonomy")) + '</h2>']
    for p in a.get("taxonomy_intro", []):
        tax.append(f"<p>{p}</p>")
    for L in a["layers"]:
        tax.append(f'<h3 style="font-size:1.25rem;margin-top:30px">{e(L["name"])}</h3><p>{L["intro"]}</p><div class="cards">')
        for t in L["tools"]:
            tax.append(tool_card(t, L["key"], L["name"]))
        tax.append('</div>')
    tax.append('</section>')
    out.append("".join(tax))
    rules = "".join(f'<li><strong>{e(r["if"])}</strong> → {r["then"]}</li>' for r in a["matrix"])
    out.append(f'<section id="land"><h2>Where to Land</h2>' + "".join(f"<p>{p}</p>" for p in a["land"]) +
               f'<ul class="matrix">{rules}</ul></section>')
    out.append(f'<section id="move" class="move"><h2>One Move</h2><p style="margin:0">{a["move"]}</p></section>')
    chips = '<button type="button" class="chip" data-filter="" aria-pressed="true">All Layers</button>' + "".join(
        f'<button type="button" class="chip" data-filter="{attr(L["key"])}" aria-pressed="false">{e(L["name"])}</button>'
        for L in a["layers"])
    layers = "".join(
        f'<div class="layer" data-mode="{attr(L["key"])}"><div class="lname">{e(L["name"])}</div>'
        f'<div class="ltools">{"".join(f"<span>{e(t["name"])}</span>" for t in L["tools"])}</div></div>'
        for L in a["layers"])
    out.append(f'<section id="stack"><h2>State of the Stack</h2><p>Where each tool sits. Filter by layer.</p>'
               f'<div class="chips">{chips}</div><div class="stack">{layers}</div></section>')
    cols = a["comparison"]["columns"]
    thead = "".join(f'<th scope="col">{e(c)}</th>' for c in cols)
    tbody = "".join("<tr>" + "".join(f"<td>{c}</td>" for c in row) + "</tr>" for row in a["comparison"]["rows"])
    out.append(f'<section id="compare"><h2>Tool Comparison</h2><div class="table-wrap"><table>'
               f'<thead><tr>{thead}</tr></thead><tbody>{tbody}</tbody></table></div></section>')
    out.append(share_block(a, url))
    out.append(evidence_block(a))
    out.append(missing_block(a))
    out.append(related_block(a, all_meta))
    out.append('</div></main>')
    out.append(footer())
    out.append(f'<script>{JS}</script>\n</body>\n</html>\n')
    return "".join(out)


def body_words(a):
    """Word count of the reader-facing prose (excludes nav, evidence and chrome)."""
    parts = [a["standfirst"], a["hook"], a["missing"], a["exclusions"].get("intro", ""), a["exclusions"]["bar"]]
    parts += [i["reason"] for i in a["exclusions"]["items"]]
    if a["format"] == "reference":
        for m in a["failure_modes"]:
            parts += [m["title"], m["body"]] + [t["fit"] + " " + t.get("limit", "") for t in m["tools"]]
        parts += a.get("choose", [])
    else:
        parts += a["problem"] + a["land"] + [a["move"]] + a.get("taxonomy_intro", [])
        parts += [r["if"] + " " + r["then"] for r in a["matrix"]]
        for L in a["layers"]:
            parts += [L["intro"]] + [t["fit"] + " " + t.get("limit", "") for t in L["tools"]]
    text = re.sub(r"<[^>]+>", " ", " ".join(parts))
    return len(text.split())


def metadata_entry(a):
    return {
        "id": a["id"],
        "slug": a["slug"],
        "title": a["title"],
        "hook": a["hook"],
        "path": f'articles/{a["slug"]}.html',
        "date": a["date"],
        "date_modified": a.get("date_modified", a["date"]),
        "status": "published",
        "format": a["format"],
        "tags": a["tags"],
        "reading_time_minutes": a["reading_time_minutes"],
        "pinned": a.get("pinned", False),
        "research_window": f'{a["research_window"][0]} to {a["research_window"][1]}',
    }


def main(argv):
    update = "--update-metadata" in argv
    files = [Path(p) for p in argv if not p.startswith("--")]
    if "--all" in argv:
        files = sorted((ROOT / "content" / "articles").glob("*.json"))
    if not files:
        print(__doc__)
        return 1
    meta_path = ROOT / "metadata.json"
    meta = json.loads(meta_path.read_text())
    articles = [json.loads(Path(f).read_text()) for f in files]
    for a in articles:
        a["reading_time_minutes"] = max(1, math.ceil(body_words(a) / WORDS_PER_MINUTE))
    if update:
        by_slug = {m.get("slug"): i for i, m in enumerate(meta["articles"])}
        for a in articles:
            entry = metadata_entry(a)
            if a["slug"] in by_slug:
                meta["articles"][by_slug[a["slug"]]] = entry
            else:
                meta["articles"].append(entry)
        meta_path.write_text(json.dumps(meta, indent=2, ensure_ascii=False) + "\n")
    for a in articles:
        render = render_reference if a["format"] == "reference" else render_essay
        out = ROOT / "articles" / f'{a["slug"]}.html'
        out.write_text(render(a, meta["articles"]))
        print(f'{out.relative_to(ROOT)}  {body_words(a)} words  {a["reading_time_minutes"]} min')
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
