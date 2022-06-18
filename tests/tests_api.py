# Unit tests for the NOIRLab SPARCL API Client
# EXAMPLES: (do after activating venv, in sandbox/sparclclient/)
#   python -m unittest tests.tests_api
#   python -m unittest  -v tests.tests_api    # VERBOSE
#   python -m unittest tests.tests_api.SparclClientTest
#   python -m unittest tests.tests_api.SparclClientTest.test_find_3

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
import tests.expected as exp
import sparcl.exceptions as ex
# External Packages
# <none>

DEFAULT = 'DEFAULT'
ALL = 'ALL'
drs = ['BOSS-DR16']

rooturl = 'http://localhost:8050/'  # @@@
#rooturl = 'http://sparc1.datalab.noirlab.edu:8000/'  # @@@

idfld = 'uuid'  # Science Field Name for uuid. Diff val than Internal name.
#idfld = 'id'  # Science Field Name for uuid. Diff val than Internal name.

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

        #! cls.clienti # Internal field names
        #! cls.client2 # Renamed, Science field names
        cls.client = sparcl.client.SparclClient(url=rooturl)
        cls.timing = dict()
        cls.doc = dict()
        cls.count = dict()
        cls.specids = [1506512395860731904, 3383388400617889792]
        found = cls.client.find([idfld, 'data_release'], limit=None)
        cls.uuids = sorted([rec.get(idfld) for rec in found.records])[:3]

        print(f'Running Client tests against Server: '
              f'{urlparse(rooturl).netloc}')

    @classmethod
    def tearDownClass(cls):
        pass
        #! print(f'\n## Times on: {urlparse(rooturl).netloc.split(".")[0]}'
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

    @skip('Not required.  EXPERIMENTAL')
    def test_df_lut(self):
        """Make sure the Data Field LookUp Table is as we expected.
        Many tests depend on this.  If the underlying DataField SPARC table
        was changed accidentally, reset it. Otherwise, change tests to
        accomodate the new DataFields.
        """
        actual = self.client.dfLUT
        if showact:
            print(f"df_lut actual={pf(actual['BOSS-DR16'])}")
        self.assertDictEqual(actual['BOSS-DR16'],
                             exp.df_lut,
                             msg='Actual to Expected')

    #################################
    # ## Convenience Functions
    # ##

    @skip('Not required.  EXPERIMENTAL')
    def test_fields_available(self):
        """Fields available in a specific record set."""
        records = self.client.sample_records(1,
                                             dataset_list=drs,
                                             random=False)
        actual = sparcl.client.fields_available(records)
        if showact:
            print(f'fields_available: actual={pf(actual)}')
        self.assertEqual(actual,
                         exp.fields_available,
                         msg='Actual to Expected')

    @skip('Not required.  EXPERIMENTAL')
    def test_record_examples(self):
        """Get one record for each Structure type. DEFAULT set."""
        records = self.client.sample_records(1,
                                             dataset_list=drs,
                                             random=False)
        examples = sparcl.client.record_examples(records)
        # Just the gist of the records (key names)
        actual = {k: sorted(v.keys()) for k, v in examples.items()}
        if showact:
            print(f'record_examples: actual={pf(actual)}')
        self.assertEqual(actual, exp.record_examples, msg='Actual to Expected')

    @skip('Not required.  EXPERIMENTAL')
    def test_get_metadata(self):
        variant_fields = ['dateobs_center', idfld]
        sids = [1429933274376612]
        records = self.client.retrieve_by_specid(sids, include=ALL,
                                                 dataset_list=drs)
        [r.pop('dirpath', None) for r in records]
        actual = sparcl.client.get_metadata(records)
        expected = exp.get_metadata
        for k in variant_fields:
            actual[0].pop(k, None)
            expected[0].pop(k, None)

        if showact:
            print(f'get_metadata: actual={pf(actual)}')
        self.assertEqual(actual, expected, msg='Actual to Expected')

    @skip('Not required.  EXPERIMENTAL')
    def test_get_vectordata(self):
        sids = [1429933274376612]
        ink = ['loglam', 'flux', 'and_mask', 'ivar', 'ra', 'dec', 'specid']
        records = self.client.retrieve_by_specid(sids, include=ink,
                                                 dataset_list=drs)
        actual = list(sparcl.client.get_vectordata(records)[0].keys())
        if showact:
            print(f'get_vectordata: actual={pf(actual)}')
        self.assertListEqual(actual,
                             exp.get_vectordata,
                             msg='Actual to Expected')

    @skip('Not required.  EXPERIMENTAL')
    def test_rename_fields(self):
        """Local rename fields in records (referenced by new names)"""
        flds = ['data_set', 'specid', 'dec', 'ra', 'redshift',
                'flux', 'ivar', 'loglam']

        records = self.client.sample_records(1,
                                             include=flds,
                                             dataset_list=drs,
                                             random=False)
        rdict = dict(dec='y', ra='x', redshift='z', flux='f')
        actual = sparcl.client.rename_fields(rdict, records)
        self.records_expected(actual, "exp.rename_fields", show=showact)

    @skip('Not required.  EXPERIMENTAL')
    def test_rename_fields_internal(self):
        """Local rename fields in records (referenced by stored names)"""
        flds = ['data_release', 'specid',
                'decr', 'rar', 'redshift',
                'flux', 'ivar', 'loglam']
        records = self.client.sample_records(1,
                                             include=flds,
                                             dataset_list=drs,
                                             random=False)
        rdict = {'dec': 'y',
                 'ra': 'x',
                 'redshift': 'z',
                 'flux': 'f2'}
        actual = sparcl.client.rename_fields(rdict, records)
        self.records_expected(actual,
                              "exp.rename_fields_internal",
                              show=showact)

    ###
    #################################

    #################################
    # ## Convenience client Methods
    # ##

    @skip('Not required.  EXPERIMENTAL')
    def test_get_field_names(self):
        actual = self.client.get_field_names('BOSS-DR16')
        if showact:
            print(f'get_field_names: actual={pf(actual)}')
        self.assertEqual(actual, exp.get_field_names, msg='Actual to Expected')

    @skip('Not required.  EXPERIMENTAL')
    def test_get_field_names_internal(self):
        actual = self.client.get_field_names('BOSS-DR16')
        if showact:
            print(f'get_field_names_internal: actual={pf(actual)}')
        self.assertEqual(actual,
                         exp.get_field_names_internal,
                         msg='Actual to Expected')

    @skip('Not required.  EXPERIMENTAL')
    def test_orig_field(self):
        actual = self.client.orig_field('BOSS-DR16', 'flux')
        if showact:
            print(f'orig_field: actual={pf(actual)}')
        self.assertEqual(actual, exp.orig_field, msg='Actual to Expected')

    @skip('Not required.  EXPERIMENTAL')
    def test_client_field(self):
        actual = self.client.client_field('BOSS-DR16', 'flux')
        if showact:
            print(f'client_field: actual={pf(actual)}')
        self.assertEqual(actual, exp.client_field, msg='Actual to Expected')

    @skip('Not required.  EXPERIMENTAL')
    def test_normalize_field_names(self):
        """Convert all included  field names to internal names"""
        sids = self.client.sample_specids(1, dataset_list=drs, random=False)
        recs = self.client.retrieve_by_specid(sids,
                                              dataset_list=drs,
                                              include=['flux', 'ivar'])
        recs_b = self.client.normalize_field_names(recs)
        actual = [sorted(r.keys()) for r in recs_b]
        if showact:
            print(f'normalize_field_names: actual={pf(actual)}')
        self.assertEqual(actual, exp.normalize_field_names,
                         msg='Actual to Expected')

    # ##
    # ################################

    @skip('Not required.  EXPERIMENTAL')
    def test_sample(self):
        specids = self.client.sample_specids()
        #print(f'DBG: specids={specids}')
        assert len(specids) == 5

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
        self.assertEqual(actual, self.specids, msg='Actual to Expected')

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

    @skip('Not required.  EXPERIMENTAL')
    def test_retrieve_5(self):
        """Get record samples with their internal (original) field names."""
        records = self.client.sample_records(1,
                                             include=ALL,
                                             dataset_list=drs,
                                             random=False)
        actual = sorted(records[0].keys())
        actual.remove('_dr')
        if showact:
            print(f'retrieve_5: actual={pf(actual)}')
        self.assertEqual(actual, exp.retrieve_5, msg='Actual to Expected')

    #############################
    # ## BOSS type conversions
    @skip('Type conversions removed until redesign')
    def test_retrieve_boss_json(self):
        """(non)Convert to JSON."""
        flds = ['dec',
                'ra',
                'redshift',
                'specid',
                'flux',
                'ivar']
        recs = self.client.sample_records(1,
                                          random=False,
                                          include=flds,
                                          dataset_list=drs)
        actual = sorted(recs[0].keys())
        if showact:
            print(f'boss_json: actual={pf(actual)}')
        self.assertEqual(actual, exp.boss_json, msg='Actual to Expected')

    @skip('Type conversions removed until redesign')
    def test_retrieve_boss_numpy(self):
        """Convert to Numpy."""
        arflds = [
            'mask',
            'flux',
            'ivar',
            'LOGLAM',
            'MODEL',
            'OR_MASK',
            'SKY',
            'WDISP',
        ]
        #!print(f'clienti={self.client}')
        recs = self.client.sample_records(1,
                                          dataset_list=drs, rtype='numpy',
                                          include=arflds, random=False)
        actual = sorted(recs[0].keys())
        if showact:
            print(f'boss_numpy: actual={pf(actual)}')
        self.assertEqual(actual, exp.boss_numpy, msg='Actual to Expected')

    @skip('Type conversions removed until redesign')
    def test_retrieve_boss_pandas(self):
        """Convert to Pandas."""
        arflds = [
            'spectra.coadd.AND_MASK',
            'spectra.coadd.FLUX',
            'spectra.coadd.IVAR',
            'spectra.coadd.LOGLAM',
            'spectra.coadd.MODEL',
            'spectra.coadd.OR_MASK',
            'spectra.coadd.SKY',
            'spectra.coadd.WDISP',
        ]
        recs = self.client.sample_records(1,
                                          dataset_list=drs,
                                          rtype='pandas',
                                          include=arflds,
                                          random=False)
        actual = sorted(recs[0].keys())
        if showact:
            print(f'boss_pandas: actual={pf(actual)}')
        self.assertEqual(actual, exp.boss_pandas, msg='Actual to Expected')

    @skip('Type conversions removed until redesign')
    def test_retrieve_boss_spectrum1d(self):
        """Convert to Spectrum1D."""
        arflds = [
            'spectra.coadd.FLUX',
            'spectra.coadd.IVAR',
            'spectra.coadd.LOGLAM',
            'spectra.coadd.AND_MASK',
            'redshift'
        ]
        recs = self.client.sample_records(1, dataset_list=drs,
                                          rtype='spectrum1d',
                                          include=arflds, random=False)
        actual = sorted(recs[0].keys())
        if showact:
            print(f'boss_spectrum1d: actual={pf(actual)}')
        self.assertEqual(actual, exp.boss_spectrum1d, msg='Actual to Expected')

    #############################
    # ## EVEREST type conversions
    @skip('OBSOLETE dataset. Replace with DES-edr')
    def test_retrieve_everest_numpy(self):
        """Convert to Numpy."""
        arflds = [
            'specid', 'ra', 'dec',
            'spectra.b_flux',
            'spectra.b_ivar',
            'spectra.b_mask',
            'spectra.b_wavelength',
            'spectra.r_flux',
            'spectra.r_ivar',
            'spectra.r_mask',
            'spectra.r_wavelength',
            'spectra.z_flux',
            'spectra.z_ivar',
            'spectra.z_mask',
            'spectra.z_wavelength',
        ]
        recs = self.client.sample_records(1,
                                          dataset_list='DESI-everest',
                                          rtype='numpy',
                                          include=arflds,
                                          random=False)
        actual = sorted(recs[0].keys())
        if showact:
            print(f'everest_numpy: actual={pf(actual)}')
        self.assertEqual(actual, exp.everest_numpy, msg='Actual to Expected')

    @skip('OBSOLETE dataset. Replace with DES-edr')
    def test_retrieve_everest_pandas(self):
        """Convert to Pandas."""
        arflds = [
            'spectra.b_flux',
            'spectra.b_ivar',
            'spectra.b_mask',
            'spectra.b_wavelength',
            'spectra.r_flux',
            'spectra.r_ivar',
            'spectra.r_mask',
            'spectra.r_wavelength',
            'spectra.z_flux',
            'spectra.z_ivar',
            'spectra.z_mask',
            'spectra.z_wavelength',
        ]
        recs = self.client.sample_records(1,
                                          dataset_list='DESI-everest',
                                          rtype='pandas',
                                          include=arflds,
                                          random=False)
        actual = sorted(recs[0].keys())
        if showact:
            print(f'everest_pandas: actual={pf(actual)}')
        self.assertEqual(actual, exp.everest_pandas, msg='Actual to Expected')

    @skip('OBSOLETE dataset. Replace with DES-edr')
    def test_retrieve_everest_spectrum1d(self):
        """Convert to Spectrum1D."""
        arflds = [
            'redshift',
            'spectra.b_flux',
            'spectra.b_ivar',
            'spectra.b_mask',
            'spectra.b_wavelength',
            'spectra.r_flux',
            'spectra.r_ivar',
            'spectra.r_mask',
            'spectra.r_wavelength',
            'spectra.z_flux',
            'spectra.z_ivar',
            'spectra.z_mask',
            'spectra.z_wavelength',
        ]
        recs = self.client.sample_records(1, dataset_list='DESI-everest',
                                          include=arflds, random=False)
        actual = sorted(recs[0].keys())
        if showact:
            print(f'everest_spectrum1d: actual={pf(actual)}')
        self.assertEqual(actual, exp.everest_spectrum1d,
                         msg='Actual to Expected')

    # To get suitable constraints (Pothier, DEV, in sparc-shell):
    #   list(FitsFile.objects.all().values('ra','dec')[:10])
    def test_find_0(self):
        """Get metadata using search spec."""
        #! name = 'find_0'
        #! this = self.test_find_0

        outfields = [idfld, 'ra', 'dec']
        # from list(FitsFile.objects.all().values('ra','dec'))
        constraints = {'ra': [180.0, 240.0], 'dec': [-2.0, +2.0]}
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

    def test_find_2(self):
        """Get metadata using search spec."""
        outfields = [idfld, 'ra', 'dec']
        found = self.client.find(outfields, limit=None, sort='id')  # @@@
        actual = len(found.records)
        if showact:
            print(f'find_2: actual={pf(actual)}')
            self.assertEqual(actual,
                             exp.find_2,
                             msg='Actual to Expected')

    def test_find_3(self):
        """Get metadata using search spec."""
        outfields = [idfld, 'ra', 'dec']
        found = self.client.find(outfields, limit=3, sort='id')  # @@@
        actual = sorted(found.records, key=lambda rec: rec[idfld])
        if showact:
            print(f'find_3: actual={pf(actual)}')
        self.assertEqual(actual,
                         sorted(exp.find_3, key=lambda rec: rec[idfld]),
                         msg='Actual to Expected')
