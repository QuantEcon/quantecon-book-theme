/**
 * Search Module
 * Handles toolbar search functionality
 */

export function initSearch() {
  $("#search-icon").on("click", function (event) {
    if ($("#search-input").hasClass("search-open")) {
      $("#search-input").closest("form").trigger("submit");
    } else {
      $("#search-input").addClass("search-open").focus();
      $(this).css("pointer-events", "none");
    }
  });

  $("#search-input").on("focusout", function () {
    if (!$(this).val()) {
      $(this).removeClass("search-open");
      $("#search-icon").css("pointer-events", "auto");
    }
  });

  // Remove the search hint
  const forms = document.querySelectorAll("form.bd-search");
  forms.forEach((f) => {
    const hint = f.querySelector(".search-button__kbd-shortcut");
    if (hint) {
      hint.remove();
    }
  });
}
