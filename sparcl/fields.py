"""Get Field names associated with various SPARCL conditions.
"""
# Python Standard Library
from collections import defaultdict
# External Packages
import requests


def validate_fields(datafields):
    # datafields is simply:
    #   DataField.objects.all().values(*atts)

    drs = set([df['data_release'] for df in datafields])
    core = {df['origdp']: df['newdp']
            for df in datafields if df['storage'] == 'C'}

    o2n = {dr: {df['origdp']: df['newdp']
                for df in datafields
                if df['data_release'] == dr}
           for dr in drs}

    for dr, df in o2n.items():
        #  1-1 mapping origdp <-> newdp across all DR
        if len(set(df.values())) != len(df):
            msg = (f'Data Release={dr} does not have a one-to-one mapping '
                   f'between Original and Science field names.')
            raise Exception(msg)

        acore = defaultdict(list)  # ambiguous core fields(more than one value)
        for k in core.keys():
            if df.get(k) != core.get(k):
                acore[k].append(df.get(k))
        if len(acore) > 0:
            msg = (f'DataFields do not have the same '
                   f'Science field name for core values across all Data Sets. '
                   f'{dict(acore)}'
                   )
            raise Exception(msg)

    return True


class Fields():  # Derived from a single query
    """Lookup of Field Names"""

    def __init__(self, apiurl):

        # [rec, ...]
        # where rec is dict containing keys:
        # 'data_release', 'origdp', 'newdp', 'storage', 'default', 'all'
        datafields = requests.get(f'{apiurl}/datafields/').json()

        validate_fields(datafields)

        dr_list = set(df['data_release'] for df in datafields)

        self.datafields = datafields
        # o2n[DR][InternalName] => ScienceName
        self.o2n = {dr: {df['origdp']: df['newdp']
                         for df in datafields
                         if df['data_release'] == dr}
                    for dr in dr_list}
        # n2o[DR][ScienceName] => InternalName
        self.n2o = {dr: {df['newdp']: df['origdp']
                         for df in datafields
                         if df['data_release'] == dr}
                    for dr in dr_list}
        self.all_drs = dr_list
        self.all_fields = set([df['newdp'] for df in datafields])
        self.datafields = datafields

        # Per DataRelease: get Storage, Default, All for each (user) fieldname
        # dr_attrs[DR][newdp] => dict[storage,default,all]
        self.attrs = {dr: {df['newdp']: {'storage': df['storage'],
                                         'default': df['default'],
                                         'all': df['all']}
                           for df in datafields
                           if df['data_release'] == dr}
                      for dr in dr_list}

    @property
    def all_datasets(self):
        return self.all_drs

    def _science_name(self, internal_name, dataset):
        return self.o2n[dataset].get(internal_name)

    def _internal_name(self, science_name, dataset):
        return self.n2o[dataset][science_name]

    def filter_fields(self, attr, dataset_list):
        fields = set()
        for dr in dataset_list:
            for k, v in self.attrs[dr].items():
                if v.get(attr):
                    fields.add(k)
        return fields

    def default_retrieve_fields(self, dataset_list=None):
        if dataset_list is None:
            dataset_list = self.all_drs
        return self.filter_fields('default', dataset_list)

    def all_retrieve_fields(self, dataset_list=None):
        if dataset_list is None:
            dataset_list = self.all_drs
        return self.filter_fields('all', dataset_list)

    def common(self, dataset_list=None):
        """Fields common to DATASET_LIST (or All datasets if None)"""
        if dataset_list is None:
            dataset_list = self.all_drs
        return sorted(set.intersection(*[set(self.n2o[dr].keys())
                                         for dr in dataset_list]))

    def common_internal(self, dataset_list=None):
        """Fields common to DATASET_LIST (or All datasets if None)"""
        if dataset_list is None:
            dataset_list = self.all_drs
        return set.intersection(*[set(self.o2n[dr].keys())
                                  for dr in dataset_list])

    # There is probably an algorithm to partition ELEMENTS into
    # the _minumum_ number of SETS such that the union of all SETS
    # contains all ELEMENTS. For now, parition by Data Set (when used).
    def field_partitions(self, fields):
        """Partition FIELDS into the DataSets that contain them"""
        dr_fields = defaultdict(list)
        for field in fields:
            for dr in self.all_drs:
                if field in self.n2o[dr]:
                    dr_fields[dr].append(field)
        return dict(dr_fields)
