from collections import OrderedDict, UserList
import copy
from sparcl.utils import _AttrDict


class Results(UserList):

    def __init__(self, dict_list, client=None):
        super().__init__(dict_list)
        self.hdr = dict_list[0]
        self.recs = dict_list[1:]
        self.client = client
        self.to_science_fields()
        self.hdr['Count'] = len(self.recs)

    @property
    def info(self):
        return self.hdr

    @property
    def records(self):
        return self.recs

    def json(self):
        return self.data

    def to_science_fields(self): # from_orig
        """Convert Internal field names to Science field names.
        SIDE-EFFECT: modifies self.recs """
        newrecs = list()
        for rec in self.recs:
            newrec = dict()
            dr = rec['_dr']
            for orig in rec.keys():
                #! print(f'dbg0: dr={dr}, orig={orig}')
                if orig == '_dr':
                    # keep DR around unchanged. We need it to rename back
                    # to Internal Field Names later.
                    newrec[orig] = rec[orig]
                else:
                    new = self.client.dr_o2n[dr][orig]
                    newrec[new] = rec[orig]
            newrecs.append(_AttrDict(newrec))
        self.recs = newrecs

    def to_internal_fields(self):
        """Convert Science field names to Internal field names."""
        for rec in self.recs:
            dr = rec.get('_dr')
            for new in rec.keys():
                if orig == '_dr':
                    # keep DR around unchanged. We need it to rename back
                    # to Internal Field Names later.
                    continue
                orig = self.client.dr_n2o[dr][new]
                rec[orig] = rec.pop(new)



# For results of retrieve()
class Retrieved(Results):
    """Hold results of 'client.retrieve()"""

    def __init__(self, dict_list, client=None):
        super().__init__(dict_list, client=client)

    def __repr__(self):
        return f'Retrieved Results: {len(self.recs)} records'



class Found(Results):
    """@@@ NEEDS DOCUMENTATION !!!"""

    def __init__(self, dict_list, client=None):
        super().__init__(dict_list, client=client)

    def __repr__(self):
        return f'Find Results: {len(self.recs)} records'

    @property
    def ids(self, idfld='uuid'):
        return [d.get(idfld) for d in self.recs]
