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

retrieve_0 = [3383388400617889792]  # PAT

retrieve_0b = ["_dr", "dec", "flux", "ra", "sparcl_id", "specid", "wavelength"]

retrieve_5 = [-9199727726476111872, -9199727451598204928]

find_0 = [
    {
        "_dr": "SDSS-DR16",
        "dec": 63.070512,
        "ra": 137.5556,
        "sparcl_id": "00186946-efa6-422b-8262-a7173300d995",
    },
    {
        "_dr": "SDSS-DR16",
        "dec": 63.241905,
        "ra": 137.26917,
        "sparcl_id": "1209520d-88fb-4474-a931-22480f509403",
    },
]

find_1 = [
    {
        "_dr": "BOSS-DR16",
        "dec": 31.224955,
        "ra": 242.45844,
        "sparcl_id": "0000237e-4015-4a41-9f97-0032712b8c99",
    }
]

find_2 = 936894  # PAT

find_3 = [
    {
        "_dr": "BOSS-DR16",
        "dec": 31.224955,
        "ra": 242.45844,
        "sparcl_id": "0000237e-4015-4a41-9f97-0032712b8c99",
    },
    {
        "_dr": "DESI-EDR",
        "dec": 32.4730346761871,
        "ra": 156.246117666088,
        "sparcl_id": "00002559-535a-4806-ade8-150b615c2087",
    },
    {
        "_dr": "BOSS-DR16",
        "dec": -2.329202,
        "ra": 212.13012,
        "sparcl_id": "00002a0f-4ad1-4a3a-a1a6-10efb50967f0",
    },
]

find_4 = [
    "0000237e-4015-4a41-9f97-0032712b8c99",
    "00002559-535a-4806-ade8-150b615c2087",
    "00002a0f-4ad1-4a3a-a1a6-10efb50967f0",
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

reorder_1b = [-5970393627659841536, 8712441763707768832, 3497074051921321984]

reorder_2a = [
    "529936c6-14ef-4119-a80d-b184dcb6308e",
    None,
    "fbb22144-25c5-4330-9b0b-8b2eac83079c",
]

reorder_2b = [-5970393627659841536, 8712441763707768832, None]
