#! /usr/local/bin/python3
"""
Stock Analysis Document.

..  moduleauthor:: Ping-Lin <billy3962@hotmail.com>
"""

import logging
DEBUG = False

if DEBUG:
    level = logging.DEBUG
else:
    level = logging.INFO
logging.basicConfig(level=level)
