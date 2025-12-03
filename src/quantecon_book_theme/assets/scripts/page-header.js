/**
 * Page Header Module
 * Handles author links and changelog functionality
 */

export function initPageHeader() {
  // Add authors to the heading of toc page
  const authors = document.getElementsByClassName("qe-page__header-authors")[0];
  if (!authors) return;

  const fontSize = authors.getAttribute("font-size");
  const h1 = document.querySelector(".main-index h1");

  // Check if its the main toc page
  if (!h1) return;

  // Creating a p tag for styling and author links
  const newParagraph = document.createElement("p");
  newParagraph.setAttribute("id", "qe-page-author-links");
  newParagraph.setAttribute(
    "style",
    fontSize ? `font-size: ${fontSize}px` : "",
  );

  // Check if there are authors
  const isAuthor =
    authors &&
    ((authors.querySelectorAll("a").length &&
      authors.querySelectorAll("a")[0].innerText !== "") ||
      authors.innerText !== "");

  if (isAuthor) {
    newParagraph.innerHTML = authors.innerHTML;
  }

  // Insert p tag after h1, even if no authors for styling
  h1.insertAdjacentElement("afterend", newParagraph);
}

/**
 * Changelog Toggle
 * Handles the collapsible changelog section
 */
export function initChangelog() {
  const toggleButton = document.getElementById("changelog-toggle");
  const changelogContent = document.getElementById("changelog-content");

  if (!toggleButton || !changelogContent) return;

  toggleButton.addEventListener("click", function (e) {
    e.preventDefault();
    const isExpanded = toggleButton.getAttribute("aria-expanded") === "true";

    if (isExpanded) {
      // Collapse
      toggleButton.setAttribute("aria-expanded", "false");
      changelogContent.setAttribute("aria-hidden", "true");
      changelogContent.classList.remove("expanded");
    } else {
      // Expand
      toggleButton.setAttribute("aria-expanded", "true");
      changelogContent.setAttribute("aria-hidden", "false");
      changelogContent.classList.add("expanded");
    }
  });

  // Close on escape key
  document.addEventListener("keydown", function (e) {
    if (
      e.key === "Escape" &&
      toggleButton.getAttribute("aria-expanded") === "true"
    ) {
      toggleButton.setAttribute("aria-expanded", "false");
      changelogContent.setAttribute("aria-hidden", "true");
      changelogContent.classList.remove("expanded");
    }
  });
}
