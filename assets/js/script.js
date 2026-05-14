const navToggle = document.querySelector(".nav-toggle");
const navLinks = document.querySelectorAll(".site-nav a");
const navGroups = document.querySelectorAll(".nav-group");
const contactForm = document.querySelector("#contact-form");
const formNote = document.querySelector("#form-note");
const sectionLinks = document.querySelectorAll("[data-section-link]");
const siteLinks = {
  "knowledge-hub": "https://ywp-sein.github.io/sein_knowledge_hub/index.html",
};

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
