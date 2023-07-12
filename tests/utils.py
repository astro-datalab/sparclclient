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


# In case I want to give CURL equivalents for client methods
def curl_retrieve_str(msg, svc="spectras", qstr="", **uparams):
    ids = "00000dd7-b1ff-48ed-b162-46d9d65f829c,BADID"
    #!svc = 'spectras' if use_async else 'retrieve'
    #! qstr = urlencode(uparams)
    url = f"https://astrosparcl.datalab.noirlab.edu/sparc/{svc}/?{qstr}"
    curlpost1 = "curl -X 'POST' -H 'Content-Type: application/json' "
    curlpost2 = f"-d '[{ids.split(',')}]' '{url}'"
    #! curlpost3 = " | python3 -m json.tool"
    return curlpost1 + curlpost2
