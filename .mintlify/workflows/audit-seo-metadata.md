---
name: Audit SEO Metadata
on:
  push:
    - repo: Adspirer/adstudio-docs
automerge: false
---

You are auditing and improving SEO metadata across the Adspirer documentation site. Use the following brand and audience context when writing titles, descriptions, and keywords.

**CRITICAL: NEVER modify files in the `.mintlify/` directory.**

## About Adspirer

**What it is:** An AI advertising agent that connects AI assistants (Claude, ChatGPT, Cursor, Codex) to ad platforms (Google Ads, Meta Ads, LinkedIn Ads, TikTok Ads) via MCP (Model Context Protocol). Users manage campaigns through natural language chat instead of manual platform UIs.

**Target audience:** Performance marketers, paid media managers, and agencies running ads on 2+ platforms.

**Key differentiators:** Works inside AI clients users already have, 190+ tools, no new UI to learn, campaigns created PAUSED for review.

**Competitor context:** Manual Google Ads Manager, traditional agency tools, other ad automation SaaS.

## Metadata Rules

### `title` field (page `<title>` tag)
- **Length:** 40–65 characters ideal, never over 70
- **Format:** `[Topic] | Adspirer` for most pages OR just the topic if long
- **Lead with the value:** "Create Google Ads with Claude" not "Claude Integration for Google Ads"
- **Include platform names where relevant:** Google Ads, Meta Ads, TikTok Ads, LinkedIn Ads
- **Avoid:** vague terms like "Overview", "Introduction", "Learn More"

### `description` field (meta description)
- **Length:** 120–160 characters
- **Must include:** what the page covers + a concrete benefit or capability
- **Include 1-2 keywords naturally** — don't keyword-stuff
- **Action verbs:** "Create", "Manage", "Analyze", "Optimize", "Connect"
- **Example (good):** "Connect Claude or ChatGPT to Google Ads with Adspirer's MCP server. Create Search, PMax, and Display campaigns through natural language — no manual setup."
- **Example (bad):** "Learn about Google Ads integration features and capabilities for Adspirer users."

### `keywords` array
- Include 5–10 relevant terms
- Always include: `"mcp"`, `"ai advertising"` or `"ai ads"`, the specific platform (e.g., `"google ads"`)
- Include long-tail variants: `"google ads automation"`, `"meta ads with ai"`, `"tiktok ads mcp"`)
- Include user intent terms: `"automate google ads"`, `"manage facebook ads with ai"`
- Don't include: generic terms like "advertising", "marketing", "software" alone

## Page-Type Patterns

### Platform pages (`/ad-platforms/*.mdx`)
Title: `[Platform] Integration | Adspirer`
Description: Lead with tool count + most compelling capability + supported campaign types

### AI client pages (`/ai-clients/*.mdx`)
Title: `Connect [Client] to Ad Platforms | Adspirer`
Description: Lead with what the user can do in that AI client + mention MCP

### Guide pages (`/guides/*.mdx`)
Title: target the exact search query the page answers (e.g., "How to Automate Google Ads with AI")
Description: lead with the outcome the reader achieves

### Knowledge base pages (`/knowledge-base/*.mdx`)
Title: question format or clear topic (e.g., "Adspirer Pricing & Tool Call Quotas")
Description: state clearly what the page answers

## What to check
1. Missing `title` or `description` frontmatter → add it
2. Description too short (< 100 chars) or too long (> 165 chars) → rewrite
3. Title too long (> 70 chars) → shorten
4. Generic descriptions that don't mention what the page actually covers → rewrite
5. Missing `keywords` array → add relevant terms
6. Duplicate titles across pages → differentiate them

## What NOT to change
- Page content (only frontmatter metadata)
- File names or URLs
- The `icon` field or `mode` field
- Navigation structure
