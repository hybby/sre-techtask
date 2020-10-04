"""
Unit tests for the sreport.py utility relating to summary report generation
"""
import pytest
from sreport import generate_summary


def test_summary_report_output():
    """
    Tests that given a summary dict of response codes and response counts,
    we produce a report in the format that we expect
    """
    sample_summary = {
      200: 50,
      403: 2,
      404: 10,
      500: 1
    }

    expected_output = [
        {
            "Status_code": 200,
            "Number_of_responses": 50
        },
        {
            "Status_code": 403,
            "Number_of_responses": 2
        },

        {
            "Status_code": 404,
            "Number_of_responses": 10
        },
        {
            "Status_code": 500,
            "Number_of_responses": 1
        },
        {
            "Number_of_responses": 63
        }
    ]

    assert generate_summary(sample_summary) == expected_output


def test_summary_bad_input_error():
    """
    Tests that we raise TypeError if a dictionary hasn't been provided
    """
    sample_object = ""

    with pytest.raises(TypeError, match="input must be dict"):
        generate_summary(sample_object)


def test_summary_bad_count_error():
    """
    Tests that we throw a ValueError if a non-integer response count provided
    """
    sample_object = {
        404: "sixty-one"
    }

    error = "bad input; response counts must be integers"
    with pytest.raises(ValueError, match=error):
        generate_summary(sample_object)


def test_summary_bad_code_error():
    """
    Tests that we throw a ValueError if a non-integer response code provided
    """
    sample_object = {
        "four-oh-four": 100
    }

    error = "bad input; response codes must be integers"
    with pytest.raises(ValueError, match=error):
        generate_summary(sample_object)
