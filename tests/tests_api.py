# Unit tests for the NOIRLab SPARCL API Client
# EXAMPLES: (do after activating venv, in sandbox/sparclclient/)
#   python -m unittest tests.tests_api
#
#  ### Run against DEV server.
#  serverurl=http://localhost:8050 python -m unittest tests.tests_api
#  showres=1 serverurl=http://localhost:8050 python -m unittest tests.tests_api
#
# python -m unittest  -v tests.tests_api    # VERBOSE
# python -m unittest tests.tests_api.SparclClientTest
# python -m unittest tests.tests_api.SparclClientTest.test_find_3

# Python library
import unittest
from unittest import skip
#! from unittest mock, skipIf, skipUnless
#!import warnings
from pprint import pformat as pf
from urllib.parse import urlparse
#!from unittest.mock import MagicMock
#!from unittest.mock import create_autospec
import os
# Local Packages
import sparcl.client
#from sparcl.client import DEFAULT, ALL
from tests.utils import tic, toc
import tests.expected as exp_pat
import tests.expected_dev1 as exp_dev
import sparcl.exceptions as ex
# External Packages
# <none>

DEFAULT = 'DEFAULT'
ALL = 'ALL'
drs = ['BOSS-DR16']

_DEV1  = 'http://localhost:8050'                    # noqa: E221
_PAT1  = 'https://sparc1.datalab.noirlab.edu'       # noqa: E221
_STAGE = 'https://sparclstage.datalab.noirlab.edu'  # noqa: E221
_PROD  = 'https://astrosparcl.datalab.noirlab.edu'  # noqa: E221

serverurl = os.environ.get('serverurl', _PAT1)
DEV_SERVERS = ['http://localhost:8050', ]
if serverurl in DEV_SERVERS:
    exp = exp_dev
else:
    exp = exp_pat


#!idfld = 'uuid'  # Science Field Name for uuid. Diff val than Internal name.
idfld = 'id'      # Science Field Name for uuid. Diff val than Internal name.

showact = False
#showact = True
showact = showact or os.environ.get('showres') == '1'


class SparclClientTest(unittest.TestCase):
    """Test access to each endpoint of the Server API"""

    maxDiff = None  # too see full values in DIFF on assert failure
    #assert_equal.__self__.maxDiff = None

    @classmethod
    def setUpClass(cls):
        # Client object creation compares the version from the Server
        # against the one expected by the Client. Raise error if
        # the Client is at least one major version behind.

        print(f'Running Client tests\n\t against Server: '
              f'"{urlparse(serverurl).netloc}"\n\t comparing to {exp}\n'
              )

        #! cls.clienti # Internal field names
        #! cls.client2 # Renamed, Science field names
        cls.client = sparcl.client.SparclClient(url=serverurl)
        cls.timing = dict()
        cls.doc = dict()
        cls.count = dict()
        cls.specids = [1506512395860731904, 3383388400617889792]
        cls.specids2 = [-5970393627659841536, 8712441763707768832,
                        3497074051921321984]
        # two real specids, one fake
        cls.specids3 = cls.specids2[0:2]
        cls.specids3.insert(2, 300000000000000001)
        # two fake specids
        cls.specids4 = [300000000000000001, 111111111111111111]
        #!found = cls.client.find([idfld, 'data_release'], limit=None)
        #!cls.uuids = sorted([rec.get(idfld) for rec in found.records])[:3]
        cls.uuids = cls.client.find([idfld, 'data_release'],
                                    sort='id', limit=3).ids
        cls.uuids2 = cls.client.find([idfld, 'data_release'],
                                     sort='data_release', limit=3).ids
        # two real UUIDs, one fake
        cls.uuids3 = cls.uuids2[1:3]
        cls.uuids3.insert(1, '00001ebf-d030-4d59-97e5-060c47202897')
        # two fake UUIDs
        cls.uuids4 = ['00001ebf-d030-4d59-97e5-060c47202897',
                      'ff1e9a12-f21a-4050-bada-a1e67a265885']

    @classmethod
    def tearDownClass(cls):
        pass
        #! print(f'\n## Times on: {urlparse(serverurl).netloc.split(".")[0]}'
        #!       ' (TestName, NumRecs, Description)')
        #! for k,v in cls.timing.items():
        #!     print(f'##   {k}: elapsed={v:.1f} secs;'
        #!           f'\t{cls.count.get(k)}'
        #!           f'\t{cls.doc.get(k)}')

    # Full records are big.  Get the gist of them.
    def records_expected(self, recs, expd, jdata=None, show=False):
        actual = sorted(recs[0].keys())
        expected = sorted(eval(expd))  # e.g. 'ep.retrieve_1'
        if show:
            #!f'\nEXPECTED={expected}'
            print(f'{expd}: ACTUAL={actual}')
        self.assertEqual(actual, expected, 'Actual to Expected')
        return(actual)

    # This is checked in SparclClient.__init__()
    #!def test_version(self):
    #!    """Get version of the NOIRLab SPARC Server API"""
    #!    version = self.client.version
    #!    expected = 4.0 # only major version part matters. Minor=.0
    #!    assert expected <= version < (1 + expected),(
    #!        f'Client/Server mismatch. '
    #!        f'Must be: expected({expected}) <= version({version}) '
    #!        f'< (1 + expected)'
    #!        )

    #################################
    # ## Convenience Functions
    # ##

    def test_get_all_fields(self):
        """Get the intersection of all fields that are tagged as 'all'."""
        actual = self.client.get_all_fields()
        if showact:
            print(f'all_fields: actual={pf(actual)}')
        self.assertEqual(actual,
                         exp.all_fields,
                         msg='Actual to Expected')

    def test_get_default_fields(self):
        """Get the intersection of all fields that are tagged as 'default'."""
        actual = self.client.get_default_fields()
        if showact:
            print(f'get_default_fields: actual={pf(actual)}')
        self.assertEqual(actual,
                         exp.default_fields,
                         msg='Actual to Expected')

    ###
    #################################

    #################################
    # ## Convenience client Methods
    # ##
    # ##
    # ################################

    def test_missing_0(self):
        """Known missing"""
        uuids = [99, 88, 777]
        missing = self.client.missing(self.uuids + uuids)
        assert sorted(missing) == sorted(uuids)

    def test_missing_1(self):
        """None missing"""
        #uuids = self.client.sample_uuids()
        uuids = self.uuids

        missing = self.client.missing(uuids)
        if showact:
            print(f'missing_1: missing={missing}')
        assert missing == []

    def test_retrieve_0(self):
        """Get spectra using small list of specids."""
        #!name = 'retrieve_0'
        #!this = self.test_retrieve_0

        res = self.client.retrieve_by_specid(self.specids,
                                             include=[idfld, 'specid'])
        actual = sorted([r['specid'] for r in res.records])
        if showact:
            print(f'retrieve_0: actual={actual}')

        #!print(f'DBG gotspecids={gotspecids} specids={specids}')
        self.assertEqual(actual, exp.retrieve_0, msg='Actual to Expected')

    def test_retrieve_0b(self):
        """Get spectra using small list of uuids."""
        name = 'retrieve_0b'
        #!this = self.test_retrieve_0b
        # uuids from expected.py:retrieve_0
        uuids = self.uuids

        tic()
        res = self.client.retrieve(uuids)
        self.timing[name] = toc()
        actual = sorted(res.records[0].keys())

        if showact:
            print(f'retrieve_0b: actual={pf(actual)}')

        self.assertEqual(actual, exp.retrieve_0b, msg='Actual to Expected')

    def test_retrieve_1(self):
        """Raise exception when unknown field referenced in include"""
        inc2 = ['bad_field_name', 'flux', 'or_mask']

        #! specids = sorted(self.client.sample_specids(samples=1,
        #!                                             dataset_list=drs))
        with self.assertRaises(ex.BadInclude):
            self.client.retrieve_by_specid(self.specids,
                                           include=inc2,
                                           dataset_list=drs)

    #! @skip('Cannot find an example of this edge case occuring')
    #! def test_retrieve_2(self):
    #!     """Issue warning when a Path has no value."""
    #!     inc2 = ['flux', 'spectra.coadd.OR_MASK']
    #!
    #!     specids = sorted(self.client.sample_specids(samples=1,
    #!                                           dataset_list=drs))
    #!     with self.assertWarns(Warning):
    #!         records = self.client.retrieve_by_specid(specids,
    #!                                        include=inc2,
    #!                                        dataset_list=drs)

    def test_retrieve_3(self):
        """Issue warning when some sids do not exist."""
        uuids = self.uuids
        with self.assertWarns(Warning):
            self.client.retrieve(uuids + [999])

    def test_find_0(self):
        """Get metadata using search spec."""
        #! name = 'find_0'
        #! this = self.test_find_0

        outfields = [idfld, 'ra', 'dec']
        # from list(FitsFile.objects.all().values('ra','dec'))

        # To get suitable constraints (in sparc-shell on Server):
        #   sorted(FitsFile.objects.all().values('ra','dec'),
        #          key=lambda r: r['dec'])
        if serverurl in DEV_SERVERS:
            constraints = {'ra': [246.0, 247.0], 'dec': [+34.7, +34.8]}
        else:
            constraints = {'ra': [137.0, 138.0], 'dec': [+63.0, +64.0]}
        found = self.client.find(outfields, constraints=constraints)
        actual = found.records[:2]
        if showact:
            print(f'find_0: actual={pf(actual)}')
        self.assertEqual(actual, exp.find_0, msg='Actual to Expected')

    def test_find_1(self):
        """Get metadata using search spec."""
        outfields = [idfld, 'ra', 'dec']
        found = self.client.find(outfields, limit=1, sort='id')  # @@@
        actual = sorted(found.records, key=lambda rec: rec[idfld])
        if showact:
            print(f'find_1: actual={pf(actual)}')
        self.assertEqual(actual,
                         sorted(exp.find_1, key=lambda rec: rec[idfld]),
                         msg='Actual to Expected')

    @skip('Takes too long for regression tests when used on big database.')
    def test_find_2(self):
        """Limit=None. """
        outfields = [idfld, 'ra', 'dec']
        found = self.client.find(outfields, limit=None, sort='id')  # @@@
        actual = len(found.records)
        if showact:
            print(f'find_2: actual={pf(actual)}')
        self.assertEqual(actual,
                         exp.find_2,
                         msg='Actual to Expected')

    def test_find_3(self):
        """Limit=3."""
        outfields = [idfld, 'ra', 'dec']
        found = self.client.find(outfields, limit=3, sort='id')  # @@@
        actual = sorted(found.records, key=lambda rec: rec[idfld])
        if showact:
            print(f'find_3: actual={pf(actual)}')
        self.assertEqual(actual,
                         sorted(exp.find_3, key=lambda rec: rec[idfld]),
                         msg='Actual to Expected')

    def test_find_4(self):
        """Check found.ids"""
        outfields = [idfld, 'ra', 'dec']
        found = self.client.find(outfields, limit=3, sort='id')  # @@@
        actual = sorted(found.ids)
        if showact:
            print(f'find_4: actual={pf(actual)}')
        self.assertEqual(actual,
                         sorted(exp.find_4),
                         msg='Actual to Expected')

    def test_reorder_1a(self):
        """Reorder retrieved records by ID."""
        name = 'reorder_1a'
        ids = self.uuids2

        tic()
        res = self.client.retrieve(ids)
        self.timing[name] = toc()
        res_reorder = res.reorder(ids)
        actual = [f['id'] for f in res_reorder.records]
        if showact:
            print(f'reorder_1a: actual={pf(actual)}')
        self.assertEqual(actual,
                         exp.reorder_1a,
                         msg='Actual to Expected')

    def test_reorder_1b(self):
        """Reorder retrieved records by specid."""
        name = 'reorder_1b'
        specids = self.specids2

        tic()
        res = self.client.retrieve_by_specid(specids)
        self.timing[name] = toc()
        res_reorder = res.reorder(specids)
        actual = [f['specid'] for f in res_reorder.records]
        if showact:
            print(f'reorder_1b: actual={pf(actual)}')
        self.assertEqual(actual,
                         exp.reorder_1b,
                         msg='Actual to Expected')

    def test_reorder_2a(self):
        """Reorder records when ID is missing from database, after using
           retrieve()."""
        name = 'reorder_2a'
        ids = self.uuids3

        tic()
        with self.assertWarns(Warning):
            res = self.client.retrieve(ids)
        self.timing[name] = toc()
        with self.assertWarns(Warning):
            res_reorder = res.reorder(ids)
        actual = [f['id'] for f in res_reorder.records]
        if showact:
            print(f'reorder_2a: actual={pf(actual)}')
        self.assertEqual(actual,
                         exp.reorder_2a,
                         msg='Actual to Expected')

    def test_reorder_2b(self):
        """Reorder records when specid is missing from database, after
           using retrieve_by_specid()."""
        name = 'reorder_2b'
        specids = self.specids3

        tic()
        res = self.client.retrieve_by_specid(specids)
        self.timing[name] = toc()
        with self.assertWarns(Warning):
            res_reorder = res.reorder(specids)
        actual = [f['specid'] for f in res_reorder.records]
        if showact:
            print(f'reorder_2b: actual={pf(actual)}')
        self.assertEqual(actual,
                         exp.reorder_2b,
                         msg='Actual to Expected')

    def test_reorder_3a(self):
        """Test for expected Exception when a list of IDs with length 0 is
           passed to reorder method after using retrieve()."""
        name = 'reorder_3a'
        ids = self.uuids2
        og_ids = []

        tic()
        res = self.client.retrieve(ids)
        self.timing[name] = toc()
        with self.assertRaises(ex.NoIDs):
            res.reorder(og_ids)

    def test_reorder_3b(self):
        """Test for expected Exception when a list of specids with length 0
           is passed to reorder method after using retrieve_by_specid()."""
        name = 'reorder_3b'
        specids = self.specids2
        og_specids = []

        tic()
        res = self.client.retrieve_by_specid(specids)
        self.timing[name] = toc()
        with self.assertRaises(ex.NoIDs):
            res.reorder(og_specids)

    def test_reorder_4a(self):
        """Test for expected Exception when there are no records, using IDs
           and retrieve()."""
        name = 'reorder_4a'
        ids = self.uuids4

        tic()
        with self.assertWarns(Warning):
            res = self.client.retrieve(ids)
        self.timing[name] = toc()
        with self.assertRaises(ex.NoRecords):
            res.reorder(ids)

    def test_reorder_4b(self):
        """Test for expected Exception when there are no records, using specids
           and retrieve_by_specid()."""
        name = 'reorder_4b'
        specids = self.specids4

        tic()
        res = self.client.retrieve_by_specid(specids)
        self.timing[name] = toc()
        with self.assertRaises(ex.NoRecords):
            res.reorder(specids)
