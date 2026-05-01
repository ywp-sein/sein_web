# SEiN Website

The open-source main website for SEiN, a Christian education, business, and
social initiative for Berlin's homeless.

This version is intentionally lightweight:

- `index.html` contains the page content and structure.
- `about.html`, `prayers.html`, `homelessness.html`, and `contact.html`
  provide the main navigation pages.
- `styles.css` contains the visual design and responsive layout.
- `script.js` contains the mobile navigation and email form behavior.

## Preview locally

Open `index.html` directly in a browser, or run a tiny local server:

```bash
python3 -m http.server 8080
```

Then visit <http://localhost:8080>.

## Next content to add

- Replace `contact@sein-live.com` in `script.js` with the preferred public email.
- Decide whether the prayers blog should stay hand-curated or be generated from
  `sein_prayers/src/weekly/*.md`.
- Decide where the generated `sein_prayers` and `sein_knowledge_hub` books will be
  published, then add archive links from `prayers.html` and `homelessness.html`.
- Add dedicated pages for Imprint and Privacy Policy if this site will fully replace Wix.
