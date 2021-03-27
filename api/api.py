# Python Standard Library
from urllib.parse import urlencode
from enum import Enum,auto
from pprint import pformat as pf
from pathlib import Path, PosixPath
from warnings import warn
import json
# Local Packages
from api.utils import tic,toc
# External Packages
import requests

# Using HTTPie (http://httpie.org):
# http :8030/sparc/version

# sids = [394069118933821440, 1355741587413428224, 1355617892355303424, 1355615143576233984, 1355661872820414464, 1355755331308775424, 1355716848401803264]
# client = api.api.SparcApi(url='http://localhost:8030/sparc')
# client.retrieve(sids)[0].keys() # >> dict_keys(['flux','loglam'])
#
# data0 = client.retrieve(sids,columns='flux')
# f'{len(str(data0)):,}'   # -> '3,435,687'
#
# dataall = client.retrieve(sids,columns=allc)
# f'{len(str(dataall)):,}' # -> '27,470,052'

_PROD = 'https://specserver.noirlab.edu'
_DEV = 'http://localhost:8030/sparc'

allc = ['flux','loglam', 'ivar', 'and_mask', 'or_mask','wdisp', 'sky', 'model']

class SparcApi():
    """Astro Data Archive - Application Programming Interface.
    Object creation compares the version from the Server
    against the one expected by the Client. Throws error if
    the Client is a major version or more behind.
    """
    KNOWN_GOOD_API_VERSION = 6.0 #@@@ Change this when Server version increments

    #! def __init__(self, url=_PROD, verbose=False): @@@
    def __init__(self, url=_DEV, verbose=False, limit=None):
        self.rooturl=url.rstrip("/")
        self.apiurl = f'{self.rooturl}'
        self.apiversion = None
        self.verbose = verbose
        self.limit = limit

        # Get API Version
        self.apiversion = float(requests.get(f'{self.apiurl}/version/').content)

        if (int(self.apiversion) - int(SparcApi.KNOWN_GOOD_API_VERSION)) >= 1:
            msg = (f'The helpers.api module is expecting an older '
                   f'version of the {self.rooturl} API services. '
                   f'Please upgrade to latest "aa_wrap".  '
                   f'This Client expected version '
                   f'{AdaApi.KNOWN_GOOD_API_VERSION} but got '
                   f'{self.apiversion} from the API.')
            raise Exception(msg)
        self.session = requests.Session()


    def retrieve(self, objid_list, columns=None, limit=False, verbose=False):
        """Get spectrum from spectObjId list"""
        verbose = verbose or self.verbose
        lim = None if limit is None else (limit or self.limit)

        cols = ['flux', 'loglam'] if columns is None else columns
        uparams =dict(limit=lim, columns=','.join(cols))
        qstr = urlencode(uparams)

        url = f'{self.apiurl}/retrieve/?{qstr}'
        if verbose:
            tic()
        res = self.session.post(url, json=objid_list)
        if verbose:
            elapsed = toc()
        res.raise_for_status()

        if res.status_code != 200:
            raise Exception(res)

        if verbose:
            count = len(res.json())
            print(f'From "{url}" got {count} spectra in '
                  f'{elapsed:.2f} seconds ({count/elapsed:.0f} spectra/sec)')
        return res.json()
