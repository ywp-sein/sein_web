#!/usr/bin/env python3
"""Generate Awaken Conscience HTML pages and its newest-first archive."""

from __future__ import annotations

import html
import re
from dataclasses import dataclass
from datetime import date, datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE_DIR = ROOT / "content" / "awaken-conscience"
OUTPUT_DIR = ROOT / "missions" / "awaken-conscience"
INDEX = OUTPUT_DIR / "index.html"
START = "          <!-- AWAKEN_ARTICLES_START -->"
END = "          <!-- AWAKEN_ARTICLES_END -->"
DEFAULT_LABELS = (
    "Society",
    "Justice",
    "Faith & Conscience",
    "Culture",
    "Beneath the Headlines",
)


@dataclass
class Article:
    title: str
    published: date
    author: str
    labels: list[str]
    summary: str
    slug: str
    body_html: str


def slugify(value: str) -> str:
    value = value.lower().replace("&", " and ")
    value = re.sub(r"[^a-z0-9]+", "-", value)
    return value.strip("-")


def render_inline(value: str) -> str:
    value = html.escape(value)
    value = re.sub(r"\[([^]]+)]\(([^)]+)\)", r'<a href="\2">\1</a>', value)
    value = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", value)
    value = re.sub(r"\*([^*]+)\*", r"<em>\1</em>", value)
    value = re.sub(r"`([^`]+)`", r"<code>\1</code>", value)
    return value


def markdown_to_html(markdown: str) -> str:
    output: list[str] = []
    paragraph: list[str] = []
    list_items: list[str] = []

    def flush_paragraph() -> None:
        if paragraph:
            text = " ".join(line.strip() for line in paragraph)
            output.append(f"        <p>{render_inline(text)}</p>")
            paragraph.clear()

    def flush_list() -> None:
        if list_items:
            items = "".join(f"<li>{render_inline(item)}</li>" for item in list_items)
            output.append(f"        <ul>{items}</ul>")
            list_items.clear()

    for raw_line in markdown.splitlines():
        line = raw_line.strip()
        if not line:
            flush_paragraph()
            flush_list()
        elif line.startswith("## "):
            flush_paragraph()
            flush_list()
            output.append(f"        <h2>{render_inline(line[3:])}</h2>")
        elif line.startswith("### "):
            flush_paragraph()
            flush_list()
            output.append(f"        <h3>{render_inline(line[4:])}</h3>")
        elif line.startswith("> "):
            flush_paragraph()
            flush_list()
            output.append(f"        <blockquote><p>{render_inline(line[2:])}</p></blockquote>")
        elif re.match(r"^[-*] ", line):
            flush_paragraph()
            list_items.append(line[2:].strip())
        else:
            flush_list()
            paragraph.append(line)

    flush_paragraph()
    flush_list()
    return "\n".join(output)


def parse_article(path: Path) -> Article:
    text = path.read_text(encoding="utf-8").strip()
    match = re.match(r"^---\s*\n(.*?)\n---\s*\n(.*)$", text, re.DOTALL)
    if not match:
        raise ValueError(f"{path.name}: expected metadata between --- lines")

    metadata: dict[str, str] = {}
    for line in match.group(1).splitlines():
        if ":" not in line:
            raise ValueError(f"{path.name}: invalid metadata line: {line}")
        key, value = line.split(":", 1)
        metadata[key.strip().lower()] = value.strip()

    missing = [key for key in ("title", "date", "author", "labels", "summary") if not metadata.get(key)]
    if missing:
        raise ValueError(f"{path.name}: missing {', '.join(missing)}")

    published = datetime.strptime(metadata["date"], "%Y-%m-%d").date()
    labels = [label.strip() for label in metadata["labels"].split(",") if label.strip()]
    slug = metadata.get("slug") or slugify(metadata["title"])
    return Article(
        title=metadata["title"],
        published=published,
        author=metadata["author"],
        labels=labels,
        summary=metadata["summary"],
        slug=slug,
        body_html=markdown_to_html(match.group(2).strip()),
    )


def display_date(value: date) -> str:
    return value.strftime("%d.%m.%Y")


def article_page(article: Article) -> str:
    labels = "".join(f'<span class="article-label">{html.escape(label)}</span>' for label in article.labels)
    return f'''<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <meta name="description" content="{html.escape(article.summary, quote=True)}">
    <title>{html.escape(article.title)} | Awaken Conscience | SEiN</title>
    <link rel="stylesheet" href="/assets/css/styles.css?v=20260819-awaken-conscience">
  </head>
  <body>
    <site-header></site-header>
    <main>
      <article class="awaken-article">
        <header class="page-hero compact-hero awaken-article-header">
          <p class="eyebrow">Awaken Conscience</p>
          <h1>{html.escape(article.title)}</h1>
          <div class="article-meta">
            <time datetime="{article.published.isoformat()}">{display_date(article.published)}</time>
            <span class="article-author">By {html.escape(article.author)}</span>
            <div class="category-labels">{labels}</div>
          </div>
          <p>{html.escape(article.summary)}</p>
        </header>
        <div class="section article-body">
{article.body_html}
          <p class="article-return"><a class="text-link" href="/missions/awaken-conscience/">Return to Awaken Conscience</a></p>
        </div>
      </article>
    </main>
    <site-footer></site-footer>
    <script src="/assets/js/script.js"></script>
  </body>
</html>
'''


def filter_markup(articles: list[Article]) -> str:
    used_labels = {label for article in articles for label in article.labels}
    labels = [label for label in DEFAULT_LABELS if label in used_labels or not articles]
    labels.extend(sorted(used_labels.difference(labels)))
    buttons = ['            <button class="is-active" type="button" data-article-filter="all" aria-pressed="true">All</button>']
    buttons.extend(
        f'            <button type="button" data-article-filter="{slugify(label)}" aria-pressed="false">{html.escape(label)}</button>'
        for label in labels
    )
    return "\n".join(buttons)


def card_markup(article: Article, featured: bool) -> str:
    classes = "post-card article-card featured" if featured else "post-card article-card"
    category_values = " ".join(slugify(label) for label in article.labels)
    labels = "".join(f'<span class="article-label">{html.escape(label)}</span>' for label in article.labels)
    return f'''            <article class="{classes}" data-article-categories="{category_values}">
              <time datetime="{article.published.isoformat()}">{display_date(article.published)}</time>
              <p class="article-author">By {html.escape(article.author)}</p>
              <div class="category-labels">{labels}</div>
              <h3>{html.escape(article.title)}</h3>
              <p>{html.escape(article.summary)}</p>
              <a class="text-link" href="/missions/awaken-conscience/{article.slug}.html">Read article</a>
            </article>'''


def archive_markup(articles: list[Article]) -> str:
    filters = filter_markup(articles)
    if articles:
        cards = "\n".join(card_markup(article, index == 0) for index, article in enumerate(articles))
        status = f"{len(articles)} {'article' if len(articles) == 1 else 'articles'}"
    else:
        status = "Articles will appear here soon"
        cards = '''            <div class="article-empty-state" data-empty-state>
              <p class="eyebrow">First edition forthcoming</p>
              <h3>The space is ready for the first article.</h3>
              <p>New writing will appear here with its category, publication date, title, and a short introduction.</p>
            </div>'''
    return f'''{START}
          <div class="article-filters" aria-label="Filter articles by category">
{filters}
          </div>
          <p class="filter-result" data-filter-result aria-live="polite">{status}</p>
          <div class="article-list" data-article-list>
{cards}
          </div>
{END}'''


def update_index(articles: list[Article]) -> None:
    text = INDEX.read_text(encoding="utf-8")
    pattern = re.compile(re.escape(START) + r".*?" + re.escape(END), re.DOTALL)
    if not pattern.search(text):
        raise ValueError("Archive markers are missing from missions/awaken-conscience/index.html")
    INDEX.write_text(pattern.sub(lambda _: archive_markup(articles), text), encoding="utf-8")


def main() -> None:
    source_files = sorted(path for path in SOURCE_DIR.glob("*.md") if not path.name.startswith("_") and path.name != "README.md")
    articles = sorted((parse_article(path) for path in source_files), key=lambda item: item.published, reverse=True)
    slugs = [article.slug for article in articles]
    if len(slugs) != len(set(slugs)):
        raise ValueError("Article titles/slugs must be unique")

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    for article in articles:
        (OUTPUT_DIR / f"{article.slug}.html").write_text(article_page(article), encoding="utf-8")
    update_index(articles)
    print(f"Generated {len(articles)} Awaken Conscience article(s), newest first.")


if __name__ == "__main__":
    main()
