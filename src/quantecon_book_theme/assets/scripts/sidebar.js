/**
 * Sidebar Module
 * Handles sidebar toggle and persistence
 */

export function initSidebar() {
  const $sidebar = $(".qe-sidebar");
  const $sidebarToggle = $(".btn__sidebar");

  function openSidebar() {
    $sidebarToggle.addClass("btn-active");
    $sidebar.removeClass("inactive");
    $(".qe-toolbar svg.feather.feather-menu").replaceWith(
      feather.icons.x.toSvg(),
    );
    localStorage.setSidebar = 1;
  }

  function closeSidebar() {
    $sidebarToggle.removeClass("btn-active");
    $sidebar.addClass("inactive");
    $(".qe-toolbar svg.feather.feather-x").replaceWith(
      feather.icons.menu.toSvg(),
    );
    localStorage.setSidebar = 0;
  }

  // Restore sidebar state from localStorage
  function setSidebar() {
    const setSidebar = localStorage.setSidebar;
    if (
      setSidebar == 1 &&
      $sidebar.hasClass("persistent") &&
      $(window).width() > 1340
    ) {
      openSidebar();
    }
  }

  setSidebar();

  // Toggle sidebar on button click
  $(document).on("click", ".btn__sidebar", function (event) {
    event.preventDefault();
    event.stopPropagation();
    if ($sidebar.hasClass("inactive")) {
      openSidebar();
    } else {
      closeSidebar();
    }
    if (window.innerWidth <= 1340) {
      $(document.body).on("click", function (e) {
        if (!$(event.target).is(".sidebar *")) {
          closeSidebar();
          $("body").off("click");
        }
      });
    }
  });
}
