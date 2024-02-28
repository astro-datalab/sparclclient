# Unit tests for the NOIRLab SPARCL API Client
# EXAMPLES: (do after activating venv, in sandbox/sparclclient/)
#   python -m unittest tests.tests_api
#
#  ### Run Against DEV Server.
#  serverurl=http://localhost:8050 python -m unittest tests.tests_api
#  showact=1 serverurl=http://localhost:8050 python -m unittest tests.tests_api
#
# python -m unittest  -v tests.tests_api    # VERBOSE
# python -m unittest tests.tests_api.SparclClientTest
# python -m unittest tests.tests_api.SparclClientTest.test_find_3
# python3 -m unittest tests.tests_api.AlignRecordsTest
#
# showact=1 python -m unittest -k test_find_5 tests.tests_api
#
#  ### Run Against DEV Server.
#  serverurl=http://localhost:8050 python -m unittest tests.tests_api
#
#  ### Run tests Against PAT Server.
#  export serverurl=https://sparc1.datalab.noirlab.edu/
#  python -m unittest tests.tests_api
#
#  ### Run Against STAGE Server.
#  serverurl=https://sparclstage.datalab.noirlab.edu/
#  python -m unittest tests.tests_api
#
#  ### Run Against PROD Server.
#  serverurl=https://astrosparcl.datalab.noirlab.edu/ python -m unittest tests.tests_api  # noqa: E501

# Python library
from contextlib import contextmanager
import unittest
from unittest import skip
import datetime

#! from unittest mock, skipIf, skipUnless
#!import warnings
from pprint import pformat as pf
from urllib.parse import urlparse

#! from urllib.parse import urlencode

#!from unittest.mock import MagicMock, create_autospec
import os

# External Packages
import numpy
import logging
import sys

# Local Packages
from tests.utils import tic, toc
import tests.expected_pat as exp_pat
import tests.expected_dev1 as exp_dev
import sparcl.exceptions as ex
import sparcl.gather_2d as sg
import sparcl.client
import sparcl.gather_2d

#! import sparcl.utils as ut


DEFAULT = "DEFAULT"
ALL = "ALL"
drs = ["BOSS-DR16"]

_DEV1 = "http://localhost:8050"  # noqa: E221
_PAT1 = "https://sparc1.datalab.noirlab.edu"  # noqa: E221
_STAGE = "https://sparclstage.datalab.noirlab.edu"  # noqa: E221
_PROD = "https://astrosparcl.datalab.noirlab.edu"  # noqa: E221

serverurl = os.environ.get("serverurl", _PAT1)
DEV_SERVERS = [
    "http://localhost:8050",
]
if serverurl in DEV_SERVERS:
    exp = exp_dev
else:
    exp = exp_pat

showact = False
showact = showact or os.environ.get("showact") == "1"

showcurl = False
showcurl = showcurl or os.environ.get("showcurl") == "1"

clverb = False


@contextmanager
def streamhandler_to_console(lggr):
    # Use 'up to date' value of sys.stdout for StreamHandler,
    # as set by test runner.
    stream_handler = logging.StreamHandler(sys.stdout)
    lggr.addHandler(stream_handler)
    yield
    lggr.removeHandler(stream_handler)


def testcase_log_console(lggr):
    def testcase_decorator(func):
        def testcase_log_console(*args, **kwargs):
            with streamhandler_to_console(lggr):
                return func(*args, **kwargs)

        return testcase_log_console

    return testcase_decorator


# Arrange to run all doctests.
# Add package paths to python files.
# The should contain testable docstrings.
def load_tests(loader, tests, ignore):
    # @@@ Add these back!!!
    # import doctest
    #
    # print(f"Arranging to run doctests against: sparcl.client")
    # tests.addTests(doctest.DocTestSuite(sparcl.client))
    #
    # print(f"Arranging to run doctests against: sparcl.gather_2d")
    # tests.addTests(doctest.DocTestSuite(sparcl.gather_2d))
    return tests


class SparclClientTest(unittest.TestCase):
    """Test access to each endpoint of the Server API"""

    maxDiff = None  # too see full values in DIFF on assert failure
    # assert_equal.__self__.maxDiff = None

    @classmethod
    def setUpClass(cls):
        if clverb:
            print(
                f"\n# Running SparclClientTest:setUpClass() "
                "{str(datetime.datetime.now())}"
            )

        # Client object creation compares the version from the Server
        # against the one expected by the Client. Raise error if
        # the Client is at least one major version behind.

        cls.client = sparcl.client.SparclClient(
            url=serverurl,
            verbose=clverb,
            show_curl=showcurl,
        )
        cls.timing = dict()
        cls.doc = dict()
        cls.count = dict()

        print(
            f"Running Client tests\n"
            f'  against Server: "{urlparse(serverurl).netloc}"\n'
            f"  comparing to: {exp.__name__}\n"
            f"  showact={showact}\n"
            f"  showcurl={showcurl}\n"
            f"  client={cls.client}\n"
        )

        # Get some id_lists to use in tests
        found = cls.client.find(
            ["sparcl_id", "specid"], sort="sparcl_id", limit=5
        )
        sparc_tups, spec_tups = list(
            zip(*[(r["sparcl_id"], r["specid"]) for r in found.records])
        )
        sparc_ids, spec_ids = list(sparc_tups), list(spec_tups)
        print(f"sparc_ids={sparc_ids}")
        print(f"spec_ids={spec_ids}")

        # Lists of SPECID
        cls.specid_list0 = spec_ids[:2]
        cls.specid_list2 = spec_ids[:3]
        cls.specid_list5 = spec_ids[:5]
        # two real specids, one fake
        cls.specid_list3 = spec_ids[:2] + [300000000000000001]
        # two fake specids
        cls.specid_list4 = [300000000000000001, 111111111111111111]

        # Lists of SPARCL_ID (UUID)
        cls.uuid_list0 = sparc_ids[:3]
        cls.uuid_list2 = sparc_ids[:3]
        # two real UUIDs, one fake
        cls.uuid_list3 = sparc_ids[:2] + [
            "00001ebf-d030-4d59-97e5-060c47202897"
        ]
        # two (probably) fake UUIDs
        cls.uuid_list4 = [
            "00001ebf-d030-4d59-97e5-060c47202897",
            "ff1e9a12-f21a-4050-bada-a1e67a265885",
        ]
        if clverb:
            print(
                f"\n# Completed SparclClientTest:setUpClass() "
                f"{str(datetime.datetime.now())}\n"
            )

    @classmethod
    def tearDownClass(cls):
        pass

    # Full records are big.  Get the gist of them.
    def records_expected(self, recs, expd, jdata=None, show=False):
        actual = sorted(recs[0].keys())
        expected = sorted(eval(expd))  # e.g. 'ep.retrieve_1'
        if show:
            #!f'\nEXPECTED={expected}'
            print(f"{expd}: ACTUAL={actual}")
        self.assertEqual(actual, expected, "Actual to Expected")
        return actual

    #################################
    # ## Convenience Functions
    # ##

    def test_get_all_fields(self):
        """Get the intersection of all fields that are tagged as 'all'."""
        actual = self.client.get_all_fields()
        if showact:
            print(f"all_fields: actual={pf(actual)}")
        self.assertEqual(actual, exp.all_fields, msg="Actual to Expected")

    def test_get_default_fields(self):
        """Get the intersection of all fields that are tagged as 'default'."""
        actual = self.client.get_default_fields()
        if showact:
            print(f"get_default_fields: actual={pf(actual)}")
        self.assertEqual(actual, exp.default_fields, msg="Actual to Expected")

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
        missing = self.client.missing(self.uuid_list0 + uuids)
        self.assertEqual(
            sorted(missing), sorted(uuids), msg="Actual to Expected"
        )

    def test_missing_1(self):
        """None missing"""
        # uuids = self.client.sample_uuids()
        uuids = self.uuid_list0

        missing = self.client.missing(uuids)
        if showact:
            print(f"missing_1: missing={missing}")
        self.assertEqual(missing, [], msg="Actual to Expected")

    def test_missing_specids_1(self):
        """Specids (not UUID) missing"""
        badid = "NOT_SPEC_ID"
        specids = set([badid] + self.specid_list0[:1])
        missing = set(self.client.missing_specids(specids, verbose=True))
        if showact:
            print(f"missing_specids_1: specids={specids}")
            print(f"missing_specids_1: missing={missing}")
        self.assertEqual(missing, set([badid]), msg="Actual to Expected")

    def test_retrieve_0(self):
        """Get spectra using small list of SPECIDS."""
        res = self.client.retrieve_by_specid(
            self.specid_list0, include=["sparcl_id", "specid"]
        )
        actual = sorted([r["specid"] for r in res.records])
        if showact:
            print(f"retrieve_0: actual={actual}")

        self.assertEqual(actual, exp.retrieve_0, msg="Actual to Expected")

    def test_retrieve_0b(self):
        """Get spectra using small list of uuids."""
        name = "retrieve_0b"
        uuids = self.uuid_list0

        tic()
        res = self.client.retrieve(uuids)
        self.timing[name] = toc()
        actual = sorted(res.records[0].keys())

        if showact:
            print(f"retrieve_0b: actual={pf(actual)}")

        self.assertEqual(actual, exp.retrieve_0b, msg="Actual to Expected")

    def test_retrieve_1(self):
        """Raise exception when unknown field referenced in include"""
        inc2 = ["bad_field_name", "flux", "or_mask"]

        #! specids = sorted(self.client.sample_specids(samples=1,
        #!                                             dataset_list=drs))
        with self.assertRaises(ex.BadInclude):
            self.client.retrieve_by_specid(
                self.specid_list0, include=inc2, dataset_list=drs
            )

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
        uuids = self.uuid_list0
        with self.assertWarns(Warning):
            self.client.retrieve(uuids + [999])

    def test_retrieve_5(self):
        """Limit number of records returned by retrieve_by_specid."""
        res = self.client.retrieve_by_specid(
            self.specid_list5, include=["specid"], limit=2
        )
        actual = sorted([r["specid"] for r in res.records])
        if showact:
            print(f"retrieve_5: actual={actual}")

        self.assertEqual(actual, exp.retrieve_5, msg="Actual to Expected")

    def test_find_0(self):
        """Get metadata using search spec."""

        outfields = ["sparcl_id", "ra", "dec"]
        # from list(FitsRecord.objects.all().values('ra','dec'))

        # To get suitable constraints (in sparc-shell on Server):
        #   sorted(FitsRecord.objects.all().values('ra','dec'),
        #          key=lambda r: r['dec'])
        if serverurl in DEV_SERVERS:
            #!constraints = {"ra": [246.0, 247.0], "dec": [+34.7, +34.8]}
            constraints = {"ra": [194.0, 195.0], "dec": [+27.5, +27.6]}
        else:
            constraints = {"ra": [340.0, 341.0], "dec": [+3.0, +4.0]}
        found = self.client.find(outfields, constraints=constraints, limit=3)
        actual = found.records[:2]
        if showact:
            print(f"find_0: actual={pf(actual[:2])}")
        self.assertEqual(actual, exp.find_0, msg="Actual to Expected")

    def test_find_1(self):
        """Get metadata using search spec."""
        outfields = ["sparcl_id", "ra", "dec"]
        found = self.client.find(outfields, limit=1, sort="sparcl_id")  # @@@
        actual = sorted(found.records, key=lambda rec: rec["sparcl_id"])
        if showact:
            print(f"find_1: actual={pf(actual)}")
        self.assertEqual(
            actual,
            sorted(exp.find_1, key=lambda rec: rec["sparcl_id"]),
            msg="Actual to Expected",
        )

    @skip("Takes too long for regression tests when used on big database.")
    def test_find_2(self):
        """Limit=None."""
        outfields = ["sparcl_id", "ra", "dec"]
        found = self.client.find(
            outfields, limit=None, sort="sparcl_id"
        )  # @@@
        actual = len(found.records)
        if showact:
            print(f"find_2: actual={pf(actual)}")
        self.assertEqual(actual, exp.find_2, msg="Actual to Expected")

    def test_find_3(self):
        """Limit=3."""
        outfields = ["sparcl_id", "ra", "dec"]
        found = self.client.find(outfields, limit=3, sort="sparcl_id")  # @@@
        actual = sorted(found.records, key=lambda rec: rec["sparcl_id"])
        if showact:
            print(f"find_3: actual={pf(actual)}")
        self.assertEqual(
            actual,
            sorted(exp.find_3, key=lambda rec: rec["sparcl_id"]),
            msg="Actual to Expected",
        )

    def test_find_4(self):
        """Check found.ids"""
        outfields = ["sparcl_id", "ra", "dec"]
        found = self.client.find(outfields, limit=3, sort="sparcl_id")  # @@@
        actual = sorted(found.ids)
        if showact:
            print(f"find_4: actual={pf(actual)}")
        self.assertEqual(actual, sorted(exp.find_4), msg="Actual to Expected")

    # DLS-365
    @skip("Not implemented. Waiting for switch to ingest-time field naming ")
    def test_find_5a(self):
        """Aux field values when they exists in all found records"""
        found = self.client.find(
            ["data_release", "mjd"], limit=5, sort="sparcl_id"
        )
        actual = found.records
        if showact:
            print(f"find_5a: actual={pf(actual)}")
        self.assertEqual(actual, exp.find_5a, msg="Actual to Expected")

    # DLS-365
    @skip("Not implemented. Waiting for switch to ingest-time field naming ")
    def test_find_5b(self):
        """Aux field in one Data Set but not another. (proper subset)"""
        cons = {"data_release": ["SDSS-DR16", "DESI-EDR"]}
        f0 = self.client.find(
            ["data_release"], constraints=cons, limit=5, sort="sparcl_id"
        )
        f1 = self.client.find(
            ["data_release", "plate"],
            constraints=cons,
            limit=5,
            sort="sparcl_id",
        )
        self.assertEqual(f0.count, f1.count)

    # DLS-365
    @skip("Not implemented. Waiting for switch to ingest-time field naming ")
    def test_find_5c(self):
        """Aux field values when they do not exist in any found records"""
        cons = {"data_release": ["SDSS-DR16", "DESI-EDR"]}
        nsf = "NO_SUCH_FIELD"
        f1 = self.client.find(
            ["data_release", nsf], constraints=cons, limit=5, sort="sparcl_id"
        )
        msg = f'Expected field "{nsf}" with value None in all records'
        self.assertTrue(nsf in f1.records[0].keys(), msg)

    def test_reorder_1a(self):
        """Reorder retrieved records by sparcl_id."""
        name = "reorder_1a"
        ids = self.uuid_list2
        print(f"ids: {ids}")

        tic()
        res = self.client.retrieve(ids)
        res_ids = [r["sparcl_id"] for r in res.records]
        print(f"retrieved: {res_ids}")
        self.timing[name] = toc()
        res_reorder = res.reorder(ids)
        actual = [f["sparcl_id"] for f in res_reorder.records]
        if showact:
            print(f"reorder_1a: actual={pf(actual)}")
        self.assertEqual(actual, exp.reorder_1a, msg="Actual to Expected")

    def test_reorder_1b(self):
        """Reorder retrieved records by specid."""
        name = "reorder_1b"
        specids = self.specid_list2

        tic()
        res = self.client.retrieve_by_specid(specids)
        self.timing[name] = toc()
        res_reorder = res.reorder(specids)
        actual = [f["specid"] for f in res_reorder.records]
        if showact:
            print(f"reorder_1b: actual={pf(actual)}")
        self.assertEqual(actual, exp.reorder_1b, msg="Actual to Expected")

    def test_reorder_2a(self):
        """Reorder records when sparcl_id is missing from database, after using
        retrieve()."""
        name = "reorder_2a"
        ids = self.uuid_list3

        tic()
        with self.assertWarns(Warning):
            res = self.client.retrieve(ids)
        self.timing[name] = toc()
        with self.assertWarns(Warning):
            res_reorder = res.reorder(ids)
        actual = [f["sparcl_id"] for f in res_reorder.records]
        if showact:
            print(f"reorder_2a: actual={pf(actual)}")
        self.assertEqual(actual, exp.reorder_2a, msg="Actual to Expected")

    def test_reorder_2b(self):
        """Reorder records when specid is missing from database, after
        using retrieve_by_specid()."""
        name = "reorder_2b"
        specids = self.specid_list3

        tic()
        res = self.client.retrieve_by_specid(specids)
        self.timing[name] = toc()
        with self.assertWarns(Warning):
            res_reorder = res.reorder(specids)
        actual = [f["specid"] for f in res_reorder.records]
        if showact:
            print(f"reorder_2b: actual={pf(actual)}")
        self.assertEqual(actual, exp.reorder_2b, msg="Actual to Expected")

    def test_reorder_3a(self):
        """Test for expected Exception when a list of sparcl_ids with
        length 0 is passed to reorder method after using retrieve()."""
        name = "reorder_3a"
        ids = self.uuid_list2
        og_ids = []

        tic()
        res = self.client.retrieve(ids)
        self.timing[name] = toc()
        with self.assertRaises(ex.NoIDs):
            res.reorder(og_ids)

    def test_reorder_3b(self):
        """Test for expected Exception when a list of specids with length 0
        is passed to reorder method after using retrieve_by_specid()."""
        name = "reorder_3b"
        specids = self.specid_list2
        og_specids = []

        tic()
        res = self.client.retrieve_by_specid(specids)
        self.timing[name] = toc()
        with self.assertRaises(ex.NoIDs):
            res.reorder(og_specids)

    def test_reorder_4a(self):
        """Test for expected Exception when there are no records, using
        sparcl_ids and retrieve()."""
        name = "reorder_4a"
        ids = self.uuid_list4

        tic()
        with self.assertWarns(Warning):
            res = self.client.retrieve(ids)
        self.timing[name] = toc()
        with self.assertRaises(ex.NoRecords):
            res.reorder(ids)

    def test_reorder_4b(self):
        """Test for expected Exception when there are no records, using specids
        and retrieve_by_specid()."""
        name = "reorder_4b"
        specids = self.specid_list4

        tic()
        res = self.client.retrieve_by_specid(specids)
        self.timing[name] = toc()
        with self.assertRaises(ex.NoRecords):
            res.reorder(specids)

    def test_dls_468(self):
        idss = self.client.find(
            constraints={"data_release": ["SDSS-DR16"]}, limit=1
        ).ids
        re = self.client.retrieve(
            uuid_list=idss, include=["ra", "dec"], verbose=True
        )
        self.assertEqual(1, re.count)


# See DLS-280
@skip("takes to long to retrieve")  # 7/12/23
class AlignRecordsTest(unittest.TestCase):
    """Test ability to align spectra and all records by wavelength grid"""

    @classmethod
    def setUpClass(cls):
        if clverb:
            print(
                f"\n# Running AlignRecordsTest:setUpClass() "
                "{str(datetime.datetime.now())}"
            )

        cls.client = sparcl.client.SparclClient(
            url=serverurl, verbose=clverb, show_curl=showcurl
        )
        found = cls.client.find(
            constraints={"data_release": ["BOSS-DR16"]}, limit=20
        )
        cls.found = found
        cls.specflds = ["wavelength", "flux", "ivar", "mask", "model"]
        cls.got = cls.client.retrieve(found.ids, include=cls.specflds)

        if clverb:
            print(
                f"\n# Completed AlignRecordsTest:setUpClass() "
                f"{str(datetime.datetime.now())}\n"
            )

    @classmethod
    def tearDownClass(cls):
        pass

    # Requirement #1 from DLS-280
    def test_align_1(self):
        """The grid value return by align_records is a numpy array of
        Floats."""
        ar_dict, grid = sg.align_records(
            self.got.records, fields=["wavelength", "flux", "model"]
        )
        self.assertTrue(isinstance(grid, numpy.ndarray))
        self.assertTrue(isinstance(grid[0], numpy.float64))

    # Requirement #2 from DLS-280
    def test_align_2(self):
        """Allow conversion of all SPECTRA-type fields (except for wavelength)
        to be returned as same type of structure and registered to the same
        wavelength grid."""

        #! print(f'Fields={list(self.got.records[0].keys())}')
        ar_dict, grid = sg.align_records(
            self.got.records, fields=self.specflds
        )
        self.assertEqual(sorted(ar_dict.keys()), sorted(self.specflds))

    # Requirement #3 from DLS-280
    def test_align_3(self):
        """Verify shapes of arrays"""

        ar_dict, grid = sg.align_records(
            self.got.records, fields=self.specflds
        )
        shape = list(ar_dict.values())[0].shape
        self.assertEqual(shape, (20, 4621))

    # Requirement #4 from DLS-280
    # Difficult to implement
    @skip("Not implemented")
    def test_align_4(self):
        """All align fields are valid spectra fields"""
        self.assertTrue(False)

    # Requirement #5 from DLS-280
    def test_align_5(self):
        """Verify wavelength given."""
        msg = 'You must provide "wavelength" spectra field'
        with self.assertRaises(Exception, msg=msg):
            ar_dict, grid = sg.align_records(
                self.got.records, fields=["flux", "model"]
            )

    # Requirement #6  from DLS-280
    def test_align_6(self):
        """Default FIELDS to flux,wavelength."""
        got = self.client.retrieve(
            self.found.ids, include=["flux", "model", "wavelength"]
        )
        ar_dict, grid = sg.align_records(got.records)
        self.assertEqual(ar_dict["flux"].shape, (20, 4621))

    # Requirement #7  from DLS-280
    @skip("Data on DEV does not seem good enough to invoke this.")
    def test_align_7(self):
        """Error message if PRECISION not adequate for alignment"""
        # 7 precision does not support alignment
        got = self.client.retrieve(
            self.found.ids, include=["wavelength", "flux", "model"]
        )
        msg = f"bad precision"
        with self.assertRaises(Exception, msg=msg):
            ar_dict, grid = sg.align_records(got.records, precision=11)
            # shape = ar_dict['flux'].shape
