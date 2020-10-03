#!/usr/bin/env python3
"""
A utility to make HTTP(S) requests to specified URLs and report on the results
"""
import json
import sys
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


def process_url(url):
    """
    Given a URL, attempt to make a request to it and return information that
    we're interested in, such as date/time of response, status code and length
    """
    output = {}
    return json.dumps(output, indent=4)


if __name__ == "__main__":
    # requirement: program is run from command line and takes input from stdin
    if sys.stdin.isatty():
        raise ValueError(
            "This program only accepts input via stdin\n{}".format(USAGE)
        )

    with sys.stdin as stdin:
        lines = parse_input(stdin.read())

    for line in lines:
        process_url(line)

    # requirements:
    #
    # - for each url:
    #   - validate url
    #   - make GET request
    #   - output JSON object containing:
    #     - if request is successful:
    #       - url
    #       - time/date of response
    #       - http status code
    #       - content length of response
    #     - if rqeuest is invalid/unsuccessful
    #       - url
    #       - error message
