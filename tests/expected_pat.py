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

retrieve_0 = ["_dr", "flux", "sparcl_id", "specid"]

retrieve_0b = ["_dr", "dec", "flux", "ra", "sparcl_id", "specid", "wavelength"]

retrieve_5 = 2

find_0 = [
    {
        "_dr": "BOSS-DR16",
        "data_release": "BOSS-DR16",
        "specid": -6444532452352045056,
    }
]

find_1 = [
    {
        "_dr": "SDSS-DR16",
        "data_release": "SDSS-DR16",
        "specid": 1506454396622366720,
    }
]

find_2 = 936894  # PAT

find_3 = [
    {"_dr": "BOSS-DR16", "data_release": "BOSS-DR16"},
    {"_dr": "DESI-EDR", "data_release": "DESI-EDR"},
    {"_dr": "SDSS-DR16", "data_release": "SDSS-DR16"},
]

find_4 = 36

find_5a = [
    {"_dr": "BOSS-DR16", "data_release": "BOSS-DR16", "mjd": 55689},
    {"_dr": "SDSS-DR16", "data_release": "SDSS-DR16", "mjd": 54763},
]

find_5d = []

authorized_1 = {
    "Loggedin_As": "test_user_1@noirlab.edu",
    "Authorized_Datasets": {
        "BOSS-DR16",
        "DESI-EDR",
        "SDSS-DR16",
        "SDSS-DR17-test",
    },
}

authorized_2 = {
    "Loggedin_As": "test_user_2@noirlab.edu",
    "Authorized_Datasets": {"BOSS-DR16", "DESI-EDR", "SDSS-DR16"},
}

authorized_3 = {
    "Loggedin_As": "Anonymous",
    "Authorized_Datasets": {"BOSS-DR16", "DESI-EDR", "SDSS-DR16"},
}

# Private and Public
pub_1 = ["BOSS-DR16"]
pub_all = ["BOSS-DR16", "DESI-EDR", "SDSS-DR16"]
priv = ["SDSS-DR17-test"]
unauth = "test_user_2@noirlab.edu"
#
auth_find_1 = auth_find_2 = pub_all + priv
# OLD as of July 9, 2024
#auth_find_3 = f"[DSDENIED] {unauth} is declined access to datasets {priv}"
auth_find_3 = auth_retrieve_3 = (f"[DSDENIED] uname='{unauth}' is declined "
                                 f"access to datasets={priv}; "
                                 f"drs_requested={pub_all + priv} "
                                 f"my_auth={pub_all}")
auth_find_4 = auth_find_6 = pub_all
# OLD as of July 9, 2024
#auth_find_5 = f"[DSDENIED] ANONYMOUS is declined access to datasets {priv}"
auth_find_5 = auth_retrieve_6 = ("[DSDENIED] uname='ANONYMOUS' is declined "
                                 f"access to datasets={priv}; "
                                 f"drs_requested={pub_all + priv} "
                                 f"my_auth={pub_all}")
auth_retrieve_1 = auth_retrieve_2 = pub_1 + priv
# OLD as of July 9, 2024
#auth_retrieve_3 = f"[DSDENIED] {unauth} is declined access to datasets {priv}"
auth_retrieve_4 = auth_retrieve_5 = auth_retrieve_7 = auth_retrieve_8 = pub_1
# OLD as of July 9, 2024
#auth_retrieve_6 = f"[DSDENIED] ANONYMOUS is declined access to datasets {priv}"  # noqa: E501
