#!/usr/bin/env python3
# Proof-of-concept for selecting a circle of data from a numpy array
# Created 25 Janurary 2021 by Sam Gardner <stgardner4@tamu.edu>


import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from cartopy import crs as ccrs
from cartopy import feature as cfeat

centerOfEye = [25, -30] # lat, lon
radiusOfEye = 50 # degrees

if __name__ == '__main__':
    # Read in data
    lonData = pd.read_csv("Sams_LON.csv")
    latData = pd.read_csv("Sams_LAT.csv")
    sstData = pd.read_csv("Sams_DATA.csv")
    # convert data to 2-D array
    lonData = lonData.to_numpy()
    lonData = np.tile(lonData, latData.shape[0]).transpose()
    latData = latData.to_numpy()
    latData = np.tile(latData, lonData.shape[1])
    sstData = sstData.to_numpy()

    # Crop data into a rasterized cricle
    sstDataMasked = sstData.copy()
    for idx, value in np.ndenumerate(sstData):
        lonAtIdx = lonData[idx]
        latAtIdx = latData[idx]
        if lonAtIdx > 180:
            lonAtIdx = lonAtIdx - 360
        if ( ((lonAtIdx - centerOfEye[1])**2) + ((latAtIdx - centerOfEye[0])**2) > radiusOfEye**2):
            sstDataMasked[idx] = np.nan

    # Plot the data
    fig = plt.figure()
    ax = plt.axes(projection=ccrs.PlateCarree())
    ax.pcolormesh(lonData, latData, sstDataMasked)
    ax.add_feature(cfeat.COASTLINE.with_scale("10m"), linewidth=0.5)
    ax.scatter([centerOfEye[1]], [centerOfEye[0]], s=1, c="black")
    px = 1/plt.rcParams["figure.dpi"]
    fig.set_size_inches(1920*px, 1080*px)
    fig.savefig("test.png")