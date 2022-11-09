# See:
#   https://spectres.readthedocs.io/en/latest/
# For info about problems with floating point,
#   See:  https://docs.python.org/3/tutorial/floatingpoint.html
#   Also: https://docs.python.org/3/library/decimal.html#floating-point-notes
#
import math
from decimal import Decimal
#
import spectres
import numpy as np
#
import sparcl.client


# Per paper, should be able to pass all flux in one call to spectres
# https://arxiv.org/pdf/1705.05165.pdf
# Perhaps users would rather the bins uniform (1,5,20 Angstroms?)
def resample_flux(records, wavstep=1):
    smallest = math.floor(min([min(r.wavelength) for r in records]))
    largest = math.ceil(max([max(r.wavelength) for r in records]))

    #!wrange = largest - smallest
    #new_wavs = np.fromfunction(lambda i: i + smallest, (wrange,), dtype=int)
    #flux_2d = np.ones([len(records), wrange])

    new_wavs = np.array(range(smallest, largest + 1, wavstep))
    flux_2d = np.full([len(records), len(new_wavs)], None, dtype=float)

    for idx, rec in enumerate(records):
        flux_2d[idx] = spectres.spectres(new_wavs,
                                         rec.wavelength,
                                         rec.flux,
                                         verbose=False)
    return flux_2d, new_wavs


def tt0(numrecs=20):
    client = sparcl.client.SparclClient()
    found = client.find(constraints=dict(data_release=['BOSS-DR16']),
                        limit=numrecs)
    got = client.retrieve(found.ids)
    flux_2d, new_wavs = resample_flux(got.records)
    return flux_2d, new_wavs


# Map every wavelength of every record to index (ri,wi)
# where
#   ri: Record Index
#   wi: Window Index (offset of wavelength in WINDOW)
#   window: ordered list of wavelengths that include ALL unique
#           wavelengths in all records
#! def rec_woffset(records, window):
#!     ar = np.ones([len(records), len(window)])
#!     for ri, r in enumerate(records):
#!         for wl in r.wavelength:
#!             try:
#!                 wi = window.index(wl)
#!             except:
#!                 continue
#!             ar[ri,wi] = wl
#!     return ar


def wavelength_offsets(records):
    # sorted list of wavelengths from ALL records
    window = sorted(
        set(records[0].wavelength).union(*[r.wavelength for r in records[1:]]))
    # offsets[ri] = index into WINDOW
    offsets = {ri: window.index(rec.wavelength[0])
               for ri, rec in enumerate(records)}
    return(window, offsets)


def validate_wavelength_alignment(records, window, offsets, precision=None):
    PLACES = Decimal(10) ** -precision if precision is not None else None
    #! print(f'DBG: PLACES={PLACES}')
    # Given an exact wavelength match between first wl (wavelength) in a rec
    # and the wl at its offset of WINDOW, ensure all the remaning wls
    # in rec match the next N wls of WINDOW.
    for ri, rec in enumerate(records):
        for wi, rwl in enumerate(rec.wavelength):  # wi=recwavelengthIndex
            if precision is None:
                recwl = Decimal(rwl)
            else:
                recwl = Decimal(rwl).quantize(PLACES)
            wwl = window[offsets[ri] + wi]
            msg = (f'Wavelength in '
                   f'Record[{ri}][{wi}] ({recwl}) does not match '
                   f'Window[{offsets[ri]+wi} = offset[{ri}]={offsets[ri]} '
                   f'+ {wi}]  ({wwl})'
                   )
            assert recwl == wwl, msg
            # f'RecWL[{wi}] {rwl} != WindowWL[{offsets[ri+wi]}] {wwl} '
            # f'offset={offsets[ri]}')


# We want to align a bunch of records by wavelength into a single
# 2d numpy array (record vs wavelength).  In general, we
# are not guaranteed that this is possible -- even if using only
# records from a single DataSet. So validate it first.
# (If not valid, allowing wavelength slop might help.)
def align_wavelengths(records):
    window, offsets = wavelength_offsets(records)
    validate_wavelength_alignment(records, window, offsets)
    ar = np.ones([len(records), len(window)])
    for ri, r in enumerate(records):
        for wi, wl in enumerate(r.wavelength):
            ar[ri, offsets[ri + wi]] = wl  # @@@WRONG!!! We want FLUX
    return ar


def tt1(numrecs=20, dr='BOSS-DR16'):
    client = sparcl.client.SparclClient()
    found = client.find(constraints=dict(data_release=[dr]),
                        limit=numrecs)
    got = client.retrieve(found.ids)
    records = got.records
    window, offsets = wavelength_offsets(records)
    print(f'Built window len={len(window)}; offsets={offsets}')
    #return records, window, offsets
    ar = align_wavelengths(records)
    return ar


# precision:: number of decimal places
def wavelength_grid_offsets(records, precision=11):
    PLACES = Decimal(10) ** -precision

    # set of wavelengths from ALL records. Quantized to precision
    gset = set()  # Grid SET
    for r in records:
        gset.update([Decimal(w).quantize(PLACES) for w in r.wavelength])
    grid = sorted(gset)  # 1D sorted list of wavelengths (bigger than any rec)
    #! print(f'DBG grid({len(grid)})[:10]={grid[:10]}')
    # offsets[ri] = index into GRID
    offsets = {ri: grid.index(Decimal(rec.wavelength[0]).quantize(PLACES))
               for ri, rec in enumerate(records)}
    return(grid, offsets)


# return 2D numpy array of FLUX values that is aligned to wavelength GRID.
# GRID is generally wider than flux for single record. Pad with NaN.
def flux_grid(records, grid, offsets, precision=None):
    validate_wavelength_alignment(records, grid, offsets, precision=precision)
    ar = np.full([len(records), len(grid)], np.nan)
    for ri, r in enumerate(records):
        for fi, flux in enumerate(r.flux):
            ar[ri, offsets[ri] + fi] = flux
    return ar


def flux_records(records, precision=None):
    grid, offsets = wavelength_grid_offsets(records, precision=precision)
    ar = flux_grid(records, grid, offsets, precision=precision)
    return ar, grid


def tt(numrecs=9, dr='BOSS-DR16', precision=7):
    # Get sample of NUMRECS records from DR DataSet.
    client = sparcl.client.SparclClient()
    found = client.find(constraints=dict(data_release=[dr]),
                        limit=numrecs)
    got = client.retrieve(found.ids)
    records = got.records

    #! grid, offsets = wavelength_grid_offsets(records, precision=precision)
    #! print(f'Built grid len={len(grid)} '
    #!       f'offsets({len(offsets)})[:5]={list(offsets.values())[:5]}')
    #! ar = flux_grid(records, grid, offsets, precision=precision)
    ar, grid = flux_records(records, precision=precision)
    return ar, grid  # ar (numRecs,len(grid))
# with np.printoptions(threshold=np.inf, linewidth=210, formatter=dict(float=lambda v: f'{v: > 7.3f}')): print(ar.T)  # noqa: E501
