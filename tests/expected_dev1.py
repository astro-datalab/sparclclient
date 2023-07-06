# For running client against SP DEV host
# See also: expected_pat.py

all_fields = [
    "data_release",
    "datasetgroup",
    "dateobs",
    "dateobs_center",
    "dec",
    "exptime",
    "flux",
    "instrument",
    "ivar",
    "mask",
    "model",
    "ra",
    "redshift",
    "redshift_err",
    "redshift_warning",
    "site",
    "sparcl_id",
    "specid",
    "specprimary",
    "spectype",
    "survey",
    "targetid",
    "telescope",
    "wave_sigma",
    "wavelength",
    "wavemax",
    "wavemin",
]

default_fields = ["dec", "flux", "ra", "sparcl_id", "specid", "wavelength"]

retrieve_0 = [2258586057769510912, 2258586332647417856]

retrieve_0b = ["_dr", "dec", "flux", "ra", "sparcl_id", "specid", "wavelength"]

retrieve_4 = [
    "FIBERID",
    "MJD",
    "PLATEID",
    "RUN1D",
    "RUN2D",
    "SPECOBJID",
    "data_release_id",
    "datasetgroup_id",
    "dateobs",
    "dateobs_center",
    "dec",
    "exptime",
    "flux",
    "instrument_id",
    "ivar",
    "mask",
    "model",
    "ra",
    "redshift_err",
    "redshift_warning",
    "site",
    "sky",
    "specid",
    "specprimary",
    "spectype_id",
    "targetid",
    "telescope_id",
    "sparcl_id",
    "wave_sigma",
    "wavelength",
    "wavemax",
    "wavemin",
    "z",
]

retrieve_5 = [2258586057769510912, 2258586332647417856]

find_0 = [
    {
        "_dr": "SDSS-DR16",
        "dec": 34.752141,
        "ra": 246.79026,
        "sparcl_id": "7aac8b45-1c1c-11ee-9124-0800273271a6",
    },
    {
        "_dr": "SDSS-DR16",
        "dec": 34.77458,
        "ra": 246.70983,
        "sparcl_id": "7b705b80-1c1c-11ee-89f4-0800273271a6",
    },
]


find_1 = [
    {
        "_dr": "SDSS-DR17",
        "dec": 33.488395,
        "ra": 195.89264,
        "sparcl_id": "00014163-1c1d-11ee-b89d-0800273271a6",
    }
]

find_2 = 640  # DEV

find_3 = [
    {
        "_dr": "SDSS-DR17",
        "dec": 33.488395,
        "ra": 195.89264,
        "sparcl_id": "00014163-1c1d-11ee-b89d-0800273271a6",
    },
    {
        "_dr": "SDSS-DR17",
        "dec": 33.655985,
        "ra": 195.886,
        "sparcl_id": "000764ca-1c1d-11ee-bd7b-0800273271a6",
    },
    {
        "_dr": "SDSS-DR17",
        "dec": 33.353793,
        "ra": 196.04631,
        "sparcl_id": "000d982b-1c1d-11ee-9638-0800273271a6",
    },
]


find_4 = [
    "00014163-1c1d-11ee-b89d-0800273271a6",
    "000764ca-1c1d-11ee-bd7b-0800273271a6",
    "000d982b-1c1d-11ee-9638-0800273271a6",
]

find_5a = [
    {"_dr": "BOSS-DR16", "data_release": "BOSS-DR16", "mjd": 55689},
    {"_dr": "SDSS-DR16", "data_release": "SDSS-DR16", "mjd": 54763},
]

find_5d = []

reorder_1a = [
    "9452379f-d82d-43bb-8fc2-c26451df4710",
    "529936c6-14ef-4119-a80d-b184dcb6308e",
    "fbb22144-25c5-4330-9b0b-8b2eac83079c",
]

reorder_1b = [2258586057769510912, 2258586332647417856, 2258586607525324800]

reorder_2a = [
    "529936c6-14ef-4119-a80d-b184dcb6308e",
    None,
    "fbb22144-25c5-4330-9b0b-8b2eac83079c",
]

reorder_2b = [2258586057769510912, 2258586332647417856, None]

missing = ["NOT_SPEC_ID", "435780743478667264"]
