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
    """Start tracking elapsed time. Works in conjunction with toc().

    Args:
       None.
    Returns:
       Elapsed time.
    """
    tic.start = time.perf_counter()

def toc():
    """Return elapsed time since previous tic().

    Args:
       None.
    Returns:
       Elapsed time since previous tic().
    """
    elapsed_seconds = time.perf_counter() - tic.start
    return elapsed_seconds # fractional

def here_now():
    """Used to track info for benchmark. Probably OBE?

    Args:
       None.
    Returns:
       Time, date, and hostname.
    """
    hostname = socket.gethostname()
    now =  str(datetime.datetime.now())
    return(hostname,now)

# dict((k,len(v)) for (k,v) in qs[0]['spzline'].items())
def objform(obj):
    """Nested structure of python object. Avoid spewing big lists.
    See also: https://code.activestate.com/recipes/577504/

    Args:
       obj: Python object.
    Returns:
       Length if list, objforms of dict contents if dict, type if anything else.
    Example:
       >>> res = client.sample_records(1)[0]
       >>> objform(res)
       <class 'api.client.AttrDict'>
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

def dict2tree(obj, name=None, prefix=''):
    """Return abstracted nested tree. Terminals contain TYPE.
    As a special case, a list is given as a dict that represents a compound
    type.  E.G. {'<list(3835)[0]>': float} means a list of 3835 elements where
    the first element is of type 'float'.  NB: Only the type of the first element
    in a list is given.  If the list has hetergeneous types, that fact is
    invisible in the structure!!
    """
    nextpfx = '' if name is None else (prefix + name + '.')
    showname = prefix if name is None else (prefix + name)
    if isinstance(obj, dict):
        children = dict()
        for (k,v) in obj.items():
            if isinstance(v, dict) or isinstance(v, list):
                val = dict2tree(v, name=k, prefix=nextpfx)
            else:
                #!val = {k: type(v).__name__}
                val = {nextpfx+k: type(v).__name__}
            children.update(val)
        tree = children if name is None else {showname:  children}
    elif isinstance(obj, list):
        children = f'<list({len(obj)})[0]>:{type(obj[0]).__name__}'
        tree = {showname: children}
    else:
        tree = {showname: type(obj).__name__}
    return(tree)
