/**
 * Theme Settings Module
 * Handles dark mode/contrast toggle and persistence
 */

export function initThemeSettings() {
  const $body = $("body");
  const $lightLogo = $(".logo-img");
  const $darkLogo = $(".dark-logo-img");

  // Set contrast from localStorage on page load
  function setContrast() {
    const setContrast = localStorage.setContrast;
    if (setContrast == 1) {
      $body.addClass("dark-theme");
      $(".btn__contrast").addClass("btn-active");
    }
  }

  setContrast();

  // Toggle contrast/dark mode
  $(".btn__contrast").on("click", function (event) {
    event.preventDefault();
    event.stopPropagation();

    if ($(this).hasClass("btn-active")) {
      $(this).removeClass("btn-active");
      localStorage.setContrast = 0;
      $body.removeClass("dark-theme");
    } else {
      $(this).addClass("btn-active");
      localStorage.setContrast = 1;
      $body.addClass("dark-theme");
      if (!$darkLogo.length) {
        $lightLogo.css("display", "block");
      }
    }
  });
}

/**
 * Font Size Module
 * Handles font size adjustment and persistence
 */

export function initFontSize() {
  function setFontSize() {
    const toolbarFont = localStorage.toolbarFont;
    if (toolbarFont == 1) {
      $("html").addClass("font-plus");
    } else if (toolbarFont == -1) {
      $("html").addClass("font-minus");
    } else {
      $("html").removeClass("font-plus");
      $("html").removeClass("font-minus");
      localStorage.toolbarFont = 0;
    }
  }

  setFontSize();

  $(".btn__plus").on("click", function (event) {
    event.preventDefault();
    event.stopPropagation();
    let toolbarFont = parseInt(localStorage.getItem("toolbarFont")) + 1;
    if (toolbarFont > 0) {
      toolbarFont = 1;
    }
    localStorage.toolbarFont = toolbarFont;
    setFontSize();
  });

  $(".btn__minus").on("click", function (event) {
    event.preventDefault();
    event.stopPropagation();
    let toolbarFont = parseInt(localStorage.getItem("toolbarFont")) - 1;
    if (toolbarFont < 0) {
      toolbarFont = -1;
    }
    localStorage.toolbarFont = toolbarFont;
    setFontSize();
  });
}
