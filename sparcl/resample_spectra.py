# NOT INTENDED FOR PUBLIC USE!
#
# See:
#   https://spectres.readthedocs.io/en/latest/
import math
import spectres
import numpy as np

# Local
import sparcl.client


# Per paper, should be able to pass all flux in one call to spectres
# https://arxiv.org/pdf/1705.05165.pdf
# Perhaps users would rather the bins uniform (1,5,20 Angstroms?)
def _resample_flux(records, wavstep=1):
    smallest = math.floor(min([min(r.wavelength) for r in records]))
    largest = math.ceil(max([max(r.wavelength) for r in records]))

    #!wrange = largest - smallest
    # new_wavs = np.fro<mfunction(lambda i: i + smallest, (wrange,), dtype=int)
    # flux_2d = np.ones([len(records), wrange])

    new_wavs = np.array(range(smallest, largest + 1, wavstep))
    flux_2d = np.full([len(records), len(new_wavs)], None, dtype=float)

    for idx, rec in enumerate(records):
        flux_2d[idx] = spectres.spectres(
            new_wavs, rec.wavelength, rec.flux, verbose=False
        )
    return flux_2d, new_wavs


def _tt0(numrecs=20):
    client = sparcl.client.SparclClient()
    found = client.find(
        constraints=dict(data_release=["BOSS-DR16"]), limit=numrecs
    )
    got = client.retrieve(found.ids)
    flux_2d, new_wavs = _resample_flux(got.records)
    return flux_2d, new_wavs
