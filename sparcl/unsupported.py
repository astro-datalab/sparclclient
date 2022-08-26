# End Users should not use anything from this file. All of it is
# considered experimentatal and be broken or change without notice.
############################################
# Python Standard Library
from urllib.parse import urlencode
#!from urllib.parse import urlparse
#!from warnings import warn
import pickle
import tempfile
import json
############################################
# External Packages
import requests
############################################
# Local Packages
#!from sparcl.fields import Fields
import sparcl.exceptions as ex

_STAGE = 'https://sparclstage.datalab.noirlab.edu'  # noqa: E221
_PAT   = 'https://sparc1.datalab.noirlab.edu'       # noqa: E221

drs = ['SDSS-DR16', 'BOSS-DR16', 'DESI-edr']


def retrieve(ids, include=['id'], dataset_list=['BOSS-DR16'],
             server=_PAT,
             svc='spectras',  # or 'retrieve',
             limit=100, verbose=True):
    uparams = dict(include=','.join(include),
                   limit=limit,
                   dataset_list=','.join(dataset_list))
    qstr = urlencode(uparams)

    url = f'{server}/sparc/{svc}/?{qstr}'
    if verbose:
        print(f'Using ids={ids[:2]}')
        print(f'Using url="{url}"')
        print(f'curl -X POST "{url}" -d \'{json.dumps(ids)}\' > retrieve.pkl')

    res = requests.post(url, json=ids)

    if res.status_code != 200:
        #! if verbose and ('traceback' in res.json()):
        #!     print(f'DBG: Server traceback=\n{res.json()["traceback"]}')
        raise ex.genSparclException(res, verbose=verbose)

    # unpack pickle file from result
    with tempfile.TemporaryFile(mode='w+b') as fp:
        for idx, chunk in enumerate(res.iter_content(chunk_size=None)):
            fp.write(chunk)
        # Position to start of file for pickle reading (load)
        fp.seek(0)
        results = pickle.load(fp)

    return results
