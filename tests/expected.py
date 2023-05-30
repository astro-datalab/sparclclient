# For running client against PAT hosts

#!idfld = 'uuid'  # Science Field Name for uuid. Diff val than Internal name.
idfld = 'sparcl_id'  # Sci Field Name for uuid. Diff val than Internal name.

all_fields = ['data_release',
              'datasetgroup',
              'dateobs',
              'dateobs_center',
              'dec',
              'exptime',
              'flux',
              'instrument',
              'ivar',
              'mask',
              'model',
              'ra',
              'redshift',
              'redshift_err',
              'redshift_warning',
              'site',
              'sparcl_id',
              'specid',
              'specprimary',
              'spectype',
              'survey',
              'targetid',
              'telescope',
              'wave_sigma',
              'wavelength',
              'wavemax',
              'wavemin']

default_fields = ['dec', 'flux', 'ra', idfld, 'specid', 'wavelength']

#retrieve_0 = [1506512395860731904]
retrieve_0 = [3383388400617889792]  # PAT

retrieve_0b = ['_dr', 'dec', 'flux', 'ra', idfld, 'specid', 'wavelength']

# OLD as of May 30, 2023
#retrieve_5 = [-9199727451598204928, -9199726901842391040]

retrieve_5 = [-9199727726476111872, -9199727451598204928]

# OLD as of May 30, 2023
#find_0 = [{'_dr': 'SDSS-DR16',
#  'dec': 63.370185,
#  'ra': 137.05005,
#  'sparcl_id': '01f9491e-90cd-4515-b28c-578e0ca1fd3c'},
# {'_dr': 'SDSS-DR16',
#  'dec': 63.295866,
#  'ra': 137.51585,
#  'sparcl_id': '1c2e3f82-9404-4a0a-8453-ba691452dbef'}]

find_0 = [{'_dr': 'SDSS-DR16',
           'dec': 63.070512,
           'ra': 137.5556,
           'sparcl_id': '00186946-efa6-422b-8262-a7173300d995'},
          {'_dr': 'SDSS-DR16',
           'dec': 63.241905,
           'ra': 137.26917,
           'sparcl_id': '1209520d-88fb-4474-a931-22480f509403'}]

# PAT

# OLD as of May 30, 2023
#find_1 = [{'_dr': 'BOSS-DR16',
#  'dec': 6.801426,
#  'ra': 194.15102,
#  'sparcl_id': '000025da-914b-4b67-b9a9-97cc811b0459'}]

find_1 = [{'_dr': 'BOSS-DR16',
           'dec': 31.224955,
           'ra': 242.45844,
           'sparcl_id': '0000237e-4015-4a41-9f97-0032712b8c99'}]

#find_2 = 640  # DEV
find_2 = 936894  # PAT

# OLD as of May 30, 2023
#find_3 = [{'_dr': 'BOSS-DR16',
#  'dec': 6.801426,
#  'ra': 194.15102,
#  'sparcl_id': '000025da-914b-4b67-b9a9-97cc811b0459'},
# {'_dr': 'DESI-EDR',
#  'dec': 57.721832586575,
#  'ra': 184.29291453372,
#  'sparcl_id': '00006d5f-b03a-4b4f-848a-92f04b6929cf'},
# {'_dr': 'DESI-EDR',
#  'dec': 2.27564113949688,
#  'ra': 216.899264432107,
#  'sparcl_id': '00009c7a-8003-4841-a3eb-a387c65e171f'}]

find_3 = [{'_dr': 'BOSS-DR16',
           'dec': 31.224955,
           'ra': 242.45844,
           'sparcl_id': '0000237e-4015-4a41-9f97-0032712b8c99'},
          {'_dr': 'DESI-EDR',
           'dec': 32.4730346761871,
           'ra': 156.246117666088,
           'sparcl_id': '00002559-535a-4806-ade8-150b615c2087'},
          {'_dr': 'BOSS-DR16',
           'dec': -2.329202,
           'ra': 212.13012,
           'sparcl_id': '00002a0f-4ad1-4a3a-a1a6-10efb50967f0'}]

# OLD as of May 30, 2023
#find_4 = ['000025da-914b-4b67-b9a9-97cc811b0459',
#          '00006d5f-b03a-4b4f-848a-92f04b6929cf',
#          '00009c7a-8003-4841-a3eb-a387c65e171f']

find_4 = ['0000237e-4015-4a41-9f97-0032712b8c99',
          '00002559-535a-4806-ade8-150b615c2087',
          '00002a0f-4ad1-4a3a-a1a6-10efb50967f0']

find_5a = [{'_dr': 'BOSS-DR16', 'data_release': 'BOSS-DR16', 'mjd': 55689},
           {'_dr': 'SDSS-DR16', 'data_release': 'SDSS-DR16', 'mjd': 54763}]

find_5d = []

# OLD as of May 30, 2023
#reorder_1a = ['eeeb383c-1e1c-4e9b-9c1c-d79537062fa8',
#              'e39f0e2e-6aea-426b-8032-288a79e31fcf',
#              '9740ee32-8909-45c8-b0ba-24a35a5ba4d7']

reorder_1a = ['9452379f-d82d-43bb-8fc2-c26451df4710',
              '529936c6-14ef-4119-a80d-b184dcb6308e',
              'fbb22144-25c5-4330-9b0b-8b2eac83079c']

reorder_1b = [-5970393627659841536, 8712441763707768832, 3497074051921321984]

# OLD as of May 30, 2023
#reorder_2a = ['e39f0e2e-6aea-426b-8032-288a79e31fcf',
#              None,
#              '9740ee32-8909-45c8-b0ba-24a35a5ba4d7']

reorder_2a = ['529936c6-14ef-4119-a80d-b184dcb6308e',
              None,
              'fbb22144-25c5-4330-9b0b-8b2eac83079c']

reorder_2b = [-5970393627659841536, 8712441763707768832, None]
