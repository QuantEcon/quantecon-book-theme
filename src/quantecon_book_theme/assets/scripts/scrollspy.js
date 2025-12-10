/**
 * ScrollSpy Module
 * 
 * Tracks scroll position and highlights the active section in the TOC.
 * Based on: https://github.com/r3plica/Scrollspy
 */

/**
 * Initialize ScrollSpy for the table of contents
 */
export function initScrollSpy() {
  const tocContainer = document.querySelector(".sticky #bd-toc-nav ul");
  if (!tocContainer) {
    return; // Only activate if sticky TOC is enabled
  }

  // Use jQuery scrollspy plugin
  if (window.jQuery) {
    jQuery(tocContainer).scrollspy({
      activeClass: "active",
      offset: 100,
    });
  }
}

/**
 * ScrollSpy jQuery Plugin
 * Minified version from https://github.com/r3plica/Scrollspy
 */
!(function ($, window, document, undefined) {
  $.fn.extend({
    scrollspy: function (options) {
      var defaults = {
        namespace: "scrollspy",
        activeClass: "active",
        animate: false,
        duration: 1000,
        offset: 0,
        container: window,
        replaceState: false,
      };
      options = $.extend({}, defaults, options);
      var add = function (ex1, ex2) {
          return parseInt(ex1, 10) + parseInt(ex2, 10);
        },
        findElements = function (links) {
          var elements = [];
          for (var i = 0; i < links.length; i++) {
            var link = links[i],
              hash = $(link).attr("href"),
              element = $(hash);
            if (element.length > 0) {
              var top = Math.floor(element.offset().top),
                bottom = top + Math.floor(element.outerHeight());
              elements.push({
                element: element,
                hash: hash,
                top: top,
                bottom: bottom,
              });
            }
          }
          return elements;
        },
        findLink = function (links, hash) {
          for (var i = 0; i < links.length; i++) {
            var link = $(links[i]);
            if (link.attr("href") === hash) return link;
          }
        },
        resetClasses = function (links) {
          for (var i = 0; i < links.length; i++)
            $(links[i]).parent().removeClass(options.activeClass);
        },
        scrollArea = "";
      return this.each(function () {
        var element = this,
          container = $(options.container),
          links = $(element).find("a");
        for (var i = 0; i < links.length; i++) {
          var link = links[i];
          $(link).on("click", function (e) {
            var target = $(this).attr("href"),
              $target = $(target);
            if ($target.length > 0) {
              var top = add($target.offset().top, options.offset);
              if (options.animate) {
                $("html, body").animate({ scrollTop: top }, options.duration);
              } else {
                window.scrollTo(0, top);
              }
              e.preventDefault();
            }
          });
        }
        resetClasses(links);
        var elements = findElements(links),
          trackChanged = function () {
            var link,
              position = {
                top: add($(this).scrollTop(), Math.abs(options.offset)),
                left: $(this).scrollLeft(),
              };
            for (var i = 0; i < elements.length; i++) {
              var current = elements[i];
              if (position.top >= current.top && position.top < current.bottom) {
                var hash = current.hash;
                if ((link = findLink(links, hash))) {
                  if (options.onChange && scrollArea !== hash) {
                    options.onChange(current.element, $(element), position);
                    scrollArea = hash;
                  }
                  if (options.replaceState) {
                    history.replaceState({}, "", "/" + hash);
                  }
                  resetClasses(links);
                  link.parent().addClass(options.activeClass);
                  break;
                }
              }
            }
            if (!link && scrollArea !== "exit" && options.onExit) {
              options.onExit($(element), position);
              resetClasses(links);
              scrollArea = "exit";
              if (options.replaceState) {
                history.replaceState({}, "", "/");
              }
            }
          };
        container.bind("scroll." + options.namespace, function () {
          trackChanged();
        });
        $(document).ready(function (e) {
          trackChanged();
        });
      });
    },
  });
})(jQuery, window, document);
