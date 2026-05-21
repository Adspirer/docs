---
name: Fix Broken Links
on:
  push:
    - repo: Adspirer/adstudio-docs
automerge: true
---

You are fixing broken links in the Adspirer documentation site. The docs are served at **adspirer.com/docs/** (Vercel rewrite to Mintlify). Use the following Adspirer-specific rules when fixing links.

**CRITICAL: NEVER modify files in the `.mintlify/` directory.**

## URL Architecture

### Internal links in MDX files
MDX sidebar navigation links are automatically prefixed by Mintlify — use paths WITHOUT `/docs/`:
- ✅ `/knowledge-base/pricing`
- ✅ `/ad-platforms/google-ads`
- ✅ `/agent-skills/tools`
- ❌ `/docs/knowledge-base/pricing`

### Links that MUST use `/docs/` prefix
These sections are NOT auto-prefixed by Mintlify and must be manually prefixed:
- `docs.json` → `banner.content` links
- `docs.json` → `errors.404.description` links
- `docs.json` → `footer.links[].items[].href` values

### External Adspirer URLs
These are the canonical external URLs — update any variants to these:
- Main site: `https://adspirer.com` or `https://www.adspirer.com`
- App (billing, connections, settings): `https://adspirer.ai`
- Monitors web UI: `https://adspirer.ai/monitors`
- API connections: `https://adspirer.ai/connections`
- API keys: `https://adspirer.ai/keys`
- REST API: `https://api.adspirer.ai`
- Swagger UI: `https://api.adspirer.ai/docs`

### Known redirect patterns
- Old `app.adspirer.com` links → update to `adspirer.ai`
- Old `adspirer.mintlify.dev` links → update to `adspirer.com/docs`

## What NOT to flag as broken
- External platform URLs (ads.google.com, business.facebook.com, ads.tiktok.com) — these are correct but may rate-limit crawlers
- GitHub repo URLs (github.com/Adspirer/...) — may be private
- YouTube embed URLs — skip, these are iframes not links
- Anchor links ending in `#some-section` — only flag if the target page itself is missing

## Fix strategy
1. For broken internal links: find the correct current file path and update the href
2. For broken external links: check if the URL has changed (common for ad platform docs) and find the current URL
3. For removed pages: find the best redirect target within the docs and update the link
4. If unsure about correct target: comment in the PR description, do not guess
