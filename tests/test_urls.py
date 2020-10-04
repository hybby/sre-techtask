"""
Unit tests for the sreport.py utility
"""
import pytest
import requests
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
    expected_output = {
      "Url": url,
      "Error": "invalid url",
    }

    assert process_url(url) == expected_output


def test_ssl_error_output(requests_mock):
    """
    Tests whether we output the correct format of message for a URL which
    returns an SSL error. For example, if the site has a bad certificate
    """
    url = "https://badcert.com"
    requests_mock.get(
        url,
        exc=requests.exceptions.SSLError
    )

    expected_output = {
      "Url": url,
      "Error": "ssl error",
    }

    assert process_url(url) == expected_output


def test_connection_error_output(requests_mock):
    """
    Tests whether we output the correct format of message for a URL which
    refuses our connection. For example, if the DNS lookup fails.
    """
    url = "http://not.exists.bbc.co.uk"
    requests_mock.get(
        url,
        exc=requests.exceptions.ConnectionError
    )

    expected_output = {
      "Url": url,
      "Error": "connection error",
    }

    assert process_url(url) == expected_output


def test_connection_timeout_output(requests_mock):
    """
    Tests whether we output the correct format of message for a URL which
    takes longer than our timeout value to return a response.
    """
    url = "http://slowsite.com"
    requests_mock.get(
        url,
        exc=requests.exceptions.Timeout
    )

    expected_output = {
      "Url": url,
      "Error": "timed out",
    }

    assert process_url(url) == expected_output


def test_too_many_redirects_output(requests_mock):
    """
    Tests whether we output the correct format of message for a URL which
    refuses our connection. For example, if the DNS lookup fails.
    """
    url = "http://here.there.everywhere.com"
    requests_mock.get(
        url,
        exc=requests.exceptions.TooManyRedirects
    )

    expected_output = {
      "Url": url,
      "Error": "too many redirects",
    }

    assert process_url(url) == expected_output


def test_40x_50x_output(requests_mock):
    """
    Tests whether we output correctly for common HTTP 40x and 50x responses
    We expect the URL, status code and datetime of the response to be returned
    """
    url = "http://not.exists.bbc.co.uk/"
    codes = [
        400,  # bad request
        401,  # unauthorized
        403,  # forbidden
        404,  # not found
        500,  # internal server error
        502,  # bad gateway
        503,  # service unavailable
        504   # gateway timeout
    ]

    for code in codes:
        requests_mock.get(
            url,
            status_code=code,
            headers={'Date': 'Sat, 03 Oct 2020 17:32:59 GMT'}
        )

        expected_output = {
          "Url": url,
          "Status_code": code,
          "Date": "Sat, 03 Oct 2020 17:32:59 GMT"
        }

        assert process_url(url) == expected_output


def test_200_output(requests_mock):
    """
    Tests whether we output the correct message for HTTP 200 responses
    We expect the URL, status code, datetime of the response and the content
    length of the response to be returned.

    As we always follow redirects, we won't test HTTP 301 responses.
    """
    url = "http://www.example.com"
    requests_mock.get(
        url,
        status_code=200,
        headers={
            'Date': 'Sat, 03 Oct 2020 17:32:59 GMT',
            'Content-Length': '12345'
        }
    )

    expected_output = {
      "Url": url,
      "Status_code": 200,
      "Content_length": '12345',
      "Date": "Sat, 03 Oct 2020 17:32:59 GMT"
    }

    assert process_url(url) == expected_output
