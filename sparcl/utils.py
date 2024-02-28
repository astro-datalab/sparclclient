# Python library
import datetime
import time
import socket
import itertools
import json
import subprocess

# External packages
#   none
# LOCAL packages
#   none


# data = {
#     "a": "aval",
#     "b": {
#         "b1": {
#             "b2b": "b2bval",
#             "b2a": {
#                 "b3a": "b3aval",
#                 "b3b": "b3bval"
#             }
#         }
#     }
# }
#
# data1 = AttrDict(data)
# print(data1.b.b1.b2a.b3b)  # -> b3bval
class _AttrDict(dict):
    """Dictionary subclass whose entries can be accessed by attributes
    (as well as normally).
    """

    def __init__(self, *args, **kwargs):
        def from_nested_dict(data):
            """Construct nested AttrDicts from nested dictionaries."""
            if not isinstance(data, dict):
                return data
            else:
                return _AttrDict(
                    {key: from_nested_dict(data[key]) for key in data}
                )

        super(_AttrDict, self).__init__(*args, **kwargs)
        self.__dict__ = self

        for key in self.keys():
            self[key] = from_nested_dict(self[key])


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
    return elapsed_seconds  # fractional


def here_now():
    """Used to track info for benchmark. Probably OBE?

    Args:
       None.
    Returns:
       Time, date, and hostname.
    """
    hostname = socket.gethostname()
    now = str(datetime.datetime.now())
    return (hostname, now)


def objform(obj):
    """Nested structure of python object. Avoid spewing big lists.
    See also: https://code.activestate.com/recipes/577504/

    Args:
       obj: Python object.
    Returns:
       Length if list, objforms of dict contents if dict, type if
       anything else.
    Example:
       >>> res = client.sample_records(1)[0]
       >>> objform(res)
       <class 'sparcl.client.AttrDict'>
    """
    # dict((k,len(v)) for (k,v) in qs[0]['spzline'].items())
    if obj is None:
        return None
    elif type(obj) is list:
        if len(obj) > 999:
            return f"CNT={len(obj)}"
        elif len(obj) < 9:
            return [objform(x) for x in obj]
        else:
            return [objform(x) for x in obj[:10]] + ["..."]
    elif type(obj) is dict:
        return dict((k, objform(v)) for (k, v) in obj.items())
    else:
        return str(type(obj))


def dict2tree(obj, name=None, prefix=""):
    """Return abstracted nested tree. Terminals contain TYPE.
    As a special case, a list is given as a dict that represents a
    compound type.  E.G. {'<list(3835)[0]>': float} means a list of
    3835 elements where the first element is of type 'float'.  NB:
    Only the type of the first element in a list is given.  If the
    list has hetergeneous types, that fact is invisible in the
    structure!!
    """
    nextpfx = "" if name is None else (prefix + name + ".")
    showname = prefix if name is None else (prefix + name)
    if isinstance(obj, dict):
        children = dict()
        for k, v in obj.items():
            if isinstance(v, dict) or isinstance(v, list):
                val = dict2tree(v, name=k, prefix=nextpfx)
            else:
                #!val = {k: type(v).__name__}
                val = {nextpfx + k: type(v).__name__}
            children.update(val)
        tree = children if name is None else {showname: children}
    elif isinstance(obj, list):
        children = f"<list({len(obj)})[0]>:{type(obj[0]).__name__}"
        tree = {showname: children}
    else:
        tree = {showname: type(obj).__name__}
    return tree


def invLUT(lut):
    """Given dict[k]=v, Return dict[v]=k"""
    return {v: k for k, v in lut.items()}


def count_values(recs):
    """Count number of non-None values in a list of dictionaries.
    A key that exists with a value of None is treated the same as a
    key that does not exist at all. i.e. It does not add to the count.

    Args:
       recs (:obj:`list`): ('records') List of dictionaries.

    Returns:
        A dictionary. Keys are the full list of keys available in any
        of the recs.  Values are the count of occurances of non-None values
        for that key.

    >>> count_values([dict(a=None, b=3), dict(a=1, b=2), dict(a=None, b=2)])
    {'a': 1, 'b': 3}
    """
    allkeys = set(list(itertools.chain(*recs)))
    return {k: sum(x.get(k) is not None for x in recs) for k in allkeys}


# In case I want to give CURL equivalents for client methods.
#
# Retrieve may return results as a pickle file since it usually contains
# spectra vectors.  To handle pickle results, write curl output to out.pkl
# and do something like:
#   with open('out.pkl', 'rb') as f: res = pickle.load(f)
def curl_retrieve_str(ids, server, svc="spectras", qstr=None):
    #! ids = ['00000dd7-b1ff-48ed-b162-46d9d65f829c', 'BADID']
    #!svc = 'spectras' if use_async else 'retrieve'
    #! qstr = urlencode(uparams)
    # server = "https://sparc1.datalab.noirlab.edu"
    qqstr = "" if qstr is None else f"?{qstr}"
    url = f"{server}/sparc/{svc}/{qqstr}"
    curlpost1 = "curl -X 'POST' -H 'Content-Type: application/json' "
    curlpost2 = f"-d '{json.dumps(ids)}' '{url}'"
    curlpost3 = " | python3 -m json.tool"
    return curlpost1 + curlpost2 + curlpost3


# see: curl_retrieve_str
def curl_find_str(sspec, server, qstr=None):
    qqstr = "" if qstr is None else f"?{qstr}"
    url = f"{server}/sparc/find/{qqstr}"
    curlpost1 = "curl -X 'POST' -H 'Content-Type: application/json' "
    curlpost2 = f"-d '{json.dumps(sspec)}' '{url}'"
    curlpost3 = " | python3 -m json.tool"
    return curlpost1 + curlpost2 + curlpost3


def githash(verbose=False):
    try:
        #  "/usr/bin/git"
        ret = subprocess.run(["git", "rev-parse", "HEAD"], capture_output=True)
        commit_hash = ret.stdout.decode().strip()
    except Exception as err:
        if verbose:
            print(err)
        commit_hash = "<NA>"
    return commit_hash
