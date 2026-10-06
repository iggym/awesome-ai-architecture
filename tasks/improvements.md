# Improvement Tasks — Awesome AI Architecture

Findings from a review of the repo and live site structure (`index.html`, `metadata.json`,
`articles/*.html`, `README.md`). Grouped by priority. Each task has a concrete
**done-when** so it can be picked up independently.

Legend: **P0** = broken/incorrect today · **P1** = high impact · **P2** = quality · **P3** = nice to have

---

## P0 — Broken or incorrect today

- [ ] **T01 · Fix duplicate multi-model routing entries in `metadata.json`.**
  Entries `0001` and `0002` share the same `slug` *and* `path`
  (`articles/multi-model-routing-ai-gateway-tools-mapped-by-failure-mode.html`), so the
  homepage shows two cards that open the same page. The 2026 version (`0002`, window
  2026-02-05 → 2026-03-12) actually lives in `articles/00012-multi-model-routing-…html`,
  which is currently orphaned.
  *Done when:* each entry points to its own file with a unique slug (e.g. rename `00012-…`
  to `multi-model-routing-ai-gateway-tools-mapped-by-failure-mode-2026.html`), or the older
  one is retired with `"status": "archived"` and the newer one supersedes it.

- [ ] **T02 · Verify factual claims flagged during review.**
  `watchtower-and-moat.html` describes "Archon (OpenAI)" at `github.com/openai/archon` as a
  capability-based agent sandbox. Confirm the project exists, its owner, and the described
  features; if it can't be verified, remove or replace it. Run the same check over every
  tool and external link in the four essay articles (they have no Evidence Log).
  *Done when:* every named tool resolves to a real primary source, and each essay has an
  Evidence Log section.

- [ ] **T03 · Normalise `metadata.json` schema.**
  The four essay entries lack `id`, `slug`, `format` and `research_window`; ids jump from
  `0003` to `0025`; tag casing is mixed (`"multi-model routing"` with a space vs.
  `multi-model-routing`).
  *Done when:* every entry has the same fields, ids are unique and sequential, all tags are
  lowercase kebab-case, and the fields match the schema in `docs/master-prompt-v1.md`.

- [ ] **T04 · Escape metadata when rendering cards in `index.html`.**
  `cardHTML()` interpolates `title`, `hook` and tags straight into `innerHTML`. A hook with a
  quote or `<` (the eval article's hook already contains `"…"`) can break the
  `data-search` attribute or inject markup.
  *Done when:* values are escaped (or nodes built with `textContent`) and a hook containing
  `"`, `<` and `&` renders correctly.

- [ ] **T05 · Fix share links that point to the site root.**
  `smoke-signals-in-production.html` shares
  `https://iggym.github.io/awesome-ai-architecture/` instead of the article URL; check all
  articles for the same issue.
  *Done when:* every X/LinkedIn/copy action shares the article's own canonical URL.

## P1 — High impact

- [ ] **T06 · SEO and social metadata on every page.**
  Only 3 of 8 articles have `<meta name="description">`; none have `rel="canonical"`, Open
  Graph, Twitter cards or JSON-LD. `index.html` has none either.
  *Done when:* every page has description, canonical, OG, Twitter and (`TechArticle` /
  `WebSite`) JSON-LD, consistent with `metadata.json`.

- [ ] **T07 · Add `sitemap.xml`, `robots.txt`, RSS/Atom feed and a social preview image.**
  The site's stated audience includes SEO; there is nothing for crawlers or feed readers.
  *Done when:* `sitemap.xml` lists all published pages with `lastmod`, `robots.txt`
  references it, `feed.xml` lists articles, and a 1200×630 `og-image.png` exists.

- [ ] **T08 · Make the homepage indexable without JavaScript.**
  The feed is rendered client-side from `metadata.json`; with JS off (and for some crawlers)
  the index is empty and says "Index is empty."
  *Done when:* a small build script (e.g. `scripts/build.py`, no dependencies) pre-renders
  the cards into `index.html` (and generates sitemap/feed from T07), with JS kept only for
  filtering and search.

- [ ] **T09 · Unify the visual design system across articles.**
  Each article uses its own palette and fonts (Space Grotesk; Inter + JetBrains Mono;
  Libre Baskerville + DM Sans; Source Serif; a dark theme) and one loads Font Awesome from a
  CDN. Readers moving from the cream/teal homepage get a different site each click.
  *Done when:* a shared `assets/site.css` (tokens from `index.html`) is used by all pages,
  with a dark-mode variant; Font Awesome is replaced with inline SVG.

- [ ] **T10 · Add a CI workflow for content checks.**
  *Done when:* a GitHub Action runs on PRs and fails on: invalid `metadata.json`, duplicate
  `id`/`slug`/`path`, `path` pointing to a missing file, orphaned article files, HTML
  validation errors, missing required meta tags, and broken links (e.g. `lychee`).

- [ ] **T11 · Rewrite the README to match the site.**
  The README promises categories (Inference Engines, Retrieval & Memory, MCP…) that have no
  articles, contains a malformed clone command
  (`git clone [https://…](https://…)` won't run), and an inline SVG that GitHub strips
  from Markdown. It doesn't list the actual articles.
  *Done when:* README has a working clone command, an article index (generated from
  `metadata.json`), the failure-mode curation philosophy, and a link to
  `docs/master-prompt-v1.md`; the diagram is committed as an `.svg` file and referenced as
  an image.

## P2 — Quality and consistency

- [ ] **T12 · Consistent article chrome.** Same top bar, breadcrumb, meta line
  (format · date · research window · reading time), footer and relative back link (`../`)
  on every article. *Done when:* all 8 articles share the same header/footer markup.

- [ ] **T13 · Accessibility pass.** Filter chips on the homepage are `<span>`s with click
  handlers (not keyboard-reachable); tag pills are nested inside the card `<a>`; no visible
  focus styles; contrast of `--muted` on cream should be checked.
  *Done when:* chips are `<button aria-pressed>`, cards don't nest interactive elements,
  focus is visible, and Lighthouse accessibility ≥ 95 on every page.

- [ ] **T14 · Static, indexable tool cards.** `multi-model-routing-…html` renders its tools
  from a JS template (`${tool.name}`), so crawlers and no-JS readers see nothing.
  *Done when:* tool cards are in the static HTML.

- [ ] **T15 · Homepage UX upgrades.** Show the format (reference/essay) on cards and allow
  filtering by it; collapse the tag cloud (20+ chips) behind "more"; sync the active
  filter/search to the URL (`?tag=…&q=…`) so filtered views are shareable; add
  "last updated" from `metadata.json`.

- [ ] **T16 · Date hygiene.** Essay dates (2025-04-14 ×3) look like batch placeholders and
  the oldest routing article is dated 2024 while referencing current tools. Add a
  `date_modified` field and show "Updated <date>" on pages that have been revised.

- [ ] **T17 · Article cross-linking.** Add "Related articles" (by shared tags) at the end of
  each article, e.g. the three agent-security essays should link to each other.

- [ ] **T18 · Consolidate overlapping security essays.** *Watchtower and Moat*,
  *Where the Sandbox Ends* and *Where Agents Break Free* make the same LLM-layer vs. runtime
  argument with overlapping tools. Decide: merge into one canonical piece + redirects, or
  differentiate each (threat model / tooling reference / implementation guide).

## P3 — Content roadmap and process

- [ ] **T19 · Fill the README's promised categories** using `docs/master-prompt-v1.md`:
  vector & hybrid retrieval, GraphRAG & memory, inference engines, structured output &
  schema repair, MCP / tool-calling protocols, LLM observability & tracing, prompt-injection
  defenses, PII & data residency, semantic caching.

- [ ] **T20 · Add contribution scaffolding.** `CONTRIBUTING.md` (inclusion bar, how to
  propose a tool, how to use the master prompt), an issue template "Suggest a tool / failure
  mode", and a PR template with the editor checklist from the master prompt.

- [ ] **T21 · Freshness review cadence.** Each reference has a research window; add a
  quarterly task to re-verify tools, update "What's Still Missing", and bump
  `date_modified`. Flag articles whose window is older than 6 months on the homepage.

- [ ] **T22 · Lightweight analytics (privacy-friendly).** Add a cookie-less analytics
  snippet (e.g. GoatCounter/Plausible) to see which failure modes readers care about and
  prioritise T19 accordingly.

- [ ] **T23 · Footer copy.** The footer says this is "the reference layer of an eight-repo
  portfolio" but links to none of the other repos. Either link them or drop the claim.

- [ ] **T24 · Tidy `.gitignore`.** It's the default Node template; the repo has no Node
  tooling. Replace with a short list relevant to a static site (`.DS_Store`, editor files,
  any build output from T08).
