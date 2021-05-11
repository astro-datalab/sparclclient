#! /usr/bin/env python
'''Benchmark speed of SPARC spectra retrieve with various parameters.
'''
# EXAMPLES:
# cd ~/sandbox/sparclclient
# python3 -m api.benchmarks.benchmarks ~/data/sparc/sids5.list
# python3 -m api.benchmarks.benchmarks ~/data/sparc/sids644.list

# Alice reported 22 minutes on 64K retrieved from specClient (rate=48 spec/sec)
#   slack.spectro: 3/31/2021

## Standard Python library
import sys, argparse, logging, os
from pprint import pprint,pformat
## External packages
import psutil
#!import speedtest
## Local packages
from ..client import SparclApi
from ..utils import tic,toc,here_now

#rooturl = 'http://localhost:8030/' #@@@
rooturl = 'http://sparc1.datalab.noirlab.edu:8000/'

def human_size(num, units=['b','KB','MB','GB','TB', 'PB', 'EB']):
    """Returns a human readable string representation of NUM."""
    return (f'{num:.1f} {units[0]}'
            if num<1024 else human_size(num/1000, units[1:]))

# with open('/data/sparc/sids5.list') as f: sids = [int(line.strip()) for line in f if not line.startswith('#')]
def run_retrieve(sids, columns=None, xfer='p', verbose=True):
    #!print(f'Retrieving {len(sids):,} spectra')
    psutil.cpu_percent() # begin interval
    client = SparclApi(url=rooturl)
    result = dict(numcols=len(columns), numsids=len(sids))
    if verbose:
        print(f'Experiment: {pformat(result)}')
    tic()
    data = client.retrieve(sids,columns=columns, xfer=xfer)
    elapsed = toc()
    cpu = psutil.cpu_percent(interval=1)
    if verbose:
        print(f'len(sids)={len(sids)} len(data)={len(data)}')
    assert len(sids) == len(data)   # @@@ but some of ingest may have failed
    assert len(data[0]['spectra__coadd__flux']) > 1000
    result.update(elapsed=elapsed,
                  retrieved=len(data),
                  rate=len(data)/elapsed,
                  end_smrem=psutil.swap_memory().free,
                  end_vmrem=psutil.virtual_memory().available,
                  end_cpuload=os.getloadavg()[1],
                  end_cpuperc=psutil.cpu_percent() # end interval
                  )
    return(result)

def run_paged_retrieve(sids, columns=None, xfer='p',
                       page=5000, verbose=True, keepall=False):
    """Do 1 more more PAGE size retrieves to get data for all sids"""
    print(f'Paged Retrieve of {len(sids):,} spectra')
    psutil.cpu_percent() # begin interval
    client = SparclApi(url=rooturl)
    result = dict(numcols=len(columns), numsids=len(sids), xfer=xfer, page=page)
    if verbose:
        print(f'Experiment: {pformat(result)}')

    data = []
    datacnt = 0
    tic()
    for cnt in range(0,len(sids),page):
        pdata = client.retrieve(sids[cnt:cnt+page], columns=columns, xfer=xfer)
        datacnt += len(pdata)
        if keepall:
            data.extend(pdata)
    elapsed = toc()

    cpu = psutil.cpu_percent(interval=1)
    if verbose:
        print(f'len(sids)={len(sids)} datacnt={datacnt}')
    #assert len(sids) == len(data)   # @@@ but some of ingest may have failed
    #!assert len(data[0]['spectra__coadd__flux']) > 1000 # @@@
    result.update(elapsed=elapsed,
                  retrieved=len(data),
                  rate=datacnt/elapsed,
                  end_smrem=psutil.swap_memory().free,
                  end_vmrem=psutil.virtual_memory().available,
                  end_cpuload=os.getloadavg()[1],
                  end_cpuperc=psutil.cpu_percent() # end interval
                  )
    return(result)


# flux,loglam,ivar,and_mask,or_mask,wdisp,sky,model
allcols = ['flux', 'loglam', 'ivar',  'and_mask', 'or_mask',
           'wdisp', 'sky', 'model']

experiment_0 = dict(
    xfers    = ['p'],
    sidcnts = [600, 60],
    numcols = range(1,3),
    )
experiment_1 = dict(
    xfers    = ['p'],
    sidcnts = [6, 60, 600, 6000, 30000],
    numcols = range(1,3),
    #numcols = range(1,len(allcols)+1),
    )
experiment_2 = dict(
    xfers    = ['p'],
    sidcnts = [1000, 100, 10],
    numcols = range(1,len(allcols)+1),
    )
experiment_3 = dict(
    xfers    = ['p'],
    sidcnts = [1000, ],
    numcols = reversed(range(1,len(allcols)+1)),
    )

experiment_8 = dict(
    xfers    = ['p',],
    sidcnts = [65000,],
    numcols = [1,2,8]
    )
experiment_9 = dict(
    xfers    = ['p','j'],
    sidcnts = sorted(set([min(7*10**x, 65000) for x in range(6)])),
    numcols = range(1,len(allcols)+1),
    )

def run_trials(allsids,  verbose=True):
    #ex = experiment_9 #@@@
    ex = experiment_8 #@@@

    xfers = ex['xfers']
    sidcnts = ex['sidcnts']
    numcols = ex['numcols']

    klist = ['elapsed','numcols','numsids','page','rate','xfer']

    all = []
    for xfer in xfers:
        for n in numcols:
            cols = allcols[:n]
            for sidcnt in sidcnts:
                sids = allsids[:sidcnt]
                #!result = run_retrieve(sids, columns=cols, xfer='p')
                result = run_paged_retrieve(sids, columns=cols, xfer='p')
                if verbose:
                    #print(f'Run-Result: {pformat(result)}')
                    reduced = dict((k,result[k]) for k in result.keys() if k in klist)
                    print(f'Run-Result: {reduced}')
                all.append(result)
    report(all, len(allsids), xfer=xfer)
    return(all)

def report(results,sidcnt, xfer=None, bandwidth=False):
    hostname,now = here_now()
    min1,min5,min15 = os.getloadavg()
    smrem = psutil.swap_memory().free
    vmrem = psutil.virtual_memory().available
    cpuperc = psutil.cpu_percent(interval=1)

    if bandwidth:
        s = speedtest.Speedtest()
        ul_speed = s.upload(threads=1)
        dl_speed = s.download(threads=1)
    else:
        ul_speed = 0
        dl_speed = 0

    #! Upload speed:    {human_size(ul_speed)}
    print(f'\nBenchmark run on {hostname} at {now} with {sidcnt} sids.')
    print(f'''
Transfer Method: {"Pickle" if xfer=='p' else "JSON"}
Download speed:  {human_size(dl_speed)}
    ''')
    # Load Avg:        {min5:.1f} (avg num processes running over last 5 minutes)
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
               "{numsids}\t"
               "{rate:.0f}\t"
               #!"{end_cpuload:.02f}\t"
               #!"{end_cpuperc:.0f}%\t"
               #!"{smrem}\t"
               #!"{vmrem}\t"
               ).format(#smrem=human_size(r['end_smrem']),
                        #vmrem=human_size(r['end_vmrem']),
                        **r))

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
    allcols = ['flux', 'loglam', 'ivar',  'and_mask', 'or_mask',
               'wdisp', 'sky', 'model']
    #!dftcols = 'flux,loglam'
    dftcols = ','.join(allcols)
    parser.add_argument('sids',  type=argparse.FileType('r'),
                        help='File containing list of specobjids. One per line.'
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

    parser.add_argument('--loglevel',      help='Kind of diagnostic output',
                        choices = ['CRTICAL','ERROR','WARNING','INFO','DEBUG'],
                        default='WARNING',
                        )
    return parser

def main():
    parser = my_parser()
    args = parser.parse_args()
    args.sids.close()
    args.sids = args.sids.name


    log_level = getattr(logging, args.loglevel.upper(), None)
    if not isinstance(log_level, int):
        parser.error('Invalid log level: %s' % args.loglevel)
    logging.basicConfig(level = log_level,
                        format='%(levelname)s %(message)s',
                        datefmt='%m-%d %H:%M'
                        )
    logging.debug('Debug output is enabled!!!')

    sids = []
    with open(args.sids,'r') as fin:
        for line in fin:
            if line.startswith('#'):
                continue
            sids.append(int(line.strip()))
    cols = args.cols.split(',')
    #print(f'sids count={len(sids)} columns={cols}')

    #run_retrieve(sids, columns=cols, xfer='p')
    print(f'Starting benchmark on {here_now()}')
    all = run_trials(sids)
    print(f'Finished benchmark on {here_now()}')

if __name__ == '__main__':
    main()
