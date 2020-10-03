"""
Unit tests for the sreport.py utility
"""
import json
import pytest
from sreport import validate_url, process_url


def test_valid_url():
    """
    Tests whether the url validator correctly identifies valid URLs
    """
    url = "https://www.google.com"
    assert validate_url(url) is True


def test_invalid_url():
    """
    Tests whether the url validator correctly identifies invalid URLs
    """
    url = "bad://address"
    assert validate_url(url) is False


def test_missing_url():
    """
    Tests whether the url validator throws an exception when no URL is provided
    """
    with pytest.raises(ValueError, match="No url provided"):
        validate_url("")


def test_invalid_url_output():
    """
    Tests whether we output the correct format of message for an invalid URL
    """
    url = "bad://address"
    expected_result = {
      "Url": url,
      "Error": "invalid url",
    }
    expected_msg = json.dumps(expected_result, indent=4)

    assert process_url(url) == expected_msg
