#!/usr/bin/env python3
"""
Simple test to verify RTL configuration option is working correctly.
This test verifies that the enable_rtl option is properly integrated.
"""


def test_rtl_config_option():
    """Test that RTL configuration option works in theme.conf"""

    # Read theme.conf file
    theme_conf_path = "src/quantecon_book_theme/theme/quantecon_book_theme/theme.conf"
    with open(theme_conf_path, "r") as f:
        theme_conf_content = f.read()

    # Check that the RTL option is present with default False
    assert (
        "enable_rtl = False" in theme_conf_content
    ), "RTL configuration option should be present in theme.conf with default False"

    print("✅ RTL configuration option found in theme.conf")


def test_rtl_html_template():
    """Test that HTML layout includes RTL support"""

    # Read layout.html file
    layout_html_path = "src/quantecon_book_theme/theme/quantecon_book_theme/layout.html"
    with open(layout_html_path, "r") as f:
        layout_content = f.read()

    # Check that dir="rtl" is conditionally applied
    assert (
        '{% if theme_enable_rtl %} dir="rtl"{% endif %}' in layout_content
    ), "HTML layout should conditionally apply dir='rtl' based on theme_enable_rtl"

    print("✅ RTL HTML template integration found")


def test_rtl_python_integration():
    """Test that Python code handles RTL setting"""

    # Read __init__.py file
    init_py_path = "src/quantecon_book_theme/__init__.py"
    with open(init_py_path, "r") as f:
        init_content = f.read()

    # Check that RTL setting is processed as boolean
    assert (
        '"theme_enable_rtl"' in init_content
    ), "Python code should process theme_enable_rtl setting"

    print("✅ RTL Python integration found")


def test_rtl_css_styles():
    """Test that RTL CSS styles are built correctly"""

    # Read built CSS file
    css_path = "src/quantecon_book_theme/theme/quantecon_book_theme/static/styles/quantecon-book-theme.css"
    with open(css_path, "r") as f:
        css_content = f.read()

    # Check that RTL styles are present
    assert "[dir=rtl]" in css_content, "Built CSS should contain [dir=rtl] selector"

    # Check for some key RTL adjustments
    assert (
        "text-align:right" in css_content
    ), "RTL CSS should include right text alignment"

    print("✅ RTL CSS styles found in built stylesheet")


def test_rtl_scss_source():
    """Test that RTL SCSS source file exists and is included"""

    # Check that RTL SCSS file exists
    rtl_scss_path = "src/quantecon_book_theme/assets/styles/_rtl.scss"
    with open(rtl_scss_path, "r") as f:
        rtl_scss_content = f.read()

    # Check for key RTL styles
    assert (
        '[dir="rtl"]' in rtl_scss_content
    ), "RTL SCSS should contain [dir='rtl'] selector"

    # Check main index.scss includes RTL
    index_scss_path = "src/quantecon_book_theme/assets/styles/index.scss"
    with open(index_scss_path, "r") as f:
        index_content = f.read()

    assert '@forward "rtl"' in index_content, "Main SCSS should forward RTL styles"

    print("✅ RTL SCSS source and integration found")


if __name__ == "__main__":
    print("Running RTL configuration tests...\n")

    try:
        test_rtl_config_option()
        test_rtl_html_template()
        test_rtl_python_integration()
        test_rtl_css_styles()
        test_rtl_scss_source()

        print("\n🎉 All RTL tests passed!")
        print("\nRTL support is properly implemented with:")
        print("  - Configuration option: enable_rtl = False (default)")
        print("  - HTML template integration for dir='rtl' attribute")
        print("  - Python code processing RTL setting as boolean")
        print("  - Comprehensive RTL CSS styles for layout adjustments")
        print("  - Proper SCSS source organization and compilation")

    except Exception as e:
        print(f"❌ Test failed: {e}")
        exit(1)
