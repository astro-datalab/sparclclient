"""Containers for results from SPARCL Server.
These include results of client.retrieve() client.find().
"""

from collections import UserList
#!import copy
from sparcl.utils import _AttrDict
#from sparcl.gather_2d import bin_spectra_records
import sparcl.exceptions as ex
from warnings import warn


class Results(UserList):

    def __init__(self, dict_list, client=None):
        super().__init__(dict_list)
        self.hdr = dict_list[0]
        self.recs = dict_list[1:]
        self.client = client
        self.fields = client.fields
        self.to_science_fields()

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
        return len(self.recs)

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

    def science_to_internal_fields(self):
        newrecs = list()
        for rec in self.recs:
            newrec = dict()
            dr = rec['_dr']
            keep = True
            for sci_name in rec.keys():
                if sci_name == '_dr':
                    # keep DR around unchanged. We need it to rename back
                    # to Internal Field Names later.
                    newrec[sci_name] = rec[sci_name]
                else:
                    new = self.fields._internal_name(sci_name, dr)
                    if new is None:
                        keep = False
                    newrec[new] = rec[sci_name]
            if keep:
                newrecs.append(_AttrDict(newrec))
        self.recs = newrecs
        return self.recs

    def reorder(self, ids_og):
        """
        Reorder the retrieved records to be in the same
        order as the original IDs passed to client.retrieve().

        Args:
            ids_og (:obj:`list`): List of sparcl_ids or specIDs.

        Returns:
            reordered (:class:`~sparcl.Results.Retrieved`): Contains header and
                                                            reordered records.
            # none_idx (:obj:`list`): List of indices where record is None.

        """
        if len(ids_og) <= 0:
            msg = (f'The list of IDs passed to the reorder method '
                   f'does not contain any sparcl_ids or specIDs.')
            raise ex.NoIDs(msg)
        elif len(self.recs) <= 0:
            msg = (f'The retrieved or found results did not '
                   f'contain any records.')
            raise ex.NoRecords(msg)
        else:
            # Transform science fields to internal fields
            new_recs = self.science_to_internal_fields()
            # Get the ids or specids from retrieved records
            if type(ids_og[0]) == str:
                ids_re = [f['id'] for f in new_recs]
            elif type(ids_og[0]) == int:
                ids_re = [f['specid'] for f in new_recs]
            # Enumerate the original ids
            dict_og = {x: i for i, x in enumerate(ids_og)}
            # Enumerate the retrieved ids
            dict_re = {x: i for i, x in enumerate(ids_re)}
            # Get the indices of the original ids. Set to None if not found
            idx = [dict_re.get(key, None) for key in dict_og.keys()]
            # Get the indices of None values
            none_idx = [i for i, v in enumerate(idx) if v is None]
            # Reorder the retrieved records
            reordered = [self.recs[i] for i in idx if i is not None]
            # Insert dummy record(s) if applicable
            dummy_record = "{'id': None, 'specid': None, '_dr': 'SDSS-DR16'}"
            for i in none_idx:
                reordered.insert(i, {'id': None, 'specid': None,
                                     '_dr': 'SDSS-DR16'})
            reordered.insert(0, self.hdr)
            meta = reordered[0]
            if len(none_idx) > 0:
                msg = (f'{len(none_idx)} sparcl_ids or specIDs were '
                       f'not found in '
                       f'the database. Use "client.missing()" '
                       f'to get a list of the unavailable IDs. '
                       f'To maintain correct reordering, a dummy '
                       f'record has been placed at the indices '
                       f'where no record was found. Those '
                       f'indices are: {none_idx}. The dummy '
                       f'record will appear as follows: '
                       f'{dummy_record}. ')
                meta['status'].update({'warnings': [msg]})
                warn(msg, stacklevel=2)
        return Results(reordered, client=self.client)


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
