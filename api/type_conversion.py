from abc import ABC, abstractmethod
import copy


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

        import numpy
        coadd = record['spectra']['coadd']
        newrec = dict(
            ra = record.get('ra_center'),
            dec = record.get('dec_center'),
            red_shift = record.get('red_shift'),
            coadd = numpy.array([
                coadd['sky'],
                coadd['flux'],
                coadd['ivar'],
                coadd['model'],
                coadd['loglam'],
                ]),
            #! specobj = record['spectra']['specobj'],
        )
        return(newrec)

    def to_spectrum1d(self, record):
        #! return(record)
        import numpy as np
        import astropy.units as u
        from specutils import Spectrum1D
        from astropy.nddata import InverseVariance

        coadd = record['spectra']['coadd']
        wavelength = (10**np.array(coadd['loglam']))*u.AA
        flux = np.array(coadd['flux'])*u.Jy
        ivar = InverseVariance(np.array(coadd['ivar']))
        z = record.get('red_shift')

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
    def to_numpy(self, record):
        coadd = record['spectra']['coadd']
        newrec = dict(
            specid = record.get('specid'),
            ra = record.get('ra_center'),
            dec = record.get('dec_center'),
            red_shift = record.get('red_shift'),
            coadd = numpy.array([
                coadd['SKY'],
                coadd['FLUX'],
                coadd['IVAR'],
                coadd['MODEL'],
                coadd['LOGLAM'],
                ]),
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

def convert(record, rtype):
    if rtype is None:
        return record

    dr = record.get('data_release_id', 'Unknown')
    drin = diLUT.get(dr,NoopConvert())

    if rtype == 'numpy':
        return drin.to_numpy(record)
    elif rtype == 'spectrum1d':
        return drin.to_spectrum1d(record)
    elif rtype == 'pandas':
        return drin.to_pandas(record)
    else:
        raise Exception(f'Unknown record type ({rtype})')
    return None
