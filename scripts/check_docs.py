#!/usr/bin/env python3
"""Validate local Markdown/HTML links, heading anchors, and documentation SVGs."""
from __future__ import annotations

import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
MD_LINK = re.compile(r"!?\[[^\]]*\]\(\s*(?:<([^>]+)>|([^\s)]+))")
HTML_LINK = re.compile(r"<(?:a|img|source|link)\b[^>]*?\b(?:href|src)=['\"]([^'\"]+)['\"]", re.I)
FENCE_CHAR = chr(96)
FENCE = re.compile(
    r"(?ms)^[ \t]{0,3}(" + re.escape(FENCE_CHAR) + r"{3,}|~{3,})[^\n]*\n.*?^[ \t]{0,3}\1[ \t]*$"
)
HEADING = re.compile(r"(?m)^ {0,3}#{1,6}\s+(.+?)\s*#*\s*$")
SVG_NS = "{http://www.w3.org/2000/svg}"


def markdown_files() -> list[Path]:
    found = set(ROOT.glob("*.md"))
    for folder in (ROOT / "docs", ROOT / "variables", ROOT / "ubuntu"):
        if folder.exists():
            found.update(folder.rglob("*.md"))
    return sorted(found)


def slugify_heading(title: str) -> str:
    title = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", title)
    title = title.replace(FENCE_CHAR, "")
    title = re.sub(r"<[^>]+>", "", title)
    title = re.sub(r"[^\w -]", "", title, flags=re.UNICODE).strip().lower()
    return re.sub(r"\s+", "-", title)


def heading_anchors(path: Path) -> set[str]:
    content = FENCE.sub("", path.read_text(encoding="utf-8"))
    seen: dict[str, int] = {}
    anchors: set[str] = set()
    for match in HEADING.finditer(content):
        slug = slugify_heading(match.group(1))
        if not slug:
            continue
        count = seen.get(slug, 0)
        seen[slug] = count + 1
        anchors.add(slug if count == 0 else f"{slug}-{count}")
    return anchors


def check_links() -> tuple[int, list[str]]:
    count = 0
    errors: list[str] = []
    for source in markdown_files():
        content = FENCE.sub("", source.read_text(encoding="utf-8"))
        links = [(m.group(1) or m.group(2), "Markdown link") for m in MD_LINK.finditer(content)]
        links += [(m.group(1), "HTML href/src") for m in HTML_LINK.finditer(content)]
        for target, kind in links:
            parsed = urlsplit(target)
            if parsed.scheme or parsed.netloc or target.startswith("//"):
                continue
            if not parsed.path and not parsed.fragment:
                continue
            raw_path = unquote(parsed.path)
            destination = (
                (ROOT / raw_path.lstrip("/"))
                if raw_path.startswith("/")
                else (source.parent / raw_path if raw_path else source)
            ).resolve()
            count += 1
            if not destination.is_relative_to(ROOT):
                errors.append(f"{source.relative_to(ROOT)}: local path escapes repository: {target}")
                continue
            if not destination.exists():
                errors.append(f"{source.relative_to(ROOT)}: broken {kind}: {target}")
                continue
            if parsed.fragment and destination.is_file() and destination.suffix.lower() == ".md":
                if parsed.fragment not in heading_anchors(destination):
                    errors.append(
                        f"{source.relative_to(ROOT)}: missing heading anchor '{parsed.fragment}' in "
                        f"{destination.relative_to(ROOT)}"
                    )
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
    print(f"Checked {link_count} local links/anchors and parsed {svg_count} SVG files.")
    if errors:
        print("Documentation checks failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1
    print("Documentation checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
