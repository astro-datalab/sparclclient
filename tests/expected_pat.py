# For running client against PAT host
# See also: expected_dev1.py   (SP DEV)

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

retrieve_0 = [1254334738051655680, 1254335012929562624]

retrieve_0b = ["_dr", "dec", "flux", "ra", "sparcl_id", "specid", "wavelength"]

retrieve_5 = [1254334738051655680, 1254335012929562624]

find_0 = [
    {
        "_dr": "BOSS-DR16",
        "dec": 28.038113,
        "ra": 132.95902999999998,
        "sparcl_id": "611a5a1c-75d8-11ee-8b9f-525400aad0aa",
    },
    {
        "_dr": "BOSS-DR16",
        "dec": 28.019856,
        "ra": 132.93685,
        "sparcl_id": "61357ba4-75d8-11ee-a1b5-525400aad0aa",
    },
]

find_1 = [
    {
        "_dr": "SDSS-DR17",
        "dec": -0.98681,
        "ra": 313.90848,
        "sparcl_id": "0002f55c-75d7-11ee-822f-525400aad0aa",
    }
]

find_2 = 936894  # PAT

find_3 = [
    {
        "_dr": "SDSS-DR17",
        "dec": -0.98681,
        "ra": 313.90848,
        "sparcl_id": "0002f55c-75d7-11ee-822f-525400aad0aa",
    },
    {
        "_dr": "SDSS-DR17",
        "dec": -0.945676,
        "ra": 313.91043,
        "sparcl_id": "000df610-75d7-11ee-9957-525400aad0aa",
    },
    {
        "_dr": "SDSS-DR17",
        "dec": -0.486388,
        "ra": 313.70407,
        "sparcl_id": "0018f253-75d7-11ee-8253-525400aad0aa",
    },
]


find_4 = [
    "0002f55c-75d7-11ee-822f-525400aad0aa",
    "000df610-75d7-11ee-9957-525400aad0aa",
    "0018f253-75d7-11ee-8253-525400aad0aa",
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

reorder_1b = [1254334738051655680, 1254335012929562624, 1254335287807469568]

reorder_2a = [1254334738051655680, 1254335012929562624, None]

reorder_2b = [1254334738051655680, 1254335012929562624, None]
