"""Tests for the language switcher feature."""

import pytest
from quantecon_book_theme import _process_languages


LANGUAGES_FULL = [
    {"code": "en", "name": "English", "url": "https://example.org"},
    {"code": "fa", "name": "فارسی", "url": "https://example.org/fa", "rtl": True},
    {"code": "zh-cn", "name": "中文", "url": "https://example.org/zh-cn"},
]


class TestProcessLanguages:
    """Tests for _process_languages validation and normalization."""

    def test_multiple_valid_languages(self):
        config = {"languages": LANGUAGES_FULL, "current_language": "en"}
        langs, current = _process_languages(config)
        assert len(langs) == 3
        assert current == "en"
        assert langs[0]["code"] == "en"
        assert langs[1]["rtl"] is True

    def test_empty_languages(self):
        langs, current = _process_languages({})
        assert langs == []
        assert current == ""

    def test_single_language_returns_empty(self):
        config = {
            "languages": [{"code": "en", "name": "English", "url": "https://x.org"}],
            "current_language": "en",
        }
        langs, current = _process_languages(config)
        assert langs == []
        assert current == ""

    def test_no_languages_key(self):
        config = {"current_language": "en"}
        langs, current = _process_languages(config)
        assert langs == []
        assert current == ""

    def test_trailing_slash_stripped(self):
        config = {
            "languages": [
                {"code": "en", "name": "English", "url": "https://example.org/"},
                {"code": "fa", "name": "فارسی", "url": "https://example.org/fa/"},
            ],
            "current_language": "en",
        }
        langs, current = _process_languages(config)
        assert langs[0]["url"] == "https://example.org"
        assert langs[1]["url"] == "https://example.org/fa"

    def test_invalid_entry_missing_code(self):
        config = {
            "languages": [
                {"name": "English", "url": "https://example.org"},
                {"code": "fa", "name": "فارسی", "url": "https://example.org/fa"},
                {"code": "zh-cn", "name": "中文", "url": "https://example.org/zh-cn"},
            ],
            "current_language": "en",
        }
        langs, current = _process_languages(config)
        # First entry invalid (no code), only 2 valid remain
        assert len(langs) == 2
        assert langs[0]["code"] == "fa"

    def test_invalid_entry_missing_url(self):
        config = {
            "languages": [
                {"code": "en", "name": "English"},
                {"code": "fa", "name": "فارسی", "url": "https://example.org/fa"},
            ],
            "current_language": "en",
        }
        langs, current = _process_languages(config)
        # Only 1 valid entry, so returns empty
        assert langs == []
        assert current == ""

    def test_non_dict_entries_skipped(self):
        config = {
            "languages": [
                "not a dict",
                {"code": "en", "name": "English", "url": "https://example.org"},
                {"code": "fa", "name": "فارسی", "url": "https://example.org/fa"},
            ],
            "current_language": "en",
        }
        langs, current = _process_languages(config)
        assert len(langs) == 2

    def test_languages_not_a_list(self):
        config = {"languages": "not a list", "current_language": "en"}
        langs, current = _process_languages(config)
        assert langs == []
        assert current == ""

    def test_original_dict_not_mutated(self):
        original = [
            {"code": "en", "name": "English", "url": "https://example.org/"},
            {"code": "fa", "name": "فارسی", "url": "https://example.org/fa/"},
        ]
        config = {"languages": original, "current_language": "en"}
        _process_languages(config)
        # Original URLs should still have trailing slashes
        assert original[0]["url"] == "https://example.org/"
        assert original[1]["url"] == "https://example.org/fa/"
