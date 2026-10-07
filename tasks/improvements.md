# Improvement Tasks — Awesome AI Architecture

Findings from a review of the repo and live site structure (`index.html`, `metadata.json`,
`articles/*.html`, `README.md`). Grouped by priority. Each task has a concrete
**done-when** so it can be picked up independently.

Legend: **P0** = broken/incorrect today · **P1** = high impact · **P2** = quality · **P3** = nice to have

---

## P0 — Broken or incorrect today

- [x] **T01 · Fix duplicate multi-model routing entries in `metadata.json`.**
  Entries `0001` and `0002` share the same `slug` *and* `path`
  (`articles/multi-model-routing-ai-gateway-tools-mapped-by-failure-mode.html`), so the
  homepage shows two cards that open the same page. The 2026 version (`0002`, window
  2026-02-05 → 2026-03-12) actually lives in `articles/00012-multi-model-routing-…html`,
  which is currently orphaned.
  *Done when:* each entry points to its own file with a unique slug (e.g. rename `00012-…`
  to `multi-model-routing-ai-gateway-tools-mapped-by-failure-mode-2026.html`), or the older
  one is retired with `"status": "archived"` and the newer one supersedes it.
  ✅ *Done (2026-10-07):* `00012-…html` renamed to `multi-model-routing-ai-gateway-tools-mapped-by-failure-mode-2026.html`; entries `0001` (2024 Edition) and `0002` (2026 Edition) now have unique slugs, paths and titles. No orphaned article files remain.

- [x] **T02 · Verify factual claims flagged during review.**
  `watchtower-and-moat.html` describes "Archon (OpenAI)" at `github.com/openai/archon` as a
  capability-based agent sandbox. Confirm the project exists, its owner, and the described
  features; if it can't be verified, remove or replace it. Run the same check over every
  tool and external link in the four essay articles (they have no Evidence Log).
  *Done when:* every named tool resolves to a real primary source, and each essay has an
  Evidence Log section.
  ✅ *Done (2026-10-07):* "Archon (OpenAI)" could not be verified — the real Archon is an unrelated YAML workflow engine by coleam00, and `github.com/openai/archon` is not an OpenAI capability sandbox. Replaced with Wasmtime (Bytecode Alliance), a verifiable capability-based runtime, in text, map, comparison table and citations. Also fixed Prompt Guard described as "~300M parameters" while linking the 86M model. Evidence Logs for the four older essays are still outstanding — tracked in new task T25.

- [x] **T03 · Normalise `metadata.json` schema.**
  The four essay entries lack `id`, `slug`, `format` and `research_window`; ids jump from
  `0003` to `0025`; tag casing is mixed (`"multi-model routing"` with a space vs.
  `multi-model-routing`).
  *Done when:* every entry has the same fields, ids are unique and sequential, all tags are
  lowercase kebab-case, and the fields match the schema in `docs/master-prompt-v1.md`.
  ✅ *Done (2026-10-07):* all 14 entries share one schema (`id`, `slug`, `title`, `hook`, `path`, `date`, `date_modified`, `status`, `format`, `tags`, `reading_time_minutes`, `pinned`, `research_window`); ids are unique and sequential `0001`–`0014` (cost-governance `0025` → `0004`); tags are kebab-case. Essays without a recorded research window use `null`. Added `site.updated`.

- [x] **T04 · Escape metadata when rendering cards in `index.html`.**
  `cardHTML()` interpolates `title`, `hook` and tags straight into `innerHTML`. A hook with a
  quote or `<` (the eval article's hook already contains `"…"`) can break the
  `data-search` attribute or inject markup.
  *Done when:* values are escaped (or nodes built with `textContent`) and a hook containing
  `"`, `<` and `&` renders correctly.
  ✅ *Done (2026-10-07):* `index.html` escapes every metadata value (`esc()`) and only links paths matching `articles/*.html` (`safePath()`); tags are now also searchable.

- [x] **T05 · Fix share links that point to the site root.**
  `smoke-signals-in-production.html` shares
  `https://iggym.github.io/awesome-ai-architecture/` instead of the article URL; check all
  articles for the same issue.
  *Done when:* every X/LinkedIn/copy action shares the article's own canonical URL.
  ✅ *Done (2026-10-07):* smoke-signals and watchtower share buttons now send the article URL; the copy actions in where-agents-break-free and where-the-sandbox-ends include the article URL. Other articles already used `window.location.href`.

## P1 — High impact

- [ ] **T06 · SEO and social metadata on every page.**
  Only 3 of 8 articles have `<meta name="description">`; none have `rel="canonical"`, Open
  Graph, Twitter cards or JSON-LD. `index.html` has none either.
  *Done when:* every page has description, canonical, OG, Twitter and (`TechArticle` /
  `WebSite`) JSON-LD, consistent with `metadata.json`.
  🟡 *Progress (2026-10-07):* the six new articles (0009–0014) ship with description, canonical, OG, Twitter and TechArticle JSON-LD. The eight older pages and `index.html` still need it.

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
  🟡 *Progress (2026-10-07):* `scripts/render_article.py` renders articles from `content/articles/*.json` with one shared token set (cream/teal/coral, Space Grotesk / Inter / IBM Plex Mono) and a dark mode. The six new articles use it; the eight older ones still have their own styles.

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
  🟡 *Progress (2026-10-07):* new articles use `<button aria-pressed>` filter chips, visible focus styles and AA-checked dark-mode colours. Homepage chips are still `<span>`s.

- [ ] **T14 · Static, indexable tool cards.** `multi-model-routing-…html` renders its tools
  from a JS template (`${tool.name}`), so crawlers and no-JS readers see nothing.
  *Done when:* tool cards are in the static HTML.
  🟡 *Progress (2026-10-07):* all new articles render tool cards as static HTML (verified with JavaScript disabled). The 2024 routing article still renders from a JS template.

- [ ] **T15 · Homepage UX upgrades.** Show the format (reference/essay) on cards and allow
  filtering by it; collapse the tag cloud (20+ chips) behind "more"; sync the active
  filter/search to the URL (`?tag=…&q=…`) so filtered views are shareable; add
  "last updated" from `metadata.json`.

- [ ] **T16 · Date hygiene.** Essay dates (2025-04-14 ×3) look like batch placeholders and
  the oldest routing article is dated 2024 while referencing current tools. Add a
  `date_modified` field and show "Updated <date>" on pages that have been revised.

- [ ] **T17 · Article cross-linking.** Add "Related articles" (by shared tags) at the end of
  each article, e.g. the three agent-security essays should link to each other.
  🟡 *Progress (2026-10-07):* new articles include a "Related on Awesome AI Architecture" section; older articles do not yet.

- [ ] **T18 · Consolidate overlapping security essays.** *Watchtower and Moat*,
  *Where the Sandbox Ends* and *Where Agents Break Free* make the same LLM-layer vs. runtime
  argument with overlapping tools. Decide: merge into one canonical piece + redirects, or
  differentiate each (threat model / tooling reference / implementation guide).

## P3 — Content roadmap and process

- [ ] **T19 · Fill the README's promised categories** using `docs/master-prompt-v1.md`:
  vector & hybrid retrieval, GraphRAG & memory, inference engines, structured output &
  schema repair, MCP / tool-calling protocols, LLM observability & tracing, prompt-injection
  defenses, PII & data residency, semantic caching.
  🟡 *Progress (2026-10-07):* six of the promised categories now have articles: vector & hybrid retrieval, inference engines, structured output, document ingestion, agent memory (essay) and MCP / tool protocols (essay). Remaining: LLM observability & tracing, prompt-injection defenses, PII & data residency, semantic caching.

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

## Added 2026-10-07

- [ ] **T25 · Evidence Logs for the four older essays.** *Smoke Signals in Production*,
  *Watchtower and Moat*, *Where the Sandbox Ends* and *Where Agents Break Free* cite tools
  without a dated Evidence Log, and their tool facts date from early 2025 (e.g. Llama Guard 2
  and Prompt Guard 86M have newer successors). *Done when:* each essay has an Evidence Log
  and a refreshed "as of" date, or is consolidated per T18.

- [ ] **T26 · Migrate older articles onto the renderer.** Port the eight hand-built
  articles into `content/articles/*.json` so every page shares one template, metadata
  block and design system (closes most of T06, T09, T12–T14 and T17 in one move).
  *Done when:* `python3 scripts/render_article.py --all` produces every article.

- [ ] **T27 · Validate metadata in CI.** Turn the checks used during this change (unique
  `id`/`slug`/`path`, every `path` exists, no orphaned files, kebab-case tags) into
  `scripts/check_content.py` and run it from the T10 workflow.

