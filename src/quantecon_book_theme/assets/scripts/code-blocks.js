/**
 * Code Blocks Module
 * Handles collapsible code blocks
 */

export function initCollapsibleCode() {
  const collapseAccToHeight = (classList, elH) => {
    for (let className of classList) {
      if (className.startsWith("tag_collapse-")) {
        const index = className.indexOf("-");
        const height = className.substring(index + 1);
        if (height && !isNaN(height)) {
          elH.style.height = parseInt(height) + 0.5 + "em";
          return true;
        }
      }
    }
    return false;
  };

  const collapsableCodeBlocks = document.querySelectorAll(
    "div.cell[class*='tag_collapse']",
  );

  for (let i = 0; i < collapsableCodeBlocks.length; i++) {
    const collapsableCodeBlocksH =
      collapsableCodeBlocks[i].querySelectorAll(".highlight")[0];

    if (collapsableCodeBlocksH) {
      // Apply initial height based on collapse class
      collapseAccToHeight(
        collapsableCodeBlocks[i].classList,
        collapsableCodeBlocksH,
      );

      const toggleBar = document.createElement("div");
      toggleBar.className = "collapse-toggle-bar";
      toggleBar.innerHTML = '<span class="collapse-indicator">Expand</span>';
      collapsableCodeBlocksH.parentNode.insertBefore(
        toggleBar,
        collapsableCodeBlocksH.nextSibling,
      );
    }
  }

  const collapsableCodeToggles = document.querySelectorAll(
    "div.cell[class*='tag_collapse'] .collapse-toggle-bar",
  );

  for (let i = 0; i < collapsableCodeToggles.length; i++) {
    collapsableCodeToggles[i].addEventListener("click", function (e) {
      e.preventDefault();
      const codeBlock = this.closest("div.cell[class*='tag_collapse']");
      const codeBlockH = codeBlock.querySelector(".highlight");
      const indicator = this.querySelector(".collapse-indicator");

      if (codeBlock.classList.contains("expanded")) {
        codeBlock.classList.remove("expanded");
        indicator.textContent = "Expand";
        collapseAccToHeight(codeBlock.classList, codeBlockH);

        // Smart scroll behavior
        setTimeout(() => {
          codeBlock.scrollIntoView({ behavior: "smooth", block: "end" });
        }, 50);
      } else {
        codeBlock.classList.add("expanded");
        indicator.textContent = "Collapse";
        codeBlockH.style.height = "auto";
      }
    });
  }
}

/**
 * Table Container
 * Wraps tables for horizontal scroll support
 */
export function initTableContainers() {
  const contentTables = document.querySelectorAll(".qe-page__content table");
  for (let i = 0; i < contentTables.length; i++) {
    const wrapper = document.createElement("div");
    wrapper.classList.add("table-container");
    contentTables[i].parentNode.insertBefore(wrapper, contentTables[i]);
    wrapper.appendChild(contentTables[i]);
  }
}
