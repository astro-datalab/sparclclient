#! /usr/bin/env python
'''Benchmark speed of SPARC spectra retrieve with various parameters.
'''
# EXAMPLES:
# cd ~/sandbox/sparclclient
# python3 -m sparcl.benchmarks.benchmarks ~/data/sparc/sids5.list
# python3 -m sparcl.benchmarks.benchmarks ~/data/sparc/sids644.list

# Alice reported 22 minutes on 64K retrieved from specClient (rate=48 spec/sec)
#   slack.spectro: 3/31/2021

# Standard Python library
import argparse
import logging
import os
from pprint import pformat
# External packages
import psutil
# Local packages
from ..client import SparclClient
from ..utils import tic, toc, here_now

#rooturl = 'http://localhost:8030/' #@@@
rooturl = 'http://sparc1.datalab.noirlab.edu:8000/'


def human_size(num, units=['b', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB']):
    """Returns a human readable string representation of NUM."""
    return (f'{num:.1f} {units[0]}'
            if num < 1024 else human_size(num / 1000, units[1:]))


# with open('/data/sparc/sids5.list') as f:
#      specids = [int(line.strip()) for line in f if not line.startswith('#')]
def run_retrieve(specids, columns=None, xfer='p', verbose=True):
    #!print(f'Retrieving {len(specids):,} spectra')
    psutil.cpu_percent()  # begin interval
    client = SparclClient(url=rooturl)
    result = dict(numcols=len(columns), numspecids=len(specids))
    if verbose:
        print(f'Experiment: {pformat(result)}')
    tic()
    data = client.retrieve(specids, columns=columns, xfer=xfer)
    elapsed = toc()
    #!cpu = psutil.cpu_percent(interval=1)
    if verbose:
        print(f'len(specids)={len(specids)} len(data)={len(data)}')
    assert len(specids) == len(data)   # @@@ but some of ingest may have failed
    assert len(data[0]['spectra__coadd__flux']) > 1000
    result.update(elapsed=elapsed,
                  retrieved=len(data),
                  rate=len(data) / elapsed,
                  end_smrem=psutil.swap_memory().free,
                  end_vmrem=psutil.virtual_memory().available,
                  end_cpuload=os.getloadavg()[1],
                  end_cpuperc=psutil.cpu_percent()  # end interval
                  )
    return(result)


def run_paged_retrieve(specids, columns=None, xfer='p',
                       page=5000, verbose=True, keepall=False):
    """Do 1 more more PAGE size retrieves to get data for all specids"""
    print(f'Paged Retrieve of {len(specids):,} spectra')
    psutil.cpu_percent()  # begin interval
    client = SparclClient(url=rooturl)
    result = dict(numcols=len(columns),
                  numspecids=len(specids),
                  xfer=xfer,
                  page=page)
    if verbose:
        print(f'Experiment: {pformat(result)}')

    data = []
    datacnt = 0
    tic()
    for cnt in range(0, len(specids), page):
        pdata = client.retrieve(specids[cnt:cnt + page],
                                columns=columns,
                                xfer=xfer)
        datacnt += len(pdata)
        if keepall:
            data.extend(pdata)
    elapsed = toc()

    #! cpu = psutil.cpu_percent(interval=1)
    if verbose:
        print(f'len(specids)={len(specids)} datacnt={datacnt}')
    #assert len(specids) == len(data)   # @@@but some of ingest may have failed
    #!assert len(data[0]['spectra__coadd__flux']) > 1000 # @@@
    result.update(elapsed=elapsed,
                  retrieved=len(data),
                  rate=datacnt / elapsed,
                  end_smrem=psutil.swap_memory().free,
                  end_vmrem=psutil.virtual_memory().available,
                  end_cpuload=os.getloadavg()[1],
                  end_cpuperc=psutil.cpu_percent()  # end interval
                  )
    return(result)


# flux,loglam,ivar,and_mask,or_mask,wdisp,sky,model
allcols = ['flux', 'loglam', 'ivar', 'and_mask', 'or_mask',
           'wdisp', 'sky', 'model']

experiment_0 = dict(
    xfers=['p'],
    specidcnts=[600, 60],
    numcols=range(1, 3),
)
experiment_1 = dict(
    xfers=['p'],
    specidcnts=[6, 60, 600, 6000, 30000],
    numcols=range(1, 3),
    #numcols=range(1,len(allcols)+1),
)
experiment_2 = dict(
    xfers=['p'],
    specidcnts=[1000, 100, 10],
    numcols=range(1, len(allcols) + 1),
)
experiment_3 = dict(
    xfers=['p'],
    specidcnts=[1000, ],
    numcols=reversed(range(1, len(allcols) + 1)),
)

experiment_8 = dict(
    xfers=['p', ],
    specidcnts=[65000, ],
    numcols=[1, 2, 8]
)
experiment_9 = dict(
    xfers=['p', 'j'],
    specidcnts=sorted(set([min(7 * 10 ** x, 65000) for x in range(6)])),
    numcols=range(1, len(allcols) + 1),
)


def run_trials(allspecids, verbose=True):
    #ex = experiment_9 #@@@
    ex = experiment_8  # @@@

    xfers = ex['xfers']
    specidcnts = ex['specidcnts']
    numcols = ex['numcols']

    klist = ['elapsed', 'numcols', 'numspecids', 'page', 'rate', 'xfer']

    all = []
    for xfer in xfers:
        for n in numcols:
            cols = allcols[:n]
            for specidcnt in specidcnts:
                specids = allspecids[:specidcnt]
                #!result = run_retrieve(specids, columns=cols, xfer='p')
                result = run_paged_retrieve(specids, columns=cols, xfer='p')
                if verbose:
                    #print(f'Run-Result: {pformat(result)}')
                    reduced = dict((k, result[k])
                                   for k in result.keys() if k in klist)
                    print(f'Run-Result: {reduced}')
                all.append(result)
    report(all, len(allspecids), xfer=xfer)
    return(all)


def report(results, specidcnt, xfer=None, bandwidth=False):
    hostname, now = here_now()
    min1, min5, min15 = os.getloadavg()
    #!smrem = psutil.swap_memory().free
    #!vmrem = psutil.virtual_memory().available
    #!cpuperc = psutil.cpu_percent(interval=1)

    if bandwidth:
        pass
        #! s = speedtest.Speedtest()
        #! ul_speed = s.upload(threads=1)
        #! dl_speed = s.download(threads=1)
    else:
        #! ul_speed = 0
        dl_speed = 0

    #! Upload speed:    {human_size(ul_speed)}
    print(f'\nBenchmark run on {hostname} at {now} with {specidcnt} specids.')
    print(f'''
Transfer Method: {"Pickle" if xfer=='p' else "JSON"}
Download speed:  {human_size(dl_speed)}
    ''')
    # Load Avg:        {min5:.1f}
    #         (avg num processes running over last 5 minutes)
    # CPU utilization: {cpuperc:.0f}%
    # Swap Mem Avail:    {human_size(smrem)}
    # Virtual Mem Avail: {human_size(vmrem)}
    # (Above statistics are for CLIENT.)

    #!print(f'Column\tSID\tRate \tAvg \tCPU \tSwap\tVirt')
    #!print(f' Count\tCnt\ts/sec\tLoad\tUtil\t Mem\t Mem')
    #!print(f'------\t---\t-----\t----\t----')
    print(f'Column\tSID\tRate ')
    print(f' Count\tCnt\ts/sec')
    print(f'------\t---\t-----')
    for r in results:
        print(("{numcols}\t"
               "{numspecids}\t"
               "{rate:.0f}\t"
               #!"{end_cpuload:.02f}\t"
               #!"{end_cpuperc:.0f}%\t"
               #!"{smrem}\t"
               #!"{vmrem}\t"
               ).format(**r))
        #smrem=human_size(r['end_smrem']),
        #vmrem=human_size(r['end_vmrem']),
    print('''
LEGEND:
  Rate:: spectra/second
  Transfer method:: Pickle, Json
  Load:: Number of processes in system run queue averaged over last 5 minutes.
  ''')
    return 'Done'

##############################################################################


def my_parser():
    parser = argparse.ArgumentParser(
        #!version='1.0.1',
        description='My shiny new python program',
        epilog='EXAMPLE: %(prog)s a b"'
    )
    allcols = ['flux', 'loglam', 'ivar', 'and_mask', 'or_mask',
               'wdisp', 'sky', 'model']
    #!dftcols = 'flux,loglam'
    dftcols = ','.join(allcols)
    parser.add_argument('specids', type=argparse.FileType('r'),
                        help=('File containing list of '
                              'specobjids. One per line.')
                        )
    parser.add_argument('--cols',
                        #choices=allcols,
                        default=dftcols,
                        help=(f'List of comma seperated columns to get. '
                              f'Default="{dftcols}"')
                        )
    parser.add_argument('--xfer', default='p',
                        help='Mode to use to transfer from Server to Client.'
                        )

    parser.add_argument('--loglevel',
                        help='Kind of diagnostic output',
                        choices=['CRTICAL', 'ERROR', 'WARNING',
                                 'INFO', 'DEBUG'],
                        default='WARNING',
                        )
    return parser


def main():
    parser = my_parser()
    args = parser.parse_args()
    args.specids.close()
    args.specids = args.specids.name

    log_level = getattr(logging, args.loglevel.upper(), None)
    if not isinstance(log_level, int):
        parser.error('Invalid log level: %s' % args.loglevel)
    logging.basicConfig(level=log_level,
                        format='%(levelname)s %(message)s',
                        datefmt='%m-%d %H:%M'
                        )
    logging.debug('Debug output is enabled!!!')

    specids = []
    with open(args.specids, 'r') as fin:
        for line in fin:
            if line.startswith('#'):
                continue
            specids.append(int(line.strip()))
    #! cols = args.cols.split(',')
    #print(f'specids count={len(specids)} columns={cols}')

    #run_retrieve(specids, columns=cols, xfer='p')
    print(f'Starting benchmark on {here_now()}')
    #! all = run_trials(specids)
    print(f'Finished benchmark on {here_now()}')


if __name__ == '__main__':
    main()
