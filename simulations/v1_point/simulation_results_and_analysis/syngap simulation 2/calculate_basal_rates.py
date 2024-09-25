import math

import numpy as np
import h5py
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.pylab as pylab
import os
import json
from scipy.optimize import curve_fit  # Yidong: Added this import for curve fitting

""" Calculate the firing rates during the 12s gray screen"""

# Yidong: Calculate the firing rate within a time interval defined by t0 (ms) and t1 (ms)
def calculateFiringRateWithinInterval(gids, ts, numNrns, t0, t1):
    gids = gids[np.where(ts > t0)[0]]
    ts = ts[np.where(ts > t0)[0]]
    gids = gids[np.where(ts <= t1)[0]]
    gid_bins = np.arange(0 - 0.5, numNrns + 0.5, 1)

    hist, bins = np.histogram(gids, bins=gid_bins)

    mean_firing_rates = hist / ((t1 - t0) / 1000.)
    return mean_firing_rates

def calculate_Rates_DF(numNrns, trials=10):  # Changed orientations to 30-degree increments

    Rates_DF = pd.DataFrame(index=range(numNrns),
                            columns=['node_id', 'Avg_rate(Hz)', 'SD_rate(Hz)'])


    firingRatesTrials = np.zeros((trials, numNrns))

    for trial in range(trials):
        spikes_file_name = '12s_full_gray_spikes_trial_' + str(trial) + '.txt'

        spikes = np.loadtxt(spikes_file_name, unpack=True)
        ts, gids = spikes
        gids = gids.astype(int)

        firingRates = calculateFiringRateWithinInterval(gids, ts, numNrns, t0=0.0, t1=12000.0)
        print(spikes_file_name)

        firingRatesTrials[trial, :] = firingRates

        Rates_DF.loc[0:numNrns-1, 'node_id'] = np.arange(numNrns)
        Rates_DF.loc[0:numNrns-1, 'Avg_rate(Hz)'] = np.mean(firingRatesTrials, axis=0)
        Rates_DF.loc[0:numNrns-1, 'SD_rate(Hz)'] = np.std(firingRatesTrials, axis=0)

    Rates_DF.to_csv('Basal_Rates_DF.csv', sep=' ', index=False)


if __name__ == "__main__":
    trials = 10

    nodes_file_name = '../../../v1_biophysical/network/v1_nodes.csv'
    nodes_DF = pd.read_csv(nodes_file_name, sep=' ')
    numNrns = len(nodes_DF)

    calculate_Rates_DF(numNrns, trials=trials)
    print("Done_Rates_DF!")
