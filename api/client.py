"""Client module for SPARCL.

This module interfaces to the SPARC-Server to get spectra data.

Todo:

  * Handle errors

    Data Type conversion is not possible if the restricted set of
    fields specified in INCLUDE parameter is insufficient for the
    desired Data Type. For instance, the 'Spectrum1D' type requires 3
    vector fields.  If they are not all INCLUDEd, fail gracefully.

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
import pkg_resources
# Local Packages
from api.utils import tic,toc
import api.utils as ut
import api.exceptions as ex
import api.type_conversion as tc
# External Packages
import requests

#23456789.123456789.123456789.123456789.123456789.123456789.123456789.123456789.

# Upload to PyPi:
#   python3 -m build --wheel
#   twine upload dist/*

# Use Google Style Python Docstrings so autogen of Sphinx doc works:
#  https://www.sphinx-doc.org/en/master/usage/extensions/example_google.html#example-google
#
# Use sphinx-doc emacs minor mode to insert docstring skeleton.
# C-c M-d in function/method def

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


#!def dict2tree(obj, name=None):
#!    """Return abstracted nested tree. Terminals contain TYPE"""
#!    if isinstance(obj, dict):
#!        children = dict()
#!        for (k,v) in obj.items():
#!            if isinstance(v, dict) or isinstance(v, list):
#!                val = dict2tree(v, name=k)
#!            else:
#!                val = {k: type(v)}
#!                #!val = {k: '-'}
#!            children.update(val)
#!        tree = children if name is None else {name:  children}
#!    elif isinstance(obj, list):
#!        children = dict()
#!        for n,v in enumerate(obj[:1]):
#!            k = f'<list({len(obj)})[0]>'
#!            if isinstance(v, dict) or isinstance(v, list):
#!                val = dict2tree(v, name=k)
#!            else:
#!                val = {k: type(v)}
#!                #!val = {k: '-'}
#!            children.update(val)
#!        tree = {name:  children}
#!    else:
#!        tree = {name,type(obj)}
#!    return(tree)
#!
#!# RETURN: nested list of node names
#!def tree_nodes(tree):
#!    """e.g. [name, name-child1, name-child2, [name-child3, name-granchild]]"""
#!    res = []
#!    if not isinstance(tree, dict):
#!        return tree
#!    for k,v in tree.items():
#!        if isinstance(v, dict):
#!            if list(v.keys())[0].startswith('<list') :
#!                res.append(k) # treat "type dict" as terminal
#!            else:
#!                res.append([k] + tree_nodes(v))
#!        else: # v is not dict
#!            res.append(k)
#!    return res
#!
#!
#!def obj_format(obj, seen=None, indent=0, showid=False, tab=4):
#!    """Recursively get the rough composition of a pure python object. Used in show_record_structure().
#!
#!        Args:
#!           obj (AttrDict): pure python object.
#!           seen (str, optional): (default: None) set of objects already visited. Avoid infinite loops!
#!           indent (int, optional): (default: 0) level of indentation for printing the format of obj.
#!           showid (boolean, optional): (default: False) OBSOLETE. # Code should be changed to remove use of this.
#!           tab (int, optional): (default: 4) amount of spaces to use for one level of indentation.
#!        Returns:
#!           The rough composition of a pure python object.
#!        Example:
#!           >>> res = client.sample_records(1)[0]
#!           >>> print(obj_format(res))
#!        """
#!    # Prevent following loops (self reference) in structures
#!    if seen is None:
#!        seen = set()
#!    oid = id(obj)
#!    if oid in seen:
#!        return ''
#!    seen.add(oid)
#!    idstr = f'{oid:<16}: ' if showid else ''
#!    s = ' '
#!    idspc = f'{s:<16}: ' if showid else ''
#!
#!    spaces = ' ' * (indent * tab)
#!    res = spaces
#!    #!res = f'[{oid}] {spaces}'
#!    indent += 1
#!    spaces2 = ' ' * (indent * tab)
#!    if isinstance(obj, dict):
#!        res += f'{idstr}dict(\n'
#!        for k,v in obj.items():
#!            if v is None:
#!                valstr = None
#!            else:
#!                valstr = obj_format(v, seen, indent, showid).strip()
#!            #!res += f'{idstr}{spaces2}{k:16} = {valstr},\n'
#!            res += f'{idstr}{spaces2}{k} = {valstr},\n'
#!        res += f'{idspc}{spaces2})'
#!    elif isinstance(obj, list):
#!        if obj[0] is None:
#!            valstr = None
#!        else:
#!            valstr = obj_format(obj[0],seen,indent, showid).strip()
#!        res += f'<list {len(obj)}: obj[0]={valstr}> ...'
#!    else:
#!        res += f'type: {type(obj)}'
#!
#!    return(res)


# Using HTTPie (http://httpie.org):
# http :8030/sparc/version

# specids = [394069118933821440, 1355741587413428224, 1355617892355303424, 1355615143576233984, 1355661872820414464, 1355755331308775424, 1355716848401803264]
# client = api.api.SparclApi(url='http://localhost:8030/sparc')
# client.retrieve(specids)[0].keys() # >> dict_keys(['flux','loglam'])
#
# data0 = client.retrieve(specids,columns='flux')
# f'{len(str(data0)):,}'   # -> '3,435,687'
#
# dataall = client.retrieve(specids,columns=allc)
# f'{len(str(dataall)):,}' # -> '27,470,052'

_PROD = 'https://specserver.noirlab.edu'
_PAT = 'http://sparc1.datalab.noirlab.edu:8000'
_PAT2 = 'http://sparc2.datalab.noirlab.edu:8000'
_DEV = 'http://localhost:8030'


client_version = pkg_resources.require("sparclclient")[0].version

class SparclApi():
    """Provides interface to SPARCL Server.

    When using this to report a bug, set verbose to True. Also print
    your instance of this.  The results will include important info
    about the Client and Server.
    Example:
      >>> client = SparclApi(verbose=True)
      >>> print(client)

    Object creation compares the version from the Server
    against the one expected by the Client. Throws error if
    the Client is a major version or more behind.
    """
    KNOWN_GOOD_API_VERSION = 3.0 #@@@ Change this when Server version increments


    def __init__(self, url=_PAT, verbose=False):
        """Create client instance.

        :param url: Base URL of SPARC Server
        :param verbose: (True,False) Default verbosity for all client methods.

        """
        self.rooturl=url.rstrip("/")
        self.apiurl = f'{self.rooturl}/sparc'
        self.apiversion = None
        self.verbose = verbose
        # require response within this num seconds
        # https://docs.python-requests.org/en/master/user/advanced/#timeouts
        # (connect time, read time)
        self.timeout = (1.1, 90*60) #(connect timeout, read timeout) seconds
        #@@@ read timeout should be a function of the POST payload size

        # Get API Version
        verstr = requests.get(
            f'{self.apiurl}/version/',timeout=self.timeout).content
        self.apiversion = float(verstr)

        if (int(self.apiversion) - int(SparclApi.KNOWN_GOOD_API_VERSION)) >= 1:
            msg = (f'The SPARCL Client you are running expects an older '
                   f'version of the API services. '
                   f'Please upgrade to the latest "sparclclient".  '
                   f'The Client you are using expected version '
                   f'{SparclApi.KNOWN_GOOD_API_VERSION} but got '
                   f'{self.apiversion} from the SPARCL Server at {self.apiurl}.')
            raise Exception(msg)
        #self.session = requests.Session()

        self.clientversion = client_version

        #############################
        ### Convenience LookUp Tables derived from one query
        ###
        # dfLUT[dr][origPath] => dict[new=newPath,required=bool]
        self.dfLUT = requests.get(f'{self.apiurl}/fields/').json()

        # required[dr] => newPath
        self.required = dict(
            (dr, [d['new'] for orig,d in v.items() if d['required']])
            for dr,v in self.dfLUT.items())

        # orig2newLUT[dr][orig] = new
        self.orig2newLUT = dict((dr,dict((orig,d['new'])
                                         for orig,d in v.items()))
                                for dr,v in self.dfLUT.items())
        # new2origLUT[dr][new] = orig
        self.new2origLUT = dict((dr,dict((d['new'],orig)
                                         for orig,d in v.items()))
                                for dr,v in self.dfLUT.items())

        # dict[drName] = [fieldName, ...]
        self.dr_fields = dict((dr,v) for dr,v in self.new2origLUT.items())
        ###
        ###################

    def get_field_names(self, structure):
        """List field names available for retreive."""
        dr = structure
        if dr in self.dr_fields:
            return list(self.dr_fields[dr].keys())
        else:
            print(f'That is not a currently support structure. '
                  f'Available structures are: '
                  f"{', '.join(self.dr_fields.keys())}"
                  )
            return None

    def orig_field(self, structure, client_name):
        """Get original field name as provided in Data Release.

        :param structure: Name of data set Structure
        :param client_name: Field name used in Client methods.
        :returns: Original field name
        :rtype: string

        """
        return self.new2origLUT[structure][client_name]

    def client_field(self, structure, orig_name):
        """Get field name used in Client methods

        :param structure: Name of data set Structure
        :param orig_name: Original field name as provided in Data Release.
        :returns: Client field name
        :rtype: string

        """
        return self.orig2newLUT[structure][orig_name]


    def __repr__(self):
        return(f'(sparclclient:{self.clientversion}, '
               f'api:{self.apiversion}, {self.apiurl})')

    def sample_specids(self, samples=5, structure=None):
        """Return a small list of specids.

        This is intended to make it easy to get just a few specids to use
        for experimenting with the rest of the API.

        Args:
           samples (int, optional): (default: 5) The number of sample specids to get.
           structure (str, optional): (default: None means ANY) The data structure from which to get specids.
        Returns:
           List of specids.
        Example:
           >>> client.sample_specids(samples=3, structure='DESI-denali')
           [616088561849992155, 39633331515559899, 39633328084618293]
        """
        url = f'{self.apiurl}/sample/?samples={samples}&dr={structure}'
        if self.verbose:
            print(f'Using url="{url}"')
        response = requests.get(url, timeout=self.timeout)
        return response.json()

    @property
    def version(self):
        """Return version of Server Rest API used by this client.

        If the Rest API changes such that the Major version increases,
        a new version of this module will likely need to be used.

        Returns:
          float: API version.
        Example:
           >>> SparclApi('http://localhost:8030').version
           1.0
        """
        if self.apiversion is None:
            response = requests.get(f'{self.apiurl}/version',
                                    timeout=self.TIMEOUT,
                                    cache=True)
            self.apiversion = float(response.content)
        return self.apiversion

    def missing_specids(self, specid_list, countOnly=False, verbose=False):
        """Return the subset of the given specid list that is NOT stored
        in the database.

        Args:
           specid_list (list): List of specids.
           verbose (boolean, optional): (default: False)
        Returns:
           The subset of the given specid list that is NOT stored in the database.
        Example:
           >>> si = [1858907533188556800, 6171312851359387648, 1647268306035435520]
           >>> client.missing_specids(si)
           [1858907533188556800, 6171312851359387648]
        """
        # Removed documentation
        #! countOnly (boolean, optional): (default: False) If true, only return the count of missing specids.


        verbose = verbose or self.verbose
        uparams = dict()
        qstr = urlencode(uparams)
        url = f'{self.apiurl}/missing/?{qstr}'
        if verbose:
            print(f'Using url="{url}"')
        res = requests.post(url, json=specid_list, timeout=self.timeout)
        res.raise_for_status()
        if res.status_code != 200:
            raise Exception(res)
        ret =  res.json()
        return ret

    def _specids2tuples(self, specids, structure):
        uparams =dict(dr=structure)
        qstr = urlencode(uparams)
        url = f'{self.apiurl}/specids2tuples/?{qstr}'
        res = requests.post(url, json=specids, timeout=self.timeout)

    def _validate_include(self, dr, include_list):
        if include_list is None:
            return True
        if not isinstance(include_list, list):
            raise Exception(
                f'INCLUDE parameter must be a LIST of field names. '
                f'Got: "{include_list}"')
        if (include_list is not None) and (dr is None):
            raise Exception(
                'Currently we do not support using an include_list '
                'when NOT specifying a structure')

        incSet = set(include_list)
        #!print(f'incSet={incSet} dr_fields={self.dr_fields[dr]}')
        unknown = incSet.difference(self.dr_fields[dr])
        if len(unknown) > 0:
            msg = (f'The INCLUDE list contains invalid data field names '
                   f'for Structure "{dr}" '
                   f'({", ".join(sorted(list(unknown)))}). '
                   f'Available fields are: '
                   f'{", ".join(sorted(self.dr_fields[dr]))}.'
                   )
            raise ex.BadInclude(msg)
        return True

    def retrieve(self, specid_list,
                 include=None,  # None means include ALL
                 #!format=None,
                 rtype=None,
                 structure=None, # was 'SDSS-DR16'
                 #xfer='database',
                 verbose=False):
        """Get spectrum from specid list.

        Args:
           specid_list (list): List of specids.
           include (list, optional): (default: None, means include ALL)
              List of paths to include in each record.
           structure (str): The data structure (DS) name associated with
              the specids.
              Or None to retrieve from any DS that contains the specid.
           verbose (boolean, optional): (default: False)
        Returns:
           List of records. Each record is a dictionary of named fields.
        Example:
           >>> ink = ['flux']
           >>> sdss_ids = [849044290804934656, 309718438815754240]
           >>> res_sdss = client.retrieve(sdss_ids, structure='SDSS-DR16', include=ink)
        """
        # OLD doc string fragments
        #!   xfer (str): (default='database') DEBUG.
        #!      Format to use to transfer from Server to Client.

        self._validate_include(structure, include)

        verbose = verbose or self.verbose
        if verbose:
            print(f'retrieve(rtype={rtype})')

        uparams =dict(include='None' if include is None else ','.join(include),
                      dr=structure)
        #! if xfer is not None:
        #!     uparams['xfer'] = xfer
        qstr = urlencode(uparams)

        url = f'{self.apiurl}/retrieve/?{qstr}'
        if verbose:
            print(f'Using url="{url}"')
            tic()

        res = requests.post(url, json=specid_list, timeout=self.timeout)
        if verbose:
            elapsed = toc()
            print(f'Got response to post in {elapsed} seconds')

        if res.status_code != 200:
            if verbose and ('traceback' in res.json()):
                #!print(f'DBG: res.json={res.json()}')
                print(f'DBG: Server traceback=\n{res.json()["traceback"]}')
            raise ex.genSparclException(**res.json())

        #!if xfer=='p':
        #!    ret = pickle.loads(res.content)
        #!elif xfer=='database':
        #!    #!ret =  res.json()
        #!    meta,*records =  res.json()
        #!    #!print(f'DBG: meta={meta}')
        #!else:
        #!    print(f'Unknown xfer parameter value "{xfer}". Defaulting to json')
        #!    ret =  res.json()
        meta,*records = res.json()
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

        return( [AttrDict(tc.convert(r, rtype, self, include))
                 for r in records] )
        #!return( records )

    def sample_records(self, count, structure=None, **kwargs):
        """Return COUNT random records from given STRUCTURE.

        Args:
           count (int): Number of sample records to get from database.

           structure (str, optional): (default: None means ANY)
               The data structure from which to get sample records.

        Returns:
           COUNT random records from given STRUCTURE.
        Example:
           >>> samrec = client.sample_records(1, structure='BOSS-DR16')
           >>> pprint.pprint(samrec,depth=2)
           [{'data_release_id': 'BOSS-DR16',
             'dec_center': 47.193549,
             'dirpath': '/net/mss1/archive/hlsp/sdss/dr16/eboss/spectro/redux/v5_13_0/spectra/lite/7399',
             'filename': 'spec-7399-57162-0376.fits',
             'specid': 1429845755960551,
             'spectra': {...},
             'updated': '2021-04-28T20:16:20.399464Z'}]
        """
        kverb = kwargs.pop('verbose',None)
        verb = self.verbose if kverb is None else kverb

        sids = self.sample_specids(count, structure=structure)
        return self.retrieve(sids, structure=structure, verbose=verb, **kwargs)

    # EXAMPLES:
    # client.show_record_structure('DESI-denali',xfer='database')
    # client.show_record_structure('SDSS-DR16')
    # client.show_record_structure('SDSS-DR16',columns=['flux', 'loglam', 'ivar',  'and_mask', 'or_mask', 'wdisp', 'sky', 'model'])
    #
    def get_record_structure(self, structure, **kwargs):
        """Get the structure of a record retrieved from STRUCTURE.

        Args:
           structure (str): The data structure.
        Returns:
           Dictionary of the record structure for the specified data structure.
        Example:
           >>> d = client.get_record_structure('DESI-denali')
        """
        recs = self.sample_records(1, structure=structure, **kwargs)
        return ut.dict2tree(recs[0])


if __name__ == "__main__":
    import doctest
    doctest.testmod()
