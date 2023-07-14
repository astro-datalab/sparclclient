# For running client against PAT host
# See also: expected_dev1.py   (SP DEV)

all_fields = [
    "data_release",
    "datasetgroup",
    "dateobs",
    "dateobs_center",
    "dec",
    "exptime",
    "extra_files",
    "file",
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
    "updated",
    "wave_sigma",
    "wavelength",
    "wavemax",
    "wavemin",
]

default_fields = ["dec", "flux", "ra", "sparcl_id", "specid", "wavelength"]

retrieve_0 = [-6444474727991586816, -6444474453113679872]

retrieve_0b = ["_dr", "dec", "flux", "ra", "sparcl_id", "specid", "wavelength"]

retrieve_5 = [-6444474727991586816, -6444474453113679872]

find_0 = [
    {
        "_dr": "BOSS-DR16",
        "dec": 28.992644,
        "ra": 132.33645,
        "sparcl_id": "00031d79-1f6d-11ee-9788-525400aad0aa",
    },
    {
        "_dr": "BOSS-DR16",
        "dec": 28.951661,
        "ra": 132.40982,
        "sparcl_id": "002f2f2a-1f6d-11ee-bd1f-525400aad0aa",
    },
]

find_1 = [
    {
        "_dr": "BOSS-DR16",
        "dec": 28.992644,
        "ra": 132.33645,
        "sparcl_id": "00031d79-1f6d-11ee-9788-525400aad0aa",
    }
]

find_2 = 936894  # PAT

find_3 = [
    {
        "_dr": "BOSS-DR16",
        "dec": 28.992644,
        "ra": 132.33645,
        "sparcl_id": "00031d79-1f6d-11ee-9788-525400aad0aa",
    },
    {
        "_dr": "BOSS-DR16",
        "dec": 29.033685,
        "ra": 132.33797,
        "sparcl_id": "0018bce9-1f6d-11ee-8cd9-525400aad0aa",
    },
    {
        "_dr": "BOSS-DR16",
        "dec": 28.951661,
        "ra": 132.40982,
        "sparcl_id": "002f2f2a-1f6d-11ee-bd1f-525400aad0aa",
    },
]

find_4 = [
    "00031d79-1f6d-11ee-9788-525400aad0aa",
    "0018bce9-1f6d-11ee-8cd9-525400aad0aa",
    "002f2f2a-1f6d-11ee-bd1f-525400aad0aa",
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

reorder_1b = [-6444474727991586816, -6444474453113679872, -6444474178235772928]

reorder_2a = [
    "529936c6-14ef-4119-a80d-b184dcb6308e",
    None,
    "fbb22144-25c5-4330-9b0b-8b2eac83079c",
]

reorder_2b = [-6444474727991586816, -6444474453113679872, None]
