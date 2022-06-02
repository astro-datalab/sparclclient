"""Get Field names associated with various SPARCL conditions.
"""

# Python Standard Library
from warnings import warn
from collections import defaultdict
# External Packages
import requests


# Derived from a single query
class Fields():
    """Lookup of Field Names"""

    def __init__(self, apiurl):

        datafields = requests.get(f'{apiurl}/datafields/').json()

        core_list = set([df['newdp']
                         for df in datafields if df['storage']=='C'])
        dr_list = set(df['data_release_id'] for df in datafields)


        atts = ['data_release', 'origdp', 'newdp', 'storage', 'default', 'all']
        self.datafields = datafields
        # o2n[DR][InternalName] => ScienceName
        self.o2n = {dr : {df['origdp'] : df['newdp']
                          for df in datafields if df['data_release_id'] == dr}
                    for dr in dr_list}
        # o2n[DR][InternalName] => ScienceName
        self.n2o = {dr : {df['newdp'] : df['origdp']
                          for df in datafields if df['data_release_id'] == dr}
                    for dr in dr_list}
        self.all_drs = dr_list
        self.all_fields = set([df['newdp'] for df in datafields])

        # Per DataRelease: get Storage, Default, All for each (user) fieldname
        # dr_attrs[DR][newdp] => dict[storage,default,all]
        self.attrs = {dr : {df['newdp'] : {'storage': df['storage'],
                                            'default': df['default'],
                                            'all': df['all']}
                            for df in datafields if df['data_release_id'] == dr}
                      for dr in dr_list}

        # Handy structures for field name management in ivars
        warn('''Implementation ignores that fact that a
        single Science Field Name might map to MULTIPLE Internal Field Names
        within a single Data Set.  If this is the case (see Admin)
        results may be unpredictable!!!''', stacklevel=2)

    @property
    def all_datasets(self):
        return self.all_drs

    def _science_name(self, internal_name, dataset):
        #!print(f'DBG _science_name: dr={dataset} name={internal_name}')
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

#!    def get_hetero_record_lists(self, records):
#!        lut = defaultdict(list)  # lut[dr] => records
#!        for dr in self.all_drs:
#!            for rec in records:
#!                lut[rec._dr].append(rec)
#!        return lut



#! dfLUT[dr][origPath] => dict[new=newPath,default=bool,store=bool]
#! lut0 = requests.get(f'{self.apiurl}/fields/').json()
#! lut1 = OrderedDict(sorted(lut0.items()))
#! self.dfLUT = {k:OrderedDict(sorted(d.items())) for k,d in lut1.items()}


#! # default[dr] => newFieldName, ...
#! self.default = dict(
#!     (dr, [d['new'] for orig,d in v.items() if d['default']])
#!     for dr,v in self.dfLUT.items())
#!
#! # orig2newLUT[dr][orig] = new
#! self.orig2newLUT = dict((dr,dict((orig,d['new'])
#!                                  for orig,d in v.items()))
#!                         for dr,v in self.dfLUT.items())
#! # new2origLUT[dr][new] = orig
#! self.new2origLUT = dict((dr,dict((d['new'],orig)
#!                                  for orig,d in v.items()))
#!                         for dr,v in self.dfLUT.items())
#!
#! # dict[drName] = [fieldName, ...]
#! self.dr_fields = dict((dr,v) for dr,v in self.new2origLUT.items())
#!
#! dsflds = [self.dr_fields[dr].values()
#!           for dr in self.dr_fields.keys()]
#! self.common_fields = set.intersection(*[set(l) for l in dsflds])

#! dr_default = {dr : {new
#!                     for new,v in dr_attrs[dr].items()
#!                     if v['default']} for dr in dr_list}
#! dr_all = {dr : {new
#!                     for new,v in dr_attrs[dr].items()
#!                     if v['all']} for dr in dr_list}
#!
#! # Fields (new) common to ALL DRs
#! common = set.intersection(*[set(dr_n2o[dr].keys())
#!                             for dr in dr_n2o.keys()])
