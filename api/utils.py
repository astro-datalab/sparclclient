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
def objform(obj):
    """Nested structure of python object. Avoid spewing big lists.
    See also: https://code.activestate.com/recipes/577504/
    """
    if obj is None:
        return None
    elif type(obj) is list:
        if len(obj) > 999:
            return f'CNT={len(obj)}'
        elif len(obj) < 9:
            return [objform(x) for x in obj]
        else:
            return [objform(x) for x in obj[:10]] + ['...']
    elif type(obj) is dict:
        return dict((k,objform(v)) for (k,v) in obj.items())
    else:
        return str(type(obj))
