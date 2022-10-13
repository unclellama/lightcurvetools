# package to do basic things with 3-column lightcurves (time, flux, error) in python
# like, load them from text file and get a nice 'lightcurve' object 
# with useful auxilary data such as redshift, units

# for now i'm storing data as floats + 'unit' strings instead of astropy quantities
# should probably use astropy quantities and make old code compatible instead...

# including a redshift parameter z which does nothing right now,
# might want to include a 'luminosity' method later, or to get rest-frame days, etc.

# v0.1 - by daniel (unclellama@gmail.com)
# last updated 13th oct 2022

import copy
import numpy as np
from matplotlib import pyplot as plt
from astropy.table import Table
from astropy.io import ascii
from scipy import interpolate
from scipy.signal import windows
from scipy.signal import convolve

class lightcurve:
    ### the lightcurve object
    def __init__(self, tt, ff, ef, z=0., tunit='days', tframe='observed', funit='cgs', label=''):
        self.tt = tt
        self.ff = ff
        self.ef = ef
        self.z = z
        self.tunit = tunit
        self.tframe = tframe
        self.funit = funit
        self.label = label
        
    def write(self, filename):
        t = Table([self.tt, self.ff, self.ef])
        ascii.write(t, filename, format='no_header', overwrite=True)
    
    def stats(self):
        dt = [self.tt[n+1]-self.tt[n] for n in range(len(self.tt)-1)]
        print('number of observations:', len(self.tt))
        print('mean flux: ',np.mean(self.ff))
        print('min, max flux: ', np.min(self.ff), np.max(self.ff))
        print('duration: ',self.tt[-1]-self.tt[0])
        print('average time sampling: ',np.mean(dt))
        print('median time sampling: ', np.median(dt))
        print('min, max time sampling: ', np.min(dt), np.max(dt))
        
def readlightcurve(file, twocol=False, tunit='days', tframe='observed', funit='cgs'):
    # reads the lightcurve from a three-col ascii file into a lightcurve object
    # if no error colum is present, set twocol=True to set errors=0 (edit manually afterwards)
    f = open(file, "r")
    times = []
    fluxes = []
    errors = []
    for line in f:
        times.append(float(line.split()[0]))
        fluxes.append(float(line.split()[1]))
        if twocol == True:
            errors.append(0.)
        else:
            errors.append(float(line.split()[2]))
    lc = lightcurve(np.asarray(times), np.asarray(fluxes), np.asarray(errors),
        tunit=tunit, tframe=tframe, funit=funit)
    return lc
    
def smoothlightcurve(lc, width, resampling=0.1, type='boxcar', prop_errors=True):
    # apply boxcar smoothing to lightcurve
    # reduces the errorbars to account for the averaging process if prop_errors=True
    ft = interpolate.interp1d(lc.tt, lc.ff,
                              fill_value=(lc.ff[0],lc.ff[-1]), bounds_error=False)
    xinter = np.arange(lc.tt[0]-width*5, lc.tt[-1]+width*5, resampling)
    fluxinter = ft(xinter)
    if type == 'boxcar':
        window = windows.boxcar(int(width/resampling))
    if type == 'gaussian':
        window = windows.gaussian(width*5/resampling, (width/2)/resampling)
    fluxsmooth = convolve(fluxinter, window, mode='same')/sum(window)
    ftsmooth = interpolate.interp1d(xinter, fluxsmooth, fill_value='extrapolate')
    fluxinter_smooth = ftsmooth(lc.tt)
    lcnew = copy.deepcopy(lc)
    lcnew.ff = fluxinter_smooth
    return lcnew
    
def subtractlightcurve(lc, lcsub):
    # subtract one lightcurve from the other, assuming *identical* time arrays!
    resflux = lc.ff - lcsub.ff
    lcres = copy.deepcopy(lc)
    lcres.ff = resflux
    return lcres
    
def plotlightcurve(lcarr):
    # plot an array of lightcurves
    for lc in lcarr:
        plt.errorbar(lc.tt, lc.ff, yerr=lc.ef, label=lc.label)
    plt.ylabel('Flux')
    plt.xlabel('Time')
    plt.legend()
    plt.show()
    plt.close()
    