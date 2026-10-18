#!/usr/bin/env python3
"""Validate repository-local Markdown links and documentation SVG files."""
from __future__ import annotations

import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
MD_LINK = re.compile(r"!?\[[^\]]*\]\(\s*(?:<([^>]+)>|([^\s)]+))")
HTML_LINK = re.compile(r"<(?:a|img|source|link)\b[^>]*?\b(?:href|src)=[\"']([^\"']+)[\"']", re.I)
FENCE = re.compile(r"(?ms)^[ \t]{0,3}(`{3,}|~{3,})[^\n]*\n.*?^[ \t]{0,3}\1[ \t]*$")
SVG_NS = "{http://www.w3.org/2000/svg}"


def markdown_files() -> list[Path]:
    found = set(ROOT.glob("*.md"))
    for folder in (ROOT / "docs", ROOT / "variables"):
        if folder.exists():
            found.update(folder.rglob("*.md"))
    return sorted(found)


def check_links() -> tuple[int, list[str]]:
    count = 0
    errors: list[str] = []
    for source in markdown_files():
        text = FENCE.sub("", source.read_text(encoding="utf-8"))
        links = [(m.group(1) or m.group(2), "Markdown link") for m in MD_LINK.finditer(text)]
        links += [(m.group(1), "HTML href/src") for m in HTML_LINK.finditer(text)]
        for target, kind in links:
            url = urlsplit(target)
            if url.scheme or url.netloc or target.startswith("//") or not url.path:
                continue
            raw = unquote(url.path)
            path = ((ROOT / raw.lstrip("/")) if raw.startswith("/") else source.parent / raw).resolve()
            count += 1
            if not path.is_relative_to(ROOT):
                errors.append(f"{source.relative_to(ROOT)}: local path escapes repository: {target}")
            elif not path.exists():
                errors.append(f"{source.relative_to(ROOT)}: broken {kind}: {target}")
    return count, errors


def check_svgs() -> tuple[int, list[str]]:
    paths = sorted((ROOT / "docs").rglob("*.svg"))
    errors: list[str] = []
    for path in paths:
        try:
            root = ET.parse(path).getroot()
            if root.tag != f"{SVG_NS}svg":
                errors.append(f"{path.relative_to(ROOT)}: root element is not SVG")
                continue
            if not (root.get("viewBox") or (root.get("width") and root.get("height"))):
                errors.append(f"{path.relative_to(ROOT)}: missing viewBox or dimensions")
            if path.name != "brand.svg" and len(root.findall(f".//{SVG_NS}text")) < 3:
                errors.append(f"{path.relative_to(ROOT)}: illustration may be incomplete")
        except (ET.ParseError, OSError) as exc:
            errors.append(f"{path.relative_to(ROOT)}: invalid SVG/XML: {exc}")
    return len(paths), errors


def main() -> int:
    link_count, link_errors = check_links()
    svg_count, svg_errors = check_svgs()
    errors = link_errors + svg_errors
    print(f"Checked {link_count} local Markdown/HTML references and parsed {svg_count} SVG files.")
    if errors:
        print("Documentation checks failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1
    print("Documentation checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
