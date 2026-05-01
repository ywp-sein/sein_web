# SEiN Website

The open-source main website for SEiN, an initiative to archive social issues
through Christ. Homelessness in Berlin is the current mission, not the whole
boundary of the work.

This version is intentionally lightweight:

- `index.html` contains the page content and structure.
- `about.html`, `prayers.html`, `homelessness.html`, and `contact.html`
  provide the main navigation pages.
- `about-me.html` is an About subpage for Yuan-Wei Pi.
- `homelessness.html` is the Missions overview.
- `archiving-homelessness.html` is the homelessness detail page under Missions.
- `imprint.html` and `privacy.html` provide local legal pages so the site does
  not depend on Wix links.
- `styles.css` contains the visual design and responsive layout.
- `script.js` contains the mobile navigation and email form behavior.
- `tools/update_prayers.py` regenerates the prayers blog from
  `../sein_prayers/src/SUMMARY.md`.
- `tools/watch_prayers.py` watches the prayer source files and regenerates the
  blog whenever `SUMMARY.md` or a weekly prayer markdown file changes.

## Preview locally

Open `index.html` directly in a browser, or run a tiny local server:

```bash
python3 -m http.server 8080
```

Then visit <http://localhost:8080>.

## Update the prayers blog

After adding a new weekly prayer to `../sein_prayers/src/weekly/` and listing it
in `../sein_prayers/src/SUMMARY.md`, run:

```bash
python3 tools/update_prayers.py
```

For automatic local updates while editing prayer files, run:

```bash
python3 tools/watch_prayers.py
```

## Next content to add

- Replace `contact@sein-live.com` in `script.js` with the preferred public email.
- Decide where the generated `sein_prayers` and `sein_knowledge_hub` books will be
  published, then add archive links from `prayers.html` and `homelessness.html`.
- Review `imprint.html` and `privacy.html` before production deployment,
  especially if analytics, donations, newsletters, or third-party embeds are added.
