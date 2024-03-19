"""Align or resample spectra related fields across multiple records."""

# See client.py for Doctest example
#
# For info about problems with floating point,
#   See:  https://docs.python.org/3/tutorial/floatingpoint.html
#   Also: https://docs.python.org/3/library/decimal.html#floating-point-notes
#
from decimal import Decimal

#
import numpy as np

#
import sparcl.client


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


def _wavelength_offsets(records):
    # sorted list of wavelengths from ALL records
    window = sorted(
        set(records[0].wavelength).union(*[r.wavelength for r in records[1:]])
    )
    # offsets[ri] = index into WINDOW
    offsets = {
        ri: window.index(rec.wavelength[0]) for ri, rec in enumerate(records)
    }
    return (window, offsets)


def _validate_wavelength_alignment(records, window, offsets, precision=None):
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
            #! msg = (f'Wavelength in '
            #!        f'Record[{ri}][{wi}] ({recwl}) does not match '
            #!        f'Window[{offsets[ri]+wi} = offset[{ri}]={offsets[ri]} '
            #!        f'+ {wi}]  ({wwl})'
            #!        )
            #! assert recwl == wwl, msg
            if recwl != wwl:
                msg = (
                    f"The spectra cannot be aligned with the given"
                    f' "precision" parameter ({precision}).'
                    f" Try lowering the precision value."
                )
                raise Exception(msg)


# We want to align a bunch of records by wavelength into a single
# 2d numpy array (record vs wavelength).  In general, we
# are not guaranteed that this is possible -- even if using only
# records from a single DataSet. So validate it first.
# (If not valid, allowing wavelength slop might help.)
def _align_wavelengths(records):
    window, offsets = _wavelength_offsets(records)
    _validate_wavelength_alignment(records, window, offsets)
    ar = np.ones([len(records), len(window)])
    for ri, r in enumerate(records):
        for wi, wl in enumerate(r.wavelength):
            ar[ri, offsets[ri + wi]] = wl  # @@@WRONG!!! We want FLUX
    return ar


def _tt1(numrecs=20, dr="BOSS-DR16"):
    client = sparcl.client.SparclClient()
    found = client.find(constraints=dict(data_release=[dr]), limit=numrecs)
    got = client.retrieve(found.ids)
    records = got.records
    window, offsets = _wavelength_offsets(records)
    print(f"Built window len={len(window)}; offsets={offsets}")
    # return records, window, offsets
    ar = _align_wavelengths(records)
    return ar


# precision:: number of decimal places
# "records" must contain "wavelength" field.
def _wavelength_grid_offsets(records, precision=11):
    PLACES = Decimal(10) ** -precision

    # set of wavelengths from ALL records. Quantized to precision
    gset = set()  # Grid SET
    for r in records:
        gset.update([Decimal(w).quantize(PLACES) for w in r.wavelength])
    grid = sorted(gset)  # 1D sorted list of wavelengths (bigger than any rec)
    #! print(f'DBG grid({len(grid)})[:10]={grid[:10]}')
    # offsets[ri] = index into GRID
    offsets = {
        ri: grid.index(Decimal(rec.wavelength[0]).quantize(PLACES))
        for ri, rec in enumerate(records)
    }
    return (grid, offsets)


# return 2D numpy array of FLUX values that is aligned to wavelength GRID.
# GRID is generally wider than flux for single record. Pad with NaN.
def _flux_grid(records, grid, offsets, precision=None):
    _validate_wavelength_alignment(records, grid, offsets, precision=precision)
    ar = np.full([len(records), len(grid)], np.nan)
    for ri, r in enumerate(records):
        for fi, flux in enumerate(r.flux):
            ar[ri, offsets[ri] + fi] = flux
    return ar


# RETURN 2D nparray(records,wavelengthGrid) = fieldValue
def _field_grid(records, fieldName, grid, offsets, precision=None):
    ar = np.full([len(records), len(grid)], np.nan)
    for ri, r in enumerate(records):
        for fi, fieldValue in enumerate(r[fieldName]):
            ar[ri, offsets[ri] + fi] = fieldValue
    return ar  # (wavelengthGrid, records)


# RETURN 2D nparray(fields,wavelengthGrid) = fieldValue
#! def rec_grid(rec, fields, grid, offsets, precision=None):
#!     ar = np.full([len(fields), len(grid)], np.nan)
#!     ri = 0
#!     for fi, fieldValue in enumerate(r[fieldName]):
#!         ar[ri, offsets[ri] + fi] = fieldValue
#!     return ar  # (wavelengthGrid, fields)


# Align flux from records into one array using quantization
#! def flux_records(records, precision=None):
#!     grid, offsets = wavelength_grid_offsets(records, precision=precision)
#!     ar = _flux_grid(records, grid, offsets, precision=precision)
#!     return ar, np.array([float(x) for x in grid])


def _validate_spectra_fields(records, fields):
    #! spectra_fields = [
    #!     client.fields.n2o["BOSS-DR16"][k]
    #!     for k, v in client.fields.attrs["BOSS-DR16"].items()
    #!     if v["storage"] == "S"
    #! ]
    [k for k in records[0].keys() if not k.startswith("_")]


# TOP level: Intended for access from Jupyter NOTEBOOK.
# Align spectra related field from records into one array using quantization.
def align_records(records, fields=["flux", "wavelength"], precision=7):
    """Align given spectra-type fields to a common wavelength grid.

    Args:
        records (list): List of dictionaries.
            The keys for all these dictionaries are Science Field Names.

        fields (:obj:`list`, optional): List of Science Field Names of
            spectra related fields to align and include in the results.
            DEFAULT=['flux', 'wavelength']

        precision (:obj:`int`, optional): Number of decimal points to use for
            quantizing wavelengths into a grid.
            DEFAULT=7

    Returns:
        tuple containing:
        - ar_dict(dict): Dictionary of 2D numpy arrays keyed by Field Name.
              Each array is shape: (numRecs, numzGridWavelengths)
        - grid(ndarray): 1D numpy array containing wavelength values.

    Example:
        >>> client = sparcl.client.SparclClient()
        >>> specflds = ['wavelength', 'model']
        >>> cons = {"data_release": ['BOSS-DR16']}
        >>> found = client.find(constraints=cons, limit=21)
        >>> got = client.retrieve(found.ids, include=specflds)
        >>> ar_dict, grid = align_records(got.records, fields=specflds)
        >>> ar_dict['model'].shape
        (21, 4669)

    """
    # Report Garbage In
    if "wavelength" not in fields:
        msg = (
            f'You must provide "wavelength" in the list provided'
            f' in the "fields" paramter.  Got: {fields}'
        )
        raise Exception(msg)
    if "wavelength" not in records[0]:
        msg = (
            f'Records must contain the "wavelength" field.'
            f" The first record contains fields: {sorted(records[0].keys())}"
        )
        raise Exception(msg)

    #! _validate_spectra_fields(records, fields)
    grid, offsets = _wavelength_grid_offsets(records, precision=precision)
    _validate_wavelength_alignment(records, grid, offsets, precision=precision)

    # One slice for each field; each slice a 2darray(wavelength, record)=fldVal
    adict = dict()
    for fld in fields:
        ar = _field_grid(records, fld, grid, offsets, precision=None)
        adict[fld] = ar

    return adict, np.array([float(x) for x in grid])


# with np.printoptions(threshold=np.inf, linewidth=210,
#   formatter=dict(float=lambda v: f'{v: > 7.3f}')): print(ar.T)  # noqa: E501

if __name__ == "__main__":
    import doctest

    doctest.testmod()
