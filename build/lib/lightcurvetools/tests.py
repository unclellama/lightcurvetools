from lightcurvetools import *

# should do a smooth-and-subtract operation on the test lightcurve, show a plot,
# and save the smoothed lc

testfile = 'testdata/lc_xrt_alldata.dat'
testlc = readlightcurve(testfile)
testlc.label = 'original'
testlc.stats()
sigma_HW = 2.355/2
wid = round(20/sigma_HW)
smoothlc = smoothlightcurve(testlc, wid)
smoothlc.label = 'smoothed'
sublc = subtractlightcurve(testlc, smoothlc)
sublc.label = 'subtracted'
plotlightcurve([testlc, smoothlc, sublc])
sublc.write('testwrite.dat')