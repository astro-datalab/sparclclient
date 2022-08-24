#!idfld = 'uuid'  # Science Field Name for uuid. Diff val than Internal name.
idfld = 'id'      # Science Field Name for uuid. Diff val than Internal name.

all_fields = ['MJD',
              'RUN2D',
              'data_release',
              'datasetgroup',
              'dateobs',
              'dateobs_center',
              'dec',
              'dirpath',
              'exptime',
              'extra_files',
              'filename',
              'filesize',
              'flux',
              'id',
              'instrument',
              'ivar',
              'mask',
              'model',
              'ra',
              'redshift',
              'redshift_err',
              'redshift_warning',
              'site',
              'sky',
              'specid',
              'specprimary',
              'spectype',
              'targetid',
              'telescope',
              'updated',
              'wave_sigma',
              'wavelength',
              'wavemax',
              'wavemin']

default_fields = ['flux', 'id', 'wavelength']

#retrieve_0 = [1506512395860731904]
retrieve_0 = [3383388400617889792]  # PAT

retrieve_0b = ['_dr', 'flux', idfld, 'wavelength']

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
           'id': '2587dc0b-296a-4f77-8197-75431d7e8773',
           'ra': 137.74507},
          {'_dr': 'SDSS-DR16',
           'dec': 63.286553,
           'id': '26616ea2-fd26-456d-bb90-d249c597f89a',
           'ra': 137.48823}]  # PAT

#find_1 = [{'_dr': 'SDSS-DR16',
#  'dec': 35.039381,
#  'id': '000547a1-8536-4b47-937b-2f595710fe09',
#  'ra': 248.1914}]

find_1 = [{'_dr': 'DESI-edr',
           'dec': 0.447694301025336,
           'id': '000005ba-5f9c-4a0e-b9d7-d29775a665bb',
           'ra': 179.626655105234}]  # PAT

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

find_3 = [{'_dr': 'DESI-edr',
           'dec': 0.447694301025336,
           'id': '000005ba-5f9c-4a0e-b9d7-d29775a665bb',
           'ra': 179.626655105234},
          {'_dr': 'BOSS-DR16',
           'dec': 44.143862,
           'id': '00000ce3-d15b-4ef5-952b-5790e96af5d7',
           'ra': 194.55856},
          {'_dr': 'BOSS-DR16',
           'dec': 21.33438,
           'id': '00001f94-96b1-4f2d-8d1d-1a47a89fe105',
           'ra': 0.863617040000008}]  # PAT

#find_4 = ['000547a1-8536-4b47-937b-2f595710fe09',
#          '01af637c-2d98-4902-b2d3-076a06a01dbd',
#          '01ba6c0d-2588-4f4e-830e-e68f9f718cf7']

find_4 = ['000005ba-5f9c-4a0e-b9d7-d29775a665bb',
          '00000ce3-d15b-4ef5-952b-5790e96af5d7',
          '00001f94-96b1-4f2d-8d1d-1a47a89fe105']  # PAT
