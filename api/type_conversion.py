"""It would be much better if this were abstracted and easier to
update with new Data Types and new DataReleases.  Perhaps use
something like the Server "Personalities".  I've rejected abstracting
for now because I think we need operational experience with the DataType
feature and how it interacts with other features (especially global
Rename and retrieve(INCLUDE).

DataType conversion should be done completely within the Client, not
the on the Server.  The obvious reason is Clients are language
dependent, the Server API is not.  But for Client to be able to know
all about fields names (mapping from original to new names, which ones
are required) it needs info from the Server.  The Client gets such
tables on instance instantiation through one web-service call that
grabs everything that pulls it appart into multiple DataField related
LUTs (LookUpTables, aka dictionaries).

Questions abound for use-cases.

1. Is it very important to be able to convert a record LIST to a
   single data structure? Example: for Pandas DataFrame we combine all
   vectors in a record into a 2D DataFrame.  What about those across
   records into a 3D DataFrame?

2. Should vectors and scalars be funadmentally separated? (see #1) If
   so, how do we avoid hard coding the distinction for every
   DataRelease?

3. There

"""


from abc import ABC, abstractmethod
import copy
import numpy as np
import pandas as pd
from specutils import Spectrum1D
import astropy.units as u
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
    def to_numpy(self, record, o2nLUT):
        """Convert FitsFile record to a structure that uses Numpy"""
        arflds = [
            'spectra.coadd.and_mask',
            'spectra.coadd.flux',
            'spectra.coadd.ivar',
            'spectra.coadd.loglam',
            'spectra.coadd.model',
            'spectra.coadd.or_mask',
            'spectra.coadd.sky',
            'spectra.coadd.wdisp',
            ]
        lofl = [record[o2nLUT[f]] for f in arflds if f in o2nLUT]
        newrec = dict(coadd = np.array(lofl))
        for orig,new in o2nLUT.items():
            if orig in arflds:
                continue
            newrec[new] = record[new]
        return(newrec)

    def to_spectrum1d(self, record, o2nLUT):
        arflds = [
            'spectra.coadd.flux',
            'spectra.coadd.ivar',
            'spectra.coadd.loglam',
            ]

        loglam = record[o2nLUT['spectra.coadd.loglam']]
        flux = record[o2nLUT['spectra.coadd.flux']]
        ivar = record[o2nLUT['spectra.coadd.ivar']]

        wavelength = (10**np.array(loglam))*u.AA
        flux = np.array(flux)*u.Jy
        ivar = InverseVariance(np.array(ivar))
        z = record.get('red_shift')

        newrec = dict(
            # flux, uncertainty, wavevelength, mask(or, and), redshift
            spec1d = Spectrum1D(spectral_axis=wavelength,
                                flux=flux,
                                uncertainty=ivar,
                                redshift=z),
            )
        for orig,new in o2nLUT.items():
            if orig in arflds:
                continue
            newrec[new] = record[new]

        return(newrec)


    def to_pandas(self, record, o2nLUT):
        arflds = [
            'spectra.coadd.and_mask',
            'spectra.coadd.flux',
            'spectra.coadd.ivar',
            'spectra.coadd.loglam',
            'spectra.coadd.model',
            'spectra.coadd.or_mask',
            'spectra.coadd.sky',
            'spectra.coadd.wdisp',
            ]
        lofl = [record[o2nLUT[f]] for f in arflds if f in o2nLUT]
        newrec = dict(df = pd.DataFrame(lofl))
        for orig,new in o2nLUT.items():
            if orig in arflds:
                continue
            newrec[new] = record[new]
        return(newrec)


class BossDr16(Convert):
    def to_numpy(self, record, o2nLUT):
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
        newrec = dict(coadd = np.array(lofl))
        for orig,new in o2nLUT.items():
            if orig in arflds:
                continue
            newrec[new] = record[new]
        return(newrec)

    def to_spectrum1d(self, record, o2nLUT):
        arflds = [
            'spectra.coadd.FLUX',
            'spectra.coadd.IVAR',
            'spectra.coadd.LOGLAM',
            ]

        loglam = record[o2nLUT['spectra.coadd.LOGLAM']]
        flux = record[o2nLUT['spectra.coadd.FLUX']]
        ivar = record[o2nLUT['spectra.coadd.IVAR']]

        wavelength = (10**np.array(loglam))*u.AA
        flux = np.array(flux)*u.Jy
        ivar = InverseVariance(np.array(ivar))
        z = record.get('red_shift')

        newrec = dict(
            # flux, uncertainty, wavevelength, mask(or, and), redshift
            spec1d = Spectrum1D(spectral_axis=wavelength,
                                flux=flux,
                                uncertainty=ivar,
                                redshift=z),
            )
        for orig,new in o2nLUT.items():
            if orig in arflds:
                continue
            newrec[new] = record[new]
        return(newrec)

    def to_pandas(self, record, o2nLUT):
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
        newrec = dict(df = pd.DataFrame(lofl))
        for orig,new in o2nLUT.items():
            if orig in arflds:
                continue
            newrec[new] = record[new]
        return(newrec)


class DesiDenali(Convert):
    def to_numpy(self, record, o2nLUT):
        arflds = [
            'spectra.b_flux',
            'spectra.b_ivar',
            'spectra.b_mask',
            'spectra.b_wavelength',
            'spectra.r_flux',
            'spectra.r_ivar',
            'spectra.r_mask',
            'spectra.r_wavelength',
            'spectra.z_flux',
            'spectra.z_ivar',
            'spectra.z_mask',
            'spectra.z_wavelength',
        ]
        lofl = [record[o2nLUT[f]] for f in arflds if f in o2nLUT]
        newrec = dict(coadd = np.array(lofl))
        for orig,new in o2nLUT.items():
            if orig in arflds:
                continue
            newrec[new] = record[new]
        return(newrec)


    def to_spectrum1d(self, record, o2nLUT):
        arflds = [
            'spectra.b_flux',
            'spectra.b_ivar',
            'spectra.b_mask',
            'spectra.b_wavelength',
            'spectra.r_flux',
            'spectra.r_ivar',
            'spectra.r_mask',
            'spectra.r_wavelength',
            'spectra.z_flux',
            'spectra.z_ivar',
            'spectra.z_mask',
            'spectra.z_wavelength',
        ]

        loglam_b = record[o2nLUT['spectra.b_wavelength']]
        flux_b = record[o2nLUT['spectra.b_flux']]
        ivar_b = record[o2nLUT['spectra.b_ivar']]

        wavelength_b = (10**np.array(loglam_b))*u.AA
        flux_b = np.array(flux_b)*u.Jy
        ivar_b = InverseVariance(np.array(ivar_b))
        z = record.get('red_shift')

        newrec = dict(
            # flux, uncertainty, wavevelength, mask(or, and), redshift
            b_spec1d = Spectrum1D(spectral_axis=wavelength_b,
                                  flux=flux_b,
                                  uncertainty=ivar_b,
                                  redshift=z),
            r_spec1d = Spectrum1D(spectral_axis=wavelength_r,
                                  flux=flux_r,
                                  uncertainty=ivar_r,
                                  redshift=z),
            z_spec1d = Spectrum1D(spectral_axis=wavelength_z,
                                  flux=flux_z,
                                  uncertainty=ivar_z,
                                  redshift=z),
            )
        for orig,new in o2nLUT.items():
            if orig in arflds:
                continue
            newrec[new] = record[new]
        return(newrec)


    def to_pandas(self, record, o2nLUT):
        arflds = [
            'spectra.b_flux',
            'spectra.b_ivar',
            'spectra.b_mask',
            'spectra.b_wavelength',
            'spectra.r_flux',
            'spectra.r_ivar',
            'spectra.r_mask',
            'spectra.r_wavelength',
            'spectra.z_flux',
            'spectra.z_ivar',
            'spectra.z_mask',
            'spectra.z_wavelength',
        ]
        lofl = [record[o2nLUT[f]] for f in arflds if f in o2nLUT]
        newrec = dict(df = pd.DataFrame(lofl))
        for orig,new in o2nLUT.items():
            if orig in arflds:
                continue
            newrec[new] = record[new]
        return(newrec)



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
    required = set(client.required[dr])
    if include is not None:
        nuke = set(n2oLUT.keys()).difference(required.union(include))
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
