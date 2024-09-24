'''
Created on Nov 7, 2017

@author: binghuangc
'''

import GLIF_network.run.bmtk.simulator.utils.nwb as nwb
import numpy as np

# multiple trials    
def create_poisson_spike_train_trials(nwb_file, num_nodes, total_time, firing_rate, dt, num_trials):
    f=nwb.create_blank_file(nwb_file, force=True)
    #trial_number=0
    time = np.arange(0, total_time, dt)
    n_bins=len(time)
    #spkTimes=np.array([200.0, 400.0, 600.0, 800.0])
    for gid in range(num_nodes):
        for trial_number in range(num_trials):
            PoissonTrain = np.random.rand(1, n_bins) < (firing_rate * dt /1000.0)
            spkTimes = time[PoissonTrain[0]]
            nwb.SpikeTrain(spkTimes, unit='millisecond').add_to_processing(f, 'trial_%s' % trial_number)
    f.close()

if __name__ == '__main__':
    
    op = '.' # output folder change accordingly
    firing_rate_list = [1000]
    total_time = 12000 # ms
    num_nodes = 1
    dt = 0.25 # ms
    num_trials = 10
    seed = 0
    np.random.seed(seed)
    
    for fr in firing_rate_list:
        nwb_file = op + 'bkg_spikes_n' + str(num_nodes) + '_fr' + str(fr) + '_dt' + str(dt) + '_' + str(num_trials) + 'trials.nwb'
        create_poisson_spike_train_trials(nwb_file, num_nodes, total_time, fr, dt, num_trials)
        
    print 'Done!'
    
