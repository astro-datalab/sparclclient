# Python library
#!import logging
#!import os
import datetime
import time
import socket
from inspect import cleandoc

# External packages
#   none
# LOCAL packages
#   none


# e.g. pdocstr(coexist_radec.__doc__),
def pdocstr(docstring):
    return cleandoc(docstring).replace("\n", " ")


def tic():
    tic.start = time.perf_counter()


def toc():
    elapsed_seconds = time.perf_counter() - tic.start
    return elapsed_seconds  # fractional


def here_now():
    hostname = socket.gethostname()
    now = str(datetime.datetime.now())
    return (hostname, now)


# dict((k,len(v)) for (k,v) in qs[0]['spzline'].items())
def objform(obj):
    """Nested structure of python object. Avoid spewing big lists."""
    if obj is None:
        return None
    elif type(obj) is list:
        return f"CNT={len(obj)}"
    elif type(obj) is dict:
        return dict((k, objform(v)) for (k, v) in obj.items())
    else:
        return str(type(obj))
