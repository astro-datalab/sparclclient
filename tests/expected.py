# For PAT hosts

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
              'mjd',
              'model',
              'ra',
              'redshift',
              'redshift_err',
              'redshift_warning',
              'site',
              'sky',
              idfld,
              'specid',
              'specprimary',
              'spectype',
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

retrieve_4 = ['FIBERID',
              'MJD',
              'PLATEID',
              'RUN1D',
              'RUN2D',
              'SPECOBJID',
              'data_release_id',
              'datasetgroup_id',
              'dateobs',
              'dateobs_center',
              'dec',
              'exptime',
              'flux',
              'instrument_id',
              'ivar',
              'mask',
              'model',
              'ra',
              'redshift_err',
              'redshift_warning',
              'site',
              'sky',
              'specid',
              'specprimary',
              'spectype_id',
              'targetid',
              'telescope_id',
              idfld,
              'wave_sigma',
              'wavelength',
              'wavemax',
              'wavemin',
              'z']

#find_0 = [{'_dr': 'SDSS-DR16',
#  'dec': 34.77458,
#  'id': 'd4ab98d4-0485-4246-9678-373964f0d29a',
#  'ra': 246.70983},
# {'_dr': 'SDSS-DR16',
#  'dec': 34.752141,
#  'id': 'f49aa604-35ad-4701-b701-ccbd2b3ec5f2',
#  'ra': 246.79026}]

find_0 = [{'_dr': 'SDSS-DR16',
           'dec': 63.029566,
           'ra': 137.74507,
           'sparcl_id': '2587dc0b-296a-4f77-8197-75431d7e8773'},
          {'_dr': 'SDSS-DR16',
           'dec': 63.286553,
           'ra': 137.48823,
           'sparcl_id': '26616ea2-fd26-456d-bb90-d249c597f89a'}]  # PAT

#find_1 = [{'_dr': 'SDSS-DR16',
#  'dec': 35.039381,
#  'id': '000547a1-8536-4b47-937b-2f595710fe09',
#  'ra': 248.1914}]

find_1 = [{'_dr': 'BOSS-DR16',
           'dec': 44.143862,
           'ra': 194.55856,
           'sparcl_id': '00000ce3-d15b-4ef5-952b-5790e96af5d7'}]

#find_2 = 640  # DEV
find_2 = 936894  # PAT

#find_3 = [{'_dr': 'SDSS-DR16',
#  'dec': 35.039381,
#  'id': '000547a1-8536-4b47-937b-2f595710fe09',
#  'ra': 248.1914},
# {'_dr': 'SDSS-DR16',
#  'dec': 36.323288,
#  'id': '01af637c-2d98-4902-b2d3-076a06a01dbd',
#  'ra': 247.89899},
# {'_dr': 'SDSS-DR16',
#  'dec': 35.816782,
#  'id': '01ba6c0d-2588-4f4e-830e-e68f9f718cf7',
#  'ra': 247.39428}]

find_3 = [{'_dr': 'BOSS-DR16',
           'dec': 44.143862,
           'ra': 194.55856,
           'sparcl_id': '00000ce3-d15b-4ef5-952b-5790e96af5d7'},
          {'_dr': 'DESI-EDR',
           'dec': 32.9667091540768,
           'ra': 141.861318540722,
           'sparcl_id': '00001c4b-c0b7-4098-bb85-59f37b81af93'},
          {'_dr': 'BOSS-DR16',
           'dec': 21.33438,
           'ra': 0.863617040000008,
           'sparcl_id': '00001f94-96b1-4f2d-8d1d-1a47a89fe105'}]

find_4 = ['00000ce3-d15b-4ef5-952b-5790e96af5d7',
          '00001c4b-c0b7-4098-bb85-59f37b81af93',
          '00001f94-96b1-4f2d-8d1d-1a47a89fe105']

reorder_1a = ['f77143fd-89d8-4c92-ad61-8826cfa1bfe2',
              '54715e2a-427d-4090-981d-5137e4f5ff21',
              '690e9fae-35f1-436f-90f6-258499fc74d7']

reorder_1b = [-5970393627659841536, 8712441763707768832, 3497074051921321984]

reorder_2a = ['54715e2a-427d-4090-981d-5137e4f5ff21',
              None,
              '690e9fae-35f1-436f-90f6-258499fc74d7']

reorder_2b = [-5970393627659841536, 8712441763707768832, None]
