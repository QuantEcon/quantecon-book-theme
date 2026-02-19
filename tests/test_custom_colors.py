"""
Tests for the text color scheme system.

Verifies that:
- A single color_scheme option is registered in theme.conf
- Seoul256-inspired CSS custom properties are used in SCSS source files
- CSS custom properties appear in compiled CSS output
- Layout template handles scheme-based class injection
- The "none" scheme is defined in _color-schemes.scss
- The color scheme is validated against known schemes
- Custom color scheme CSS is auto-detected from _static/
"""

from pathlib import Path
from unittest.mock import MagicMock

from quantecon_book_theme import _VALID_COLOR_SCHEMES, validate_color_scheme


# Paths
THEME_DIR = Path("src/quantecon_book_theme/theme/quantecon_book_theme")
ASSETS_DIR = Path("src/quantecon_book_theme/assets")


class TestColorSchemeThemeOption:
    """Test that the color_scheme option is registered in theme.conf."""

    def test_color_scheme_option_exists(self):
        """theme.conf should define a color_scheme option."""
        content = (THEME_DIR / "theme.conf").read_text()
        assert "color_scheme =" in content

    def test_color_scheme_defaults_to_seoul256(self):
        """color_scheme should default to 'seoul256'."""
        content = (THEME_DIR / "theme.conf").read_text()
        lines = content.splitlines()
        matching = [line for line in lines if line.strip().startswith("color_scheme =")]
        assert len(matching) == 1
        assert matching[0].strip() == "color_scheme = seoul256"

    def test_old_individual_color_options_removed(self):
        """Individual color options (emphasis_color, etc.) should not exist."""
        content = (THEME_DIR / "theme.conf").read_text()
        for old_option in [
            "emphasis_color",
            "emphasis_color_dark",
            "strong_color",
            "strong_color_dark",
            "definition_color",
            "definition_color_dark",
        ]:
            lines = content.splitlines()
            matching = [
                line for line in lines if line.strip().startswith(f"{old_option} =")
            ]
            assert (
                len(matching) == 0
            ), f"Old option '{old_option}' should be removed from theme.conf"


class TestSeoul256ColorScheme:
    """Test that Seoul256-inspired colors are used in SCSS source files."""

    def test_colors_scss_defines_emphasis(self):
        """_colors.scss should define $emphasis with Seoul256 teal."""
        content = (ASSETS_DIR / "styles" / "_colors.scss").read_text()
        assert "$emphasis: #005f5f" in content

    def test_colors_scss_defines_emphasis_dark(self):
        """_colors.scss should define $emphasis-dark for dark mode."""
        content = (ASSETS_DIR / "styles" / "_colors.scss").read_text()
        assert "$emphasis-dark: #5fafaf" in content

    def test_colors_scss_defines_definition(self):
        """_colors.scss should define $definition with Seoul256 amber."""
        content = (ASSETS_DIR / "styles" / "_colors.scss").read_text()
        assert "$definition: #875f00" in content

    def test_colors_scss_defines_definition_dark(self):
        """_colors.scss should define $definition-dark for dark mode."""
        content = (ASSETS_DIR / "styles" / "_colors.scss").read_text()
        assert "$definition-dark: #d7af5f" in content


class TestColorSchemeCSSVariables:
    """Test that SCSS uses CSS custom properties for emphasis/strong."""

    def test_base_scss_uses_emphasis_variable(self):
        """_base.scss should use --qe-emphasis-color CSS variable for em."""
        content = (ASSETS_DIR / "styles" / "_base.scss").read_text()
        assert "var(--qe-emphasis-color" in content

    def test_base_scss_uses_strong_variable(self):
        """_base.scss should use --qe-strong-color CSS variable for strong."""
        content = (ASSETS_DIR / "styles" / "_base.scss").read_text()
        assert "var(--qe-strong-color" in content

    def test_base_scss_has_emphasis_fallback(self):
        """_base.scss should have SCSS fallback value for emphasis color."""
        content = (ASSETS_DIR / "styles" / "_base.scss").read_text()
        assert "var(--qe-emphasis-color, colors.$emphasis)" in content

    def test_base_scss_has_strong_fallback(self):
        """_base.scss should have SCSS fallback value for strong color."""
        content = (ASSETS_DIR / "styles" / "_base.scss").read_text()
        assert "var(--qe-strong-color, colors.$definition)" in content

    def test_dark_theme_uses_emphasis_variable(self):
        """_dark-theme.scss should use --qe-emphasis-color CSS variable."""
        content = (ASSETS_DIR / "styles" / "_dark-theme.scss").read_text()
        assert "var(--qe-emphasis-color" in content

    def test_dark_theme_uses_strong_variable(self):
        """_dark-theme.scss should use --qe-strong-color CSS variable."""
        content = (ASSETS_DIR / "styles" / "_dark-theme.scss").read_text()
        assert "var(--qe-strong-color" in content

    def test_dark_theme_has_emphasis_dark_fallback(self):
        """_dark-theme.scss should fall back to $emphasis-dark."""
        content = (ASSETS_DIR / "styles" / "_dark-theme.scss").read_text()
        assert "colors.$emphasis-dark" in content

    def test_dark_theme_has_definition_dark_fallback(self):
        """_dark-theme.scss should fall back to $definition-dark."""
        content = (ASSETS_DIR / "styles" / "_dark-theme.scss").read_text()
        assert "colors.$definition-dark" in content

    def test_base_scss_uses_definition_variable(self):
        """_base.scss should use --qe-definition-color for dl dt elements."""
        content = (ASSETS_DIR / "styles" / "_base.scss").read_text()
        assert "var(--qe-definition-color" in content

    def test_base_scss_definition_falls_back_to_strong(self):
        """_base.scss definition color should fall back to strong color."""
        content = (ASSETS_DIR / "styles" / "_base.scss").read_text()
        assert (
            "var(--qe-definition-color, var(--qe-strong-color, colors.$definition))"
            in content
        )

    def test_base_scss_targets_definition_list_terms(self):
        """_base.scss should target dl.simple dt, dl.glossary dt."""
        content = (ASSETS_DIR / "styles" / "_base.scss").read_text()
        assert "dl.simple dt" in content
        assert "dl.glossary dt" in content


class TestNoneColorScheme:
    """Test that the 'none' scheme resets markup colors to inherit."""

    def test_color_schemes_scss_exists(self):
        """_color-schemes.scss should exist."""
        assert (ASSETS_DIR / "styles" / "_color-schemes.scss").is_file()

    def test_none_scheme_resets_em(self):
        """'none' scheme should reset em color to inherit."""
        content = (ASSETS_DIR / "styles" / "_color-schemes.scss").read_text()
        assert "color-scheme-none" in content
        assert "inherit" in content

    def test_none_scheme_resets_strong(self):
        """'none' scheme should reset strong color to inherit."""
        content = (ASSETS_DIR / "styles" / "_color-schemes.scss").read_text()
        assert "strong" in content

    def test_color_schemes_imported(self):
        """index.scss should import _color-schemes."""
        content = (ASSETS_DIR / "styles" / "index.scss").read_text()
        assert '"color-schemes"' in content


class TestCompiledCSS:
    """Test that compiled CSS contains custom properties."""

    def test_compiled_css_has_emphasis_variable(self):
        """Compiled CSS should contain --qe-emphasis-color variable."""
        css_path = THEME_DIR / "static" / "styles" / "quantecon-book-theme.css"
        content = css_path.read_text()
        assert "--qe-emphasis-color" in content

    def test_compiled_css_has_strong_variable(self):
        """Compiled CSS should contain --qe-strong-color variable."""
        css_path = THEME_DIR / "static" / "styles" / "quantecon-book-theme.css"
        content = css_path.read_text()
        assert "--qe-strong-color" in content

    def test_compiled_css_has_definition_variable(self):
        """Compiled CSS should contain --qe-definition-color variable."""
        css_path = THEME_DIR / "static" / "styles" / "quantecon-book-theme.css"
        content = css_path.read_text()
        assert "--qe-definition-color" in content

    def test_compiled_css_has_none_scheme(self):
        """Compiled CSS should contain the color-scheme-none class."""
        css_path = THEME_DIR / "static" / "styles" / "quantecon-book-theme.css"
        content = css_path.read_text()
        assert "color-scheme-none" in content


class TestLayoutTemplateScheme:
    """Test that layout.html handles color scheme correctly."""

    def _read_layout(self):
        return (THEME_DIR / "layout.html").read_text()

    def test_template_checks_color_scheme(self):
        """Layout template should reference theme_color_scheme."""
        content = self._read_layout()
        assert "theme_color_scheme" in content

    def test_template_handles_none_scheme(self):
        """Layout template should add color-scheme-none class for 'none'."""
        content = self._read_layout()
        assert "color-scheme-none" in content

    def test_template_no_individual_color_injection(self):
        """Layout template should NOT inject individual color variables."""
        content = self._read_layout()
        assert "theme_emphasis_color" not in content
        assert "theme_strong_color" not in content
        assert "theme_definition_color" not in content


class TestValidColorSchemes:
    """Test the valid color scheme list."""

    def test_seoul256_is_valid(self):
        """'seoul256' should be a valid color scheme."""
        assert "seoul256" in _VALID_COLOR_SCHEMES

    def test_none_is_valid(self):
        """'none' should be a valid color scheme."""
        assert "none" in _VALID_COLOR_SCHEMES


class TestValidateColorSchemeFunction:
    """Test the validate_color_scheme function with a mock Sphinx app."""

    def _make_app(self, color_scheme=None, static_paths=None):
        """Create a mock Sphinx app with given theme options."""
        app = MagicMock()
        theme_options = {}
        if color_scheme is not None:
            theme_options["color_scheme"] = color_scheme
        app.config.html_theme_options = theme_options
        app.config.html_static_path = static_paths or []
        app.confdir = "/fake/confdir"
        return app

    def test_default_scheme_is_seoul256(self):
        """Default color_scheme should be 'seoul256'."""
        app = self._make_app()
        validate_color_scheme(app)
        assert app.config.html_theme_options["color_scheme"] == "seoul256"

    def test_valid_seoul256_preserved(self):
        """Valid 'seoul256' scheme should be preserved."""
        app = self._make_app(color_scheme="seoul256")
        validate_color_scheme(app)
        assert app.config.html_theme_options["color_scheme"] == "seoul256"

    def test_valid_none_preserved(self):
        """Valid 'none' scheme should be preserved."""
        app = self._make_app(color_scheme="none")
        validate_color_scheme(app)
        assert app.config.html_theme_options["color_scheme"] == "none"

    def test_invalid_scheme_falls_back(self):
        """Invalid scheme should fall back to 'seoul256' with warning."""
        app = self._make_app(color_scheme="nonexistent")
        validate_color_scheme(app)
        assert app.config.html_theme_options["color_scheme"] == "seoul256"

    def test_case_insensitive(self):
        """Scheme names should be case-insensitive."""
        app = self._make_app(color_scheme="Seoul256")
        validate_color_scheme(app)
        assert app.config.html_theme_options["color_scheme"] == "seoul256"

    def test_whitespace_trimmed(self):
        """Whitespace should be trimmed from scheme name."""
        app = self._make_app(color_scheme="  none  ")
        validate_color_scheme(app)
        assert app.config.html_theme_options["color_scheme"] == "none"
