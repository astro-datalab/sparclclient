# Unit tests for the NOIRLab SPARCL API Client
# EXAMPLES: (do after activating venv, in sandbox/sparclclient/)
# usrpw (User Password) is intentionally left blank in these examples.
# When actually running tests, the User Password should be included.
#
#   usrpw='' python -m unittest tests.tests_api
#
#  ### Run Against DEV Server.
#  usrpw='' serverurl=http://localhost:8050 python -m unittest tests.tests_api
#  usrpw='' serverurl=http://sparcdev2.csdc.noirlab.edu:8050 python -m unittest tests.tests_api  # noqa: E501
#  showact=1 usrpw='' serverurl=http://localhost:8050 python -m unittest tests.tests_api  # noqa: E501
#
# python -m unittest  -v tests.tests_api    # VERBOSE (show what is skipped)
# python -m unittest tests.tests_api.SparclClientTest
# python -m unittest tests.tests_api.SparclClientTest.test_find_3
# python3 -m unittest tests.tests_api.AlignRecordsTest
# usrpw='' python3 -m unittest tests.tests_api.AuthTest
#
# showact=1 python -m unittest -k test_find_5 tests.tests_api
#
#  ### Run Against DEV Server.
#  usrpw='' serverurl=http://localhost:8050 python -m unittest tests.tests_api
#
#  ### Run tests Against PAT Server.
#  export serverurl=https://sparc1.datalab.noirlab.edu/
#  usrpw='' python -m unittest tests.tests_api
#
#  ### Run Against STAGE Server.
#  serverurl=https://sparclstage.datalab.noirlab.edu/
#  usrpw='' python -m unittest tests.tests_api
#
#  ### Run Against PROD Server.
#  usrpw='' serverurl=https://astrosparcl.datalab.noirlab.edu/ python -m unittest tests.tests_api  # noqa: E501

# Python library
from contextlib import contextmanager
import unittest
from unittest import skip, skipUnless, skipIf
import datetime
import requests

#!import time
from contextlib import redirect_stdout

#! from unittest mock, skipIf, skipUnless
#!import warnings
from pprint import pformat as pf
from urllib.parse import urlparse

#! from urllib.parse import urlencode

#!from unittest.mock import MagicMock, create_autospec
import os
import io

# External Packages
import numpy
import logging
import sys
import warnings

# Local Packages
from tests.utils import tic, toc
import tests.expected_pat as exp
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

serverurl = os.environ.get("serverurl", _PROD)
showact = False
showact = showact or os.environ.get("showact") == "1"
showcurl = False
showcurl = showcurl or os.environ.get("showcurl") == "1"
clverb = False
clverb = clverb or os.environ.get("clverb") == "1"
showall = False
showall = showall or os.environ.get("showall") == "1"
if showall:
    showact = showcurl = clverb = True

usrpw = os.environ.get("usrpw")  # password for test users
show_run_context = True  # Print message about parameters of this test run


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
    import doctest

    if serverurl == _PROD:
        print(f"Arranging to run doctests against: sparcl.client")
        tests.addTests(doctest.DocTestSuite(sparcl.client))

        print(f"Arranging to run doctests against: sparcl.gather_2d")
        tests.addTests(doctest.DocTestSuite(sparcl.gather_2d))
    else:
        print(
            "Not running doctests since you are not running client"
            " against the PRODUCTION server."
        )

    return tests


def print_run_context(cls):
    print(
        f"""
    Running Client Tests
      against Server: \t"{urlparse(serverurl).netloc}"
      comparing to: \t{exp.__name__}
      {showact=}
      {showcurl=}
      client={cls.client}

    For REPRODUCIBLE RESULTS rebuild Server DB before running tests!
    Use: init-db.sh
    """
    )


class SparclClientTest(unittest.TestCase):
    """Test access to each endpoint of the Server API"""

    maxDiff = None  # too see full values in DIFF on assert failure
    # assert_equal.__self__.maxDiff = None

    @classmethod
    def setUpClass(cls):
        if clverb:
            print(
                f"\n# Running SparclClientTest:setUpClass() "
                f"{str(datetime.datetime.now())}!"
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

        global show_run_context

        if show_run_context:
            print_run_context(cls)
            show_run_context = False

        # Get some id_lists to use in tests
        found = cls.client.find(
            ["sparcl_id", "specid"], sort="sparcl_id", limit=5
        )
        sparc_tups, spec_tups = list(
            zip(*[(r["sparcl_id"], r["specid"]) for r in found.records])
        )
        sparc_ids, spec_ids = list(sparc_tups), list(spec_tups)
        if showact:
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
        missing = set(self.client.missing_specids(specids, verbose=False))
        if showact:
            print(f"missing_specids_1: specids={specids}")
            print(f"missing_specids_1: missing={missing}")
        self.assertEqual(missing, set([badid]), msg="Actual to Expected")

    def test_retrieve_0(self):
        """Get spectra using small list of SPECIDS."""
        drs = ["SDSS-DR16", "BOSS-DR16", "DESI-EDR"]
        res = self.client.retrieve_by_specid(
            self.specid_list0,
            include=["sparcl_id", "specid", "flux"],
            dataset_list=drs,
        )
        actual = sorted(res.records[0].keys())
        if showact:
            print(f"retrieve_0: actual={actual}")

        self.assertEqual(actual, exp.retrieve_0, msg="Actual to Expected")

    def test_retrieve_0b(self):
        """Get spectra using small list of uuids."""
        name = "retrieve_0b"
        uuids = self.uuid_list0
        drs = ["SDSS-DR16", "BOSS-DR16", "DESI-EDR"]

        tic()
        res = self.client.retrieve(uuids, dataset_list=drs)
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
        drs = ["SDSS-DR16", "BOSS-DR16", "DESI-EDR"]
        with self.assertWarns(Warning):
            self.client.retrieve(uuids + [999], dataset_list=drs)

    def test_retrieve_5(self):
        """Limit number of records returned by retrieve_by_specid."""
        drs = ["SDSS-DR16", "BOSS-DR16", "DESI-EDR"]
        res = self.client.retrieve_by_specid(
            self.specid_list5,
            include=["specid", "ivar"],
            dataset_list=drs,
            limit=2,
        )
        actual = len(res.records)
        if showact:
            print(f"retrieve_5: actual={actual}")

        self.assertEqual(actual, exp.retrieve_5, msg="Actual to Expected")

    def test_find_0(self):
        """Get metadata using search spec."""

        outfields = ["data_release", "specid"]
        # To get suitable constraints (in sparc-shell on Server):
        #    list(FitsRecord.objects.all().values('ra','dec'))
        constraints = {"ra": [132.1, 132.2], "dec": [+28.0, +28.1]}
        found = self.client.find(outfields, constraints=constraints, limit=3)
        actual = found.records[:2]
        if showact:
            print(f"find_0: actual={pf(actual[:2])}")
        self.assertEqual(actual, exp.find_0, msg="Actual to Expected")

    @skip("fiddly bit skipped until we use factoryboy")
    def test_find_1(self):
        """Get metadata using search spec."""
        outfields = ["data_release", "specid"]
        constraints = {
            "redshift": [0.191, 0.192],
            "exptime": [2100.2, 2100.31],
            "data_release": ["SDSS-DR16"],
        }
        found = self.client.find(
            outfields, constraints=constraints, limit=1, sort="specid"
        )  # @@@
        actual = sorted(found.records, key=lambda rec: rec["specid"])
        if showact:
            print(f"find_1: actual={pf(actual)}")
        self.assertEqual(
            actual,
            sorted(exp.find_1, key=lambda rec: rec["specid"]),
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
        outfields = ["data_release"]
        found = self.client.find(outfields, limit=3, sort="data_release")
        actual = sorted(found.records, key=lambda rec: rec["data_release"])
        if showact:
            print(f"find_3: actual={pf(actual)}")
        self.assertEqual(
            actual,
            sorted(exp.find_3, key=lambda rec: rec["data_release"]),
            msg="Actual to Expected",
        )

    def test_find_4(self):
        """Check found.ids"""
        outfields = ["sparcl_id", "ra", "dec"]
        found = self.client.find(outfields, limit=3, sort="sparcl_id")  # @@@
        # Since all UUIDs have the same length, check the length of the
        # first ID to match.
        actual = len(sorted(found.ids)[0])
        if showact:
            print(f"find_4: actual={pf(actual)}")
        self.assertEqual(actual, exp.find_4, msg="Actual to Expected")

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

        tic()
        drs = ["SDSS-DR16", "BOSS-DR16", "DESI-EDR"]
        res = self.client.retrieve(ids, dataset_list=drs)
        self.timing[name] = toc()
        res_reorder = res.reorder(ids)
        actual = [f["sparcl_id"] for f in res_reorder.records]
        if showact:
            print(f"reorder_1a: actual={pf(actual)}")
        self.assertEqual(actual, ids, msg="Actual to Expected")

    def test_reorder_1b(self):
        """Reorder retrieved records by specid."""
        name = "reorder_1b"
        specids = self.specid_list2

        tic()
        drs = ["SDSS-DR16", "BOSS-DR16", "DESI-EDR"]
        res = self.client.retrieve_by_specid(specids, dataset_list=drs)
        self.timing[name] = toc()
        res_reorder = res.reorder(specids)
        actual = [f["specid"] for f in res_reorder.records]
        if showact:
            print(f"reorder_1b: actual={pf(actual)}")
        self.assertEqual(actual, specids, msg="Actual to Expected")

    def test_reorder_2a(self):
        """Reorder records when sparcl_id is missing from database, after using
        retrieve()."""
        name = "reorder_2a"
        ids = self.uuid_list3

        tic()
        drs = ["SDSS-DR16", "BOSS-DR16", "DESI-EDR"]
        with self.assertWarns(Warning):
            res = self.client.retrieve(ids, dataset_list=drs)
        self.timing[name] = toc()
        with self.assertWarns(Warning):
            res_reorder = res.reorder(ids)
        actual = [f["sparcl_id"] for f in res_reorder.records]
        if showact:
            print(f"reorder_2a: actual={pf(actual)}")
        self.assertEqual(actual, ids[:2] + ["None"], msg="Actual to Expected")

    def test_reorder_2b(self):
        """Reorder records when specid is missing from database, after
        using retrieve_by_specid()."""
        name = "reorder_2b"
        specids = self.specid_list3

        tic()
        drs = ["SDSS-DR16", "BOSS-DR16", "DESI-EDR"]
        res = self.client.retrieve_by_specid(specids, dataset_list=drs)
        self.timing[name] = toc()
        with self.assertWarns(Warning):
            res_reorder = res.reorder(specids)
        actual = [f["specid"] for f in res_reorder.records]
        if showact:
            print(f"reorder_2b: actual={pf(actual)}")
        self.assertEqual(
            actual, specids[:2] + [None], msg="Actual to Expected"
        )

    def test_reorder_3a(self):
        """Test for expected Exception when a list of sparcl_ids with
        length 0 is passed to reorder method after using retrieve()."""
        name = "reorder_3a"
        ids = self.uuid_list2
        og_ids = []

        tic()
        drs = ["SDSS-DR16", "BOSS-DR16", "DESI-EDR"]
        res = self.client.retrieve(ids, dataset_list=drs)
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
        drs = ["SDSS-DR16", "BOSS-DR16", "DESI-EDR"]
        res = self.client.retrieve_by_specid(specids, dataset_list=drs)
        self.timing[name] = toc()
        with self.assertRaises(ex.NoIDs):
            res.reorder(og_specids)

    def test_reorder_4a(self):
        """Test for expected Exception when there are no records, using
        sparcl_ids and retrieve()."""
        name = "reorder_4a"
        ids = self.uuid_list4

        tic()
        drs = ["SDSS-DR16", "BOSS-DR16", "DESI-EDR"]
        with self.assertWarns(Warning):
            res = self.client.retrieve(ids, dataset_list=drs)
        self.timing[name] = toc()
        with self.assertRaises(ex.NoRecords):
            res.reorder(ids)

    def test_reorder_4b(self):
        """Test for expected Exception when there are no records, using specids
        and retrieve_by_specid()."""
        name = "reorder_4b"
        specids = self.specid_list4

        tic()
        drs = ["SDSS-DR16", "BOSS-DR16", "DESI-EDR"]
        res = self.client.retrieve_by_specid(specids, dataset_list=drs)
        self.timing[name] = toc()
        with self.assertRaises(ex.NoRecords):
            res.reorder(specids)

    def test_dls_468(self):
        idss = self.client.find(
            constraints={"data_release": ["SDSS-DR16"]}, limit=1
        ).ids
        re = self.client.retrieve(
            uuid_list=idss,
            include=["ra", "dec"],
            dataset_list=["SDSS-DR16"],
            verbose=False,
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


@skipIf("usrpw" in os.environ, "Testing auth using usrpw env var")
class NoopTest(unittest.TestCase):
    """Non-tests."""

    def test_noop(self):
        print("<Skipped-AuthTest>", end="", flush=True)


@skipUnless("usrpw" in os.environ, "Password is required to test auth")
class AuthTest(unittest.TestCase):
    """Test authorization and authentication features"""

    @classmethod
    def setUpClass(cls):
        if clverb:
            print(
                f"\n# Running AuthTest:setUpClass() "
                f"{str(datetime.datetime.now())}"
            )

        cls.client = sparcl.client.SparclClient(
            url=serverurl, verbose=clverb, show_curl=showcurl
        )

        global show_run_context

        if show_run_context:
            print_run_context(cls)
            show_run_context = False

        cls.outflds = ["sparcl_id", "data_release"]
        cls.inc = ["data_release", "flux"]

        # Test users
        cls.auth_user = "test_user_1@noirlab.edu"
        cls.unauth_user = "test_user_2@noirlab.edu"

        # Dataset lists
        cls.Pub = ["BOSS-DR16", "DESI-EDR", "SDSS-DR16"]
        cls.Priv = ["SDSS-DR17-test"]
        cls.PrivPub = cls.Priv + cls.Pub

        # Sample list of sparcl_ids from each data set
        out = ["sparcl_id"]

        cls.cons = dict(spectype=["GALAXY"], redshift=[0.5, 0.9])

        # Silence output from login/logout
        #   (redirect only affects the WITH context)
        with redirect_stdout(io.StringIO()):  # as f:
            cls.client.login(cls.auth_user, usrpw)
        cls.uuid_priv = (
            cls.client.find(
                outfields=out,
                constraints={"data_release": cls.Priv},
                limit=2,
                sort="sparcl_id",
            )
        ).ids
        # cls.uuid_pub = (  # cls.uuid_sdssdr16
        #    cls.client.find(
        #        outfields=out,
        #        constraints={"data_release": cls.Pub},
        #        limit=2,
        #        sort="sparcl_id",
        #    )
        # ).ids
        cls.uuid_pub = (
            cls.client.find(
                outfields=out,
                constraints={"data_release": ["BOSS-DR16"]},
                limit=2,
                sort="sparcl_id",
            )
        ).ids
        cls.uuid_privpub = cls.uuid_priv + cls.uuid_pub

        with redirect_stdout(io.StringIO()):  # as f:
            cls.client.logout()

        if clverb:
            print(  # @@@ Was not displaying
                f"\n# Completed AuthTest:setUpClass() "
                f"{str(datetime.datetime.now())}\n"
            )

    def silent_login(cls, usr, usrpw, silent=True):
        if silent:
            with redirect_stdout(io.StringIO()):  # as f:
                cls.client.login(usr, usrpw)
        else:
            cls.client.login(usr, usrpw)

    def silent_logout(cls):
        with redirect_stdout(io.StringIO()):  # as f:
            cls.client.logout()

    @classmethod
    def tearDownClass(cls):
        pass

    # curl -X 'POST' \
    #   'http://localhost:8050/sparc/get_token/' \
    #   -H 'Content-Type: application/json' \
    #   -d '{"email": "test_user_1@noirlab.edu", "password": "XX"}'; echo
    #
    # > Could not get token from SSO server:
    #   HTTPSConnectionPool(host='docker1.csdc.noirlab.edu', port=443):
    #   Max retries exceeded with url: /api/token/
    # (Caused by SSLError(SSLCertVerificationError(1,
    #                                   '[SSL: CERTIFICATE_VERIFY_FAILED]
    # certificate verify failed: unable to get local issuer certificate
    # (_ssl.c:997)')))

    def test_sso_server(self):
        sso_server = "https://sso.csdc.noirlab.edu/"
        response = requests.get(sso_server)
        self.assertEqual(response.status_code, 200, response.content.decode())

    def test_get_token(self):
        """Make sure we can get expected SSO token."""
        json = {"email": self.auth_user, "password": usrpw}
        if showact:
            print(f"test_get_token: {json=}")

        expected = 281
        res = requests.post(f"{self.client.apiurl}/get_token/", json=json)
        self.assertEqual(res.status_code, 200, res.content.decode())
        token = res.content.decode()
        actual = len(token)
        if showact:
            print(f"test_get_token: ({len(token)}) {token=!s}")
        self.assertEqual(actual, expected, msg="Actual to Expected")

    def test_authorized_1(self):
        """Test authorized method with authorized user signed in"""
        self.silent_login(self.auth_user, usrpw)
        actual = self.client.authorized
        if showact:
            print(f"1 authorized_1: {actual=}")
            #!time.sleep(1)
            #!print(f"2 authorized_1: {self.client.authorized}")
            #!time.sleep(20)
            #!print(f"3 authorized_1: {self.client.authorized}")
        self.assertEqual(actual, exp.authorized_1, msg="Actual to Expected")
        self.silent_logout()

    def test_authorized_2(self):
        """Test authorized method with unauthorized user signed in"""
        self.silent_login(self.unauth_user, usrpw)
        actual = self.client.authorized
        if showact:
            print(f"authorized_2: actual={actual}")

        self.assertEqual(actual, exp.authorized_2, msg="Actual to Expected")
        self.silent_logout()

    def test_authorized_3(self):
        """Test authorized method on anonymous user not signed in"""
        self.silent_logout()
        actual = self.client.authorized
        if showact:
            print(f"authorized_3: actual={actual}")
        self.assertEqual(actual, exp.authorized_3, msg="Actual to Expected")

    def auth_find(self, user, drs, expvar, limit=21000):
        expected = eval(expvar)  # e.g. 'ep.retrieve_N'
        #!print(f'{expvar}: {user=} {drs=} ')
        self.silent_login(user, usrpw)
        #!print(f'{expvar}: {self.client.authorized=} {user=} {drs=} ')
        out = self.outflds
        try:
            if drs is None:
                found = self.client.find(outfields=out, limit=limit)
            else:
                found = self.client.find(
                    outfields=out,
                    constraints=dict(data_release=drs),
                    limit=limit,
                )
            #!if showact:
            #!    print(f"{expvar}: {found.records=}")

            actual = sorted(set([r._dr for r in found.records]))
        except Exception as err:
            actual = str(err)
        finally:
            self.silent_logout()
        if showact:
            print(
                f"{expvar}: {actual=}"
                f" {self.client.authorized=} {user=} {drs=}"
            )
        self.assertEqual(actual, expected, msg="Actual to Expected")

    def auth_retrieve(self, user, drs, expvar):
        expected = eval(expvar)  # e.g. 'ep.retrieve_N'
        self.silent_login(user, usrpw)
        #!print(f'{expvar}: {self.client.authorized=} {user=} {drs=} ')
        ids = self.uuid_privpub
        inc = ["sparcl_id", "data_release"]
        try:
            if drs is None:
                got = self.client.retrieve(uuid_list=ids, include=inc)
            else:
                got = self.client.retrieve(
                    uuid_list=ids, include=inc, dataset_list=drs
                )
            actual = sorted(set([r._dr for r in got.records]))
        except Exception as err:
            actual = str(err)
        finally:
            self.silent_logout()
        if showact:
            print(
                f"{expvar}: {actual=}"
                f" {self.client.authorized=} {user=} {drs=}"
            )
        self.assertEqual(actual, expected, msg="Actual to Expected")

    # | METHOD | USER | DATASETS | OK? |
    # | find | Auth | Priv,Pub | PASS |
    # @skip("Does not return Priv")  # @@@
    def test_auth_find_1(self):
        """Test find method with authorized user; private data set specified.
        Should find Authorized Private DR"""
        exp = "exp.auth_find_1"
        self.auth_find(self.auth_user, self.PrivPub, exp)

    # | find | Auth | None | PASS |
    # @skip("Does not return Priv")  # @@@
    def test_auth_find_2(self):
        """Test find method with authorized user; no data sets specified.
        Should find Authorized Private DR"""
        exp = "exp.auth_find_2"
        self.auth_find(self.auth_user, None, exp)

    # | find | Unauth | Priv,Pub | FAIL |
    def test_auth_find_3(self):
        """Test find method with unauthorized user; private data set"""
        exp = "exp.auth_find_3"
        self.auth_find(self.unauth_user, self.PrivPub, exp)

    # | find | Unauth | None | PASS |
    def test_auth_find_4(self):
        """Test find method with unauthorized user; no data sets specified"""
        exp = "exp.auth_find_4"
        self.auth_find(self.unauth_user, None, exp)

    # | find | Anon | Priv,Pub | FAIL |
    def test_auth_find_5(self):
        """Test find method with anonymous user; private data set
        specified"""
        exp = "exp.auth_find_5"
        self.auth_find(None, self.PrivPub, exp)

    # | find | Anon | None | PASS |
    def test_auth_find_6(self):
        """Test find method with anonymous user; no data sets specified"""
        exp = "exp.auth_find_6"
        self.auth_find(None, None, exp)

    # | retrieve | Auth | Priv,Pub | PASS |
    # @skip("Does not return Priv")  # @@@
    def test_auth_retrieve_1(self):
        """Retrieve method with authorized user; private data set specified"""
        exp = "exp.auth_retrieve_1"
        self.auth_retrieve(self.auth_user, self.PrivPub, exp)

    # | retrieve | Auth | None | PASS |
    # @skip("Does not return Priv")  # @@@
    def test_auth_retrieve_2(self):
        """Retrieve method with authorized user; no data sets specified.
        Should include Authorized Private DR"""
        exp = "exp.auth_retrieve_2"
        self.auth_retrieve(self.auth_user, None, exp)

    # | retrieve | Unauth | Priv,Pub | FAIL|
    def test_auth_retrieve_3(self):
        """Retrieve method with unauthorized user; private dataset specified"""
        exp = "exp.auth_retrieve_3"
        self.auth_retrieve(self.unauth_user, self.PrivPub, exp)

    # | retrieve | Unauth | None | PASS |
    # Should PASS since default (no data sets) means only
    # retrieve from authorized datasets (Public, in this case)
    def test_auth_retrieve_4(self):
        """Retrieve method with unauthorized user; no datasets specified"""
        warnings.filterwarnings("ignore")
        exp = "exp.auth_retrieve_4"
        self.auth_retrieve(self.unauth_user, None, exp)

    # | retrieve | Unauth | Pub | PASS |
    def test_auth_retrieve_5(self):
        """Retrieve method with unauthorized user; public datasets specified"""
        warnings.filterwarnings("ignore")
        exp = "exp.auth_retrieve_5"
        self.auth_retrieve(self.unauth_user, self.Pub, exp)

    # | retrieve | Anon | Priv,Pub | FAIL |
    def test_auth_retrieve_6(self):
        """Retrieve method with anonymous user; private data set specified"""
        self.silent_logout()
        exp = "exp.auth_retrieve_6"
        self.auth_retrieve(None, self.PrivPub, exp)
        #!# Replace exception name below once real one is created

    # | retrieve | Anon | None | PASS |
    # Should PASS since default (no data sets) means only
    # retrieve from authorized datasets (Public, in this case)
    def test_auth_retrieve_7(self):
        """Retrieve method with anonymous user; no data sets specified"""
        warnings.filterwarnings("ignore")
        exp = "exp.auth_retrieve_7"
        self.auth_retrieve(None, None, exp)

    # | retrieve | Anon | Pub | PASS |
    def test_auth_retrieve_8(self):
        """Retrieve method with anonymous user; public data sets specified"""
        warnings.filterwarnings("ignore")
        exp = "exp.auth_retrieve_8"
        self.auth_retrieve(None, self.Pub, exp)
