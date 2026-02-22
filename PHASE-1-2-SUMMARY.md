# Mintlify Docs Migration — Phase 1 & 2 Summary

**Date:** February 22, 2026
**Status:** Complete

---

## Phase 1: Repository Setup & Configuration

### What Was Done

1. **Cloned the `adspirer/docs` repo** to `/Users/a0m14pe/Documents/Adspirer-projects/adspirer-docs/`
2. **Created folder structure:**
   - `ai-clients/` — 6 AI client setup guides
   - `ad-platforms/` — 4 ad platform integration docs
   - `agent-skills/` — 3 skills documentation pages
   - `guides/` — 7 guide/pillar pages (placeholders for Phase 3)
   - `logo/` — Dark and light SVG logos + favicon
   - `snippets/` — Reusable MDX snippets
3. **Wrote `docs.json` configuration:**
   - Theme: maple (dark mode default)
   - Primary color: `#3B82F6` (Adspirer blue)
   - 2 navigation tabs: Documentation + Guides
   - 4 navigation groups: Getting Started, AI Clients, Ad Platforms, Agent Skills
   - Global anchors: Blog link + MCP Server link
   - Navbar: Pricing link + "Start Free Trial" CTA button
   - Footer: X, GitHub, LinkedIn social links
   - Contextual code options: copy, view, ChatGPT, Claude, Perplexity, MCP, Cursor, VS Code
4. **Copied logo assets** from main website repo (adspirer-logo-full.svg)
5. **Created introduction.mdx and quickstart.mdx** as new landing pages
6. **Added `.mintignore`** to exclude AGENTS.md from Mintlify builds
7. **Tested with `mint dev`** — all routes returned 200 OK

### Key Decisions

- **Separate repo architecture:** Docs live in `github.com/Adspirer/docs`, not in the main website codebase
- **Subpath approach:** Docs will be served at `adspirer.com/docs` via Vercel rewrites to Mintlify
- **Blog stays on main site:** 19 blog posts remain at `/blog/*` for SEO domain authority
- **Integration pages stay on main site:** Marketing/conversion pages at `/integrations/*` unchanged

---

## Phase 2: Documentation Page Migration (TSX → MDX)

### What Was Done

Converted all 14 documentation pages from Next.js TSX components to Mintlify MDX format.

### Converted Pages

| Page | Lines | Source |
|------|-------|--------|
| `ad-platforms/google-ads.mdx` | 325 | google-ads/page.tsx |
| `agent-skills/workflows.mdx` | 303 | skills/page.tsx (workflows section) |
| `ai-clients/openclaw.mdx` | 282 | openclaw/page.tsx |
| `ai-clients/cursor.mdx` | 276 | cursor/page.tsx |
| `ai-clients/codex.mdx` | 275 | codex/page.tsx |
| `ad-platforms/tiktok-ads.mdx` | 270 | tiktok-ads/page.tsx |
| `ad-platforms/linkedin-ads.mdx` | 262 | linkedin-ads/page.tsx |
| `ad-platforms/meta-ads.mdx` | 235 | meta-ads/page.tsx (gold standard) |
| `agent-skills/overview.mdx` | 219 | skills/page.tsx |
| `ai-clients/windsurf.mdx` | 213 | windsurf/page.tsx |
| `ai-clients/claude-code.mdx` | 210 | claude-code/page.tsx |
| `ai-clients/custom-gpt.mdx` | 175 | custom-gpt/page.tsx (expanded) |
| `agent-skills/tools.mdx` | 125 | skills/page.tsx (tools section) |
| `quickstart.mdx` | 60 | New content |
| `introduction.mdx` | 6 | New content |

**Total:** ~3,236 lines of documentation across 15 files.

### Conversion Approach

- **Gold standard template:** Meta Ads was converted first as the reference format
- **Parallel conversion:** AI client pages, ad platform pages, and skills pages converted simultaneously by multiple agents
- **Content enrichment:** Where source pages were thin (custom-gpt, google-ads), content was enhanced to match the quality of fully-developed pages

### Conversion Rules Applied

- All TSX/JSX stripped → Mintlify MDX components
- `<div className="bg-muted/20 ...">` → `<Note>`, `<Warning>`, `<Tip>`
- `<pre><code>` → Standard markdown code blocks
- `<table>` → Markdown pipe tables
- Internal links: `/documentation/X` → `/ai-clients/X`, `/ad-platforms/X`, `/agent-skills/X`
- External links: pricing → `https://www.adspirer.com/pricing`
- JSON-LD schemas removed (Mintlify handles SEO)
- Metadata export → MDX frontmatter (title, description)
- FAQ sections → `<AccordionGroup>` + `<Accordion>`
- Card layouts → `<CardGroup>` + `<Card>`

### Test Results

All 15 pages tested with `mint dev` and returned HTTP 200:

```
✓ /introduction
✓ /quickstart
✓ /ai-clients/claude-code
✓ /ai-clients/cursor
✓ /ai-clients/codex
✓ /ai-clients/openclaw
✓ /ai-clients/windsurf
✓ /ai-clients/custom-gpt
✓ /ad-platforms/google-ads
✓ /ad-platforms/meta-ads
✓ /ad-platforms/linkedin-ads
✓ /ad-platforms/tiktok-ads
✓ /agent-skills/overview
✓ /agent-skills/tools
✓ /agent-skills/workflows
```

---

## What's Next

### Phase 3: Migrate 7 Guide/Pillar Pages
- Extract content from `app/lib/pillar-data.ts` in the website repo
- Convert to MDX format in `guides/` directory
- These are longer-form SEO content pages

### Phase 4: Website Integration
- Create `vercel.json` with Mintlify rewrites
- Add 301 redirects from `/documentation/*` to `/docs/*`
- Add "Docs" link to website navbar
- Update sitemap.ts, robots.txt, llms.txt

### Phase 5: Verification & Launch
- End-to-end testing of `adspirer.com/docs`
- Verify llms.txt, sitemap.xml auto-generation
- Test 301 redirects
- Submit updated sitemap to Google Search Console

---

## Files Modified

### New files (adspirer-docs repo)
- `docs.json` — Mintlify configuration
- `introduction.mdx` — Docs landing page
- `quickstart.mdx` — Getting started guide
- `ai-clients/*.mdx` — 6 AI client setup guides
- `ad-platforms/*.mdx` — 4 ad platform integration docs
- `agent-skills/*.mdx` — 3 skills documentation pages
- `logo/dark.svg`, `logo/light.svg`, `favicon.svg` — Brand assets
- `.mintignore` — Build exclusions

### Unchanged
- Main website repo (`website-v3-claude-code/`) — No changes yet (Phase 4)
- Blog posts — Staying on main site
- Integration pages — Staying on main site
