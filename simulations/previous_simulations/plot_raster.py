import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.pylab as pylab
import scipy.stats as stats
from matplotlib.patches import Rectangle
from matplotlib.collections import PatchCollection


params = {'legend.fontsize': 50,
          'axes.labelsize': 50,
          'axes.titlesize': 50,
          'xtick.labelsize':50,
          'ytick.labelsize':50}
pylab.rcParams.update(params)



def plot_raster_query(ax,spikes,nodes_df,cmap, plot_order, twindow=[0,3], marker=".", lw=0,s=10):
    '''
    Plot raster colored according to a query.
    Query's key defines node selection and the corresponding values defines color

    Parameters:
    -----------
        ax: matplotlib axes object
            axes to use
        spikes: tuple of numpy arrays
            includes [times, gids]
        nodes_df: pandas DataFrame
            nodes table
        cmap: dict
            key: query string, value:color
        twindow: tuple
            [start_time,end_time]
        plot_order: order to plot cell classes - list

    '''
    tstart = twindow[0]
    tend = twindow[1]

    ix_t = np.where((spikes[0]>tstart) & (spikes[0]<tend))

    spike_times = spikes[0][ix_t]
    spike_gids = spikes[1][ix_t]

    counter = 0
    # Grey boxes to be drawn to delineate layers with the below colormap
    patch_colors = ['grey', 'w', 'grey', 'w', 'grey']
    for query in plot_order:

        col = cmap[query]
        gids_query = np.where(nodes_df.pop_name.str.startswith(query))[0]
        tuning_angles = nodes_df.tuning_angle[gids_query]

        print (query, "ncells:", len(gids_query), col)

        ix_g = np.in1d(spike_gids, gids_query)

        spikes_gids_temp = spike_gids[ix_g]
        gids_temp = stats.rankdata(tuning_angles, method='dense') - 1
        gids_temp = gids_temp + counter
        for i, gid in enumerate(gids_query):
            inds = np.where(spikes_gids_temp == gid)
            spikes_gids_temp[inds] = gids_temp[i]

        counter += len(gids_query)


        ax.plot(spike_times[ix_g], spikes_gids_temp,
                    marker= marker,
                    color = col,
                    label=query,
                    lw=lw,
                    markersize = s
                    );

        # Plotting for boxes to be drawn to delineate layers
        if ('Htr3a' in query):
            if 'xy' not in locals():
                xy = (0,0)
                w = twindow[1] + 500
                h = counter
                h_cumsum = h
            else:
                xy = (0, h_cumsum)
                h = counter - h_cumsum
                h_cumsum += h

            ax.add_patch(Rectangle(xy, w, h, color=patch_colors.pop(), alpha=0.2))






if __name__ == '__main__':

    # Spikes file to load and plot
    spikes_file_name = 'biophysical/spikes_driftingGratings_ori90.0_trial0.txt'
    # spikes_file_name = 'biophysical/spikes_flash_trial0.txt'
    # spikes_file_name = 'biophysical/spikes_naturalMovie_trial0.txt'
    spikes = np.loadtxt(spikes_file_name, unpack=True)

    # Nodes file to read
    nodes_DF = pd.read_csv('../Biophysical_network/network/v1_nodes.csv', sep=' ')


    # Color map to be used
    cmap = {
        "i1Htr3a": 'indigo',
        "e23": 'firebrick',
        "i23Pvalb": 'blue',
        "i23Sst": 'forestgreen',
        "i23Htr3a": 'indigo',
        "e4": 'firebrick',
        "i4Pvalb": 'blue',
        "i4Sst": 'forestgreen',
        "i4Htr3a": 'indigo',
        "e5": 'firebrick',
        "i5Pvalb": 'blue',
        "i5Sst": 'forestgreen',
        "i5Htr3a": 'indigo',
        "e6": 'firebrick',
        "i6Pvalb": 'blue',
        "i6Sst": 'forestgreen',
        "i6Htr3a": 'indigo',
    }

    # To plot L6 at the bottom and L1 at the top
    plot_order = [
        "e6", "i6Pvalb", "i6Sst", "i6Htr3a",
        "e5", "i5Pvalb", "i5Sst", "i5Htr3a",
        "e4", "i4Pvalb", "i4Sst", "i4Htr3a",
        "e23", "i23Pvalb", "i23Sst", "i23Htr3a",
        "i1Htr3a",
        ]

    # Plot the results
    fig, ax = plt.subplots(figsize=(24, 16))
    plot_raster_query(ax, spikes, nodes_DF, cmap, plot_order, twindow=[0, 3000], marker=".", lw=0, s=2.)
    ax.set_xlabel('Time (ms)');
    ax.set_ylabel('Neuron ID');



    # For gratings or movie: 500ms grey then 2500ms stimulus
    if 'flash' not in spikes_file_name:
        plt.plot([500, 3000], [-1000, -1000], color='k', lw=5)
        plt.plot([0, 500], [-7000, -7000], color='k', lw=5)
        plt.plot([500, 500], [-1000, -7000], color='k', lw=5)
        ax.set_ylim([-10000, 54000])

    # For flashes: grey for 500ms then ON for 250ms then grey then OFF for 250ms then grey again
    else:
        plt.plot([0, 500], [-7000, -7000], color='k', lw=5)
        plt.plot([500, 750], [-1000, -1000], color='k', lw=5)
        plt.plot([750, 1750], [-7000, -7000], color='k', lw=5)
        plt.plot([1750, 2000], [-13000, -13000], color='k', lw=5)
        plt.plot([2000, 2500], [-7000, -7000], color='k', lw=5)

        plt.plot([500, 500], [-1000, -7000], color='k', lw=5)
        plt.plot([750, 750], [-1000, -7000], color='k', lw=5)
        plt.plot([1750, 1750], [-13000, -7000], color='k', lw=5)
        plt.plot([2000, 2000], [-13000, -7000], color='k', lw=5)
        ax.set_ylim([-16000, 54000])

    plt.show()


