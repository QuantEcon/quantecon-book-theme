/**
 * Stderr Warnings Module
 * Handles collapsible stderr output display
 */

export function initStderrWarnings() {
  // Find all cell outputs that contain stderr
  const cellOutputs = document.querySelectorAll(".cell_output");

  cellOutputs.forEach((cellOutput) => {
    const stderrElements = cellOutput.querySelectorAll(".output.stderr");

    if (stderrElements.length === 0) return;

    // Create wrapper structure for collapsible stderr
    const wrapper = document.createElement("div");
    wrapper.className = "stderr-collapsible-wrapper";

    // Create toggle button
    const toggleButton = document.createElement("button");
    toggleButton.className = "stderr-toggle-button";
    toggleButton.setAttribute("aria-expanded", "false");
    toggleButton.setAttribute("aria-label", "Show code warnings");
    toggleButton.innerHTML =
      '<span class="stderr-icon">⚠</span> <span class="stderr-label">Code warnings</span> <span class="stderr-chevron">▶</span>';

    // Create content container
    const contentContainer = document.createElement("div");
    contentContainer.className = "stderr-content";
    contentContainer.setAttribute("aria-hidden", "true");

    // Move all stderr elements into the content container
    stderrElements.forEach((stderr) => {
      contentContainer.appendChild(stderr.cloneNode(true));
      stderr.remove();
    });

    // Assemble the structure
    wrapper.appendChild(toggleButton);
    wrapper.appendChild(contentContainer);

    // Insert the wrapper at the beginning of the cell output
    cellOutput.insertBefore(wrapper, cellOutput.firstChild);

    // Add toggle functionality
    toggleButton.addEventListener("click", function (e) {
      e.preventDefault();
      const isExpanded = toggleButton.getAttribute("aria-expanded") === "true";

      if (isExpanded) {
        // Collapse
        toggleButton.setAttribute("aria-expanded", "false");
        toggleButton.setAttribute("aria-label", "Show code warnings");
        contentContainer.setAttribute("aria-hidden", "true");
        contentContainer.classList.remove("expanded");
      } else {
        // Expand
        toggleButton.setAttribute("aria-expanded", "true");
        toggleButton.setAttribute("aria-label", "Hide code warnings");
        contentContainer.setAttribute("aria-hidden", "false");
        contentContainer.classList.add("expanded");
      }
    });
  });
}
