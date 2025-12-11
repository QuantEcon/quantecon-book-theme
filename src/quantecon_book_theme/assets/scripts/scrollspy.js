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
  const stickyContainer = document.querySelector(".inner.sticky");
  if (!stickyContainer) {
    return;
  }

  const stickyToc = stickyContainer.querySelector("#bd-toc-nav");
  if (!stickyToc) {
    return;
  }

  // Check if autoexpand is enabled via data attribute
  const autoExpandEnabled = stickyContainer.dataset.autoexpand === "true";

  const tocLinks = stickyToc.querySelectorAll("a");
  if (tocLinks.length === 0) {
    return;
  }

  // Build a map of section IDs to their TOC links with hierarchy info
  const sections = [];
  // Get only top-level TOC items (direct children of the main ul)
  const topLevelUl = stickyToc.querySelector("ul");
  const topLevelItems = topLevelUl
    ? Array.from(topLevelUl.children).filter((el) => el.tagName === "LI")
    : [];

  tocLinks.forEach((link) => {
    const href = link.getAttribute("href");
    if (href && href.startsWith("#")) {
      const targetId = href.substring(1);
      const targetElement = document.getElementById(targetId);
      if (targetElement) {
        const listItem = link.parentElement;
        // Find which top-level item this link belongs to
        // Traverse up through ancestors to find a top-level item
        let topLevelParent = null;
        let current = listItem;
        while (current) {
          if (topLevelItems.includes(current)) {
            topLevelParent = current;
            break;
          }
          // Move to parent li
          current = current.parentElement;
          if (current) {
            current = current.closest("li");
          }
        }

        sections.push({
          id: targetId,
          element: targetElement,
          link: link,
          listItem: listItem,
          topLevelItem: topLevelParent,
        });
      }
    }
  });

  if (sections.length === 0) {
    return;
  }

  // Offset from top of viewport to consider a section "active"
  const OFFSET = 120;

  // Get the back-to-top button if it exists
  const backToTopBtn = document.querySelector(".back-to-top-btn");
  // Scroll threshold before showing the back-to-top button
  const BACK_TO_TOP_THRESHOLD = 300;

  /**
   * Update active state based on current scroll position
   */
  function updateActiveSection() {
    const scrollTop = window.scrollY || document.documentElement.scrollTop;
    const viewportHeight = window.innerHeight;
    let activeSection = null;

    // Show/hide back-to-top button based on scroll position
    if (backToTopBtn) {
      if (scrollTop > BACK_TO_TOP_THRESHOLD) {
        backToTopBtn.classList.add("visible");
      } else {
        backToTopBtn.classList.remove("visible");
      }
    }

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
    if (
      scrollTop + viewportHeight >=
      document.documentElement.scrollHeight - 50
    ) {
      activeSection = sections[sections.length - 1];
    }

    // First, clear all active classes
    sections.forEach((section) => {
      section.listItem.classList.remove("active");
      section.link.classList.remove("active");
    });

    // Clear expanded classes only if autoexpand is enabled
    if (autoExpandEnabled) {
      const allListItems = stickyToc.querySelectorAll("li");
      allListItems.forEach((li) => {
        li.classList.remove("expanded");
      });
    }

    // Now set active class on current section
    if (activeSection) {
      activeSection.listItem.classList.add("active");
      activeSection.link.classList.add("active");

      // Only do auto-expand logic if the feature is enabled
      if (autoExpandEnabled) {
        // Strategy: Expand all ancestors of the active item so it's visible,
        // AND expand the active item itself if it has children (to show its subsections)

        // Debug logging
        console.log("Active section:", activeSection.id);
        console.log("Active listItem:", activeSection.listItem);

        // 1. First, expand the active item itself if it has children
        // This ensures when you're on "4.2 Function Basics", you see 4.2.1, 4.2.2, etc.
        if (activeSection.listItem.querySelector(":scope > ul")) {
          activeSection.listItem.classList.add("expanded");
          console.log("Expanded active item (has children)");
        }

        // 2. Expand all ancestors from the active item up to the root
        // Start from the parent of the active item's li
        let parentUl = activeSection.listItem.parentElement;
        console.log("Starting parent traversal from:", parentUl);
        while (parentUl) {
          // parentUl is a <ul>, find its parent <li>
          let parentLi = parentUl.parentElement;
          console.log("parentLi:", parentLi, "tagName:", parentLi?.tagName);
          if (parentLi && parentLi.tagName === "LI") {
            // This li contains a ul (which contains our active item), so expand it
            parentLi.classList.add("expanded");
            console.log("Expanded parent li:", parentLi);
            // Move up to the next level
            parentUl = parentLi.parentElement;
          } else {
            // We've reached the top (nav element or similar)
            console.log("Reached top, breaking");
            break;
          }
        }
      }
    }
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
