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
#from api.client import DEFAULT, ALL
from tests.utils import tic,toc
import tests.expected as exp
import api.exceptions as ex
# External Packages
# <none>

DEFAULT='DEFAULT'
ALL='ALL'

rooturl = 'http://localhost:8030/' #@@@
rooturl = 'http://sparc1.datalab.noirlab.edu:8000/' #@@@

showact = False
#showact = True


class ApiTest(unittest.TestCase):
    """Test access to each endpoint of the Server API"""

    maxDiff = None # too see full values in DIFF on assert failure
    #assert_equal.__self__.maxDiff = None

    @classmethod
    def setUpClass(cls):
        # Client object creation compares the version from the Server
        # against the one expected by the Client. Raise error if
        # the Client is at least one major version behind.

        cls.clienti = api.client.SparclApi(url=rooturl, internal_names=True)
        cls.client2 = api.client.SparclApi(url=rooturl) # renamed fields
        cls.timing = dict()
        cls.doc = dict()
        cls.count = dict()
        print(f'Running Client tests against Server: {urlparse(rooturl).netloc}')

    @classmethod
    def tearDownClass(cls):
        print(f'\n## Times on: {urlparse(rooturl).netloc.split(".")[0]}'
              ' (TestName, NumRecs, Description)')
        for k,v in cls.timing.items():
            print(f'##   {k}: elapsed={v:.1f} secs;'
                  f'\t{cls.count.get(k)}'
                  f'\t{cls.doc.get(k)}')

    # Full records are big.  Get the gist of them.
    def records_expected(self, recs, expd, jdata=None, show=False):
        actual = sorted(recs[0].keys())
        expected = sorted(eval(expd))  # e.g. 'ep.retrieve_1'
        if show:
            #!f'\nEXPECTED={expected}'
            print(f'{expd}: ACTUAL={actual}')
        self.assertEqual(actual, expected, 'Actual to Expected')
        return(actual)

    # This is checked in SparclApi.__init__()
    #!def test_version(self):
    #!    """Get version of the NOIRLab SPARC Server API"""
    #!    version = self.client.version
    #!    expected = 4.0 # only major version part matters. Minor=.0
    #!    assert expected <= version < (1 + expected),(
    #!        f'Client/Server mismatch. '
    #!        f'Must be: expected({expected}) <= version({version}) '
    #!        f'< (1 + expected)'
    #!        )

    def test_df_lut(self):
        """Make sure the Data Field LookUp Table is as we expected.
        Many tests depend on this.  If the underlying DataField SPARC table
        was changed accidentally, reset it. Otherwise, change tests to
        accomodate the new DataFields.
        """
        actual = self.client2.dfLUT
        if showact:
            print(f"df_lut actual={pformat(actual['BOSS-DR16'])}")
        self.assertDictEqual(actual['BOSS-DR16'],
                             exp.df_lut,
                             msg = 'Actual to Expected')

    def test_df_lut_internal(self):
        """Make sure the Data Field LookUp Table is as we expected.
        Many tests depend on this.  If the underlying DataField SPARC table
        was changed accidentally, reset it. Otherwise, change tests to
        accomodate the new DataFields.
        """
        actual = self.clienti.dfLUT
        if showact:
            print(f"df_lut_internal actual={pformat(actual['BOSS-DR16'])}")
        self.assertDictEqual(actual['BOSS-DR16'],
                             exp.df_lut_internal,
                             msg = 'Actual to Expected')

    #################################
    ### Convenience Functions
    ###

    def test_fields_available(self):
        """Fields available in a specific record set."""
        records = self.clienti.sample_records(1,
                                             structure='BOSS-DR16', random=False)
        actual = api.client.fields_available(records)
        if showact:
            print(f'fields_available: actual={pformat(actual)}')
        self.assertEqual(actual, exp.fields_available,msg = 'Actual to Expected')

    def test_record_examples(self):
        """Get one record for each Structure type. DEFAULT set."""
        records = self.clienti.sample_records(1,
                                             structure='BOSS-DR16',
                                             random=False)
        examples = api.client.record_examples(records)
        # Just the gist of the records (key names)
        actual = {k: sorted(v.keys()) for k,v in examples.items()}
        if showact:
            print(f'record_examples: actual={pformat(actual)}')
        self.assertEqual(actual, exp.record_examples, msg='Actual to Expected')

    def test_get_metadata(self):
        variant_fields = ['dateobs_center','id']
        sids = [1429933274376612]
        records = self.clienti.retrieve(sids, include=ALL, structure='BOSS-DR16')
        [r.pop('dirpath',None) for r in records]
        actual = api.client.get_metadata(records)
        expected = exp.get_metadata
        for k in variant_fields:
            actual[0].pop(k,None)
            expected[0].pop(k,None)

        if showact:
            print(f'get_metadata: actual={pformat(actual)}')
        self.assertEqual(actual, expected , msg = 'Actual to Expected')

    def test_rename_fields(self):
        """Local rename fields in records (referenced by new names)"""
        flds = ['data_set', 'specid', 'dec', 'ra','redshift',
                'flux', 'ivar', 'loglam']

        records = self.client2.sample_records(1,
                                              include=flds,
                                              structure='BOSS-DR16',
                                              random=False)
        rdict = dict(dec='y', ra='x', redshift='z', flux='f')
        actual = api.client.rename_fields(rdict, records)
        self.records_expected(actual,"exp.rename_fields", show=showact)

    @skip('Not required.  EXPERIMENTAL')
    def test_rename_fields_internal(self):
        """Local rename fields in records (referenced by stored names)"""
        flds = ['data_release_id', 'specid',
                'decr', 'rar','redshift',
                'spectra.coadd.FLUX',
                'spectra.coadd.IVAR',
                'spectra.coadd.LOGLAM']
        records = self.clienti.sample_records(1,
                                              include=flds,
                                              structure='BOSS-DR16',
                                              random=False)
        rdict = {'dec': 'y',
                 'ra': 'x',
                 'redshift':'z',
                 'spectra.coadd.FLUX': 'f2'}
        actual = api.client.rename_fields(rdict, records)
        self.records_expected(actual,"exp.rename_fields_internal", show=showact)

    ###
    #################################

    #################################
    ### Convenience client Methods
    ###

    def test_get_field_names(self):
        actual = self.client2.get_field_names('BOSS-DR16')
        if showact:
            print(f'get_field_names: actual={pformat(actual)}')
        self.assertEqual(actual, exp.get_field_names, msg='Actual to Expected')

    def test_get_field_names_internal(self):
        actual = self.clienti.get_field_names('BOSS-DR16')
        if showact:
            print(f'get_field_names_internal: actual={pformat(actual)}')
        self.assertEqual(actual, exp.get_field_names_internal, msg='Actual to Expected')

    def test_orig_field(self):
        actual = self.client2.orig_field('BOSS-DR16', 'flux')
        if showact:
            print(f'orig_field: actual={pformat(actual)}')
        self.assertEqual(actual, exp.orig_field, msg='Actual to Expected')

    def test_client_field(self):
        actual = self.client2.client_field('BOSS-DR16','spectra.coadd.FLUX')
        if showact:
            print(f'client_field: actual={pformat(actual)}')
        self.assertEqual(actual, exp.client_field, msg='Actual to Expected')

    def test_normalize_field_names(self):
        """Convert all included  field names to internal names"""
        sids = self.client2.sample_specids(1,structure='BOSS-DR16',random=False)
        recs = self.client2.retrieve(sids, structure='BOSS-DR16',
                                     include=['flux','ivar'])
        recs_b = self.client2.normalize_field_names(recs)
        actual = [sorted(r.keys()) for r in recs_b]
        if showact:
            print(f'normalize_field_names: actual={pformat(actual)}')
        self.assertEqual(actual, exp.normalize_field_names,
                         msg = 'Actual to Expected')

    #!@skip('Deprecate functions to return Record Structure.  Use Server site instead.')
    #!def test_boss_record_structure(self):
    #!    sids = self.clienti.sample_specids(1,structure='BOSS-DR16', random=False)
    #!    actual = self.clienti.get_record_structure('BOSS-DR16',specid=sids[0])
    #!    if showact:
    #!        print(f'boss_record_structure: actual={pformat(actual)}')
    #!    self.assertEqual(actual, exp.boss_record_structure,
    #!                     msg = 'Actual to Expected')

    ###
    #################################


    def test_sample(self):
        specids = self.clienti.sample_specids()
        #print(f'DBG: specids={specids}')
        assert len(specids) == 5

    def test_missing_0(self):
        """Known missing"""
        specids= [99,88]
        missing = self.clienti.missing_specids(specids)
        assert sorted(missing) == sorted(specids)

    def test_missing_1(self):
        """None missing"""
        specids = self.clienti.sample_specids()
        missing = self.clienti.missing_specids(specids)
        assert missing == []

    def test_retrieve_0(self):
        """Get spectra using small list of specids."""
        name = 'retrieve_0'
        this = self.test_retrieve_0
        getcnt = 3
        dr='SDSS-DR16'
        specids = sorted(self.clienti.sample_specids(samples=getcnt,structure=dr))
        tic()
        records = self.clienti.retrieve(specids, structure=dr)
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

        specids = sorted(self.clienti.sample_specids(samples=1,
                                                    structure='BOSS-DR16'))
        with self.assertRaises(ex.BadInclude):
            records = self.clienti.retrieve(specids,
                                           include=inc2,
                                           structure='BOSS-DR16')

    #! @skip('Cannot find an example of this edge case occuring')
    #! def test_retrieve_2(self):
    #!     """Issue warning when a Path has no value."""
    #!     inc2 = ['flux', 'spectra.coadd.OR_MASK']
    #!
    #!     specids = sorted(self.clienti.sample_specids(samples=1,
    #!                                           structure='BOSS-DR16'))
    #!     with self.assertWarns(Warning):
    #!         records = self.clienti.retrieve(specids,
    #!                                        include=inc2,
    #!                                        structure='BOSS-DR16')

    def test_retrieve_3(self):
        """Issue warning when some sids do not exist."""
        inc = ['specid']
        sids = sorted(self.client2.sample_specids(samples=1, random=False,
                                                 structure='BOSS-DR16'))
        with self.assertWarns(Warning):
            records = self.client2.retrieve(sids+[999], include=inc,
                                            structure='BOSS-DR16')
    def test_retrieve_3_internal(self):
        """Issue warning when some sids do not exist."""
        sids = sorted(self.clienti.sample_specids(samples=1, random=False,
                                                 structure='BOSS-DR16'))
        with self.assertWarns(Warning):
            records = self.clienti.retrieve(sids+[999], structure='BOSS-DR16')

    def test_retrieve_4(self):
        """Get ALL records with their internal (original) field names."""
        dr='BOSS-DR16'
        specids = sorted(self.clienti.sample_specids(samples=1, structure=dr,
                                                    random=False))
        #print(f'DBG retrieve_4: specids={specids}')
        records = self.clienti.retrieve(specids,structure=dr,
                                       include=ALL,
                                       verbose=True)
        actual = sorted(records[0].keys())
        actual.remove('_dr')
        if showact:
            print(f'retrieve_4: actual={pformat(actual)}')
        self.assertEqual(actual, exp.retrieve_4, msg='Actual to Expected')

    def test_retrieve_5(self):
        """Get record samples with their internal (original) field names."""
        dr='BOSS-DR16'
        records = self.clienti.sample_records(1,
                                             include=ALL,
                                             structure=dr,
                                             random=False)
        actual = sorted(records[0].keys())
        actual.remove('_dr')
        if showact:
            print(f'retrieve_5: actual={pformat(actual)}')
        self.assertEqual(actual, exp.retrieve_5, msg='Actual to Expected')

    #############################
    ## BOSS type conversions
    def test_retrieve_boss_json(self):
        """(non)Convert to JSON."""
        flds = ['dec',
                'ra',
                'redshift',
                'specid',
                'spectra.coadd.FLUX',
                'spectra.coadd.IVAR']
        recs = self.clienti.sample_records(1,
                                           random=False,
                                           include=flds,
                                           structure='BOSS-DR16',
                                           rtype='json')
        actual = sorted(recs[0].keys())
        if showact:
            print(f'boss_json: actual={pformat(actual)}')
        self.assertEqual(actual, exp.boss_json, msg='Actual to Expected')

    def test_retrieve_boss_numpy(self):
        """Convert to Numpy."""
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
        #!print(f'clienti={self.clienti}')
        recs = self.clienti.sample_records(1,
                                           structure='BOSS-DR16', rtype='numpy',
                                           include=arflds, random=False)
        actual = sorted(recs[0].keys())
        if showact:
            print(f'boss_numpy: actual={pformat(actual)}')
        self.assertEqual(actual, exp.boss_numpy, msg='Actual to Expected')

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
        recs = self.clienti.sample_records(1,
                                           structure='BOSS-DR16',rtype='pandas',
                                           include=arflds, random=False)
        actual = sorted(recs[0].keys())
        if showact:
            print(f'boss_pandas: actual={pformat(actual)}')
        self.assertEqual(actual, exp.boss_pandas, msg='Actual to Expected')

    def test_retrieve_boss_spectrum1d(self):
        """Convert to Spectrum1D."""
        arflds = [
            'spectra.coadd.FLUX',
            'spectra.coadd.IVAR',
            'spectra.coadd.LOGLAM',
            'redshift'
        ]
        recs = self.clienti.sample_records(1, structure='BOSS-DR16',
                                           rtype='spectrum1d',
                                          include=arflds, random=False)
        actual = sorted(recs[0].keys())
        if showact:
            print(f'boss_spectrum1d: actual={pformat(actual)}')
        self.assertEqual(actual, exp.boss_spectrum1d, msg='Actual to Expected')

    #############################
    ## EVEREST type conversions
    @skip('OBSOLETE dataset. Replace with DES-edr')
    def test_retrieve_everest_numpy(self):
        """Convert to Numpy."""
        arflds = [
            'specid', 'ra','dec',
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
        recs = self.clienti.sample_records(1, structure='DESI-everest',
                                           rtype='numpy',
                                           include=arflds,
                                           random=False)
        actual = sorted(recs[0].keys())
        if showact:
            print(f'everest_numpy: actual={pformat(actual)}')
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
        recs = self.clienti.sample_records(1, structure='DESI-everest', rtype='pandas',
                                          include=arflds, random=False)
        actual = sorted(recs[0].keys())
        if showact:
            print(f'everest_pandas: actual={pformat(actual)}')
        self.assertEqual(actual, exp.everest_pandas, msg='Actual to Expected')


    @skip('OBSOLETE dataset. Replace with DES-edr')
    def test_retrieve_everest_spectrum1d(self):
        """Convert to Spectrum1D."""
        arflds = [
            'redshift',

            'spectra.b_flux',
            'spectra.b_ivar',
            'spectra.b_mask',
            'spectra.b_wavelength'
            ,
            'spectra.r_flux',
            'spectra.r_ivar',
            'spectra.r_mask',
            'spectra.r_wavelength',

            'spectra.z_flux',
            'spectra.z_ivar',
            'spectra.z_mask',
            'spectra.z_wavelength',
        ]
        recs = self.clienti.sample_records(1, structure='DESI-everest', rtype='spectrum1d',
                                          include=arflds, random=False)
        actual = sorted(recs[0].keys())
        if showact:
            print(f'everest_spectrum1d: actual={pformat(actual)}')

        self.assertEqual(actual, exp.everest_spectrum1d,
                         msg='Actual to Expected')


    def test_find_0(self):
        """Get metadata using search spec."""
        name = 'find_0'
        this = self.test_find_0

        outfields = ['id','ra','dec']
        # from list(FitsFile.objects.all().values('ra','dec'))
        constraints = [
            ['ra', 198.0, 199.0],
            ['dec', -2.0, -1.0],
        ]

        found = self.clienti.find(outfields, constraints)
        #print(f'find_0 found={found.rows}')
        actual = found.rows

        self.assertDictEqual(actual[0], exp.find_0[0], msg='Actual to Expected')
