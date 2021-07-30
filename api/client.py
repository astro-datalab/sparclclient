"""Client module for SPARCL.

This module interfaces to the SPARC-Server to get spectra data.

Todo:
  * Add conversion from Server pickle (json) to Pandas.

"""

# Python Standard Library
from urllib.parse import urlencode
from enum import Enum,auto
from pprint import pformat as pf
from pathlib import Path, PosixPath
from warnings import warn
import json
import pickle
from collections.abc import MutableMapping
# Local Packages
from api.utils import tic,toc
import api.exceptions as ex
# External Packages
import requests

#23456789.123456789.123456789.123456789.123456789.123456789.123456789.123456789.

# Upload to PyPi:
#   python3 -m build --wheel
#   twine upload dist/*

# Use Google Style Python Docstrings so autogen of Sphinx doc works:
#  https://www.sphinx-doc.org/en/master/usage/extensions/example_google.html#example-google

#### Generate documentation:
# cd ~/sandbox/sparclclient
# sphinx-apidoc -f -o source api
# make html
# firefox -new-tab "`pwd`/build/html/index.html"


## data = {
##     "a": "aval",
##     "b": {
##         "b1": {
##             "b2b": "b2bval",
##             "b2a": {
##                 "b3a": "b3aval",
##                 "b3b": "b3bval"
##             }
##         }
##     }
## }
##
## data1 = AttrDict(data)
## print(data1.b.b1.b2a.b3b)  # -> b3bval
class AttrDict(dict):
    """ Dictionary subclass whose entries can be accessed by attributes
    (as well as normally).
    """
    def __init__(self, *args, **kwargs):
        def from_nested_dict(data):
            """ Construct nested AttrDicts from nested dictionaries. """
            if not isinstance(data, dict):
                return data
            else:
                return AttrDict({key: from_nested_dict(data[key])
                                 for key in data})

        super(AttrDict, self).__init__(*args, **kwargs)
        self.__dict__ = self

        for key in self.keys():
            self[key] = from_nested_dict(self[key])

# A non-recursive version, which also works for numeric dictionary keys:
def set_value_at_path(obj, path, value):
    *parts, last = path.split('.')

    for part in parts:
        if isinstance(obj, MutableMapping):
            obj = obj[part]
        else:
            obj = obj[int(part)]

    if isinstance(obj, MutableMapping):
        obj[last] = value
    else:
        obj[int(last)] = value

def get_value_at_path(obj, path):
    *parts, last = path.split('.')

    for part in parts:
        if isinstance(obj, MutableMapping):
            obj = obj[part]
        else:
            obj = obj[int(part)]

    return(obj[last])

def obj_format(obj, seen=None, indent=0, showid=False, tab=4):
    """Recursively get the rough composition of a pure python object"""
    # Prevent following loops (self reference) in structures
    if seen is None:
        seen = set()
    oid = id(obj)
    if oid in seen:
        return ''
    seen.add(oid)
    idstr = f'{oid:<16}: ' if showid else ''
    s = ' '
    idspc = f'{s:<16}: ' if showid else ''

    spaces = ' ' * (indent * tab)
    res = spaces
    #!res = f'[{oid}] {spaces}'
    indent += 1
    spaces2 = ' ' * (indent * tab)
    if isinstance(obj, dict):
        res += f'{idstr}dict(\n'
        for k,v in obj.items():
            if v is None:
                valstr = None
            else:
                valstr = obj_format(v, seen, indent, showid).strip()
            #!res += f'{idstr}{spaces2}{k:16} = {valstr},\n'
            res += f'{idstr}{spaces2}{k} = {valstr},\n'
        res += f'{idspc}{spaces2})'
    elif isinstance(obj, list):
        if obj[0] is None:
            valstr = None
        else:
            valstr = obj_format(obj[0],seen,indent, showid).strip()
        res += f'<list {len(obj)}: obj[0]={valstr}> ...'
    else:
        res += f'type: {type(obj)}'

    return(res)


# Using HTTPie (http://httpie.org):
# http :8030/sparc/version

# sids = [394069118933821440, 1355741587413428224, 1355617892355303424, 1355615143576233984, 1355661872820414464, 1355755331308775424, 1355716848401803264]
# client = api.api.SparclApi(url='http://localhost:8030/sparc')
# client.retrieve(sids)[0].keys() # >> dict_keys(['flux','loglam'])
#
# data0 = client.retrieve(sids,columns='flux')
# f'{len(str(data0)):,}'   # -> '3,435,687'
#
# dataall = client.retrieve(sids,columns=allc)
# f'{len(str(dataall)):,}' # -> '27,470,052'

_PROD = 'https://specserver.noirlab.edu'
#_PAT = 'https://sparc1.datalab.noirlab.edu'
_PAT = 'http://sparc1.datalab.noirlab.edu:8000'
_PAT2 = 'http://sparc2.datalab.noirlab.edu:8000'
_DEV = 'http://localhost:8030'


allc = ['flux','loglam', 'ivar', 'and_mask', 'or_mask','wdisp', 'sky', 'model']

class SparclApi():
    """Provides interface to SPARCL Server.

    Object creation compares the version from the Server
    against the one expected by the Client. Throws error if
    the Client is a major version or more behind.
    """
    # version = 2.0;  <2021-07-04> retrieve return value includes status
    KNOWN_GOOD_API_VERSION = 2.0 #@@@ Change this when Server version increments

    def __init__(self, url=_PAT, verbose=False, limit=None):
        self.rooturl=url.rstrip("/")
        self.apiurl = f'{self.rooturl}/sparc'
        self.apiversion = None
        self.verbose = verbose
        self.limit = limit
        # require response within this num seconds
        # https://docs.python-requests.org/en/master/user/advanced/#timeouts
        # (connect time, read time)
        self.timeout = (1.1, 90*60) #(connect timeout, read timeout) seconds
        #@@@ read timeout should be a function of the POST payload size

        # Get API Version
        verstr = requests.get(f'{self.apiurl}/version/',timeout=self.timeout).content
        self.apiversion = float(verstr)

        if (int(self.apiversion) - int(SparclApi.KNOWN_GOOD_API_VERSION)) >= 1:
            msg = (f'The helpers.api module is expecting an older '
                   f'version of the {self.rooturl} API services. '
                   f'Please upgrade to latest "sparclclient".  '
                   f'This Client expected version '
                   f'{SparclApi.KNOWN_GOOD_API_VERSION} but got '
                   f'{self.apiversion} from the API.')
            raise Exception(msg)
        #self.session = requests.Session()

    def sample_sids(self, samples=5, structure='SDSS-DR16'):
        """Return a small list of spect ids.

        This is intended to make it easy to get just a few spect ids to use
        for experimenting with the rest of the API.
        """
        response = requests.get(
            f'{self.apiurl}/sample/?samples={samples}&dr={structure}',
            timeout=self.timeout)
        return response.json()

    @property
    def version(self):
        """Return version of Server Rest API used by this client.

        If the Rest API changes such that the Major version increases,
        a new version of this module will likely need to be used.

        Returns:
          float: API version

        Examples:
           >>> SparclApi('http://localhost:8030').version
           1.0
        """
        if self.apiversion is None:
            response = requests.get(f'{self.apiurl}/version',
                                    timeout=self.TIMEOUT,
                                    cache=True)
            self.apiversion = float(response.content)
        return self.apiversion

    def missing_sids(self, sid_list, countOnly=False, verbose=False):
        """Return the subset of the given spect id list that is NOT stored
        in the database."""
        verbose = verbose or self.verbose
        uparams = dict()
        qstr = urlencode(uparams)
        url = f'{self.apiurl}/missing/?{qstr}'
        if verbose:
            print(f'Using url="{url}"')
        res = requests.post(url, json=sid_list, timeout=self.timeout)
        res.raise_for_status()
        if res.status_code != 200:
            raise Exception(res)
        ret =  res.json()
        return ret


    def retrieve(self, sid_list,
                 include=None,  # None means include ALL
                 #!format=None,
                 structure='SDSS-DR16',
                 xfer='database',
                 limit=False, verbose=False):
        """Get spectrum from spect id list.

        Args:
           sid_list (list): list of spect ids
           include (dict, optional): (default: include ALL) List of paths
              to include in each record. key=storedPath, val=alias
           structure (str): the data structure of the spect ids
           xfer (str): (default='database') DEBUG.
              Format to use to transfer from Server to Client
           limit (int, optional): Maximum number of spectra records to return.
        Returns:
           list of record's data
        """
        #! Args TODO
        #!   format (str): Format of the data structure that contains spectra

        verbose = verbose or self.verbose
        lim = None if limit is None else (limit or self.limit)

        uparams =dict(include=include,
                      limit=lim,
                      dr=structure)
        if xfer is not None:
            uparams['xfer'] = xfer
        qstr = urlencode(uparams)

        url = f'{self.apiurl}/retrieve/?{qstr}'
        if verbose:
            print(f'Using url="{url}"')
            tic()

        res = requests.post(url, json=sid_list, timeout=self.timeout)
        if verbose:
            elapsed = toc()

        if res.status_code != 200:
            #!print(f'DBG: res.json={res.json()}')
            raise ex.genSparclException(**res.json())

        if xfer=='p':
            ret = pickle.loads(res.content)
        elif xfer=='database':
            #!ret =  res.json()
            meta,*records =  res.json()
            #!print(f'DBG: meta={meta}')
        else:
            print(f'Unknown xfer parameter value "{xfer}". Defaulting to json')
            ret =  res.json()
        if verbose:
            count = len(records)
            print(f'Got {count} spectra in '
                  f'{elapsed:.2f} seconds ({count/elapsed:.0f} '
                  'spectra/sec)')
            print(f'{meta["status"]}')

        if len(meta['status'].get('warnings',[])) > 0:
            warn(f"{'; '.join(meta['status'].get('warnings'))}")

        #!if not meta['status'].get('success'):
        #!    raise Exception(f"Error in retrieve: {meta['status']}")

        return( [AttrDict(r) for r in records] )

    def sample_records(self, count, structure='SDSS-DR16', **kwargs):
        """Return COUNT random records from given STRUCTURE"""
        return self.retrieve(self.sample_sids(count, structure=structure),
                             structure=structure, **kwargs)

    # EXAMPLES:
    # client.show_record_structure('DESI-denali',xfer='database')
    # client.show_record_structure('SDSS-DR16')
    # client.show_record_structure('SDSS-DR16',columns=['flux', 'loglam', 'ivar',  'and_mask', 'or_mask', 'wdisp', 'sky', 'model'])
    #
    def show_record_structure(self, structure, **kwargs):
        """Show the structure of a record retrieved from STRUCTURE using
        transfer method XFER"""
        res = self.sample_records(1, structure=structure, **kwargs)
        rec = res[0]
        print(obj_format(rec))
        return rec
    # rec = client.show_record_structure('SDSS-DR16',xfer='database')
    # rec1 = api.client.AttrDict(rec)
    # rec1.spectra.specobj.CZ => [0.6159544898118924]

if __name__ == "__main__":
    import doctest
    doctest.testmod()
