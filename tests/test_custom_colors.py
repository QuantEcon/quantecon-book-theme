"""
Tests for customizable emphasis and definition text colors.

Verifies that:
- Theme options are registered in theme.conf
- CSS custom properties are used in SCSS source files
- CSS custom properties appear in compiled CSS output
- Layout template injects custom color styles when options are set
"""

from pathlib import Path


# Paths
THEME_DIR = Path("src/quantecon_book_theme/theme/quantecon_book_theme")
ASSETS_DIR = Path("src/quantecon_book_theme/assets")


class TestCustomColorThemeOptions:
    """Test that color customization options are registered in theme.conf."""

    def test_emphasis_color_option_exists(self):
        """theme.conf should define emphasis_color option."""
        content = (THEME_DIR / "theme.conf").read_text()
        assert "emphasis_color =" in content

    def test_emphasis_color_dark_option_exists(self):
        """theme.conf should define emphasis_color_dark option."""
        content = (THEME_DIR / "theme.conf").read_text()
        assert "emphasis_color_dark =" in content

    def test_definition_color_option_exists(self):
        """theme.conf should define definition_color option."""
        content = (THEME_DIR / "theme.conf").read_text()
        assert "definition_color =" in content

    def test_definition_color_dark_option_exists(self):
        """theme.conf should define definition_color_dark option."""
        content = (THEME_DIR / "theme.conf").read_text()
        assert "definition_color_dark =" in content

    def test_options_default_to_empty(self):
        """All color options should default to empty (use CSS fallback)."""
        content = (THEME_DIR / "theme.conf").read_text()
        for option in [
            "emphasis_color",
            "emphasis_color_dark",
            "definition_color",
            "definition_color_dark",
        ]:
            # Each option should appear as "option_name =" with no value
            # Use a targeted check to avoid matching substrings
            lines = content.splitlines()
            matching = [
                line for line in lines if line.strip().startswith(f"{option} =")
            ]
            assert len(matching) == 1, f"Expected exactly one '{option}' option"
            assert matching[0].strip() == f"{option} =", (
                f"'{option}' should default to empty string"
            )


class TestCustomColorCSSVariables:
    """Test that SCSS uses CSS custom properties for emphasis/definition."""

    def test_base_scss_uses_emphasis_variable(self):
        """_base.scss should use --qe-emphasis-color CSS variable for em."""
        content = (ASSETS_DIR / "styles" / "_base.scss").read_text()
        assert "var(--qe-emphasis-color" in content

    def test_base_scss_uses_definition_variable(self):
        """_base.scss should use --qe-definition-color CSS variable for strong."""
        content = (ASSETS_DIR / "styles" / "_base.scss").read_text()
        assert "var(--qe-definition-color" in content

    def test_base_scss_has_emphasis_fallback(self):
        """_base.scss should have SCSS fallback value for emphasis color."""
        content = (ASSETS_DIR / "styles" / "_base.scss").read_text()
        assert "var(--qe-emphasis-color, colors.$emphasis)" in content

    def test_base_scss_has_definition_fallback(self):
        """_base.scss should have SCSS fallback value for definition color."""
        content = (ASSETS_DIR / "styles" / "_base.scss").read_text()
        assert "var(--qe-definition-color, colors.$definition)" in content

    def test_dark_theme_uses_emphasis_variable(self):
        """_dark-theme.scss should use --qe-emphasis-color CSS variable."""
        content = (ASSETS_DIR / "styles" / "_dark-theme.scss").read_text()
        assert "var(--qe-emphasis-color" in content

    def test_dark_theme_uses_definition_variable(self):
        """_dark-theme.scss should use --qe-definition-color CSS variable."""
        content = (ASSETS_DIR / "styles" / "_dark-theme.scss").read_text()
        assert "var(--qe-definition-color" in content

    def test_dark_theme_has_emphasis_fallback(self):
        """_dark-theme.scss should have fallback for emphasis in dark mode."""
        content = (ASSETS_DIR / "styles" / "_dark-theme.scss").read_text()
        assert "var(--qe-emphasis-color, #66bb6a)" in content

    def test_dark_theme_has_definition_fallback(self):
        """_dark-theme.scss should have fallback for definition in dark mode."""
        content = (ASSETS_DIR / "styles" / "_dark-theme.scss").read_text()
        assert "var(--qe-definition-color, #cd853f)" in content


class TestCustomColorCompiledCSS:
    """Test that compiled CSS contains custom properties."""

    def test_compiled_css_has_emphasis_variable(self):
        """Compiled CSS should contain --qe-emphasis-color variable."""
        css_path = THEME_DIR / "static" / "styles" / "quantecon-book-theme.css"
        content = css_path.read_text()
        assert "--qe-emphasis-color" in content

    def test_compiled_css_has_definition_variable(self):
        """Compiled CSS should contain --qe-definition-color variable."""
        css_path = THEME_DIR / "static" / "styles" / "quantecon-book-theme.css"
        content = css_path.read_text()
        assert "--qe-definition-color" in content

    def test_compiled_css_em_uses_variable(self):
        """Compiled CSS em rule should use var(--qe-emphasis-color)."""
        css_path = THEME_DIR / "static" / "styles" / "quantecon-book-theme.css"
        content = css_path.read_text()
        assert "var(--qe-emphasis-color" in content

    def test_compiled_css_strong_uses_variable(self):
        """Compiled CSS strong rule should use var(--qe-definition-color)."""
        css_path = THEME_DIR / "static" / "styles" / "quantecon-book-theme.css"
        content = css_path.read_text()
        assert "var(--qe-definition-color" in content


class TestCustomColorLayoutTemplate:
    """Test that layout.html injects custom color styles."""

    def _read_layout(self):
        return (THEME_DIR / "layout.html").read_text()

    def test_template_checks_emphasis_color(self):
        """Layout template should conditionally check theme_emphasis_color."""
        content = self._read_layout()
        assert "theme_emphasis_color" in content

    def test_template_checks_definition_color(self):
        """Layout template should conditionally check theme_definition_color."""
        content = self._read_layout()
        assert "theme_definition_color" in content

    def test_template_checks_emphasis_color_dark(self):
        """Layout template should conditionally check theme_emphasis_color_dark."""
        content = self._read_layout()
        assert "theme_emphasis_color_dark" in content

    def test_template_checks_definition_color_dark(self):
        """Layout template should conditionally check theme_definition_color_dark."""
        content = self._read_layout()
        assert "theme_definition_color_dark" in content

    def test_template_sets_emphasis_css_variable(self):
        """Layout template should set --qe-emphasis-color CSS variable."""
        content = self._read_layout()
        assert "--qe-emphasis-color: {{ theme_emphasis_color }}" in content

    def test_template_sets_definition_css_variable(self):
        """Layout template should set --qe-definition-color CSS variable."""
        content = self._read_layout()
        assert "--qe-definition-color: {{ theme_definition_color }}" in content

    def test_template_sets_dark_emphasis_css_variable(self):
        """Layout template should set --qe-emphasis-color for dark mode."""
        content = self._read_layout()
        assert "--qe-emphasis-color: {{ theme_emphasis_color_dark }}" in content

    def test_template_sets_dark_definition_css_variable(self):
        """Layout template should set --qe-definition-color for dark mode."""
        content = self._read_layout()
        assert "--qe-definition-color: {{ theme_definition_color_dark }}" in content

    def test_template_dark_mode_uses_body_dark_theme(self):
        """Layout template should target body.dark-theme for dark colors."""
        content = self._read_layout()
        assert "body.dark-theme" in content

    def test_template_light_mode_uses_root(self):
        """Layout template should target :root for light mode colors."""
        content = self._read_layout()
        assert ":root" in content
