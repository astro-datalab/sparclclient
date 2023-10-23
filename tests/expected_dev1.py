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

retrieve_0 = [39627077367894679, 39627077367894679, 1254363325353977856]

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

retrieve_5 = [39627077367894679, 1254363325353977856]

find_0 = [
    {
        "_dr": "DESI-EDR",
        "dec": 27.534720830788544,
        "ra": 194.5244478923875,
        "sparcl_id": "44c62511-71fa-11ee-b2bf-08002725f1ef",
    },
    {
        "_dr": "DESI-EDR",
        "dec": 27.586173146527337,
        "ra": 194.57877483102325,
        "sparcl_id": "44cc3989-71fa-11ee-a65c-08002725f1ef",
    },
]

find_1 = [
    {
        "_dr": "SDSS-DR17",
        "dec": 1.2262562,
        "ra": 314.87155,
        "sparcl_id": "02bf79b8-060f-446f-81de-1dd88cd14db1",
    }
]

find_2 = 640  # DEV

find_3 = [
    {
        "_dr": "SDSS-DR17",
        "dec": 1.2262562,
        "ra": 314.87155,
        "sparcl_id": "02bf79b8-060f-446f-81de-1dd88cd14db1",
    },
    {
        "_dr": "DESI-EDR",
        "dec": -30.8575384091412,
        "ra": 59.9283382246379,
        "sparcl_id": "1206a8d3-d3f4-42c0-a5ee-2846d8caa3be",
    },
    {
        "_dr": "SDSS-DR16",
        "dec": 35.966759,
        "ra": 247.76868,
        "sparcl_id": "1ec5eb87-c678-4a17-9fec-2fe2982e24b0",
    },
]


find_4 = [
    "02bf79b8-060f-446f-81de-1dd88cd14db1",
    "1206a8d3-d3f4-42c0-a5ee-2846d8caa3be",
    "1ec5eb87-c678-4a17-9fec-2fe2982e24b0",
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

reorder_1b = [1254363325353977856, 39627077367894679, 1506485182947944448]

reorder_2a = [
    "529936c6-14ef-4119-a80d-b184dcb6308e",
    None,
    "fbb22144-25c5-4330-9b0b-8b2eac83079c",
]

reorder_2b = [1254363325353977856, 39627077367894679, None]

missing = ["NOT_SPEC_ID", "435780743478667264"]
