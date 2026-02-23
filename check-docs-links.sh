#!/bin/bash
# Check docs.json for internal links missing the /docs/ prefix.
# Mintlify CLI (mint broken-links) only checks MDX content files,
# not links in docs.json config (banner, footer, 404 page, etc.).
# This script fills that gap for subdirectory deployments.
#
# Usage: ./check-docs-links.sh
# Run this alongside: mint validate && mint broken-links --check-anchors

node -e '
const fs = require("fs");
const config = JSON.parse(fs.readFileSync("docs.json", "utf8"));
let errors = 0;

function check(path, value) {
  if (typeof value !== "string") return;
  // Check if value is an internal link (starts with /)
  if (value.startsWith("/") && !value.startsWith("/docs/")) {
    console.log("  BROKEN: " + path + " = \"" + value + "\" — missing /docs/ prefix");
    errors++;
  }
  // Check markdown links in string values: [text](/path)
  const mdLinks = value.match(/\]\(\/[^)]+\)/g) || [];
  mdLinks.forEach(m => {
    const link = m.slice(2, -1); // extract /path from ](/path)
    if (!link.startsWith("/docs/")) {
      console.log("  BROKEN: " + path + " markdown link \"" + link + "\" — missing /docs/ prefix");
      errors++;
    }
  });
}

console.log("Checking docs.json for internal links missing /docs/ prefix...");

// Check banner content (markdown links)
if (config.banner?.content) check("banner.content", config.banner.content);

// Check 404 error page (markdown links)
if (config.errors?.["404"]?.description) check("errors.404.description", config.errors["404"].description);

// Check footer link hrefs
(config.footer?.links || []).forEach((col, i) => {
  (col.items || []).forEach((item, j) => {
    check("footer.links[" + i + "].items[" + j + "].href (" + item.label + ")", item.href);
  });
});

// NOTE: navigation.global.anchors hrefs are NOT checked because
// Mintlify auto-prefixes them with the base path.

if (errors > 0) {
  console.log("FAIL: " + errors + " internal link(s) missing /docs/ prefix");
  process.exit(1);
} else {
  console.log("PASS: all config links in docs.json have /docs/ prefix");
  process.exit(0);
}
'
