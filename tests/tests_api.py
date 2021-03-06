# Unit tests for the NOIRLab SPARC API Client
# EXAMPLES: (do after activating venv, in sandbox/sparclclient/)
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
import tests.expected as exp
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
        print(f'\n## Times on: {urlparse(rooturl).netloc.split(".")[0]}'
              ' (TestName, NumRecs, Description)')
        for k,v in cls.timing.items():
            print(f'##   {k}: elapsed={v:.1f} secs;'
                  f'\t{cls.count.get(k)}'
                  f'\t{cls.doc.get(k)}')


    def test_version(self):
        """Get version of the NOIRLab SPARC server API"""
        version = self.client.version
        expected = 3.0 # only major version part matters. Minor=.0
        assert expected <= version < (1 + expected),(
            f'Client/Server mismatch. '
            f'Must be: expected({expected}) <= version({version}) '
            f'< (1 + expected)'
            )

    def test_sample(self):
        specids = self.client.sample_specids()
        #!print(f'DBG: specids={specids}')
        assert len(specids) == 5

    def test_missing_0(self):
        """Known missing"""
        specids= [99,88]
        missing = self.client.missing_specids(specids)
        assert sorted(missing) == sorted(specids)

    def test_missing_1(self):
        """None missing"""
        specids = self.client.sample_specids()
        missing = self.client.missing_specids(specids)
        assert missing == []

    def test_retrieve_0(self):
        """Get spectra using small list of specids."""
        name = 'retrieve_0'
        this = self.test_retrieve_0
        getcnt = 3
        dr='SDSS-DR16'
        specids = sorted(self.client.sample_specids(samples=getcnt,structure=dr))
        tic()
        records = self.client.retrieve(specids)
        #! status = ret['status']
        #! records = ret['records']
        gotspecids = sorted(r['specid'] for r in records)

        self.timing[name] = toc()
        self.doc[name] = this.__doc__
        self.count[name] = len(records)

        #!print(f'DBG gotspecids={gotspecids} specids={specids}')
        assert gotspecids == specids, "Actual to Expected"

    def test_retrieve_1(self):
        """Raise exception when unknown field referenced in include"""
        inc2 = ['bad_field_name', 'flux', 'spectra.coadd.OR_MASK']

        specids = sorted(self.client.sample_specids(samples=1,
                                                    structure='BOSS-DR16'))
        with self.assertRaises(ex.BadInclude):
            records = self.client.retrieve(specids,
                                           include=inc2,
                                           structure='BOSS-DR16')

    #! @skip('Cannot find an example of this edge case occuring')
    #! def test_retrieve_2(self):
    #!     """Issue warning when a Path has no value."""
    #!     inc2 = ['flux', 'spectra.coadd.OR_MASK']
    #!
    #!     specids = sorted(self.client.sample_specids(samples=1,
    #!                                           structure='BOSS-DR16'))
    #!     with self.assertWarns(Warning):
    #!         records = self.client.retrieve(specids,
    #!                                        include=inc2,
    #!                                        structure='BOSS-DR16')

    def test_retrieve_3(self):
        """Issue warning when some sids do not exist."""
        inc2 = ['flux']
        sids = sorted(self.client.sample_specids(samples=1,
                                              structure='BOSS-DR16'))
        with self.assertWarns(Warning):
            records = self.client.retrieve(sids+[999],
                                           include=inc2,
                                           structure='BOSS-DR16')

    def test_retrieve_5(self):
        """Convert to Numpy."""
        recs = self.client.sample_records(1, structure='BOSS-DR16',
                                          rtype='numpy')
        actual = sorted(recs[0].keys())
        self.assertEqual(actual, exp.boss_numpy, msg='Actual to Expected')

    def test_retrieve_6(self):
        """Convert to Pandas."""
        recs = self.client.sample_records(1, structure='BOSS-DR16',
                                          rtype='pandas')
        actual = sorted(recs[0].keys())
        self.assertEqual(actual, exp.boss_pandas, msg='Actual to Expected')

    def test_retrieve_7(self):
        """Convert to Spectrum1D."""
        inc2 = ['flux']
        recs = self.client.sample_records(1, structure='BOSS-DR16',
                                          rtype='spectrum1d')
        actual = sorted(recs[0].keys())
        self.assertEqual(actual, exp.boss_spectrum1d, msg='Actual to Expected')

    def test_get_record_structure(self):
        actual = self.client.get_record_structure('BOSS-DR16')
        #!print(f'actual={pformat(actual)}')
        self.assertEqual(actual, exp.boss_record_structure,
                         msg = 'Actual to Expected')
