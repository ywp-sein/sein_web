# SEiN Website

The open-source main website for SEiN, an initiative to end social issues
through Christ. Homelessness in Berlin is the current mission, not the whole
boundary of the work.

This version is intentionally lightweight:

- `index.html` is the landing page.
- `about/` contains the About SEiN overview, Why SEiN, and About Us pages.
- `missions/` contains the Missions overview.
- `missions/homelessness/` contains the Ending Homelessness mission page,
  How It Begins, and its action subpages: Awakening Hope, Knowledge Hub,
  A Step Forward PoC, and Compassion Voucher PoC.
- `prayers/` contains the generated prayers blog.
- `contact/` contains the contact page.
- `legal/` contains Imprint and Privacy Policy pages.
- `assets/` contains shared CSS, JavaScript, and media.
- `assets/js/script.js` renders the shared `<site-header>` and `<site-footer>`
  components used by every page.
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
publishes the repository root as a static GitHub Pages site for
`https://sein-live.com/`.

In GitHub, keep Pages configured to use **GitHub Actions** as the source. After
pushing to `main`, check the `Deploy GitHub Pages` workflow run. The public URL
will be shown in that run after deployment succeeds.

## Update the prayers blog

After adding a new weekly prayer to `../sein_prayers/src/weekly/` and listing it
in `../sein_prayers/src/SUMMARY.md`, run the update script and the latest entry
will appear in `prayers/index.html`:

```bash
python3 tools/update_prayers.py
```

For automatic local updates while editing prayer files, run:

```bash
python3 tools/watch_prayers.py
```

## Contact form

The contact form submits through FormSubmit from `assets/js/script.js`.
`formSubmitToken` is a public frontend token provided by FormSubmit after
activating the form for `https://sein-live.com/`; it is not a private secret,
because all browser JavaScript can be viewed by visitors. Keep the token in the
script for direct delivery, and update `contact@sein-live.com` only if the
fallback email address changes.

## Inner page header with image

Use this template on non-landing pages when a page needs an image beside the H1.
Place local title images under `assets/media/title_images/` and keep
descriptive alt text.

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

## Long content section

Use this one-column template when the section text is long and should read like
an article: title first, content directly after it.

```html
<section class="section content-section" id="example" aria-labelledby="example-title">
  <div>
    <p class="eyebrow">Section Label</p>
    <h2 id="example-title">Section title.</h2>
  </div>
  <div class="prose-panel">
    <p>Long-form content goes here.</p>
  </div>
</section>
```

## Next content to add

- Decide where the generated `sein_prayers` book will be published, then add
  published links from `prayers/`.
- Review `legal/imprint.html` and `legal/privacy.html` before production deployment,
  especially if analytics, donations, newsletters, or third-party embeds are added.
- Update the Knowledge Hub URL in `assets/js/script.js` when its custom domain changes.
