/**
 * ScrollSpy Module - Tracks scroll position and highlights active TOC items
 *
 * This module provides scroll tracking functionality for the sticky table of contents.
 * It highlights the currently visible section in the TOC as the user scrolls.
 */

/**
 * Initialize ScrollSpy for the sticky table of contents
 * Only activates when the .sticky class is present on the TOC inner container
 */
export function initScrollSpy() {
  // Only initialize if sticky TOC is enabled
  const stickyToc = document.querySelector(".inner.sticky #bd-toc-nav");
  if (!stickyToc) {
    return;
  }

  const tocLinks = stickyToc.querySelectorAll("a");
  if (tocLinks.length === 0) {
    return;
  }

  // Build a map of section IDs to their TOC links
  const sections = [];

  tocLinks.forEach((link) => {
    const href = link.getAttribute("href");
    if (href && href.startsWith("#")) {
      const targetId = href.substring(1);
      const targetElement = document.getElementById(targetId);
      if (targetElement) {
        sections.push({
          id: targetId,
          element: targetElement,
          link: link,
        });
      }
    }
  });

  if (sections.length === 0) {
    return;
  }

  // Offset from top of viewport to consider a section "active"
  const OFFSET = 120;

  /**
   * Update active state based on current scroll position
   */
  function updateActiveSection() {
    const scrollTop = window.scrollY || document.documentElement.scrollTop;
    const viewportHeight = window.innerHeight;
    let activeSection = null;

    // Find the section that is currently in view
    // We iterate through sections and find the last one whose top is above the threshold
    for (let i = 0; i < sections.length; i++) {
      const section = sections[i];
      const rect = section.element.getBoundingClientRect();
      const sectionTop = rect.top + scrollTop;

      // Section is considered active if its top is above the offset threshold
      if (sectionTop <= scrollTop + OFFSET) {
        activeSection = section;
      } else {
        // Since sections are in order, once we find one below threshold, stop
        break;
      }
    }

    // If we're near the bottom of the page, activate the last section
    if (scrollTop + viewportHeight >= document.documentElement.scrollHeight - 50) {
      activeSection = sections[sections.length - 1];
    }

    // Update active classes
    sections.forEach((section) => {
      const listItem = section.link.parentElement;
      if (section === activeSection) {
        listItem.classList.add("active");
        section.link.classList.add("active");
      } else {
        listItem.classList.remove("active");
        section.link.classList.remove("active");
      }
    });
  }

  // Throttle scroll events for better performance
  let ticking = false;

  function onScroll() {
    if (!ticking) {
      window.requestAnimationFrame(() => {
        updateActiveSection();
        ticking = false;
      });
      ticking = true;
    }
  }

  // Listen for scroll events
  window.addEventListener("scroll", onScroll, { passive: true });

  // Initial update
  updateActiveSection();
}
