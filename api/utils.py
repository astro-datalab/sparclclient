# Python library
import os
import datetime
import time
import socket
# External packages
#   none
# LOCAL packages
#   none


def tic():
    tic.start = time.perf_counter()

def toc():
    elapsed_seconds = time.perf_counter() - tic.start
    return elapsed_seconds # fractional

def here_now():
    hostname = socket.gethostname()
    now =  str(datetime.datetime.now())
    return(hostname,now)

# dict((k,len(v)) for (k,v) in qs[0]['spzline'].items())
def json_structure(dd):
    """Nested structure of JSON object. Avoid spewing big lists."""
    if type(dd) is list:
        return f'CNT={len(dd)}'
    elif type(dd) is dict:
        return dict((k,dict_structure(v)) for (k,v) in dd.items())
    else:
        return 'NA'
