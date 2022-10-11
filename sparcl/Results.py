"""Containers for results from SPARCL Server.
These include results of client.retrieve() client.find().
"""

from collections import UserList
#!import copy
from sparcl.utils import _AttrDict
#from sparcl.gather_2d import bin_spectra_records


class Results(UserList):

    def __init__(self, dict_list, client=None):
        super().__init__(dict_list)
        self.hdr = dict_list[0]
        self.recs = dict_list[1:]
        self.client = client
        self.fields = client.fields
        self.to_science_fields()
        self.hdr['Count'] = len(self.recs)

    # https://docs.python.org/3/library/collections.html#collections.deque.clear
    def clear(self):
        """Delete the contents of this collection."""
        super().clear()
        self.hdr = {}
        self.recs = []

    @property
    def info(self):
        """Info about this collection.
        e.g. Warnings, parameters used to get the collection, etc."""
        return self.hdr

    @property
    def count(self):
        """Number of records in this collection."""
        return self.hdr['Count']
        return self.hdr['Count']

    @property
    def records(self):
        """Records in this collection. Each record is a dictionary."""
        return self.recs

    def json(self):
        return self.data

    # Convert Internal field names to Science field names.
    # SIDE-EFFECT: modifies self.recs
    def to_science_fields(self):  # from_orig
        newrecs = list()
        for rec in self.recs:
            newrec = dict()
            dr = rec['_dr']
            keep = True
            for orig in rec.keys():
                if orig == '_dr':
                    # keep DR around unchanged. We need it to rename back
                    # to Internal Field Names later.
                    newrec[orig] = rec[orig]
                else:
                    new = self.fields._science_name(orig, dr)
                    if new is None:
                        keep = False
                    newrec[new] = rec[orig]
            if keep:
                newrecs.append(_AttrDict(newrec))
        self.recs = newrecs

    # Convert Science field names to Internal field names.
    def to_internal_fields(self):
        for rec in self.recs:
            dr = rec.get('_dr')
            for new in rec.keys():
                if new == '_dr':
                    # keep DR around unchanged. We need it to rename back
                    # to Internal Field Names later.
                    continue
                new = self.fields._internal_name(new, dr)
                rec[new] = rec.pop(new)


# For results of retrieve()
class Retrieved(Results):
    """Holds spectra records (and header)."""

    def __init__(self, dict_list, client=None):
        super().__init__(dict_list, client=client)

    def __repr__(self):
        return f'Retrieved Results: {len(self.recs)} records'

#!    def bin_spectra(self):
#!        """Align flux from all records by common wavelength bin.
#!
#!        A value of nan is used where a record does not contain a flux
#!        value for a specific bin.
#!
#!        Returns:
#!           flux: 2d numpy array with shape (numRecords, numWavelengthBins)
#!                 Flux value for each record, each bin
#!           wavs: 1d numpy array with shape (numWavelengthBins)
#!                 Wavelength values for each bin
#!
#!        Example:
#!            >>> client = sparcl.client.SparclClient()
#!            >>> found = client.find(
#!                            constraints={"data_release": ['BOSS-DR16']},
#!                            limit=10)
#!            >>> got = client.retrieve(found.ids)
#!            >>> flux2d,wavs = got.bin_spectra()
#!
#!        """
#!        flux2d, wavs = bin_spectra_records(self.recs)
#!        return flux2d, wavs


class Found(Results):
    """Holds metadata records (and header)."""

    def __init__(self, dict_list, client=None):
        super().__init__(dict_list, client=client)

    def __repr__(self):
        return f'Find Results: {len(self.recs)} records'

    @property
    def ids(self):
        """List of unique identifiers of matched records."""
        dr = list(self.fields.all_drs)[0]
        idfld = self.fields._science_name('id', dr)

        return [d.get(idfld) for d in self.recs]
