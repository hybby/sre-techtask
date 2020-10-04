"""
Unit tests for the sreport.py utility
"""
import pytest
from sreport import parse_input, output_json


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


def test_json_output(capsys):
    """
    Tests that outputting an object in JSON is done in the manner we expect
    """
    sample_object = {
        "foo": "bar"
    }

    output_json(sample_object)
    captured = capsys.readouterr()
    assert captured.out == '{\n    "foo": "bar"\n}\n'


def test_invalid_json_output():
    """
    Tests that we raise TypeError if an object doesn't seem 'json-able'
    """
    sample_object = ""

    with pytest.raises(TypeError, match="input must be dict or list"):
        output_json(sample_object)
