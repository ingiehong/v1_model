import numpy as np
import pandas as pd
import os

"""
create csv files holding poisson spikes
"""
def generate_poisson_spikes(rate, duration, dt):
    """
    Generates Poisson spike timings given a rate (spikes per second), a duration (ms), and a temporal resolution (dt)
    """
    # disallow spike at time 0.0
    time = np.arange(1, duration + dt, dt)
    n_bins = len(time)
    poisson_train = np.random.rand(1, n_bins) < (rate * dt / 1000.0)
    timestamps = time[poisson_train[0]]
    return timestamps




def save_spikes_to_csv(timestamps, trial_number, directory):
    """
    Saves the spike timings to a CSV file in the specified format.
    """
    df = pd.DataFrame({
        'timestamps': timestamps,
        'population': ['lgn'] * len(timestamps),
        'node_ids': [0] * len(timestamps)
    })
    if not os.path.exists(directory):
        os.makedirs(directory)
    df.to_csv(f'{directory}/spikes.trial_{trial_number}.csv', sep=' ', index=False, header=True)


def run_simulation(num_trials, rate, duration, dt, directory, seed):
    """
    Runs the Poisson spike simulation for the given number of trials.
    """
    np.random.seed(seed)  # Set the random seed
    for trial in range(0, num_trials):
        timestamps = generate_poisson_spikes(rate, duration, dt)
        save_spikes_to_csv(timestamps, trial, directory)


# Parameters
num_trials = 10
rate = 1000  # spikes per second
duration = 12000  # duration in ms
dt = 0.25  # ms
seed = 0
directory = 'results/bkg_spikes_n1_fr1000_dt0.25_12s'

# Run the simulation
run_simulation(num_trials, rate, duration, dt, directory, seed)
