#!/usr/bin/env python3
"""Archive the public SML slides site and generate searchable module notes."""

import concurrent.futures
import hashlib
import html
import json
import os
import urllib.parse
import urllib.request
from html.parser import HTMLParser
from pathlib import Path


BASE = "https://sml-slides.aws.yikyakyuk.com/slides/"
SESSION = Path(__file__).resolve().parents[1] / "sessions" / "2026-09-24-modern-data-platform-bfsi"
SOURCE = SESSION / "source"
TITLES = {
    1: "Modern Data Architecture Foundations",
    2: "The Open Data Platform — SageMaker Catalog & Lakehouse",
    3: "Data Lake Use Cases for BFSI",
    4: "Wrap-Up, Patterns & Next Steps",
    5: "Redshift & RMS Deep Dive",
}


class VisibleText(HTMLParser):
    def __init__(self):
        super().__init__()
        self.parts = []

    def handle_starttag(self, tag, attrs):
        if tag in {"p", "div", "li", "h1", "h2", "h3", "br"}:
            self.parts.append("\n")
        if tag == "li":
            self.parts.append("- ")

    def handle_data(self, data):
        self.parts.append(data)

    def text(self):
        return "\n\n".join(
            line.strip() for line in html.unescape("".join(self.parts)).splitlines() if line.strip()
        )


def get(path: str) -> bytes:
    parsed = urllib.parse.urlparse(path)
    if parsed.scheme or parsed.netloc or path.startswith("/") or ".." in Path(path).parts:
        raise ValueError(f"Invalid source path: {path}")
    request = urllib.request.Request(urllib.parse.urljoin(BASE, path), headers={"User-Agent": "aws-training-personal-archive/1.0"})
    with urllib.request.urlopen(request, timeout=30) as response:
        return response.read()


def download(path: str) -> tuple[str, int, str]:
    data = get(path)
    target = SOURCE / path
    target.parent.mkdir(parents=True, exist_ok=True)
    temp = target.with_name(target.name + ".download")
    temp.write_bytes(data)
    os.replace(temp, target)
    return path, len(data), hashlib.sha256(data).hexdigest()


def markdown(module: int, slides: list[dict]) -> str:
    lines = [f"# Module {module}: {TITLES[module]}", "", f"Original: {BASE}deck.html?m={module}", ""]
    for slide in slides:
        lines += [f"## Slide {slide['n']}", ""]
        native = slide.get("native", "")
        if native:
            parser = VisibleText()
            parser.feed(native)
            lines += [parser.text(), ""]
        if slide.get("image"):
            lines += [f"![Slide {slide['n']}](../source/{slide['image']})", ""]
        if slide.get("student"):
            lines += ["### Slide notes", "", slide["student"].strip(), ""]
        if slide.get("instructor"):
            lines += ["### Instructor notes", "", slide["instructor"].strip(), ""]
        if slide.get("audio"):
            lines += [f"[Narration MP3](../source/{slide['audio']})", ""]
    return "\n".join(lines).rstrip() + "\n"


def main() -> None:
    SOURCE.mkdir(parents=True, exist_ok=True)
    paths = {"index.html", "deck.html", "doc.html"}
    paths.update(f"decks/m{i}.json" for i in range(1, 6))
    paths.update(f"docs/phase{i}.md" for i in range(1, 4))
    decks = {}
    for module in TITLES:
        slides = json.loads(get(f"decks/m{module}.json"))
        decks[module] = slides
        for slide in slides:
            for key in ("image", "audio"):
                if slide.get(key):
                    paths.add(slide[key])
    with concurrent.futures.ThreadPoolExecutor(max_workers=12) as pool:
        manifest = sorted(pool.map(download, sorted(paths)))
    (SESSION / "slides").mkdir(exist_ok=True)
    for module, slides in decks.items():
        (SESSION / "slides" / f"module-{module}.md").write_text(markdown(module, slides), encoding="utf-8")
    (SESSION / "source-manifest.json").write_text(
        json.dumps({"source": BASE, "files": [{"path": p, "bytes": n, "sha256": h} for p, n, h in manifest]}, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"Archived {len(manifest)} files ({sum(n for _, n, _ in manifest):,} bytes) to {SESSION}")


if __name__ == "__main__":
    main()
