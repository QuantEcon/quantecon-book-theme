/**
 * Popups Module
 * Handles Tippy.js popups for downloads, settings, and tooltips
 */

export function initPopups() {
  // Download PDF popup
  if (document.getElementById("downloadButton")) {
    const template = document.getElementById("downloadPDFModal");
    template.style.display = "block";
    tippy("#downloadButton", {
      content: template,
      theme: "light-border",
      animation: "shift-away",
      inertia: true,
      duration: [200, 200],
      arrow: true,
      delay: [200, 200],
      interactive: true,
      trigger: "click",
    });
  }

  // Notebook Launcher popup
  if (document.getElementById("settingsButton")) {
    const template = document.getElementById("settingsModal");
    template.style.display = "block";
    tippy("#settingsButton", {
      content: template,
      theme: "light-border",
      animation: "shift-away",
      inertia: true,
      duration: [200, 200],
      arrow: true,
      delay: [200, 200],
      interactive: true,
      trigger: "click",
    });
  }

  // General tooltips
  tippy("[data-tippy-content]", {
    touch: false,
  });
}

/**
 * Launcher Settings
 * Handles the notebook launcher URL configuration
 */
export function initLauncherSettings() {
  window.onChangeListener = () => {
    let privateInput = document.getElementById("launcher-private-input").value;
    if (
      $(this.event.currentTarget)[0].getAttribute("id").indexOf("private") > -1
    ) {
      if (!privateInput.includes("http") && !privateInput.includes("https")) {
        privateInput = "http://" + privateInput;
      }
      const pagename = document
        .getElementsByClassName("page")[0]
        .getAttribute("id");
      const repo = document.getElementById("launcher-private-input").dataset
        .repourl;
      const urlpath = document.getElementById("launcher-private-input").dataset
        .urlpath;
      const repoPrefix =
        "/user-redirect/git-pull?repo=" + repo + "&urlpath=" + urlpath;
      const url = privateInput + repoPrefix + pagename + ".ipynb";
      launchButton.getElementsByTagName("a")[0].setAttribute("href", url);
    } else {
      const url = document.getElementById("launcher-public-input").value;
      const launchButton = document.getElementById("launchButton");
      launchButton.getElementsByTagName("a")[0].setAttribute("href", url);
    }
  };
}
