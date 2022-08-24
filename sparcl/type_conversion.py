# Python Standard Library
from abc import ABC, abstractmethod
import copy
#!from pprint import pformat
from enum import Enum, auto
# External Packages
import numpy as np
#!import pandas as pd
from specutils import Spectrum1D
import astropy.units as u
from astropy.nddata import InverseVariance
# Local Packages
import sparcl.exceptions as ex


"""It would be much better if this were abstracted and easier to
update with new Data Types and new DataReleases.  Perhaps use
something like the Server "Personalities".  I've rejected abstracting
for now because I think we need operational experience with the DataType
feature and how it interacts with other features (especially global
Rename and retrieve(INCLUDE).

DataType conversion should be done completely within the Client, not
on the Server.  The obvious reason is Clients are language
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

"""


# Replace all uses of string rtype with enum @@@
class Rtype(Enum):
    JSON = auto()
    NUMPY = auto()
    PANDAS = auto()
    SPECTRUM1D = auto()


class Convert(ABC):
    """Convert JSON record to mix of plain python
       and selected data record type.
    """

    @abstractmethod
    def to_numpy(self, record, o2nLUT):
        newrec = copy.deepcopy(record)
        return(newrec)

    @abstractmethod
    def to_spectrum1d(self, record, o2nLUT):
        newrec = copy.deepcopy(record)
        return(newrec)

#!    @abstractmethod
#!    def to_pandas(self, record, o2nLUT):
#!        newrec = copy.deepcopy(record)
#!        return(newrec)


class NoopConvert(Convert):
    def to_numpy(self, record, o2nLUT):
        return(record)

    def to_spectrum1d(self, record, o2nLUT):
        return(record)

    def to_pandas(self, record, o2nLUT):
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
        newrec = dict(nparr=np.array(lofl))
        for orig, new in o2nLUT.items():
            if orig in arflds:
                continue
            if new in record:
                newrec[new] = record[new]
        return(newrec)

    # Sdss
    def to_spectrum1d(self, record, o2nLUT):
        arflds = [
            'red_shift',
            'spectra.coadd.flux',
            'spectra.coadd.ivar',
            'spectra.coadd.loglam',
            'spectra.coadd.and_mask',
        ]

        loglam = record[o2nLUT['spectra.coadd.loglam']]
        flux = record[o2nLUT['spectra.coadd.flux']]
        ivar = record[o2nLUT['spectra.coadd.ivar']]
        and_mask = record[o2nLUT['spectra.coadd.and_mask']]

        wavelength = (10**np.array(loglam)) * u.AA
        flux = np.array(flux) * 10 ** -17 * u.Unit('erg cm-2 s-1 AA-1')
        ivar = InverseVariance(np.array(ivar))
        z = record.get('red_shift')

        newrec = dict(
            # flux, uncertainty, wavevelength, mask(and), redshift
            spec1d=Spectrum1D(spectral_axis=wavelength,
                              flux=flux,
                              uncertainty=ivar,
                              redshift=z,
                              mask=and_mask),
        )
        for orig, new in o2nLUT.items():
            if orig in arflds:
                continue
            if new in record:
                newrec[new] = record[new]

        return(newrec)


#!    def to_pandas(self, record, o2nLUT):
#!        arflds = [
#!            'spectra.coadd.and_mask',
#!            'spectra.coadd.flux',
#!            'spectra.coadd.ivar',
#!            'spectra.coadd.loglam',
#!            'spectra.coadd.model',
#!            'spectra.coadd.or_mask',
#!            'spectra.coadd.sky',
#!            'spectra.coadd.wdisp',
#!            ]
#!        dfdict = dict((o2nLUT[f], record[o2nLUT[f]])
#!                      for f in arflds if f in o2nLUT)
#!        newrec = dict(df = pd.DataFrame(dfdict))
#!        for orig,new in o2nLUT.items():
#!            if orig in arflds:
#!                continue
#!            if new in record:
#!                newrec[new] = record[new]
#!        return(newrec)


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
        newrec = dict(nparr=np.array(lofl))
        for orig, new in o2nLUT.items():
            # Don't carry over the fields used to build the new datatype.
            # This would be duplication since their content is already
            # in the new datatype.
            if orig in arflds:
                continue
            if new in record:
                newrec[new] = record[new]
        return(newrec)

    # BOSS
    def to_spectrum1d(self, record, o2nLUT):
        arflds = [
            'red_shift',
            'spectra.coadd.FLUX',
            'spectra.coadd.IVAR',
            'spectra.coadd.LOGLAM',
            'spectra.coadd.AND_MASK',
        ]
        loglam = record[o2nLUT['spectra.coadd.LOGLAM']]
        flux = record[o2nLUT['spectra.coadd.FLUX']]
        ivar = record[o2nLUT['spectra.coadd.IVAR']]
        and_mask = record[o2nLUT['spectra.coadd.AND_MASK']]

        wavelength = (10**np.array(loglam)) * u.AA
        flux = np.array(flux) * 10 ** -17 * u.Unit('erg cm-2 s-1 AA-1')
        ivar = InverseVariance(np.array(ivar))
        z = record.get('red_shift')

        newrec = dict(
            # flux, uncertainty, wavelength, mask(and), redshift
            spec1d=Spectrum1D(spectral_axis=wavelength,
                              flux=flux,
                              uncertainty=ivar,
                              redshift=z,
                              mask=and_mask),
        )
        for orig, new in o2nLUT.items():
            if orig in arflds:
                continue
            if new in record:
                newrec[new] = record[new]
        return(newrec)

#!    def to_pandas(self, record, o2nLUT): # BOSS
#!        arflds = [
#!            'spectra.coadd.AND_MASK',
#!            'spectra.coadd.FLUX',
#!            'spectra.coadd.IVAR',
#!            'spectra.coadd.LOGLAM',
#!            'spectra.coadd.MODEL',
#!            'spectra.coadd.OR_MASK',
#!            'spectra.coadd.SKY',
#!            'spectra.coadd.WDISP',
#!            ]
#!        dfdict = dict((o2nLUT[f], record[o2nLUT[f]])
#!                      for f in arflds if f in o2nLUT)
#!        newrec = dict(df = pd.DataFrame(dfdict))
#!        for orig,new in o2nLUT.items():
#!            if orig in arflds:
#!                continue
#!            if new in record:
#!                newrec[new] = record[new]
#!        return(newrec)


class Desi(Convert):
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
        newrec = dict(nparr=np.array(lofl))
        for orig, new in o2nLUT.items():
            if orig in arflds:
                continue
            if new in record:
                newrec[new] = record[new]
        return(newrec)

    def to_spectrum1d(self, record, o2nLUT):  # Desi
        arflds = [
            'red_shift',
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

        z = record.get('red_shift')

        # _b
        wavelength_b = record[o2nLUT['spectra.b_wavelength']]
        flux_b = record[o2nLUT['spectra.b_flux']]
        ivar_b = record[o2nLUT['spectra.b_ivar']]
        mask_b = record[o2nLUT['spectra.b_mask']]
        # Define units
        wavelength_b = np.array(wavelength_b) * u.AA
        flux_b = np.array(flux_b) * 10 ** -17 * u.Unit('erg cm-2 s-1 AA-1')
        ivar_b = InverseVariance(np.array(ivar_b))

        # _r
        wavelength_r = record[o2nLUT['spectra.r_wavelength']]
        flux_r = record[o2nLUT['spectra.r_flux']]
        ivar_r = record[o2nLUT['spectra.r_ivar']]
        mask_r = record[o2nLUT['spectra.r_mask']]
        # Define units
        wavelength_r = np.array(wavelength_r) * u.AA
        flux_r = np.array(flux_r) * 10 ** -17 * u.Unit('erg cm-2 s-1 AA-1')
        ivar_r = InverseVariance(np.array(ivar_r))

        # _z
        wavelength_z = record[o2nLUT['spectra.z_wavelength']]
        flux_z = record[o2nLUT['spectra.z_flux']]
        ivar_z = record[o2nLUT['spectra.z_ivar']]
        mask_z = record[o2nLUT['spectra.z_mask']]
        # Define units
        wavelength_z = np.array(wavelength_z) * u.AA
        flux_z = np.array(flux_z) * 10 ** -17 * u.Unit('erg cm-2 s-1 AA-1')
        ivar_z = InverseVariance(np.array(ivar_z))

        newrec = dict(
            # flux, uncertainty, wavevelength, mask, redshift
            b_spec1d=Spectrum1D(spectral_axis=wavelength_b,
                                flux=flux_b,
                                uncertainty=ivar_b,
                                redshift=z,
                                mask=mask_b),
            r_spec1d=Spectrum1D(spectral_axis=wavelength_r,
                                flux=flux_r,
                                uncertainty=ivar_r,
                                redshift=z,
                                mask=mask_r),
            z_spec1d=Spectrum1D(spectral_axis=wavelength_z,
                                flux=flux_z,
                                uncertainty=ivar_z,
                                redshift=z,
                                mask=mask_z),
        )
        for orig, new in o2nLUT.items():
            if orig in arflds:
                continue
            if new in record:
                newrec[new] = record[new]
        return(newrec)


class DesiDenali(Desi):
    pass


class DesiEverest(Desi):
    pass


# DR Instance LookUp Table
diLUT = {
    'SDSS-DR16': SdssDr16(),
    'BOSS-DR16': BossDr16(),
    'DESI-denali': DesiDenali(),
    'DESI-everest': DesiEverest(),
    #'Unknown': NoopConvert(),
}


def convert(record, rtype, client, include, verbose=False):
    if rtype is None:
        return record

    dr = record['_dr']

    # Validate parameters
    if dr not in diLUT:
        allowed = ', '.join(list(diLUT.keys()))
        msg = (f'The Data Set associated with a records, "{dr}",'
               f' is not supported for Type Conversion.'
               f' Available Data Sets are: {allowed}.')
        raise ex.UnkDr(msg)

    drin = diLUT.get(dr, NoopConvert())

    o2nLUT = copy.copy(client.orig2newLUT[dr])  # orig2newLUT[dr][orig] = new
    o2nLUT['_dr'] = '_dr'
    #!n2oLUT = client.new2origLUT[dr]
    #!required = set(client.required[dr])
    #!if include is not None:
    #!    nuke = set(n2oLUT.keys()).difference(required.union(include))
    #!    for new in nuke:
    #!        del o2nLUT[n2oLUT[new]]

    if rtype == 'json':
        return record
    elif rtype == 'numpy':
        return drin.to_numpy(record, o2nLUT)
    elif rtype == 'pandas':
        return drin.to_pandas(record, o2nLUT)
    elif rtype == 'spectrum1d':
        return drin.to_spectrum1d(record, o2nLUT)
    else:
        raise Exception(f'Unknown record type ({rtype})')
    return None
