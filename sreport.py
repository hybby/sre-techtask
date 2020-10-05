#!/usr/bin/env python3
"""
A utility to make HTTP(S) requests to specified URLs and report on the results
"""
import sys
import json
import requests
from validator_collection import checkers
USAGE = "Usage: ./sreport.py < urls.txt"


def parse_input(input_):
    """
    Given an input string, return a list of strings split by newline character
    """
    if len(input_) <= 0:
        raise ValueError("No input provided")

    return input_.splitlines()


def validate_url(url):
    """
    Determine if a given URL is valid.  Return True if so, False if not
    """
    if not url:
        raise ValueError("No url provided")

    return checkers.is_url(url)


def process_url(url, timeout_secs=10):
    """
    Given a URL, attempt to make a request to it and return information that
    we're interested in, such as date/time of response, status code and length
    """
    output = {}
    output['Url'] = url

    if validate_url(url):
        output['Error'] = 'invalid url'
        return output

    # attempt a request and deal with common exceptions we may encounter and
    # wish to report upon. erroring out on other exceptions seems reasonable
    # https://requests.readthedocs.io/en/master/_modules/requests/exceptions
    try:
        response = requests.get(  # pylint: disable=unused-variable
            url,
            allow_redirects=True,
            timeout=timeout_secs
        )
    except requests.exceptions.SSLError:
        output['Error'] = "ssl error"
        return output
    except requests.exceptions.TooManyRedirects:
        output['Error'] = "too many redirects"
        return output
    except requests.exceptions.ConnectionError:
        # catches dns failures and refused connections
        output['Error'] = "connection error"
        return output
    except requests.exceptions.Timeout:
        # catches connection timeouts and read timeouts
        output['Error'] = "timed out"
        return output

    # build our output message, adding attributes if they're available
    if response.status_code:
        output['Status_code'] = response.status_code

    if 'Content-Length' in response.headers:
        output['Content_length'] = response.headers['Content-Length']

    if 'Date' in response.headers:
        output['Date'] = response.headers['Date']

    return output


def generate_summary(summary):
    """
    Given a dictionary of status codes and occurrances, generate a report
    object (array of objects) that summarises a count of overall responses
    along with a breakdown of counts of different response codes.
    """
    if not isinstance(summary, dict):
        raise TypeError("input must be dict")

    overall_responses = 0
    output = []

    for status_code, quantity in summary.items():
        if not isinstance(status_code, int):
            raise ValueError("bad input; response codes must be integers")

        if not isinstance(quantity, int):
            raise ValueError("bad input; response counts must be integers")

        overall_responses = overall_responses + quantity
        output.append({
            'Status_code': status_code,
            'Number_of_responses': quantity
        })

    output.append({
        'Number_of_responses': overall_responses
    })

    return output


def output_json(output):
    """
    Given a dict or a list, output it to stdout as a JSON document
    """
    if not isinstance(output, (dict, list)):
        raise TypeError("input must be dict or list")

    print(json.dumps(output, indent=4))


if __name__ == "__main__":
    # requirement: program is run from command line and takes input from stdin
    if sys.stdin.isatty():
        raise ValueError(
            "This program only accepts input via stdin\n{}".format(USAGE)
        )

    with sys.stdin as stdin:
        lines = parse_input(stdin.read())

    stats = {}
    for line in lines:
        result = process_url(line)
        output_json(result)

        # if we recieved a successful response, increment our stats counter
        # presence of a 'Status_code' attribute means a valid response
        if 'Status_code' in result:
            if result['Status_code'] in stats:
                stats[result['Status_code']] = stats[result['Status_code']] + 1
            else:
                stats[result['Status_code']] = 1

    # build our summary document
    report = generate_summary(stats)
    output_json(report)
