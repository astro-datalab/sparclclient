#! /usr/bin/env python
#
# Unit tests for the notebook SPARCL_client_method_tests.ipynb
#
# Created by nb2test.py from SPARCL_client_method_tests.ipynb
#
# To run tests:
#   python -m unittest methods_tests.py
#
###############################################################################

# START Pre-notebook code

import unittest

#! from unittest import skip

# END Pre-notebook code

###########################################################################
# Notebook combined into one function per Section
#


# NoSection
__author__ = "Alice Jacques <alice.jacques@noirlab.edu>"
__version__ = "20230608"  # yyyymmdd;
__datasets__ = ["sdss_dr16", "boss_dr16", "desi_edr"]
#!pip install sparclclient==1.2.0b4
# SPARCL imports
from sparcl.client import SparclClient

# 3rd party imports
#! from time import time

# Data Lab imports
# from dl import queryClient as qc
# from dl import authClient as ac
# from getpass import getpass
client = SparclClient(url="https://sparc1.datalab.noirlab.edu")
client


def get_all_fields():
    global client, ids_any, ids_boss, ids_desi, ids_lots, ids_sdss
    global outs, some_missing_ids, some_missing_specids, specids_any
    global specids_boss, specids_desi, specids_lots, specids_sdss
    #! client.get_all_fields?
    # Get all fields common to all datasets
    print(client.get_all_fields())


def get_all_fields_dataset_list():
    global client, ids_any, ids_boss, ids_desi, ids_lots, ids_sdss, outs
    global some_missing_ids, some_missing_specids, specids_any, specids_boss
    global specids_desi, specids_lots, specids_sdss
    # Get all fields in SDSS-DR16
    print(client.get_all_fields(dataset_list=["SDSS-DR16"]))
    # Get all fields in BOSS-DR16
    print(client.get_all_fields(dataset_list=["BOSS-DR16"]))
    # Get all fields in DESI-EDR
    print(client.get_all_fields(dataset_list=["DESI-EDR"]))
    # Get all fields common to both SDSS-DR16 and DESI-EDR
    print(client.get_all_fields(dataset_list=["SDSS-DR16", "DESI-EDR"]))


def get_default_fields():
    global client, ids_any, ids_boss, ids_desi, ids_lots, ids_sdss, outs
    global some_missing_ids, some_missing_specids, specids_any, specids_boss
    global specids_desi, specids_lots, specids_sdss
    #! client.get_default_fields?
    # Get default fields common to all datasets
    print(client.get_default_fields())


def get_default_fields_dataset_list():
    global client, ids_any, ids_boss, ids_desi, ids_lots, ids_sdss, outs
    global some_missing_ids, some_missing_specids, specids_any, specids_boss
    global specids_desi, specids_lots, specids_sdss
    # Get default fields in SDSS-DR16
    print(client.get_default_fields(dataset_list=["SDSS-DR16"]))
    # Get default fields in BOSS-DR16
    print(client.get_default_fields(dataset_list=["BOSS-DR16"]))
    # Get default fields in DESI-EDR
    print(client.get_default_fields(dataset_list=["DESI-EDR"]))
    # Get default fields common to both SDSS-DR16 and DESI-EDR
    print(client.get_default_fields(dataset_list=["SDSS-DR16", "DESI-EDR"]))


def get_available_fields():
    global client, ids_any, ids_boss, ids_desi, ids_lots, ids_sdss, outs
    global some_missing_ids, some_missing_specids, specids_any, specids_boss
    global specids_desi, specids_lots, specids_sdss

    #! client.get_available_fields?
    # Get available fields common to all datasets
    print(client.get_available_fields())


def get_available_fields_dataset_list():
    global client, ids_any, ids_boss, ids_desi, ids_lots, ids_sdss, outs
    global some_missing_ids, some_missing_specids, specids_any, specids_boss
    global specids_desi, specids_lots, specids_sdss

    # Get available fields in SDSS-DR16
    print(client.get_available_fields(dataset_list=["SDSS-DR16"]))
    # Get available fields in BOSS-DR16
    print(client.get_available_fields(dataset_list=["BOSS-DR16"]))
    # Get available fields in DESI-EDR
    print(client.get_available_fields(dataset_list=["DESI-EDR"]))
    # Get available fields common to both SDSS-DR16 and DESI-EDR
    print(client.get_available_fields(dataset_list=["SDSS-DR16", "DESI-EDR"]))


def find():
    global client, ids_any, ids_boss, ids_desi, ids_lots, ids_sdss, outs
    global some_missing_ids, some_missing_specids, specids_any, specids_boss
    global specids_desi, specids_lots, specids_sdss
    #! client.find?
    outs = [
        "data_release",
        "datasetgroup",
        "dateobs_center",
        "dec",
        "exptime",
        "sparcl_id",
        "instrument",
        "ra",
        "redshift",
        "redshift_err",
        "redshift_warning",
        "site",
        "specid",
        "specprimary",
        "spectype",
        "targetid",
        "telescope",
        "wavemax",
        "wavemin",
    ]


def find_limit():
    global client, ids_any, ids_boss, ids_desi, ids_lots, ids_sdss, outs
    global some_missing_ids, some_missing_specids, specids_any, specids_boss
    global specids_desi, specids_lots, specids_sdss
    #! # does the default limit work?
    client.find()
    #! # does setting a limit less than the default value work?
    client.find(limit=2)
    # does setting a limit over the default value but under
    #! # the maximum value work?
    client.find(limit=800)
    #! # does setting the limit to None work?
    client.find(limit=None)


def find_constraints():  # noqa: C901
    global client, ids_any, ids_boss, ids_desi, ids_lots, ids_sdss, outs
    global some_missing_ids, some_missing_specids, specids_any, specids_boss
    global specids_desi, specids_lots, specids_sdss
    # No constraints passed

    found = client.find(outfields=outs, limit=10)
    print(f"# records found: {len(found.records)}")
    print(f"Datasets found: {set([f['data_release'] for f in found.records])}")
    print(f"First record: {found.records[0]}")
    # No outfields passed

    cons = {
        "data_release": ["SDSS-DR16"],
        "dec": [4, 29],
        "exptime": [2000, 12000],
        "ra": [80, 136],
        "redshift": [2, 5],
    }

    found = client.find(constraints=cons, limit=10)
    print(f"# records found: {len(found.records)}")
    print(f"First record: {found.records[0]}")
    # Invalid constraint value: data_release

    cons = {"data_release": [{"poppy"}]}

    try:
        found = client.find(outfields=outs, constraints=cons, limit=10)
    except Exception as e:
        print(e)
    # Invalid constraint value: datasetgroup

    cons = {"datasetgroup": [{"daffodil"}]}

    try:
        found = client.find(outfields=outs, constraints=cons, limit=10)
    except Exception as e:
        print(e)
    # Invalid constraint value: dateobs_center

    cons = {"dateobs_center": ["2011-12-21 12:00"]}

    try:
        found = client.find(outfields=outs, constraints=cons, limit=10)
    except Exception as e:
        print(e)
    # Invalid constraint value: dec

    cons = {"dec": [29]}

    try:
        found = client.find(outfields=outs, constraints=cons, limit=10)
    except Exception as e:
        print(e)
    # Invalid constraint value: exptime

    cons = {"exptime": [30]}

    try:
        found = client.find(outfields=outs, constraints=cons, limit=10)
    except Exception as e:
        print(e)
    # Invalid constraint value: instrument

    cons = {"instrument": [{"hyacinth"}]}

    try:
        found = client.find(outfields=outs, constraints=cons, limit=10)
    except Exception as e:
        print(e)
    # Invalid constraint value: ra

    cons = {"ra": [80]}

    try:
        found = client.find(outfields=outs, constraints=cons, limit=10)
    except Exception as e:
        print(e)
    # Invalid constraint value: redshift

    cons = {"redshift": [1]}

    try:
        found = client.find(outfields=outs, constraints=cons, limit=10)
    except Exception as e:
        print(e)
    # Invalid constraint value: redshift_err

    cons = {"redshift_err": [0.0001]}

    try:
        found = client.find(outfields=outs, constraints=cons, limit=10)
    except Exception as e:
        print(e)
    # Invalid constraint value: redshift_warning

    cons = {"redshift_warning": ["magnolia"]}

    try:
        found = client.find(outfields=outs, constraints=cons, limit=10)
    except Exception as e:
        print(e)
    # Invalid constraint value: site

    cons = {"site": [{"lotus"}]}

    try:
        found = client.find(outfields=outs, constraints=cons, limit=10)
    except Exception as e:
        print(e)
    # Invalid constraint value: specprimary

    cons = {"specprimary": ["chrysanthemum"]}

    try:
        found = client.find(outfields=outs, constraints=cons, limit=10)
    except Exception as e:
        print(e)
    # Invalid constraint value: spectype

    cons = {"spectype": [{"tulip"}]}

    try:
        found = client.find(outfields=outs, constraints=cons, limit=10)
    except Exception as e:
        print(e)
    # Invalid constraint value: telescope

    cons = {"telescope": [{"carnation"}]}

    try:
        found = client.find(outfields=outs, constraints=cons, limit=10)
    except Exception as e:
        print(e)
    # Invalid constraint value: wavemax

    cons = {"wavemax": [10500]}

    try:
        found = client.find(outfields=outs, constraints=cons, limit=10)
    except Exception as e:
        print(e)
    # Invalid constraint value: wavemin

    cons = {"wavemin": [3800]}

    try:
        found = client.find(outfields=outs, constraints=cons, limit=10)
    except Exception as e:
        print(e)
    # Test all possible constraint fields with specified constraint values,
    # SDSS-DR16 only

    cons = {
        "data_release": ["SDSS-DR16"],
        "datasetgroup": ["SDSS_BOSS"],
        "dateobs_center": ["2003-11-21 00:00", "2011-12-21 00:00"],
        "dec": [4, 29],
        "exptime": [2000, 12000],
        "instrument": ["SDSS", "BOSS"],
        "ra": [80, 136],
        "redshift": [2, 5],
        "redshift_err": [0.0001, 0.001],
        "redshift_warning": [0, 3, 5],
        "site": ["apo"],
        "specprimary": [1],
        "spectype": ["QSO", "GALAXY"],
        "telescope": ["sloan25m"],
        "wavemax": [9210, 10500],
        "wavemin": [3800, 3900],
    }

    found = client.find(outfields=outs, constraints=cons, limit=10)
    print(f"# records found: {len(found.records)}")
    print(f"Datasets found: {set([f['data_release'] for f in found.records])}")
    print(f"First record: {found.records[0]}")
    # Test all possible constraint fields with specified constraint values,
    # BOSS-DR16 only

    cons = {
        "data_release": ["BOSS-DR16"],
        "datasetgroup": ["SDSS_BOSS"],
        "dateobs_center": [
            "2018-10-07 08:44:43+00:00",
            "2018-10-07 08:44:43+00:00",
        ],
        "dec": [4, 20],
        "exptime": [2000, 12000],
        "instrument": ["SDSS", "BOSS"],
        "ra": [20, 150],
        "redshift": [0, 3],
        "redshift_err": [0.0001, 0.002],
        "redshift_warning": [0],
        "site": ["apo"],
        "specprimary": [1],
        "spectype": ["QSO", "GALAXY"],
        "telescope": ["sloan25m"],
        "wavemax": [9210, 10500],
        "wavemin": [3200, 3900],
    }

    found = client.find(outfields=outs, constraints=cons, limit=10)
    print(f"# records found: {len(found.records)}")
    print(f"Datasets found: {set([f['data_release'] for f in found.records])}")
    print(f"First record: {found.records[0]}")
    # Test constraint fields with specified constraint values,
    # DESI-EDR only

    cons = {
        "data_release": ["DESI-EDR"],
        "dec": [1, 90],
        "exptime": [2000, 2500],
        "instrument": ["DESI"],
        "ra": [50, 190],
        "redshift": [1, 1.7],
        "redshift_err": [0.00006, 0.001],
        "redshift_warning": [0, 5],
        "site": ["kpno"],
        "specprimary": [1],
        "spectype": ["GALAXY", "STAR"],
        "telescope": ["kp4m"],
        "wavemax": [9700, 9900],
        "wavemin": [3500, 3700],
    }

    found = client.find(outfields=outs, constraints=cons, limit=10)
    print(f"# records found: {len(found.records)}")
    print(f"Datasets found: {set([f['data_release'] for f in found.records])}")
    print(f"First record: {found.records[0]}")
    # Test constraint fields with specified constraint values,
    # all datasets

    cons = {
        "data_release": ["BOSS-DR16", "SDSS-DR16", "DESI-EDR"],
        "datasetgroup": ["SDSS_BOSS", "DESI"],
        "dec": [4, 29],
        "exptime": [2000, 12000],
        "instrument": ["SDSS", "BOSS", "DESI"],
        "ra": [80, 136],
        "redshift": [2, 5],
        "redshift_err": [0.0001, 0.001],
        "redshift_warning": [0, 3, 5],
        "site": ["apo", "kpno"],
        "specprimary": [1],
        "spectype": ["QSO", "GALAXY"],
        "telescope": ["sloan25m", "kp4m"],
    }

    found = client.find(outfields=outs, constraints=cons, limit=50)
    print(f"# records found: {len(found.records)}")
    print(f"Datasets found: {set([f['data_release'] for f in found.records])}")
    print(f"First record: {found.records[0]}")
    # Test combo of constraint fields with specified constraint values:
    # datasetgroup, redshift, specprimary, redshift_warning, spectype

    cons = {
        "datasetgroup": ["SDSS_BOSS"],
        "redshift": [0, 0.2],
        "specprimary": [1],
        "redshift_warning": [0],
        "spectype": ["STAR"],
    }

    found = client.find(outfields=outs, constraints=cons, limit=10)
    print(f"# records found: {len(found.records)}")
    print(f"Datasets found: {set([f['data_release'] for f in found.records])}")
    print(f"First record: {found.records[0]}")
    # Test combo of constraint fields with specified constraint values:
    # datasetgroup, exptime, redshift_warning

    cons = {
        "datasetgroup": ["DESI"],
        "exptime": [1000.2, 1050.9],
        "redshift_warning": [4],
    }

    found = client.find(outfields=outs, constraints=cons, limit=10)
    print(f"# records found: {len(found.records)}")
    print(f"Datasets found: {set([f['data_release'] for f in found.records])}")
    print(f"First record: {found.records[0]}")
    # Test instrument and telescope constraint fields, SDSS-DR16 only

    cons = {"instrument": ["SDSS"], "telescope": ["sloan25m"]}

    found = client.find(outfields=outs, constraints=cons, limit=10)
    print(f"# records found: {len(found.records)}")
    print(f"Datasets found: {set([f['data_release'] for f in found.records])}")
    print(f"First record: {found.records[0]}")
    # Test instrument and telescope constraint fields, BOSS-DR16 only

    cons = {"instrument": ["BOSS"], "telescope": ["sloan25m"]}

    found = client.find(outfields=outs, constraints=cons, limit=10)
    print(f"# records found: {len(found.records)}")
    print(f"Datasets found: {set([f['data_release'] for f in found.records])}")
    print(f"First record: {found.records[0]}")
    # Test instrument and telescope constraint fields, DESI-EDR only

    cons = {"instrument": ["DESI"], "telescope": ["kp4m"]}

    found = client.find(outfields=outs, constraints=cons, limit=10)
    print(f"# records found: {len(found.records)}")
    print(f"Datasets found: {set([f['data_release'] for f in found.records])}")
    print(f"First record: {found.records[0]}")
    # Test combo of constraint fields with specified constraint values:
    # site, specprimary, spectype

    cons = {"site": ["apo"], "specprimary": [1], "spectype": ["STAR"]}

    found = client.find(outfields=outs, constraints=cons, limit=10)
    print(f"# records found: {len(found.records)}")
    print(f"Datasets found: {set([f['data_release'] for f in found.records])}")
    print(f"First record: {found.records[0]}")
    # Test combo of constraint fields with specified constraint values:
    # site, specprimary, exptime

    cons = {"site": ["kpno"], "specprimary": [1], "exptime": [3000, 3010]}

    found = client.find(outfields=outs, constraints=cons, limit=10)
    print(f"# records found: {len(found.records)}")
    print(f"Datasets found: {set([f['data_release'] for f in found.records])}")
    print(f"First record: {found.records[0]}")


def find_outfields():
    global client, ids_any, ids_boss, ids_desi, ids_lots, ids_sdss, outs
    global some_missing_ids, some_missing_specids, specids_any, specids_boss
    global specids_desi, specids_lots, specids_sdss
    # No constraints passed, no limit passed

    found = client.find(outfields=outs)
    print(f"# records found: {len(found.records)}")
    print(f"Datasets found: {set([f['data_release'] for f in found.records])}")
    print(f"First record: {found.records[0]}")
    # AUX field in only SDSS-DR16 and BOSS-DR16
    found = client.find(outfields=["run2d", "data_release"])
    print(f"# records found: {len(found.records)}")
    print(f"Datasets found: {set([f['data_release'] for f in found.records])}")
    print(f"First record: {found.records[0]}")
    # AUX field in only DESI-EDR
    found = client.find(outfields=["healpix", "data_release"])
    print(f"# records found: {len(found.records)}")
    print(f"Datasets found: {set([f['data_release'] for f in found.records])}")
    print(f"First record: {found.records[0]}")
    # AUX field in all datasets
    found = client.find(outfields=["survey", "data_release"])
    print(f"# records found: {len(found.records)}")
    print(f"Datasets found: {set([f['data_release'] for f in found.records])}")
    print(f"First record: {found.records[0]}")
    # Field does not exist in any dataset
    found = client.find(outfields=["petunia"])
    print(f"# records found: {len(found.records)}")
    print(f"First record: {found.records[0]}")
    # Field exists in at least one dataset
    found = client.find(outfields=["fiberid", "data_release"])
    print(f"# records found: {len(found.records)}")
    print(f"Datasets found: {set([f['data_release'] for f in found.records])}")
    print(f"First record: {found.records[0]}")
    # One field exists in at least one dataset, another field does not exist
    # in any datasets
    found = client.find(outfields=["plate", "dahlia", "data_release"])
    print(f"# records found: {len(found.records)}")
    print(f"Datasets found: {set([f['data_release'] for f in found.records])}")
    print(f"First record: {found.records[0]}")
    # A field does not exist in the specified data_release
    try:
        found = client.find(
            outfields=["location", "data_release"],
            constraints={"data_release": ["SDSS-DR16"]},
        )
        print(f"# records found: {len(found.records)}")
        print(
            f"Datasets found: "
            "{set([f['data_release'] for f in found.records])}"
        )
        print(f"First record: {found.records[0]}")
    except Exception as e:
        print(e)
    # A field exists in only one of the specified data_releases
    found = client.find(
        outfields=["sv_primary", "data_release"],
        constraints={"data_release": ["SDSS-DR16", "DESI-EDR"]},
    )
    print(f"# records found: {len(found.records)}")
    print(f"Datasets found: {set([f['data_release'] for f in found.records])}")
    print(f"First record: {found.records[0]}")


def find_sort():
    global client, ids_any, ids_boss, ids_desi, ids_lots, ids_sdss, outs
    global some_missing_ids, some_missing_specids, specids_any, specids_boss
    global specids_desi, specids_lots, specids_sdss

    def sortby(sort_field, cons={}, lim=500):
        found = client.find(
            outfields=outs, constraints=cons, sort=f"{sort_field}", limit=lim
        )
        print(f"Records found: {len(found.records)}")
        print(
            f"Datasets found: "
            "{set([f['data_release'] for f in found.records])}\n"
        )
        print(f"First record: {found.records[0]}\n")
        print(f"{sort_field} in first 5 records:")
        for i in range(5):
            print(found.records[i][sort_field])
        print(f"\n{sort_field} in last 5 records:")
        for i in range(495, 500):
            print(found.records[i][sort_field])

    sortby(
        "dateobs_center",
        cons={
            "dateobs_center": ["2000-05-02T23:59:59Z", "2000-08-07T03:47:16Z"]
        },
    )
    sortby("dec", cons={"dec": [4, 4.3]})
    sortby("exptime")
    sortby("ra", cons={"ra": [3, 3.3]})
    sortby("redshift", cons={"redshift": [0.9, 0.91]})
    sortby("redshift_err", cons={"redshift_err": [10.0, 20.0]})
    sortby("redshift_warning", cons={"redshift_warning": [1, 3, 5]})
    found = client.find(outfields=outs, sort="id")
    print(f"# records found: {len(found.records)}")
    print(
        f"Datasets found: {set([f['data_release'] for f in found.records])}\n"
    )
    print(f"First record: {found.records[0]}\n")
    print("sparcl_id in first 5 records:")
    for i in range(5):
        print(found.records[i].sparcl_id)
    print("\nsparcl_id in last 5 records:")
    for i in range(495, 500):
        print(found.records[i].sparcl_id)
    sortby("specid", cons={"data_release": ["DESI-EDR"]})
    sortby(
        "specprimary",
        cons={"data_release": ["BOSS-DR16", "DESI-EDR"]},
        lim=1000,
    )
    sortby("spectype")
    sortby("targetid", cons={"data_release": ["DESI-EDR"]})
    sortby("wavemax", cons={"wavemax": [10, 10000]})
    sortby(
        "wavemin",
        cons={
            "data_release": ["SDSS-DR16", "BOSS-DR16"],
            "wavemin": [1, 5000],
        },
    )
    print("\n###################### UNSORTED ######################\n")
    found = client.find(
        outfields=outs, constraints={"ra": [1, 200], "dec": [0, 80]}
    )
    print(f"Records found: {len(found.records)}")
    print(
        f"Datasets found: {set([f['data_release'] for f in found.records])}\n"
    )
    print(f"First record: {found.records[0]}\n")
    print(f"ra, dec in first 5 records:")
    for i in range(5):
        print(f"{found.records[i]['ra']}, {found.records[i]['dec']}")
    print(f"\nra, dec in last 5 records:")
    for i in range(495, 500):
        print(f"{found.records[i]['ra']}, {found.records[i]['dec']}")

    print("\n###################### SORTED ######################\n")
    found = client.find(
        outfields=outs,
        constraints={"ra": [1, 200], "dec": [0, 80]},
        sort="ra,dec",
    )
    print(f"Records found: {len(found.records)}")
    print(
        f"Datasets found: {set([f['data_release'] for f in found.records])}\n"
    )
    print(f"First record: {found.records[0]}\n")
    print(f"ra, dec in first 5 records:")
    for i in range(5):
        print(f"{found.records[i]['ra']}, {found.records[i]['dec']}")
    print(f"\nra, dec in last 5 records:")
    for i in range(495, 500):
        print(f"{found.records[i]['ra']}, {found.records[i]['dec']}")


def retrieve():
    global client, ids_any, ids_boss, ids_desi, ids_lots, ids_sdss, outs
    global some_missing_ids, some_missing_specids, specids_any, specids_boss
    global specids_desi, specids_lots, specids_sdss

    #! client.retrieve?
    ids_lots = client.find(limit=60000).ids
    # ids from SDSS-DR16 only
    ids_sdss = client.find(
        outfields=["sparcl_id"],
        constraints={"data_release": ["SDSS-DR16"]},
        limit=3,
    ).ids

    # ids from BOSS-DR16 only
    ids_boss = client.find(
        outfields=["sparcl_id"],
        constraints={"data_release": ["BOSS-DR16"]},
        limit=3,
    ).ids

    # ids from DESI-EDR only
    ids_desi = client.find(
        outfields=["sparcl_id"],
        constraints={"data_release": ["DESI-EDR"]},
        limit=3,
    ).ids

    # ids from any dataset
    ids_any = ids_sdss + ids_boss + ids_desi


def retrieve_limit():
    global client, ids_any, ids_boss, ids_desi, ids_lots, ids_sdss, outs
    global some_missing_ids, some_missing_specids, specids_any, specids_boss
    global specids_desi, specids_lots, specids_sdss

    #! # does the default limit work?
    client.retrieve(uuid_list=ids_lots)
    #! # does setting a limit less than the default value work?
    client.retrieve(uuid_list=ids_lots, limit=2)
    # does setting a limit over the default value but under
    #! # the maximum value work?
    client.retrieve(uuid_list=ids_lots, limit=800)
    # does trying to retrieve more than the maximum allowed
    #! # by setting limit=30000 produce the right error message?
    try:
        client.retrieve(uuid_list=ids_lots, limit=30000)
    except Exception as e:
        print(e)
    # does trying to retrieve more than the maximum allowed
    #! # by setting limit=None produce the right error message?
    try:
        client.retrieve(uuid_list=ids_lots, limit=None)
    except Exception as e:
        print(e)


def retrieve_dataset_list():
    global client, ids_any, ids_boss, ids_desi, ids_lots, ids_sdss, outs
    global some_missing_ids, some_missing_specids, specids_any, specids_boss
    global specids_desi, specids_lots, specids_sdss

    # Retrieve from all datasets (dataset_list=None, the default)
    r = client.retrieve(uuid_list=ids_any, include=["data_release"])
    set([f["data_release"] for f in r.records])
    # Retrieve from only SDSS-DR16 (should get a warning about missing ids)
    r = client.retrieve(
        uuid_list=ids_any, include=["data_release"], dataset_list=["SDSS-DR16"]
    )
    set([f["data_release"] for f in r.records])
    # Retrieve from only BOSS-DR16 (should get a warning about missing ids)
    r = client.retrieve(
        uuid_list=ids_any, include=["data_release"], dataset_list=["BOSS-DR16"]
    )
    set([f["data_release"] for f in r.records])
    # Retrieve from only DESI-EDR (should get a warning about missing ids)
    r = client.retrieve(
        uuid_list=ids_any, include=["data_release"], dataset_list=["DESI-EDR"]
    )
    set([f["data_release"] for f in r.records])
    # Retrieve from only SDSS-DR16 and DESI-EDR
    # (should get a warning about missing ids)
    r = client.retrieve(
        uuid_list=ids_any,
        include=["data_release"],
        dataset_list=["SDSS-DR16", "DESI-EDR"],
    )
    set([f["data_release"] for f in r.records])


def retrieve_include():
    global client, ids_any, ids_boss, ids_desi, ids_lots, ids_sdss, outs
    global some_missing_ids, some_missing_specids, specids_any, specids_boss
    global specids_desi, specids_lots, specids_sdss

    # include only default fields common to all datasets
    r = client.retrieve(uuid_list=ids_any, include="DEFAULT")
    print([set(r.records[i].keys()) for i in range(len(r.records))][0])
    # include all fields common to all datasets
    r = client.retrieve(uuid_list=ids_any, include="ALL")
    print([set(r.records[i].keys()) for i in range(len(r.records))][0])
    # include all fields in SDSS-DR16 only
    # (should get a warning about missing ids)
    r = client.retrieve(
        uuid_list=ids_any, include="ALL", dataset_list=["SDSS-DR16"]
    )
    print([set(r.records[i].keys()) for i in range(len(r.records))][0])
    # include all fields in BOSS-DR16 only
    # (should get a warning about missing ids)
    r = client.retrieve(
        uuid_list=ids_any, include="ALL", dataset_list=["BOSS-DR16"]
    )
    print([set(r.records[i].keys()) for i in range(len(r.records))][0])
    # include all fields in DESI-EDR only
    # (should get a warning about missing ids)
    r = client.retrieve(
        uuid_list=ids_any, include="ALL", dataset_list=["DESI-EDR"]
    )
    print([set(r.records[i].keys()) for i in range(len(r.records))][0])
    # include all fields in SDSS-DR16 and DESI-EDR only
    # (should get a warning about missing ids)
    r = client.retrieve(
        uuid_list=ids_any,
        include="ALL",
        dataset_list=["SDSS-DR16", "DESI-EDR"],
    )
    print([set(r.records[i].keys()) for i in range(len(r.records))][0])
    # include only specified fields
    r = client.retrieve(
        uuid_list=ids_any, include=["sparcl_id", "flux", "redshift"]
    )
    print([set(r.records[i].keys()) for i in range(len(r.records))][0])
    # include aux fields in SDSS-DR16 only
    r = client.retrieve(
        uuid_list=ids_sdss,
        include=["run2d", "primtarget"],
        dataset_list=["SDSS-DR16"],
    )
    print([set(r.records[i].keys()) for i in range(len(r.records))][0])
    # include aux fields in BOSS-DR16 only
    r = client.retrieve(
        uuid_list=ids_boss,
        include=["fiberid", "mjd"],
        dataset_list=["BOSS-DR16"],
    )
    print([set(r.records[i].keys()) for i in range(len(r.records))][0])
    # include aux fields in BOSS-DR16 only
    r = client.retrieve(
        uuid_list=ids_any,
        include=["fiberid", "mjd"],
        dataset_list=["BOSS-DR16"],
    )
    print([set(r.records[i].keys()) for i in range(len(r.records))][0])
    # include aux fields in DESI-EDR only
    r = client.retrieve(
        uuid_list=ids_desi,
        include=["survey", "sv_primary"],
        dataset_list=["DESI-EDR"],
    )
    print([set(r.records[i].keys()) for i in range(len(r.records))][0])
    # try to include fields that do not exist in the DB
    try:
        r = client.retrieve(
            uuid_list=ids_any, include=["sparcl_id", "magnolia"]
        )
        print([set(r.records[i].keys()) for i in range(len(r.records))][0])
    except Exception as e:
        print(e)


def retrieve_by_specid():
    global client, ids_any, ids_boss, ids_desi, ids_lots, ids_sdss, outs
    global some_missing_ids, some_missing_specids, specids_any, specids_boss
    global specids_desi, specids_lots, specids_sdss

    #! client.retrieve_by_specid?
    found_specids = client.find(outfields=["specid"], limit=60000)
    specids_lots = [f["specid"] for f in found_specids.records]
    # specids from SDSS-DR16 only
    found_sdss = client.find(
        outfields=["specid"],
        constraints={"data_release": ["SDSS-DR16"]},
        limit=3,
    )
    specids_sdss = [f["specid"] for f in found_sdss.records]

    # specids from BOSS-DR16 only
    found_boss = client.find(
        outfields=["specid"],
        constraints={"data_release": ["BOSS-DR16"]},
        limit=3,
    )
    specids_boss = [f["specid"] for f in found_boss.records]

    # specids from DESI-EDR only
    found_desi = client.find(
        outfields=["specid"],
        constraints={"data_release": ["DESI-EDR"]},
        limit=3,
    )
    specids_desi = [f["specid"] for f in found_desi.records]

    # specids from any dataset
    specids_any = specids_sdss + specids_boss + specids_desi


def retrieve_by_specid_limit():
    global client, ids_any, ids_boss, ids_desi, ids_lots, ids_sdss, outs
    global some_missing_ids, some_missing_specids, specids_any, specids_boss
    global specids_desi, specids_lots, specids_sdss

    #! # does the default limit work?
    client.retrieve_by_specid(specid_list=specids_lots)
    #! # does setting a limit less than the default value work?
    client.retrieve_by_specid(specid_list=specids_lots, limit=2)
    # does setting a limit over the default value but under
    #! # the maximum value work?
    client.retrieve_by_specid(specid_list=specids_lots, limit=800)
    # does trying to retrieve more than the maximum allowed
    #! # by setting limit=30000 produce the right error message?
    try:
        client.retrieve_by_specid(specid_list=specids_lots, limit=30000)
    except Exception as e:
        print(e)
    # does trying to retrieve more than the maximum allowed
    #! # by setting limit=None produce the right error message?
    try:
        client.retrieve_by_specid(specid_list=specids_lots, limit=None)
    except Exception as e:
        print(e)


def retrieve_by_specid_dataset_list():
    global client, ids_any, ids_boss, ids_desi, ids_lots, ids_sdss, outs
    global some_missing_ids, some_missing_specids, specids_any, specids_boss
    global specids_desi, specids_lots, specids_sdss

    # Retrieve from all datasets (dataset_list=None, the default)
    r = client.retrieve_by_specid(
        specid_list=specids_any, include=["data_release"]
    )
    set([f["data_release"] for f in r.records])
    # Retrieve from only SDSS-DR16
    r = client.retrieve_by_specid(
        specid_list=specids_any,
        include=["data_release"],
        dataset_list=["SDSS-DR16"],
    )
    set([f["data_release"] for f in r.records])
    # Retrieve from only BOSS-DR16
    r = client.retrieve_by_specid(
        specid_list=specids_any,
        include=["data_release"],
        dataset_list=["BOSS-DR16"],
    )
    set([f["data_release"] for f in r.records])
    # Retrieve from only DESI-EDR
    r = client.retrieve_by_specid(
        specid_list=specids_any,
        include=["data_release"],
        dataset_list=["DESI-EDR"],
    )
    set([f["data_release"] for f in r.records])
    # Retrieve from only SDSS-DR16 and DESI-EDR
    r = client.retrieve_by_specid(
        specid_list=specids_any,
        include=["data_release"],
        dataset_list=["SDSS-DR16", "DESI-EDR"],
    )
    set([f["data_release"] for f in r.records])


def retrieve_by_specid_include():
    global client, ids_any, ids_boss, ids_desi, ids_lots, ids_sdss, outs
    global some_missing_ids, some_missing_specids, specids_any, specids_boss
    global specids_desi, specids_lots, specids_sdss

    # include only default fields common to all datasets
    r = client.retrieve_by_specid(specid_list=specids_any, include="DEFAULT")
    print([set(r.records[i].keys()) for i in range(len(r.records))][0])
    # include all fields common to all datasets
    r = client.retrieve_by_specid(specid_list=specids_any, include="ALL")
    print([set(r.records[i].keys()) for i in range(len(r.records))][0])
    # include all fields in SDSS-DR16 only
    r = client.retrieve_by_specid(
        specid_list=specids_any, include="ALL", dataset_list=["SDSS-DR16"]
    )
    print([set(r.records[i].keys()) for i in range(len(r.records))][0])
    # include all fields in BOSS-DR16 only
    r = client.retrieve_by_specid(
        specid_list=specids_any, include="ALL", dataset_list=["BOSS-DR16"]
    )
    print([set(r.records[i].keys()) for i in range(len(r.records))][0])
    # include all fields in DESI-EDR only
    r = client.retrieve_by_specid(
        specid_list=specids_any, include="ALL", dataset_list=["DESI-EDR"]
    )
    print([set(r.records[i].keys()) for i in range(len(r.records))][0])
    # include all fields in SDSS-DR16 and DESI-EDR only
    r = client.retrieve_by_specid(
        specid_list=specids_any,
        include="ALL",
        dataset_list=["SDSS-DR16", "DESI-EDR"],
    )
    print([set(r.records[i].keys()) for i in range(len(r.records))][0])
    # include only specified fields
    r = client.retrieve_by_specid(
        specid_list=specids_any, include=["sparcl_id", "flux", "redshift"]
    )
    print([set(r.records[i].keys()) for i in range(len(r.records))][0])
    # include aux fields in SDSS-DR16 only
    r = client.retrieve_by_specid(
        specid_list=specids_sdss,
        include=["vdisp", "run2d"],
        dataset_list=["SDSS-DR16"],
    )
    print([set(r.records[i].keys()) for i in range(len(r.records))][0])
    # include aux fields in BOSS-DR16 only
    r = client.retrieve_by_specid(
        specid_list=specids_boss,
        include=["fiberid", "mjd"],
        dataset_list=["BOSS-DR16"],
    )
    print([set(r.records[i].keys()) for i in range(len(r.records))][0])
    # include aux fields in DESI-EDR only
    r = client.retrieve_by_specid(
        specid_list=specids_desi,
        include=["survey", "sv_primary"],
        dataset_list=["DESI-EDR"],
    )
    print([set(r.records[i].keys()) for i in range(len(r.records))][0])
    # try to include fields that do not exist in the DB
    try:
        r = client.retrieve_by_specid(
            specid_list=specids_any, include=["sparcl_id", "marigold"]
        )
        print([set(r.records[i].keys()) for i in range(len(r.records))][0])
    except Exception as e:
        print(e)


def missing():
    global client, ids_any, ids_boss, ids_desi, ids_lots, ids_sdss, outs
    global some_missing_ids, some_missing_specids, specids_any, specids_boss
    global specids_desi, specids_lots, specids_sdss

    #! client.missing?
    some_missing_ids = ids_any + [
        "00009f84-8acc-425b-87e1-0a819f11697c",
        "00002f94-96b1-4f2d-8d1d-1a47a89fe105",
    ]


def missing_uuid_list():
    global client, ids_any, ids_boss, ids_desi, ids_lots, ids_sdss, outs
    global some_missing_ids, some_missing_specids, specids_any, specids_boss
    global specids_desi, specids_lots, specids_sdss

    client.missing(uuid_list=ids_any)
    # List of 60,000 ids -- produces error
    # client.missing(uuid_list=ids_lots)
    # 2 ids not in any datasets
    client.missing(uuid_list=some_missing_ids)


def missing_dataset_list():
    global client, ids_any, ids_boss, ids_desi, ids_lots, ids_sdss, outs
    global some_missing_ids, some_missing_specids, specids_any, specids_boss
    global specids_desi, specids_lots, specids_sdss

    # ids only in DESI-EDR
    client.missing(uuid_list=ids_desi, dataset_list=["SDSS-DR16", "BOSS-DR16"])
    # ids only in SDSS-DR16
    client.missing(uuid_list=ids_sdss, dataset_list=["DESI-EDR", "BOSS-DR16"])
    # ids only in BOSS-DR16
    client.missing(uuid_list=ids_boss, dataset_list=["DESI-EDR", "SDSS-DR16"])


def missing_countOnly():
    global client, ids_any, ids_boss, ids_desi, ids_lots, ids_sdss, outs
    global some_missing_ids, some_missing_specids, specids_any, specids_boss
    global specids_desi, specids_lots, specids_sdss

    client.missing(uuid_list=some_missing_ids, countOnly=True)


def missing_specids():
    global client, ids_any, ids_boss, ids_desi, ids_lots, ids_sdss, outs
    global some_missing_ids, some_missing_specids, specids_any, specids_boss
    global specids_desi, specids_lots, specids_sdss

    #! client.missing_specids?
    some_missing_specids = specids_any + [
        11111111111111111,
        999999999999999999,
    ]


def missing_specids_specid_list():
    global client, ids_any, ids_boss, ids_desi, ids_lots, ids_sdss, outs
    global some_missing_ids, some_missing_specids, specids_any, specids_boss
    global specids_desi, specids_lots, specids_sdss

    client.missing_specids(specid_list=specids_any)
    # List of 60,000 specids -- produces error
    # client.missing_specids(specid_list=specids_lots)
    # 2 specids not in any datasets
    client.missing_specids(specid_list=some_missing_specids)


def missing_specids_dataset_list():
    global client, ids_any, ids_boss, ids_desi, ids_lots, ids_sdss, outs
    global some_missing_ids, some_missing_specids, specids_any, specids_boss
    global specids_desi, specids_lots, specids_sdss

    # specids only in DESI-EDR
    client.missing_specids(
        specid_list=specids_desi, dataset_list=["SDSS-DR16", "BOSS-DR16"]
    )
    # specids only in SDSS-DR16
    client.missing_specids(
        specid_list=specids_sdss, dataset_list=["DESI-EDR", "BOSS-DR16"]
    )
    # specids only in BOSS-DR16
    client.missing_specids(
        specid_list=specids_boss, dataset_list=["DESI-EDR", "SDSS-DR16"]
    )


def missing_specids_countOnly():
    global client, ids_any, ids_boss, ids_desi, ids_lots, ids_sdss, outs
    global some_missing_ids, some_missing_specids, specids_any, specids_boss
    global specids_desi, specids_lots, specids_sdss

    client.missing_specids(specid_list=some_missing_specids, countOnly=True)


###
###########################################################################

###########################################################################
# Tests
#


# START Pre-notebook-sections code
class NotebookSectionTest(unittest.TestCase):
    """Test each section in notebook: SPARCL_client_method_tests.ipynb"""

    def test000_get_all_fields(self):
        actual = get_all_fields()
        expected = None
        self.assertEqual(actual, expected, msg="Actual to Expected")

    def test001_get_all_fields_dataset_list(self):
        actual = get_all_fields_dataset_list()
        expected = None
        self.assertEqual(actual, expected, msg="Actual to Expected")

    def test002_get_default_fields(self):
        actual = get_default_fields()
        expected = None
        self.assertEqual(actual, expected, msg="Actual to Expected")

    def test003_get_default_fields_dataset_list(self):
        actual = get_default_fields_dataset_list()
        expected = None
        self.assertEqual(actual, expected, msg="Actual to Expected")

    def test004_get_available_fields(self):
        actual = get_available_fields()
        expected = None
        self.assertEqual(actual, expected, msg="Actual to Expected")

    def test005_get_available_fields_dataset_list(self):
        actual = get_available_fields_dataset_list()
        expected = None
        self.assertEqual(actual, expected, msg="Actual to Expected")

    def test006_find(self):
        actual = find()
        expected = None
        self.assertEqual(actual, expected, msg="Actual to Expected")

    def test007_find_limit(self):
        actual = find_limit()
        expected = None
        self.assertEqual(actual, expected, msg="Actual to Expected")

    def test008_find_constraints(self):
        actual = find_constraints()
        expected = None
        self.assertEqual(actual, expected, msg="Actual to Expected")

    def test009_find_outfields(self):
        actual = find_outfields()
        expected = None
        self.assertEqual(actual, expected, msg="Actual to Expected")

    def test010_find_sort(self):
        actual = find_sort()
        expected = None
        self.assertEqual(actual, expected, msg="Actual to Expected")

    def test011_retrieve(self):
        actual = retrieve()
        expected = None
        self.assertEqual(actual, expected, msg="Actual to Expected")

    def test012_retrieve_limit(self):
        actual = retrieve_limit()
        expected = None
        self.assertEqual(actual, expected, msg="Actual to Expected")

    def test013_retrieve_dataset_list(self):
        actual = retrieve_dataset_list()
        expected = None
        self.assertEqual(actual, expected, msg="Actual to Expected")

    def test014_retrieve_include(self):
        actual = retrieve_include()
        expected = None
        self.assertEqual(actual, expected, msg="Actual to Expected")

    def test015_retrieve_by_specid(self):
        actual = retrieve_by_specid()
        expected = None
        self.assertEqual(actual, expected, msg="Actual to Expected")

    def test016_retrieve_by_specid_limit(self):
        actual = retrieve_by_specid_limit()
        expected = None
        self.assertEqual(actual, expected, msg="Actual to Expected")

    def test017_retrieve_by_specid_dataset_list(self):
        actual = retrieve_by_specid_dataset_list()
        expected = None
        self.assertEqual(actual, expected, msg="Actual to Expected")

    def test018_retrieve_by_specid_include(self):
        actual = retrieve_by_specid_include()
        expected = None
        self.assertEqual(actual, expected, msg="Actual to Expected")

    def test019_missing(self):
        actual = missing()
        expected = None
        self.assertEqual(actual, expected, msg="Actual to Expected")

    def test020_missing_uuid_list(self):
        actual = missing_uuid_list()
        expected = None
        self.assertEqual(actual, expected, msg="Actual to Expected")

    def test021_missing_dataset_list(self):
        actual = missing_dataset_list()
        expected = None
        self.assertEqual(actual, expected, msg="Actual to Expected")

    def test022_missing_countOnly(self):
        actual = missing_countOnly()
        expected = None
        self.assertEqual(actual, expected, msg="Actual to Expected")

    def test023_missing_specids(self):
        actual = missing_specids()
        expected = None
        self.assertEqual(actual, expected, msg="Actual to Expected")

    def test024_missing_specids_specid_list(self):
        actual = missing_specids_specid_list()
        expected = None
        self.assertEqual(actual, expected, msg="Actual to Expected")

    def test025_missing_specids_dataset_list(self):
        actual = missing_specids_dataset_list()
        expected = None
        self.assertEqual(actual, expected, msg="Actual to Expected")

    def test026_missing_specids_countOnly(self):
        actual = missing_specids_countOnly()
        expected = None
        self.assertEqual(actual, expected, msg="Actual to Expected")
