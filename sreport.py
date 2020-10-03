#!/usr/bin/env python3
"""
A utility to make HTTP(S) requests to specified URLs and report on the results
"""
import sys
USAGE = "Usage: ./sreport.py < urls.txt"


if __name__ == "__main__":
    # requirement: program is run from command line and takes input from stdin
    if sys.stdin.isatty():
        raise ValueError(
            "This program only accepts input via stdin\n{}".format(USAGE)
        )

    # requirements:
    #
    # - parse input
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
