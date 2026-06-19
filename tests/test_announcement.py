"""
Tests for the dismissible announcement banner.

Verifies that:
- The `announcement` / `announcement_expires` options are registered in theme.conf
- The SCSS partial, JS module, and layout markup are wired in
- `_parse_iso_date` parses ISO dates and rejects bad input
- `_build_announcements` builds the render list, hashes content for dismissal,
  and skips announcements that have already expired at build time
- `validate_announcement` fails open on an invalid expiry date
"""

from datetime import datetime, timedelta, timezone
from pathlib import Path
from unittest.mock import MagicMock

from quantecon_book_theme import (
    _build_announcements,
    _parse_iso_date,
    validate_announcement,
)

# Paths
THEME_DIR = Path("src/quantecon_book_theme/theme/quantecon_book_theme")
ASSETS_DIR = Path("src/quantecon_book_theme/assets")


def _future_date(days=365):
    return (datetime.now(timezone.utc).date() + timedelta(days=days)).isoformat()


def _past_date(days=1):
    return (datetime.now(timezone.utc).date() - timedelta(days=days)).isoformat()


class TestAnnouncementThemeOption:
    """The options must be registered in theme.conf so Sphinx accepts them."""

    def test_announcement_option_exists(self):
        content = (THEME_DIR / "theme.conf").read_text()
        assert "announcement =" in content

    def test_announcement_expires_option_exists(self):
        content = (THEME_DIR / "theme.conf").read_text()
        assert "announcement_expires =" in content


class TestAnnouncementAssets:
    """The SCSS, JS, and template pieces must be present and wired together."""

    def test_scss_partial_exists(self):
        content = (ASSETS_DIR / "styles" / "_announcement.scss").read_text()
        assert ".qe-announcement" in content

    def test_scss_partial_is_forwarded(self):
        content = (ASSETS_DIR / "styles" / "index.scss").read_text()
        assert '@forward "announcement"' in content

    def test_scss_has_dark_mode_styles(self):
        content = (ASSETS_DIR / "styles" / "_announcement.scss").read_text()
        assert "body.dark-theme .qe-announcement" in content

    def test_scss_has_rtl_styles(self):
        content = (ASSETS_DIR / "styles" / "_announcement.scss").read_text()
        assert '[dir="rtl"] .qe-announcement' in content

    def test_js_module_exists(self):
        content = (ASSETS_DIR / "scripts" / "announcement.js").read_text()
        assert "qe-dismissed-announcements" in content
        assert "export function initAnnouncement" in content

    def test_js_module_is_imported(self):
        content = (ASSETS_DIR / "scripts" / "index.js").read_text()
        assert 'from "./announcement.js"' in content
        assert "initAnnouncement()" in content

    def test_layout_renders_announcement_loop(self):
        content = (THEME_DIR / "layout.html").read_text()
        assert "qe-announcement-bar" in content
        assert "data-announcement-id" in content
        assert "data-announcement-expires" in content


class TestParseIsoDate:
    """_parse_iso_date should parse YYYY-MM-DD and reject everything else."""

    def test_valid_date(self):
        assert _parse_iso_date("2026-07-01").isoformat() == "2026-07-01"

    def test_whitespace_is_stripped(self):
        assert _parse_iso_date("  2026-07-01  ").isoformat() == "2026-07-01"

    def test_empty_returns_none(self):
        assert _parse_iso_date("") is None
        assert _parse_iso_date(None) is None

    def test_invalid_format_returns_none(self):
        assert _parse_iso_date("July 1 2026") is None
        assert _parse_iso_date("2026/07/01") is None
        assert _parse_iso_date("not-a-date") is None


class TestBuildAnnouncements:
    """_build_announcements turns config into the list the template renders."""

    def test_no_message_is_empty(self):
        assert _build_announcements({}) == []
        assert _build_announcements({"announcement": ""}) == []
        assert _build_announcements({"announcement": "   "}) == []

    def test_message_produces_one_entry(self):
        result = _build_announcements({"announcement": "Hello <b>world</b>"})
        assert len(result) == 1
        assert result[0]["html"] == "Hello <b>world</b>"
        assert result[0]["expires_iso"] == ""
        assert result[0]["id"]  # a non-empty content hash

    def test_id_is_stable_for_same_message(self):
        a = _build_announcements({"announcement": "Same message"})[0]["id"]
        b = _build_announcements({"announcement": "Same message"})[0]["id"]
        assert a == b

    def test_id_changes_when_message_changes(self):
        a = _build_announcements({"announcement": "Message A"})[0]["id"]
        b = _build_announcements({"announcement": "Message B"})[0]["id"]
        assert a != b

    def test_future_expiry_is_kept(self):
        future = _future_date()
        result = _build_announcements(
            {"announcement": "Upgrade notice", "announcement_expires": future}
        )
        assert len(result) == 1
        assert result[0]["expires_iso"] == future

    def test_past_expiry_is_skipped_at_build_time(self):
        result = _build_announcements(
            {"announcement": "Stale notice", "announcement_expires": _past_date()}
        )
        assert result == []

    def test_today_expiry_is_kept(self):
        today = datetime.now(timezone.utc).date().isoformat()
        result = _build_announcements(
            {"announcement": "Ends today", "announcement_expires": today}
        )
        assert len(result) == 1

    def test_invalid_expiry_is_ignored_not_expired(self):
        # _build_announcements treats an unparseable date as no expiry (fail open).
        result = _build_announcements(
            {"announcement": "Keep showing", "announcement_expires": "bad-date"}
        )
        assert len(result) == 1
        assert result[0]["expires_iso"] == ""


class TestValidateAnnouncement:
    """validate_announcement fails open: a bad date is cleared, not the message."""

    def _make_app(self, theme_options):
        app = MagicMock()
        app.config.html_theme_options = theme_options
        return app

    def test_invalid_date_is_cleared(self):
        app = self._make_app(
            {"announcement": "Notice", "announcement_expires": "July 1"}
        )
        validate_announcement(app)
        assert app.config.html_theme_options["announcement_expires"] == ""
        # The message itself is untouched.
        assert app.config.html_theme_options["announcement"] == "Notice"

    def test_valid_date_is_preserved(self):
        app = self._make_app({"announcement_expires": "2026-07-01"})
        validate_announcement(app)
        assert app.config.html_theme_options["announcement_expires"] == "2026-07-01"

    def test_empty_date_is_left_alone(self):
        app = self._make_app({"announcement_expires": ""})
        validate_announcement(app)
        assert app.config.html_theme_options["announcement_expires"] == ""
