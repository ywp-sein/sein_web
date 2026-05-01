#!/usr/bin/env python3
"""Generate prayers.html from ../sein_prayers/src/SUMMARY.md."""

from __future__ import annotations

import html
import re
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PRAYERS_SRC = ROOT.parent / "sein_prayers" / "src"
SUMMARY = PRAYERS_SRC / "SUMMARY.md"
OUTPUT = ROOT / "prayers.html"


@dataclass
class PrayerPost:
    number: str
    title: str
    date_display: str
    date_iso: str
    excerpt: str
    body_html: str


def parse_summary() -> list[tuple[str, str]]:
    text = SUMMARY.read_text(encoding="utf-8")
    entries = re.findall(r"- \[(\d+)\s+([^\]]+)\]\((weekly/\d+\.md)\)", text)
    return [(title.strip(), rel_path) for _, title, rel_path in entries]


def parse_post(title_from_summary: str, rel_path: str) -> PrayerPost:
    source = PRAYERS_SRC / rel_path
    text = source.read_text(encoding="utf-8").strip()
    lines = text.splitlines()

    title = title_from_summary
    if lines and lines[0].startswith("# "):
      title = lines[0][2:].strip()
      lines = lines[1:]

    date_display = ""
    if lines:
        while lines and not lines[0].strip():
            lines = lines[1:]
        if lines and re.fullmatch(r"\*[^*]+\*", lines[0].strip()):
            date_display = lines[0].strip().strip("*")
            lines = lines[1:]

    body_text = "\n".join(lines).strip()
    excerpt = make_excerpt(body_text)
    number = Path(rel_path).stem
    date_iso = make_iso_date(date_display)

    return PrayerPost(
        number=number,
        title=title,
        date_display=date_display,
        date_iso=date_iso,
        excerpt=excerpt,
        body_html=markdown_to_html(body_text),
    )


def make_iso_date(date_display: str) -> str:
    try:
        return datetime.strptime(date_display, "%d.%m.%Y").date().isoformat()
    except ValueError:
        return ""


def strip_markdown(text: str) -> str:
    cleaned = re.sub(r"<br\s*/?>", " ", text)
    cleaned = re.sub(r"[*_`>#-]", "", cleaned)
    cleaned = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", cleaned)
    cleaned = re.sub(r"\s+", " ", cleaned)
    return cleaned.strip()


def make_excerpt(text: str, words: int = 34) -> str:
    plain = strip_markdown(text)
    pieces = plain.split()
    if len(pieces) <= words:
        return plain
    return " ".join(pieces[:words]).rstrip(",.;:") + "..."


def render_inline(text: str) -> str:
    escaped = html.escape(text)
    escaped = re.sub(r"&lt;br\s*/?&gt;", "<br>", escaped, flags=re.IGNORECASE)
    escaped = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2">\1</a>', escaped)
    escaped = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", escaped)
    escaped = re.sub(r"\*([^*]+)\*", r"<em>\1</em>", escaped)
    escaped = re.sub(r"`([^`]+)`", r"<code>\1</code>", escaped)
    return escaped


def flush_paragraph(block: list[str], output: list[str]) -> None:
    if not block:
        return
    paragraph = " ".join(line.strip() for line in block).strip()
    output.append(f"              <p>{render_inline(paragraph)}</p>")
    block.clear()


def markdown_to_html(text: str) -> str:
    output: list[str] = []
    paragraph: list[str] = []

    for raw_line in text.splitlines():
        line = raw_line.rstrip()
        stripped = line.strip()

        if not stripped:
            flush_paragraph(paragraph, output)
            continue

        if stripped.startswith("# "):
            flush_paragraph(paragraph, output)
            output.append(f"              <h4>{render_inline(stripped[2:].strip())}</h4>")
            continue

        if stripped.startswith(">"):
            flush_paragraph(paragraph, output)
            quote = stripped.lstrip(">").strip()
            output.append(f"              <blockquote><p>{render_inline(quote)}</p></blockquote>")
            continue

        if re.match(r"^[-*]\s+", stripped):
            flush_paragraph(paragraph, output)
            item = re.sub(r"^[-*]\s+", "", stripped)
            output.append(f"              <p class=\"list-item\">{render_inline(item)}</p>")
            continue

        paragraph.append(stripped)

    flush_paragraph(paragraph, output)
    return "\n".join(output)


def post_html(post: PrayerPost, featured: bool) -> str:
    classes = "post-card featured" if featured else "post-card"
    return f"""          <article class="{classes}" id="post-{post.number}">
            <time datetime="{html.escape(post.date_iso)}">{html.escape(post.date_display)}</time>
            <h3>{html.escape(post.title)}</h3>
            <p>{html.escape(post.excerpt)}</p>
            <details class="post-expand">
              <summary>Read full prayer</summary>
              <div class="post-body">
{post.body_html}
              </div>
            </details>
          </article>"""


def render_page(posts: list[PrayerPost]) -> str:
    latest = posts[0]
    post_markup = "\n\n".join(post_html(post, index == 0) for index, post in enumerate(posts))

    return f"""<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <meta
      name="description"
      content="Weekly prayers for SEiN in a blog-style archive."
    >
    <title>Prayers | SEiN</title>
    <link rel="stylesheet" href="styles.css">
  </head>
  <body>
    <header class="site-header">
      <a class="brand" href="index.html" aria-label="SEiN home">
        <img class="brand-logo" src="media/logo/logo_cross_final.png" alt="SEiN - Save Everyone in Need">
      </a>

      <button class="nav-toggle" type="button" aria-expanded="false" aria-controls="site-nav">
        <span class="sr-only">Toggle navigation</span>
        <span></span>
        <span></span>
        <span></span>
      </button>

      <nav class="site-nav" id="site-nav" aria-label="Primary navigation">
        <a href="index.html">Home</a>
        <a href="about.html">About</a>
        <a href="prayers.html" aria-current="page">Prayers</a>
        <a href="homelessness.html">Homelessness</a>
        <a href="contact.html">Contact</a>
      </nav>
    </header>

    <main>
      <section class="page-hero">
        <p class="eyebrow">Prayers</p>
        <h1>Weekly prayers for SEiN.</h1>
        <p>
          A blog-style rhythm of prayer, reflection, and dependence on God as
          the initiative grows step by step.
        </p>
      </section>

      <section class="section blog-layout" aria-labelledby="latest-prayers-title">
        <div class="blog-intro">
          <p class="eyebrow">Latest Posts</p>
          <h2 id="latest-prayers-title">Prayer before planning, communion before action.</h2>
          <p>
            This page is generated from <code>sein_prayers/src/SUMMARY.md</code>.
            Add a new weekly prayer there, run the update script, and the latest
            entry appears here automatically.
          </p>
          <a class="button primary" href="#post-{latest.number}">Read latest prayer</a>
        </div>

        <div class="post-list">
{post_markup}
        </div>
      </section>
    </main>

    <footer class="site-footer">
      <p>© 2026 Yuan-Wei Pi. All rights reserved.</p>
      <p>
        <a href="index.html">Home</a>
        <a href="about.html">About</a>
        <a href="prayers.html">Prayers</a>
        <a href="homelessness.html">Homelessness</a>
        <a href="contact.html">Contact</a>
      </p>
    </footer>

    <script src="script.js"></script>
  </body>
</html>
"""


def main() -> None:
    posts = [parse_post(title, rel_path) for title, rel_path in parse_summary()]
    posts.reverse()
    OUTPUT.write_text(render_page(posts), encoding="utf-8")
    print(f"Updated {OUTPUT.relative_to(ROOT.parent)} with {len(posts)} prayer posts.")


if __name__ == "__main__":
    main()
