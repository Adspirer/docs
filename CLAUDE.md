# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Adspirer documentation site built on **Mintlify**. Content-only project (no package.json, no build pipeline). 33 MDX pages documenting an MCP server that connects AI assistants to advertising platforms (Google Ads, Meta Ads, LinkedIn Ads, TikTok Ads).

## Mintlify CLI Commands

```bash
# Install CLI
npm i -g mint

# Local preview (serves at http://localhost:3000)
mint dev

# Custom port
mint dev --port 3333

# Skip OpenAPI processing for faster startup
mint dev --disable-openapi

# Update CLI
mint update

# Find broken internal links
mint broken-links
mint broken-links --check-anchors    # also check anchor links

# Accessibility check
mint a11y

# Validate build (strict mode, for CI/CD)
mint validate

# Rename files and update all references
mint rename <path/to/old-filename> <path/to/new-filename>

# Check OpenAPI spec
mint openapi-check <filename-or-url>
```

Full Mintlify docs index: https://www.mintlify.com/docs/llms.txt

## Deployment

Push to `main` → Mintlify GitHub App auto-deploys. No manual build step. Served at adspirer.mintlify.dev (Vercel rewrites route `/docs/*` to Mintlify).

**Do not push to remote without confirming with the user first.**

## Configuration

- `docs.json` — Main Mintlify config: navigation (3 tabs), theme ("maple"), colors, GA4, redirects, footer, SEO
- `.mintignore` — Excludes drafts/, *.draft.mdx, AGENTS.md from the published site
- `.gitignore` — Excludes audit files, TTS scripts, MP3s, source logo files

## Content Architecture

Three navigation tabs defined in `docs.json`:

| Tab | Sections | Purpose |
|-----|----------|---------|
| **Documentation** | Getting Started, AI Clients (8), Ad Platforms (4), Agent Skills (3) | Core product docs |
| **Guides** | Google Ads (3), Meta Ads (1), TikTok (1), Strategy (2) | SEO pillar content / tutorials |
| **Knowledge Base** | Pricing, Security, Platform Comparison, Multi-account, Multi-client, Capabilities | Reference / FAQ |

Global sidebar anchors: Blog, MCP Server, Changelog.

## MDX Conventions

**Frontmatter** — Every page must have `title` and `description`:
```yaml
---
title: "Page Title"
description: "SEO-optimized description"
---
```

**Mintlify components used across the site:**
- `<Tabs>` + `<Tab>` — Tabbed content (setup methods: Quick Install vs Manual)
- `<Steps>` + `<Step title="">` — Numbered step-by-step instructions
- `<Card title="" icon="" href="">` — Clickable navigation cards
- `<CardGroup cols={2}>` / `<Columns cols={2}>` — Multi-column card layouts
- `<Frame caption="">` — Wraps YouTube iframes with captions
- `<Prompt description="" actions={["copy", "cursor"]}>` — Copy-to-clipboard prompts
- `<Badge color="red|yellow|green">` — Status/level indicators
- `<Tooltip tip="definition">` — Hover definitions for acronyms (CPC, MCP, ROAS, etc.)
- `<Note>`, `<Tip>`, `<Info>`, `<Check>` — Callout boxes
- `<AccordionGroup>` + `<Accordion title="">` — FAQ sections
- Mermaid flowcharts in fenced code blocks for workflow diagrams

**Reusable content:** `snippets/snippet-intro.mdx` for shared content blocks (use `<Snippet file="snippet-intro.mdx" />`).

## Content Patterns

**AI Client setup pages** (`ai-clients/*.mdx`) follow this structure:
1. Intro paragraph → Prerequisites (`<Note>`) → Demo video (`<Frame>`)
2. `<Tabs>` with Quick Install and Manual Setup, each containing `<Steps>`
3. Verification steps with `<Check>` callout
4. Example prompts using `<Prompt>` component
5. Troubleshooting FAQ using `<AccordionGroup>`

**Ad Platform pages** (`ad-platforms/*.mdx`):
1. Intro → Demo video → Connection instructions → Tool reference table
2. Campaign types → Workflow sequences (code blocks + Mermaid diagrams)
3. Example prompts → Related links

**Guide pages** (`guides/*.mdx`): Long-form SEO content with videos, step-by-step workflows, and cross-links.

**Knowledge Base pages** (`knowledge-base/*.mdx`): Reference content with tables, callouts, and FAQ accordions.

## Icons

Custom SVG icons in `icons/` directory: chatgpt.svg, claude.svg, claude-code.svg, cursor.svg, codex.svg, openclaw.svg, windsurf.svg, google-ads.svg, meta.svg, linkedin.svg, tiktok.svg. Referenced as `icon="/icons/filename.svg"` in Card components.

## URL / Routing

URLs are auto-generated from file paths (no config needed). File `ai-clients/claude-code.mdx` → `/ai-clients/claude-code`. Redirects for old paths are defined in `docs.json` under `redirects`.

## Auto-generated Endpoints

Mintlify auto-generates these (do not create manually):
- `llms.txt` / `llms-full.txt` — LLM-friendly doc index
- `sitemap.xml` — Search engine sitemap
- `skill.md` / `.well-known/skills/index.json` — Agent skill discovery
