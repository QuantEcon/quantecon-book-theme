"""
Tests for the modular SCSS and JavaScript structure.
Verifies that all module files exist and are properly organized.
"""

import pytest
from pathlib import Path


class TestSCSSModuleStructure:
    """Test that all SCSS modules exist and are properly structured."""

    EXPECTED_SCSS_MODULES = [
        "_admonitions.scss",
        "_autodoc.scss",
        "_base.scss",
        "_breakpoints.scss",
        "_code.scss",
        "_colors.scss",
        "_content.scss",
        "_dark-theme.scss",
        "_dropdown.scss",
        "_footnotes.scss",
        "_html5boilerplate.scss",
        "_margin.scss",
        "_modals.scss",
        "_normalize.scss",
        "_page.scss",
        "_quantecon-defaults.scss",
        "_rtl.scss",
        "_sidebar.scss",
        "_stderr.scss",
        "_syntax.scss",
        "_tippy-themes.scss",
        "_toolbar.scss",
        "index.scss",
    ]

    def test_all_scss_modules_exist(self, styles_dir):
        """Verify all expected SCSS modules exist."""
        for module in self.EXPECTED_SCSS_MODULES:
            module_path = styles_dir / module
            assert module_path.exists(), f"Missing SCSS module: {module}"

    def test_index_scss_imports_modules(self, styles_dir):
        """Verify index.scss forwards all component modules."""
        index_content = (styles_dir / "index.scss").read_text()

        # Check for @forward directives for key modules
        expected_forwards = [
            "base",
            "dark-theme",
            "toolbar",
            "sidebar",
            "page",
            "content",
            "admonitions",
            "footnotes",
            "stderr",
            "modals",
            "autodoc",
        ]

        for module in expected_forwards:
            assert (
                f'@forward "{module}"' in index_content
            ), f"index.scss missing @forward for {module}"

    def test_scss_modules_use_sass_module_syntax(self, styles_dir):
        """Verify SCSS modules use modern @use syntax for dependencies."""
        modules_with_colors = ["_base.scss", "_dark-theme.scss", "_toolbar.scss"]

        for module in modules_with_colors:
            module_path = styles_dir / module
            if module_path.exists():
                content = module_path.read_text()
                # Should use @use for colors, not @import
                if "colors." in content or "colors.$" in content:
                    assert '@use "colors"' in content, (
                        f"{module} should use @use for colors module"
                    )


class TestJavaScriptModuleStructure:
    """Test that all JavaScript modules exist and are properly structured."""

    EXPECTED_JS_MODULES = [
        "code-blocks.js",
        "index.js",
        "navigation.js",
        "page-header.js",
        "popups.js",
        "search.js",
        "sidebar.js",
        "stderr-warnings.js",
        "theme-settings.js",
    ]

    def test_all_js_modules_exist(self, scripts_dir):
        """Verify all expected JavaScript modules exist."""
        for module in self.EXPECTED_JS_MODULES:
            module_path = scripts_dir / module
            assert module_path.exists(), f"Missing JavaScript module: {module}"

    def test_index_js_imports_all_modules(self, scripts_dir):
        """Verify index.js imports all feature modules."""
        index_content = (scripts_dir / "index.js").read_text()

        expected_imports = [
            "theme-settings.js",
            "sidebar.js",
            "search.js",
            "navigation.js",
            "code-blocks.js",
            "popups.js",
            "page-header.js",
            "stderr-warnings.js",
        ]

        for module in expected_imports:
            assert (
                module in index_content
            ), f"index.js missing import for {module}"

    def test_js_modules_export_functions(self, scripts_dir):
        """Verify JavaScript modules export their functions."""
        modules_to_check = {
            "theme-settings.js": ["initThemeSettings", "initFontSize"],
            "sidebar.js": ["initSidebar"],
            "search.js": ["initSearch"],
            "navigation.js": ["initFullscreen", "initBackToTop"],
            "code-blocks.js": ["initCollapsibleCode", "initTableContainers"],
            "popups.js": ["initPopups", "initLauncherSettings"],
            "page-header.js": ["initPageHeader", "initChangelog"],
            "stderr-warnings.js": ["initStderrWarnings"],
        }

        for module, exports in modules_to_check.items():
            module_path = scripts_dir / module
            content = module_path.read_text()
            for export in exports:
                assert (
                    f"export function {export}" in content
                    or f"export {{ {export}" in content
                ), f"{module} should export {export}"

    def test_no_console_polyfill(self, scripts_dir):
        """Verify the obsolete console polyfill has been removed."""
        index_content = (scripts_dir / "index.js").read_text()

        # The old polyfill had this pattern
        assert "window.console = window.console || {}" not in index_content
        assert "var noop = function () {}" not in index_content


class TestLayoutTemplate:
    """Test the layout.html template configuration."""

    def test_preconnect_hints_present(self, theme_dir):
        """Verify preconnect hints are present for performance."""
        layout_content = (theme_dir / "layout.html").read_text()

        expected_preconnects = [
            "https://unpkg.com",
            "https://cdn.jsdelivr.net",
            "https://fonts.googleapis.com",
            "https://fonts.gstatic.com",
        ]

        for url in expected_preconnects:
            assert f'<link rel="preconnect" href="{url}"' in layout_content, (
                f"Missing preconnect hint for {url}"
            )

    def test_sri_hashes_present(self, theme_dir):
        """Verify SRI hashes are present on CDN scripts."""
        layout_content = (theme_dir / "layout.html").read_text()

        # Check that integrity attributes are present
        assert 'integrity="sha384-' in layout_content
        assert 'crossorigin="anonymous"' in layout_content

    def test_external_scripts_loaded(self, theme_dir):
        """Verify external scripts are loaded from CDN."""
        layout_content = (theme_dir / "layout.html").read_text()

        expected_scripts = [
            "@popperjs/core",
            "tippy.js",
            "feather-icons",
        ]

        for script in expected_scripts:
            assert script in layout_content, f"Missing external script: {script}"
