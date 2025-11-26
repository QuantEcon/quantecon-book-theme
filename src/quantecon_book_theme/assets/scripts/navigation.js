/**
 * Fullscreen Module
 * Handles fullscreen toggle with cross-browser support
 */

export function initFullscreen() {
  $(".btn__fullscreen").on("click", function () {
    event.preventDefault();
    event.stopPropagation();
    $(this).toggleClass("btn-active");

    if (
      document.fullscreenElement ||
      document.webkitFullscreenElement ||
      document.mozFullScreenElement ||
      document.msFullscreenElement
    ) {
      // Currently in fullscreen, so exit
      if (document.exitFullscreen) {
        document.exitFullscreen();
      } else if (document.msExitFullscreen) {
        document.msExitFullscreen();
      } else if (document.mozCancelFullScreen) {
        document.mozCancelFullScreen();
      } else if (document.webkitExitFullscreen) {
        document.webkitExitFullscreen();
      }
    } else {
      // Not fullscreen, so enter
      if (document.documentElement.requestFullscreen) {
        document.documentElement.requestFullscreen();
      } else if (document.documentElement.webkitRequestFullscreen) {
        document.documentElement.webkitRequestFullscreen();
      } else if (document.documentElement.mozRequestFullScreen) {
        document.documentElement.mozRequestFullScreen();
      } else if (document.documentElement.msRequestFullscreen) {
        document.documentElement.msRequestFullscreen();
      }
    }
  });
}

/**
 * Back to Top Button
 */
export function initBackToTop() {
  $(".btn__top").on("click", function (event) {
    event.preventDefault();
    event.stopPropagation();
    $("html, body").animate({ scrollTop: 0 }, "slow");
  });

  // Intersection Observer for hiding 'Back To Top' when overlapping margins
  const Margin = document.getElementsByClassName("margin");
  const figCaption = document.querySelectorAll(
    "figure.margin-caption figcaption",
  );
  const BackToTop = document.getElementsByClassName("qe-page__toc-footer")[0];

  if (!BackToTop) return;

  const targetElements = Array.from(Margin).concat(Array.from(figCaption));

  const handleIntersection = (entries, observer) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        BackToTop.style.display = "none";
      } else {
        BackToTop.style.display = "";
      }
    });
  };

  const observer = new IntersectionObserver(handleIntersection, {
    root: null,
    rootMargin: "0px 0px -80% 0px",
  });

  Array.from(targetElements).forEach((el) => observer.observe(el));
}
