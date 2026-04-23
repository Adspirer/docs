#!/usr/bin/env python3
"""
Post-process openapi.json for Mintlify hosting.

Two fixes:

1. Hoist nested `$defs` into `components.schemas` so Mintlify (which only
   resolves `#/components/schemas/...`) can render every endpoint.

2. Replace the `summary` Pydantic auto-fills with the first line of each
   tool's docstring. Those lines are verbose ("🚨 **IF THIS TOOL...**"),
   collide across tools (producing URL suffixes `-1`, `-2`, …), and make
   both the sidebar and Google's SERPs unreadable. We derive a clean
   "Title Case" summary from `operationId` and move the original long
   description to `description` (prepended) when useful.

Run after copying the spec from adstudio:

    python3 scripts/inline_openapi_defs.py api-reference/openapi.json
"""
import json
import re
import sys
from pathlib import Path


def rewrite_refs(node, prefix):
    if isinstance(node, dict):
        for k, v in list(node.items()):
            if k == "$ref" and isinstance(v, str) and v.startswith("#/$defs/"):
                name = v[len("#/$defs/"):]
                node[k] = f"#/components/schemas/{prefix}_{name}"
            else:
                rewrite_refs(v, prefix)
    elif isinstance(node, list):
        for item in node:
            rewrite_refs(item, prefix)


def hoist_defs(spec):
    components = spec.setdefault("components", {})
    schemas = components.setdefault("schemas", {})
    hoisted = 0

    for path, path_item in spec.get("paths", {}).items():
        for method, op in path_item.items():
            if not isinstance(op, dict):
                continue
            op_id = op.get("operationId") or f"{method}_{path}".replace("/", "_")
            body = (
                op.get("requestBody", {})
                .get("content", {})
                .get("application/json", {})
                .get("schema", {})
            )
            args = body.get("properties", {}).get("arguments", {})
            defs = args.pop("$defs", None)
            if not defs:
                continue
            for def_name, def_schema in defs.items():
                hoisted_name = f"{op_id}_{def_name}"
                rewrite_refs(def_schema, op_id)
                schemas[hoisted_name] = def_schema
                hoisted += 1
            rewrite_refs(args, op_id)
    return hoisted


# Special-case casing for generated summaries. Keys are lowercase tokens as
# they appear in operationId; values are the rendered label.
_CASE = {
    "api": "API",
    "dco": "DCO",
    "dsa": "DSA",
    "roi": "ROI",
    "roas": "ROAS",
    "cpa": "CPA",
    "cpc": "CPC",
    "cpm": "CPM",
    "ctr": "CTR",
    "cpv": "CPV",
    "utm": "UTM",
    "url": "URL",
    "id": "ID",
    "ids": "IDs",
    "ai": "AI",
    "ml": "ML",
    "ua": "UA",
    "pmax": "PMax",
    "linkedin": "LinkedIn",
    "tiktok": "TikTok",
    "demandgen": "Demand Gen",
    "youtube": "YouTube",
    "github": "GitHub",
    "openai": "OpenAI",
    "chatgpt": "ChatGPT",
}


def titleize(operation_id: str) -> str:
    """execute_add_meta_ad → 'Add Meta Ad'."""
    name = re.sub(r"^execute_", "", operation_id)
    parts = name.split("_")
    words = []
    for p in parts:
        if not p:
            continue
        low = p.lower()
        if low in _CASE:
            words.append(_CASE[low])
        else:
            words.append(p[:1].upper() + p[1:].lower())
    return " ".join(words)


def clean_summaries(spec):
    """Replace noisy summaries with Title Case names from operationId.

    The old summary is the first line of the tool's docstring and is already
    reproduced in `description`. Don't prepend it — that duplicates text in
    the meta tags Google sees.
    """
    updated = 0
    for path, path_item in spec.get("paths", {}).items():
        for method, op in path_item.items():
            if not isinstance(op, dict):
                continue
            op_id = op.get("operationId")
            if not op_id:
                continue
            new_summary = titleize(op_id)
            if op.get("summary") == new_summary:
                continue
            op["summary"] = new_summary
            updated += 1
    return updated


# Boilerplate LLM-prompt preamble that every Google Ads tool docstring starts
# with. Useful for Claude Desktop, meaningless for API consumers (they get the
# quota info from HTTP 402 responses and the documented error envelope).
_QUOTA_PREAMBLE_RE = re.compile(
    r"^🚨\s*\*\*IF THIS TOOL RETURNS A QUOTA ERROR:\*\*"
    r"(?:\n-[^\n]*)+"
    r"\n\n",
    re.MULTILINE,
)

# Tool docstrings mix functional API docs with LLM-orchestration prompts
# (directing Claude to call other tools, ask the user, etc.). Everything from
# the first LLM-addressed heading onward is orchestration — cut it.
_LLM_SECTION_RE = re.compile(
    r"\n[^\n]*(?:"
    r"\*?\*?YOUR\s+(?:CRITICAL\s+)?(?:ROLE|TASK|JOB)\*?\*?\s*:"
    r"|\*?\*?CRITICAL\s+RULES\s+FOR\s+AI\*?\*?"
    r"|\*?\*?MANDATORY\s+(?:WORKFLOW|\d+[-\s]PHASE)"
    r"|\*\*MANDATORY\s*[—:\-]"
    r"|\*\*STEP\s+\d+\.5\s*[:—]"
    r"|🔴\s*\*\*(?:STEP|MANDATORY)"
    r"|📋\s*\*\*YOUR"
    r"|🎯\s*\*\*YOUR"
    r"|BEFORE\s+calling\s+this\s+tool,?\s+YOU\s+MUST"
    r"|YOU\s+MUST\s+(?:call|use|first|follow)"
    r")[\s\S]*$",
    re.MULTILINE,
)


# Split description into alternating prose / code segments so we only escape
# MDX-special characters in prose. A fenced ``` block or an inline `...`
# passes through untouched — backslashes inside code fences render literally.
_CODE_SEGMENT_RE = re.compile(
    r"(```[\s\S]*?```|`[^`\n]+`)",
    re.MULTILINE,
)


_INLINE_BRACES_RE = re.compile(r"\{[^{}\n]{0,500}\}")


def _escape_mdx(prose: str) -> str:
    """Neutralize MDX-special `{`, `}`, and stray `<` sequences in prose.

    Mintlify's MDX parser trips on `{...}` (JSX expression) and `<x` (JSX
    tag), silently falling back to plain-text rendering for the whole
    description. Backslash escapes (`\\{`) and HTML entities (`&#123;`)
    both leak through as literal text in Mintlify.

    Strategy that works: wrap small single-line `{...}` blocks in inline
    backticks. MDX never parses JSX inside inline code, and the content
    (usually JSON-like snippets) is semantically code anyway. Lone `{`
    or `}` that don't pair up get wrapped individually. Stray `<` gets
    the same treatment.
    """
    prose = _INLINE_BRACES_RE.sub(lambda m: f"`{m.group(0)}`", prose)
    # Any remaining unpaired braces — wrap individually.
    prose = re.sub(r"(?<!`)([{}])(?!`)", r"`\1`", prose)
    # Stray `<` followed by anything that isn't a letter or `/`.
    prose = re.sub(r"<(?=[^a-zA-Z/])", "`<`", prose)
    return prose


def _escape_outside_code(text: str) -> str:
    parts = _CODE_SEGMENT_RE.split(text)
    # Odd indices are code segments; even indices are prose.
    for i in range(0, len(parts), 2):
        parts[i] = _escape_mdx(parts[i])
    return "".join(parts)


def clean_descriptions(spec):
    """Strip LLM-only preambles and escape MDX-breaking characters.

    Mintlify renders each operation's `description` through its MDX parser.
    If the description contains `{...}` or `<foo>` sequences, MDX treats
    them as JSX — parsing fails silently and the whole description falls
    back to plain text (bold markers, lists, headings all break).

    We:
      1. Strip the boilerplate 🚨 quota-error preamble that every Google Ads
         tool docstring starts with. (LLM prompt for Claude Desktop — noise
         for human API consumers.)
      2. Escape `{`, `}`, and stray `<` in *prose only* (not inside `code`
         or ``` fenced blocks, where backslashes would render literally).
    """
    stripped = 0
    llm_cut = 0
    escaped = 0
    for path, path_item in spec.get("paths", {}).items():
        for method, op in path_item.items():
            if not isinstance(op, dict):
                continue
            desc = op.get("description")
            if not desc:
                continue
            new = desc
            stripped_this = False
            llm_cut_this = False
            if _QUOTA_PREAMBLE_RE.match(new):
                new = _QUOTA_PREAMBLE_RE.sub("", new, count=1)
                stripped_this = True
            llm_match = _LLM_SECTION_RE.search(new)
            if llm_match:
                new = new[: llm_match.start()].rstrip() + "\n"
                llm_cut_this = True
            new = _escape_outside_code(new)
            if new != desc:
                op["description"] = new
                escaped += 1
            if stripped_this:
                stripped += 1
            if llm_cut_this:
                llm_cut += 1
    return stripped, llm_cut, escaped


def main():
    if len(sys.argv) != 2:
        print("usage: inline_openapi_defs.py <path-to-openapi.json>", file=sys.stderr)
        sys.exit(2)

    path = Path(sys.argv[1])
    spec = json.loads(path.read_text())
    hoisted = hoist_defs(spec)
    summaries = clean_summaries(spec)
    stripped, llm_cut, escaped = clean_descriptions(spec)
    path.write_text(json.dumps(spec, indent=2))
    print(
        f"Hoisted {hoisted} $defs; "
        f"rewrote {summaries} summaries; "
        f"stripped quota preamble from {stripped}; "
        f"cut LLM-orchestration sections from {llm_cut}; "
        f"neutralized MDX in {escaped} descriptions in {path}"
    )


if __name__ == "__main__":
    main()
