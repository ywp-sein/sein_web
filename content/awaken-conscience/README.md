# Awaken Conscience articles

Write each article as a Markdown file in this folder. Copy `_template.md`, give
the copy a descriptive filename, complete its metadata and write the article.
The filename is not published; the generator creates the URL from the title.

Required metadata:

- `title`: article title
- `date`: publication date in `YYYY-MM-DD` format
- `author`: the writer's published name
- `labels`: comma-separated category labels
- `summary`: short archive description

Generate the website from the `sein_web` directory:

```bash
make update-awaken-conscience
```

The generator creates one HTML page per article and rebuilds the archive in
newest-first order. Files beginning with `_` are ignored, so `_template.md`
never appears as an article.
