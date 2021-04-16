# Unit tests for the NOIRLab SPARC API Client
# EXAMPLES:
#   python -m unittest tests.tests_api
#   python -m unittest tests.tests_api.ApiTest
#   python -m unittest tests.tests_api.ApiTest.test_find_3

# Python library
import unittest
from unittest import skip,mock,skipIf,skipUnless
import warnings
from pprint import pformat,pprint
from urllib.parse import urlparse
# Local Packages
import api.api
from tests.utils import tic,toc
# External Packages
# <none>

rooturl = 'http://localhost:8030/' #@@@

class ApiTest(unittest.TestCase):
    """Test access to each endpoint of the Server API"""

    @classmethod
    def setUpClass(cls):
        # AdaApi object creation compares the version from the Server
        # against the one expected by the Client. Throws error if
        # the Client is a major version behind.
        cls.client = api.api.SparcApi(url=rooturl)
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
        assert 1.0 <= version < 2.0

    def test_retrieve_0(self):
        """Get spectra using small list of spectObjIds"""
        name = 'retrieve_0'
        this = self.test_retrieve_0
        sids = [1355590404564609024, 1355598650901817344]
        tic()
        data = self.client.retrieve(sids)
        self.timing[name] = toc()
        self.doc[name] = this.__doc__
        self.count[name] = len(data)
        assert len(data) == 2
