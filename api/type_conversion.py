from abc import ABC, abstractmethod
import copy
import numpy as np
import astropy.units as u
from specutils import Spectrum1D
from astropy.nddata import InverseVariance


class Convert(ABC):
    """Convert JSON record to mix of plain python and selected data record type.
    """

    @abstractmethod
    def to_numpy(self,record):
        newrec = copy.deepcopy(record)
        return(newrec)

    @abstractmethod
    def to_spectrum1d(self,record):
        newrec = copy.deepcopy(record)
        return(newrec)

    @abstractmethod
    def to_pandas(self,record):
        newrec = copy.deepcopy(record)
        return(newrec)


class NoopConvert(Convert):
    def to_numpy(self, record):
        return(record)
    def to_spectrum1d(self, record):
        return(record)
    def to_pandas(self, record):
        return(record)

class SdssDr16(Convert):
    out_data_paths = [
        'specid',
        'ra_center',
        'dec_center',
        'red_shift',
        'coadd', # 5 columns
        ]

    # client = api.client.SparclApi()
    # sdss_rec = client.sample_records(1,structure='SDSS-DR16')[0]
    def to_numpy(self, record):
        """Convert FitsFile record to a structure that uses Numpy"""


        newrec = dict(
            ra = record.get('ra_center'),
            dec = record.get('dec_center'),
            red_shift = record.get('red_shift'),
            coadd = np.array([
                record['sky'],
                record['flux'],
                record['ivar'],
                record['model'],
                record['loglam'],
                ]),
            #! specobj = record['spectra']['specobj'],
        )
        return(newrec)

    def to_spectrum1d(self, record):
        #! return(record)

        coadd = record['spectra']['coadd']
        wavelength = (10**np.array(coadd['loglam']))*u.AA
        flux = np.array(coadd['flux'])*u.Jy
        ivar = InverseVariance(np.array(coadd['ivar']))
        z = record.get('red_shift')

        lofl = []

        newrec = dict(
            ra = record.get('ra_center'),
            dec = record.get('dec_center'),
            red_shift = record.get('red_shift'),
            # flux, uncertainty, wavevelength, mask(or, and), redshift
            spec1d = Spectrum1D(spectral_axis=wavelength, flux=flux,
                                uncertainty=ivar, redshift=z),
            )
            #! specobj = record['spectra']['specobj'],
        return(newrec)


    def to_pandas(self, record):
        return(record)

class BossDr16(Convert):
    out_data_paths = [
        'specid',
        'ra_center',
        'dec_center',
        'red_shift',
        'spectra.coadd', # 5 columns
        ]
    def to_numpy(self, record, o2nLUT, verbose=True):
        if verbose:
            print(f'DBG-1: BOSS-DR16.to_numpy record.keys={list(record.keys())}')


        arflds = [
            'spectra.coadd.AND_MASK',
            'spectra.coadd.FLUX',
            'spectra.coadd.IVAR',
            'spectra.coadd.LOGLAM',
            'spectra.coadd.MODEL',
            'spectra.coadd.OR_MASK',
            'spectra.coadd.SKY',
            'spectra.coadd.WDISP',
            ]
        lofl = [record[o2nLUT[f]] for f in arflds if f in o2nLUT]

        newrec = dict(
            specid = record.get('specid'),
            #! ra = record.get('ra_center'),
            #! dec = record.get('dec_center'),
            #! red_shift = record.get('red_shift'),
            coadd = numpy.array(lofl),
            #! specobj = record['spectra']['specobj'],
        )
        return(newrec)

    def to_spectrum1d(self, record):
        return(record)
    def to_pandas(self, record):
        return(record)

class DesiDenali(Convert):
    def to_numpy(self, record):
        return(record)
    def to_spectrum1d(self, record):
        return(record)
    def to_pandas(self, record):
        return(record)


# DR Instance LookUp Table
diLUT = {
    'SDSS-DR16': SdssDr16(),
    'BOSS-DR16': BossDr16(),
    'DESI-denali': DesiDenali(),
    'Unknown': NoopConvert(),
    }

def convert(record, rtype, client, include, verbose=False):
    if verbose:
        print(f'convert(record={list(record.keys())}, rtype={rtype}')

    if rtype is None:
        return record

    dr = record['data_release']
    drin = diLUT.get(dr,NoopConvert())

    o2nLUT = copy.copy(client.orig2newLUT[dr]) # orig2newLUT[dr][orig] = new
    n2oLUT = client.new2origLUT[dr]
    if include is not None:
        nuke = set(n2oLUT.keys()).difference(include)
        for new in nuke:
            del o2nLUT[n2oLUT[new]]

    print(f'o2nLUT={o2nLUT}, include={include}')
    if rtype == 'numpy':
        return drin.to_numpy(record, o2nLUT)
    elif rtype == 'spectrum1d':
        return drin.to_spectrum1d(record, o2nLUT)
    elif rtype == 'pandas':
        return drin.to_pandas(record, o2nLUT)
    else:
        raise Exception(f'Unknown record type ({rtype})')
    return None
