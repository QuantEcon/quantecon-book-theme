/**
 * Language Switcher
 *
 * Toggle dropdown for switching between language versions of a site.
 * Handles open/close, keyboard navigation, and click-outside-to-close.
 */

export function initLanguageSwitcher() {
  const switchers = document.querySelectorAll(".language-switcher");

  switchers.forEach((switcher) => {
    const toggle = switcher.querySelector(".language-switcher__toggle");
    const menu = switcher.querySelector(".language-switcher__menu");

    if (!toggle || !menu) return;

    // Toggle menu on button click
    toggle.addEventListener("click", (e) => {
      e.stopPropagation();
      const isOpen = menu.classList.contains("is-open");
      closeAllMenus();
      if (!isOpen) {
        menu.classList.add("is-open");
        toggle.setAttribute("aria-expanded", "true");
      }
    });

    // Keyboard support
    toggle.addEventListener("keydown", (e) => {
      if (e.key === "Escape") {
        menu.classList.remove("is-open");
        toggle.setAttribute("aria-expanded", "false");
        toggle.focus();
      }
    });

    menu.addEventListener("keydown", (e) => {
      if (e.key === "Escape") {
        menu.classList.remove("is-open");
        toggle.setAttribute("aria-expanded", "false");
        toggle.focus();
      }
    });
  });

  // Close all menus when clicking outside
  document.addEventListener("click", () => {
    closeAllMenus();
  });

  function closeAllMenus() {
    document.querySelectorAll(".language-switcher__menu.is-open").forEach((m) => {
      m.classList.remove("is-open");
    });
    document
      .querySelectorAll('.language-switcher__toggle[aria-expanded="true"]')
      .forEach((t) => {
        t.setAttribute("aria-expanded", "false");
      });
  }
}
