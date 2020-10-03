"""
Unit tests for the sreport.py utility
"""
import pytest
from sreport import parse_input


def test_input():
    """
    Tests that newline separated input is split into a list of strings
    """
    sample_input = "foo\nbar"
    assert parse_input(sample_input) == ['foo', 'bar']


def test_no_input():
    """
    Tests that an exception is thrown when no input is provided to script
    """
    with pytest.raises(ValueError, match="No input provided"):
        parse_input("")
