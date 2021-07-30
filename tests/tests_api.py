# Unit tests for the NOIRLab SPARC API Client
# EXAMPLES:
#   python -m unittest tests.tests_api
#   python -m unittest  -v tests.tests_api    # VERBOSE
#   python -m unittest tests.tests_api.ApiTest
#   python -m unittest tests.tests_api.ApiTest.test_find_3

# Python library
import unittest
from unittest import skip,mock,skipIf,skipUnless
import warnings
from pprint import pformat,pprint
from urllib.parse import urlparse
from unittest.mock import MagicMock
from unittest.mock import create_autospec
# Local Packages
import api.client
from tests.utils import tic,toc
import api.exceptions as ex
# External Packages
# <none>

rooturl = 'http://localhost:8030/' #@@@
#rooturl = 'http://sparc1.datalab.noirlab.edu:8000/' #@@@

class ApiTest(unittest.TestCase):
    """Test access to each endpoint of the Server API"""

    @classmethod
    def setUpClass(cls):
        # Client object creation compares the version from the Server
        # against the one expected by the Client. Raise error if
        # the Client is at least one major version behind.

        cls.client = api.client.SparclApi(url=rooturl)
        #! cls.client = create_autospec(api.client.SparclApi(url=rooturl))
        cls.timing = dict()
        cls.doc = dict()
        cls.count = dict()
        print(f'Running Client tests against Server: '
              f'{urlparse(rooturl).netloc.split(".")[0]}')

    @classmethod
    def tearDownClass(cls):
        print(f'\n## Times on: {urlparse(rooturl).netloc.split(".")[0]}')
        for k,v in cls.timing.items():
            print(f'##   {k}: elapsed={v:.1f} secs;'
                  f'\t{cls.count.get(k)}'
                  f'\t{cls.doc.get(k)}')


    def test_version(self):
        """Get version of the NOIRLab SPARC server API"""
        version = self.client.version
        expected = 2.0 # only major version part matters. Minor=.0
        assert expected <= version < (1 + expected)


    def test_sample(self):
        sids = self.client.sample_sids()
        #print(f'sids={sids}')
        assert len(sids) == 5

    def test_missing_0(self):
        """Known missing"""
        sids= [99,88]
        missing = self.client.missing_sids(sids)
        assert sorted(missing) == sorted(sids)

    def test_missing_1(self):
        """None missing"""
        sids = self.client.sample_sids()
        missing = self.client.missing_sids(sids)
        assert missing == []


    def test_retrieve_0(self):
        """Get spectra using small list of spectObjIds"""
        name = 'retrieve_0'
        this = self.test_retrieve_0
        getcnt = 3
        sids = sorted(self.client.sample_sids(samples=getcnt))
        tic()
        records = self.client.retrieve(sids)
        #! status = ret['status']
        #! records = ret['records']
        gotsids = sorted(r['specid'] for r in records)

        self.timing[name] = toc()
        self.doc[name] = this.__doc__
        self.count[name] = len(records)
        assert gotsids == sids, "Actual to Expected"

    def test_retrieve_1(self):
        """Raise exception when unknown core field referenced in include"""
        inc2 = {'spectra.coadd.FLUX': 'flux',
                'bad_field_name': 'alias',
                'spectra.specobj.CX': 'cx'}
        sids = sorted(self.client.sample_sids(samples=1,
                                              structure='BOSS-DR16'))
        with self.assertRaises(ex.BadPath):
            records = self.client.retrieve(sids,
                                           include=inc2,
                                           structure='BOSS-DR16')

    def test_retrieve_2(self):
        """Issue warning when a Path has no value."""
        inc2 = {'spectra.coadd.FLUX': 'flux',
                'spectra.bad_field_name': 'alias', # None value
                'spectra.specobj.CX': 'cx'}
        sids = sorted(self.client.sample_sids(samples=1,
                                              structure='BOSS-DR16'))
        with self.assertWarns(Warning):
            records = self.client.retrieve(sids,
                                           include=inc2,
                                           structure='BOSS-DR16')
