from libHOLOSPECImages import oscan_and_trim, SaveCCDListIntoFitsFile

import numpy as np

# Set up matplotlib and use a nicer set of plot parameters
#config InlineBackend.rc = {}
#config Backend.rc = {}
import matplotlib
matplotlib.rc_file("../templates/matplotlibrc")  # default config obtained from astropy examples
import matplotlib.pyplot as plt

import matplotlib.colors as colors
import matplotlib.cm as cmx
from matplotlib.colors import LogNorm

from astropy.utils.data import download_file

from astropy.io import fits
import ccdproc

import os

NBCHAN=16
jet =plt.get_cmap('jet')
cNorm  = colors.Normalize(vmin=0, vmax=NBCHAN)
scalarMap = cmx.ScalarMappable(norm=cNorm, cmap=jet)
all_colors= scalarMap.to_rgba(np.arange(NBCHAN),alpha=1)
#colorVal = scalarMap.to_rgba(num,alpha=1)

# -------------------------------------------------------------------------------------------------
#   Main to test the library
# -------------------------------------------------------------------------------------------------
if __name__ == "__main__":

    path = '../data/20181025/'
    filename = '10_CCD1_20181025173846.fz'


    fullfilename = os.path.join(path, filename)

    fileparts=os.path.splitext(filename)

    filename_out = fileparts[0] + '_ovsc' + fileparts[1]
    fullfilename_out = os.path.join(path,filename_out)

    NB_OF_CHANNELS=NBCHAN



    hdu_list = fits.open(fullfilename)
    #hdu_list.info()

    header1 = fits.getheader(fullfilename)  # to retreive the header of the file
    header1=hdu_list[0].header

    print(header1)


    header2 = hdu_list[0].header
    header3 = header1 +header2

    #print '----------------- Header1 read from file :: '
    #print header1

    #print '------------------- Header2 read from file :: '
    #print header2

    #print '-------------------- Header3 read from file :: '
    #print header3



    # all CCDPROC data collector : each channel as a list of biases data
    allccd = []
    for chan in range(1, NB_OF_CHANNELS + 1, 1):
        ccd_chan = ccdproc.CCDData(hdu_list[chan].data, meta=header3, unit="adu")
        allccd.append(ccd_chan)


    #make the overscan
    all_overscanned=oscan_and_trim(allccd)
    

    SaveCCDListIntoFitsFile(all_overscanned,fullfilename_out, header1,header2,imagetyp="OVSCTRIM")
    hdu_list.close()



