# See:
#   https://spectres.readthedocs.io/en/latest/

import math
import spectres
import numpy as np
#
import sparcl.client


def bin_spectra_records(records):
    smallest = min([min(r.wavelength) for r in records])
    largest = max([max(r.wavelength) for r in records])
    range = math.ceil(largest - smallest)
    new_wavs = np.fromfunction(lambda i: i + smallest, [range], dtype=int)

    flux_2d = np.ones([len(records), range])

    for idx, rec in enumerate(records):
        flux_2d[idx] = spectres.spectres(new_wavs,
                                         rec.wavelength,
                                         rec.flux,
                                         verbose=False)
    return flux_2d, new_wavs


def tt(numrecs=20):
    client = sparcl.client.SparclClient()
    found = client.find(constraints=dict(data_release=['BOSS-DR16']),
                        limit=numrecs)
    got = client.retrieve(found.ids)
    flux_2d, new_wavs = bin_spectra_records(got.records)
    return flux_2d, new_wavs
