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
# Local Packages
from api.utils import tic,toc
# External Packages
import requests

# Use Google Style Python Docstrings so autogen of Sphinx doc works:
#  https://www.sphinx-doc.org/en/master/usage/extensions/example_google.html#example-google

#### Generate documentation:
# cd ~/sandbox/sparclclient
# sphinx-apidoc -f -o source api
# make html
# firefox -new-tab "`pwd`/build/html/index.html"


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
#_TEST = 'https://sparc1.datalab.noirlab.edu'
_TEST = 'http://sparc1.datalab.noirlab.edu:8000'
_DEV = 'http://localhost:8030'


allc = ['flux','loglam', 'ivar', 'and_mask', 'or_mask','wdisp', 'sky', 'model']

class SparclApi():
    """Provides interface to SPARCL Server.

    Object creation compares the version from the Server
    against the one expected by the Client. Throws error if
    the Client is a major version or more behind.
    """
    KNOWN_GOOD_API_VERSION = 1.0 #@@@ Change this when Server version increments

    def __init__(self, url=_TEST, verbose=False, limit=None):
        self.rooturl=url.rstrip("/")
        self.apiurl = f'{self.rooturl}/sparc'
        self.apiversion = None
        self.verbose = verbose
        self.limit = limit
        # require response within this num seconds
        self.timeout = (1.1, 90*60) #(connect timeout, read timeout) seconds
        #@@@ read timeout should be a function of the POST payload size

        # Get API Version
        verstr = requests.get(f'{self.apiurl}/version/',timeout=self.timeout).content
        self.apiversion = float(verstr)

        if (int(self.apiversion) - int(SparclApi.KNOWN_GOOD_API_VERSION)) >= 1:
            msg = (f'The helpers.api module is expecting an older '
                   f'version of the {self.rooturl} API services. '
                   f'Please upgrade to latest "aa_wrap".  '
                   f'This Client expected version '
                   f'{AdaApi.KNOWN_GOOD_API_VERSION} but got '
                   f'{self.apiversion} from the API.')
            raise Exception(msg)
        #self.session = requests.Session()

    def sample_sids(self):
        """Return a small list of spect ids.

        This is intended to make it easy to get just a few spect ids to use
        for experimenting with the rest of the API.
        """
        response = requests.get(f'{self.apiurl}/sample', timeout=self.timeout)
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

    def retrieve(self, objid_list,
                 columns=None,  format=None,
                 xfer=None, limit=False, verbose=False):
        """Get spectrum from spectObjId list.

        Args:
           columns (list[int], optional): List of column names.
              Defaults to ['flux', 'loglam'].
              One of: flux, loglam, ivar,  and_mask, or_mask, wdisp, sky, model
           format (str): TODO. Format of the data structure that contains spectra
           xfer (str): DEBUGGING. Format to use to transfer from Server to Client
           limit (int, optional): Maximum number of spectra records to return.

        Returns:
           list: JSON structures (format=None).

        """
        coadd_columns = ['flux', 'loglam', 'ivar',  'and_mask', 'or_mask',
                         'wdisp', 'sky', 'model']
        dftcols = ['flux', 'loglam']
        verbose = verbose or self.verbose
        lim = None if limit is None else (limit or self.limit)

        cols = dftcols if columns is None else columns
        uparams =dict(columns=','.join(cols), limit=lim)
        if xfer is not None:
            uparams['xfer'] = xfer
        qstr = urlencode(uparams)

        url = f'{self.apiurl}/retrieve/?{qstr}'
        if verbose:
            print(f'Using url="{url}"')
            if columns is None:
                print(f'WARNING: No "columns" parameter provided. '
                      f'Defaulting to {dftcols}. '
                      f'The available columns are {allc}')
            tic()
        #@@@res = self.session.post(url, json=objid_list, timeout=self.timeout)
        res = requests.post(url, json=objid_list, timeout=self.timeout)
        if verbose:
            elapsed = toc()

        res.raise_for_status()

        if res.status_code != 200:
            raise Exception(res)

        if xfer=='p':
            ret = pickle.loads(res.content)
        elif xfer=='database':
            ret =  res.json()
        else:
            print(f'Unknown xfer paremter value "{xfer}". Defaulting to json')
            ret =  res.json()
        if verbose:
            count = len(ret)
            print(f'Got {count} spectra in '
                  f'{elapsed:.2f} seconds ({count/elapsed:.0f} '
                  'spectra/sec)')

        return ret

if __name__ == "__main__":
    import doctest
    doctest.testmod()
