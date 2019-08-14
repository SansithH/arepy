import time
class showLeap:
    def __enter__(self):
        return self
    def __exit__(self, type, value, tb):
        self.end()
        return
    def __init__(self,name):
        print(name,end="")
        self.itime = time.time()
        self.stime = time.time()
        self.etime = 0
        self.details = False
    def show(self,name):
        ntime = time.time()
        self.etime = ntime - self.stime
        self.stime = ntime
        if self.details: 
            print('\n  %-20s'%name, self.etime,end="")
    def end(self):
        if self.details: 
            print('\nFinished',end="")
        print(' in %.3f s'%(time.time() - self.itime))        
    

# Keeping track of the module loading times

with showLeap('Loading external modules') as leap:
    import numpy as np;              leap.show('numpy')
    import h5py as hp;               leap.show('h5py')
    import scipy as scp;             leap.show('scipy')
    import matplotlib as mpl;        leap.show('matplotlib')
    import multiprocessing as mpi;   leap.show('multiprocessing')

with showLeap('Loading arepy modules') as leap:
    import arepy.constants as const; leap.show('const')
    from   arepy.units import *;     leap.show('units')
    import arepy.shell;              leap.show('shell')
    import arepy.data;               leap.show('data')
    import arepy.files;              leap.show('files')
    import arepy.plot;               leap.show('plot')   # this module takes more time because of the pyplot
    import arepy.util;               leap.show('util')
    import arepy.coord;              leap.show('coord')
    import arepy.phys;               leap.show('phys')
    import arepy.scripy;             leap.show('scripy')

from os.path import dirname,realpath,expanduser
dirHome = expanduser("~")
dirModule = dirname(dirname(dirname(realpath(__file__))))
dirArepy = dirModule+'/python/arepy'
dirScripy = dirModule+'/python/scripy'
dirResults = dirModule+'/results'

numCpu = mpi.cpu_count()
