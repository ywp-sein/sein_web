# SEiN Website

The open-source main website for SEiN, an initiative to archive social issues
through Christ. Homelessness in Berlin is the current mission, not the whole
boundary of the work.

This version is intentionally lightweight:

- `index.html` is the landing page.
- `about/` contains the About SEiN overview, Why SEiN, and About Us pages.
- `missions/` contains the Missions overview.
- `missions/homelessness/` contains the Archiving Homelessness mission page,
  How It Begins, and its action subpages: Awakening Hope, Knowledge Hub,
  A Step Forward PoC, and Compassion Voucher PoC.
- `prayers/` contains the generated prayers blog.
- `contact/` contains the contact page.
- `legal/` contains Imprint and Privacy Policy pages.
- `assets/` contains shared CSS, JavaScript, and media.
- `tools/update_prayers.py` regenerates `prayers/index.html` from
  `../sein_prayers/src/SUMMARY.md`.
- `tools/watch_prayers.py` watches the prayer source files and regenerates the
  blog whenever `SUMMARY.md` or a weekly prayer markdown file changes.

## Preview locally

Open `index.html` directly in a browser, or run a tiny local server:

```bash
python3 -m http.server 8080
```

Then visit <http://localhost:8080>.

## Deploy to GitHub Pages

The site deploys automatically from `main` through GitHub Actions. The workflow
publishes the repository root as a static GitHub Pages site. During deployment,
it rewrites root-relative local paths so the project site works at
`https://ywp-sein.github.io/sein_web/`.

In GitHub, keep Pages configured to use **GitHub Actions** as the source. After
pushing to `main`, check the `Deploy GitHub Pages` workflow run. The public URL
will be shown in that run after deployment succeeds.

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

## Inner page header with image

Use this template on non-landing pages when a page needs an image beside the H1.
Place local images under `assets/media/` and keep descriptive alt text.

```html
<section class="page-hero media-hero" id="example-top">
  <div class="media-hero-copy">
    <p class="eyebrow">Page Label</p>
    <h1>Page title.</h1>
    <p>A short page introduction that explains why this page exists.</p>
  </div>
  <figure class="media-hero-image">
    <img src="/assets/media/example/example.jpg" alt="Describe the image">
  </figure>
</section>
```

## Next content to add

- Replace `contact@sein-live.com` in `assets/js/script.js` with the preferred public email.
- Decide where the generated `sein_prayers` and `sein_knowledge_hub` books will be
  published, then add archive links from `prayers/` and `missions/`.
- Review `legal/imprint.html` and `legal/privacy.html` before production deployment,
  especially if analytics, donations, newsletters, or third-party embeds are added.
