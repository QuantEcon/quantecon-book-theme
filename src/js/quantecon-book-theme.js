$(window).on('load', () => {

    // Avoid `console` errors in browsers that lack a console.
    (function() {
        var method;
        var noop = function () {};
        var methods = [
        'assert', 'clear', 'count', 'debug', 'dir', 'dirxml', 'error',
        'exception', 'group', 'groupCollapsed', 'groupEnd', 'info', 'log',
        'markTimeline', 'profile', 'profileEnd', 'table', 'time', 'timeEnd',
        'timeline', 'timelineEnd', 'timeStamp', 'trace', 'warn'
        ];
        var length = methods.length;
        var console = (window.console = window.console || {});

        while (length--) {
        method = methods[length];

        // Only stub undefined methods.
        if (!console[method]) {
            console[method] = noop;
        }
        }
    }());

    // Place any jQuery/helper plugins in here.

    var $window = $(window),
    $head = $('head'),
    $body = $('body'),
    $sidebar = $('.sidebar'),
    $sidebarToggle = $('.btn__sidebar');

    function setContrast() {
        var setContrast = localStorage.setContrast;
        if (setContrast == 1) {
            $body.addClass('dark-theme');
            $('.btn__contrast').addClass('btn-active');
        }
    }

    setContrast();

    $('.btn__contrast').on('click', function (event) {
        // Prevent default.
        event.preventDefault();
        event.stopPropagation();

        if ($(this).hasClass('btn-active')) {
            $(this).removeClass('btn-active');
            localStorage.setContrast = 0;
            $body.removeClass('dark-theme');
        } else {
            $(this).addClass('btn-active');
            localStorage.setContrast = 1;
            $body.addClass('dark-theme');
        }
    });

    // Sidebar toggles

    function openSidebar() {
        $sidebarToggle.addClass('btn-active');
        $sidebar.removeClass('inactive');
        $(".toolbar svg.feather.feather-menu").replaceWith(feather.icons.x.toSvg());
    }
    function closeSidebar() {
        $sidebarToggle.removeClass('btn-active');
        $sidebar.addClass('inactive');
        $(".toolbar svg.feather.feather-x").replaceWith(feather.icons.menu.toSvg());
    }

    $(document).on('click', '.btn__sidebar', function (event) {
        event.preventDefault();
        event.stopPropagation();
        if ($sidebar.hasClass('inactive')) {
            openSidebar();
        } else {
            closeSidebar();
        }
        if (window.innerWidth <= 1340) {
            $(document.body).on('click', function (e) {
                if (!$(event.target).is('.sidebar *')) {
                    closeSidebar();
                    $body.off('click');
                }
            });
        }
    });

    $('.btn__top').on('click', function (event) {
        event.preventDefault();
        event.stopPropagation();
        $('html, body').animate({ scrollTop: 0 }, 'slow');
    });

    $('.btn__fullscreen').on('click', function () {
        event.preventDefault();
        event.stopPropagation();
        $(this).toggleClass('btn-active');

        if (document.fullscreenElement || document.webkitFullscreenElement || document.mozFullScreenElement || document.msFullscreenElement) {
            //in fullscreen, so exit it
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
            //not fullscreen, so enter it
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

    function setFontSize() {
        // Get font size from local storage
        var toolbarFont = localStorage.toolbarFont;
        if (toolbarFont == 1) {
            $('html').addClass('font-plus');
        } else if (toolbarFont == -1) {
            $('html').addClass('font-minus');
        } else {
            $('html').removeClass('font-plus');
            $('html').removeClass('font-minus');
            localStorage.toolbarFont = 0;
        }
    }

    setFontSize();

    $('.btn__plus').on('click', function (event) {
        event.preventDefault();
        event.stopPropagation();
        var toolbarFont = parseInt(localStorage.getItem('toolbarFont')) + 1;
        if (toolbarFont > 0) {
            toolbarFont = 1;
        }
        localStorage.toolbarFont = toolbarFont;
        setFontSize();
    });

    $('.btn__minus').on('click', function (event) {
        event.preventDefault();
        event.stopPropagation();
        var toolbarFont = parseInt(localStorage.getItem('toolbarFont')) - 1;
        if (toolbarFont < 0) {
            toolbarFont = -1;
        }
        localStorage.toolbarFont = toolbarFont;
        setFontSize();
    });

    /* Collapsed code block */

    const collapsableCodeBlocks = document.querySelectorAll("div[class^='collapse'] .highlight");
    for (var i = 0; i < collapsableCodeBlocks.length; i++) {
        const toggleContainer = document.createElement('div');
        toggleContainer.innerHTML = '<a href="#" class="toggle toggle-less" style="display:none;"><span class="icon icon-angle-double-up"></span><em>Show less...</em></a><a href="#" class="toggle toggle-more"><span class="icon icon-angle-double-down"></span><em>Show more...</em></a>';
        collapsableCodeBlocks[i].parentNode.insertBefore(toggleContainer, collapsableCodeBlocks[i].nextSibling);
    }

    const collapsableCodeToggles = document.querySelectorAll("div[class^='collapse'] .toggle");
    for (var i = 0; i < collapsableCodeToggles.length; i++) {
        collapsableCodeToggles[i].addEventListener('click', function (e) {
            e.preventDefault();
            var codeBlock = this.closest('div[class^="collapse"]');
            if (codeBlock.classList.contains('expanded')) {
                codeBlock.classList.remove('expanded');
                this.style.display = 'none';
                this.nextSibling.style.display = 'block';
            } else {
                codeBlock.classList.add('expanded');
                this.style.display = 'none';
                this.previousSibling.style.display = 'block';
            }
        });
    }

    /* Wrap container around all tables allowing hirizontal scroll */

    const contentTables = document.querySelectorAll('.page__content table');
    for (var i = 0; i < contentTables.length; i++) {
        var wrapper = document.createElement('div');
        wrapper.classList.add('table-container');
        contentTables[i].parentNode.insertBefore(wrapper, contentTables[i]);
        wrapper.appendChild(contentTables[i]);
    }

    /* Download button dropdown */
    if ( document.getElementById('downloadButton') ) {
        const template = document.getElementById('downloadPDFModal');
        template.style.display = 'block';
        tippy('#downloadButton', {
            content: template,
            theme: 'light-border',
            animation: 'shift-away',
            inertia: true,
            duration: [200,200],
            arrow: true,
            arrowType: 'round',
            delay: [200, 200],
            interactive: true,
            trigger: "click"
        });
    }

    // Notebook Launcher popup
    if ( document.getElementById('settingsButton') ) {
        const template = document.getElementById('settingsModal');
        template.style.display = 'block';
        tippy('#settingsButton', {
        content: template,
        theme: 'light-border',
        animation: 'shift-away',
        inertia: true,
        duration: [200,200],
        arrow: true,
        arrowType: 'round',
        delay: [200, 200],
        interactive: true,
        trigger: "click"
        });
    }

    // onchangeListener for launcher popup
    window.onChangeListener = () => {
        // let private = document.getElementById("launcher-private-input").value
        // if ($(this.event.currentTarget)[0].getAttribute("id").indexOf("private") > -1) {
        //     let pagename = document.getElementsByClassName("page")[0].getAttribute("id")
        //     const repoPrefix = "/jupyter/hub/user-redirect/git-pull?repo=https://github.com/QuantEcon/quantecon-notebooks-datascience&urlpath=lab/tree/quantecon-notebooks-datascience/";
        //     url = private + repoPrefix + pagename + ".ipynb";
        //     launchButton.getElementsByTagName("a")[0].setAttribute("href", url)
        // } else {
        let url = document.getElementById("launcher-public-input").value
        let launchButton = document.getElementById("launchButton")
        launchButton.getElementsByTagName("a")[0].setAttribute("href", url)
    }

    window.MathJax = {
        loader: {load: ['[tex]/boldsymbol']},
        tex: {packages: {'[+]': ['boldsymbol']}},
        tex: {
            inlineMath: [
                ['$', '$'],
                ['\\(', '\\)'],
            ],
            processEscapes: true
        },
        chtml: {
            scale: 0.92,
            displayAlign: "center"
        },
        svg: {
            scale: 0.92,
            displayAlign: "center",
        },
        options: {
            menuOptions: {
                settings: {
                    renderer: 'SVG'
                }
            }
        },
    };

})
