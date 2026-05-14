const siteLinks = {
  "knowledge-hub": "https://ywp-sein.github.io/sein_knowledge_hub/index.html",
};

const normalizePath = (path) => {
  const cleanPath = path.replace(/^\/sein_web(?=\/|$)/, "") || "/";
  return cleanPath.endsWith("/index.html")
    ? cleanPath.replace(/index\.html$/, "")
    : cleanPath;
};

const currentPath = normalizePath(window.location.pathname);
const currentAttr = (href, section = href) => {
  const cleanHref = normalizePath(href);
  const inSection = section && currentPath.startsWith(normalizePath(section));

  return currentPath === cleanHref || inSection ? ' aria-current="page"' : "";
};

const renderHeader = () => `
  <header class="site-header">
    <a class="brand" href="/" aria-label="SEiN home">
      <img class="brand-logo" src="/assets/media/logo/logo_cross_white.png" alt="SEiN - Save Everyone in Need">
    </a>
    <button class="nav-toggle" type="button" aria-expanded="false" aria-controls="site-nav">
      <span class="sr-only">Toggle navigation</span>
      <span></span>
      <span></span>
      <span></span>
    </button>
    <nav class="site-nav" id="site-nav" aria-label="Primary navigation">
      <a href="/"${currentAttr("/", "")}>Home</a>
      <div class="nav-group">
        <a href="/about/"${currentAttr("/about/", "/about/")}>About</a>
        <div class="sub-nav" aria-label="About pages">
          <a href="/about/why-sein.html"${currentAttr("/about/why-sein.html", "")}>Why SEiN</a>
          <a href="/about/us.html"${currentAttr("/about/us.html", "")}>About Us</a>
        </div>
      </div>
      <a href="/prayers/"${currentAttr("/prayers/", "/prayers/")}>Prayers</a>
      <div class="nav-group">
        <a href="/missions/"${currentAttr("/missions/", "/missions/")}>Missions</a>
        <div class="sub-nav mission-sub-nav" aria-label="Mission pages">
          <a href="/missions/"${currentAttr("/missions/", "")}>Mission Overview</a>
          <div class="sub-nav-section">
            <span class="sub-nav-label">Ending Homelessness</span>
            <div class="sub-nav-nested">
              <a href="/missions/homelessness/how-it-begins.html"${currentAttr("/missions/homelessness/how-it-begins.html", "")}>How It Begins</a>
              <a href="/missions/homelessness/"${currentAttr("/missions/homelessness/", "")}>Overview</a>
              <a href="/missions/homelessness/awakening-hope.html"${currentAttr("/missions/homelessness/awakening-hope.html", "")}>01 Awakening Hope</a>
              <a href="/missions/homelessness/knowledge-hub.html"${currentAttr("/missions/homelessness/knowledge-hub.html", "")}>02 Knowledge Hub</a>
              <a href="/missions/homelessness/a-step-forward-poc.html"${currentAttr("/missions/homelessness/a-step-forward-poc.html", "")}>03 A Step Forward PoC</a>
              <a href="/missions/homelessness/compassion-voucher-poc.html"${currentAttr("/missions/homelessness/compassion-voucher-poc.html", "")}>04 Compassion Voucher PoC</a>
            </div>
          </div>
        </div>
      </div>
      <a href="/contact/"${currentAttr("/contact/", "/contact/")}>Contact</a>
    </nav>
  </header>
`;

const renderFooter = () => `
  <footer class="site-footer">
    <p>© 2026 Yuan-Wei Pi. All rights reserved.</p>
    <p>
      <a href="/">Home</a>
      <a href="/about/">About</a>
      <a href="/prayers/">Prayers</a>
      <a href="/missions/">Missions</a>
      <a href="/contact/">Contact</a>
      <a href="/legal/imprint.html">Imprint</a>
      <a href="/legal/privacy.html">Privacy policy</a>
    </p>
  </footer>
`;

customElements.define(
  "site-header",
  class extends HTMLElement {
    connectedCallback() {
      this.outerHTML = renderHeader();
    }
  },
);

customElements.define(
  "site-footer",
  class extends HTMLElement {
    connectedCallback() {
      this.outerHTML = renderFooter();
    }
  },
);

const navToggle = document.querySelector(".nav-toggle");
const navLinks = document.querySelectorAll(".site-nav a");
const navGroups = document.querySelectorAll(".nav-group");
const contactForm = document.querySelector("#contact-form");
const formNote = document.querySelector("#form-note");
const sectionLinks = document.querySelectorAll("[data-section-link]");

document.querySelectorAll("[data-site-link]").forEach((link) => {
  const href = siteLinks[link.dataset.siteLink];

  if (href) {
    link.href = href;

    if (link.dataset.siteLinkLabel === "url") {
      link.textContent = href;
    }
  }
});

if (navToggle) {
  navToggle.addEventListener("click", () => {
    const isOpen = document.body.classList.toggle("nav-open");
    navToggle.setAttribute("aria-expanded", String(isOpen));
  });
}

navLinks.forEach((link) => {
  link.addEventListener("click", () => {
    if (link.parentElement?.classList.contains("nav-group") && window.innerWidth > 880) {
      return;
    }

    document.body.classList.remove("nav-open");
    navToggle?.setAttribute("aria-expanded", "false");
    navGroups.forEach((group) => group.classList.remove("is-open"));
  });
});

navGroups.forEach((group) => {
  const trigger = group.querySelector(":scope > a");

  trigger?.addEventListener("click", (event) => {
    if (window.innerWidth <= 880) {
      return;
    }

    if (!group.classList.contains("is-open")) {
      event.preventDefault();
      navGroups.forEach((other) => {
        if (other !== group) {
          other.classList.remove("is-open");
        }
      });
      group.classList.add("is-open");
    }
  });
});

document.addEventListener("click", (event) => {
  if (!event.target.closest(".site-nav")) {
    navGroups.forEach((group) => group.classList.remove("is-open"));
  }
});

if (contactForm) {
  contactForm.addEventListener("submit", (event) => {
    event.preventDefault();

    const data = new FormData(contactForm);
    const name = String(data.get("name") || "").trim();
    const email = String(data.get("email") || "").trim();
    const message = String(data.get("message") || "").trim();

    const subject = encodeURIComponent(`SEiN contact from ${name}`);
    const body = encodeURIComponent(`${message}\n\nFrom: ${name}\nEmail: ${email}`);

    window.location.href = `mailto:contact@sein-live.com?subject=${subject}&body=${body}`;
    formNote.textContent = "Your email app should open with the message prepared.";
  });
}

if (sectionLinks.length) {
  const sectionIds = [...sectionLinks].map((link) => link.dataset.sectionLink);
  const sections = sectionIds
    .map((id) => document.getElementById(id))
    .filter(Boolean);

  const setActiveSection = (id) => {
    sectionLinks.forEach((link) => {
      link.classList.toggle("is-active", link.dataset.sectionLink === id);
    });
  };

  const observer = new IntersectionObserver(
    (entries) => {
      const visible = entries
        .filter((entry) => entry.isIntersecting)
        .sort((a, b) => b.intersectionRatio - a.intersectionRatio)[0];

      if (visible) {
        setActiveSection(visible.target.id);
      }
    },
    {
      rootMargin: "-30% 0px -45% 0px",
      threshold: [0.1, 0.35, 0.6],
    },
  );

  sections.forEach((section) => observer.observe(section));
  setActiveSection(sections[0]?.id || sectionIds[0]);
}
