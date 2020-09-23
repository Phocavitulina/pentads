import argparse
import os
import h5py
import json
import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
matplotlib.use('Agg')
import seaborn as sns
sns.set_context('poster')
import warnings
warnings.filterwarnings('ignore')

# PARSING ARGUMENTS
parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)

parser.add_argument('average_compartment_path', type = str,
                    help = 'Path to the average_compartment JSON file generated by pentad.py')

# Plot
parser.add_argument('--vmin', default = 0.5, type = float, required = False,
                    help = 'Lower limit for the colormap')
parser.add_argument('--vmax', default = 2, type = float, required = False,
                    help = 'Upper limit for the colormap')
parser.add_argument('--cmap', default = 'coolwarm', type = str, required = False,
                    help = 'Colormap to use for the visualization')
parser.add_argument('--title', default = '', type = str, required = False,
                    help = 'Suptitle to use for the visualization')
parser.add_argument('--closed', action = 'store_true', required = False,
                    help = 'If called closes intervals')
# Output
parser.add_argument('--out_pref', default = 'pentad', type = str, required = False,
                    help='Prefix for the output files')
parser.add_argument('--format', default = 'png', type = str, required = False,
                    help='Output files format')

args = parser.parse_args()

# Parse arguments
average_compartment_path = args.average_compartment_path

vmin = args.vmin
vmax = args.vmax
cmap = args.cmap
title = args.title
closed = args.closed

out_pref = args.out_pref
format = args.format

# Read file
with open(average_compartment_path, 'r') as f:
    data = json.load(f)
    average_compartment = data['data']
    data_type = data['type']

# Plot
if data_type == 'cis':
    subplot_titles = ['Short-range A', 'Short-range B',
                      'Long-range A', 'Long-range B',
                      'Between A and B']
    subplot_indexes = [4, 8, 6, 2, 5]

    fig = plt.figure(figsize = (10, 10))
    plt.suptitle(title, x = 0.5125, y = 0.98, fontsize = 22)

    for subtitle, index in zip(subplot_titles, subplot_indexes):
        plt.subplot(3, 3, index)
        plt.title(subtitle, fontsize = 15)
        plt.imshow(average_compartment[subtitle], cmap = cmap, norm = LogNorm(vmax = vmax, vmin = vmin))
        plt.xticks([], [])
        plt.yticks([], [])

    cbar_ax = fig.add_axes([0.95, 0.25, 0.02, 0.5])
    cbar = plt.colorbar(cax = cbar_ax)

    plt.savefig(out_pref + '.' + format, bbox_inches = 'tight')
    plt.clf()

    print('Visualization created!')

elif data_type == 'trans':
    subplot_titles = ['A', 'B', 'AB']
    subplot_indexes = [1, 2, 3]

    fig = plt.figure(figsize = (12, 4))
    plt.suptitle(title, x = 0.5125, y = 1.02, fontsize = 22)

    for subtitle, index in zip(subplot_titles, subplot_indexes):
        plt.subplot(1, 3, index)
        plt.title(subtitle, fontsize = 15)
        plt.imshow(average_compartment[subtitle], cmap = cmap, norm = LogNorm(vmax = vmax, vmin = vmin))
        plt.xticks([], [])
        plt.yticks([], [])

    cbar_ax = fig.add_axes([0.95, 0.15, 0.02, 0.7])
    cbar = plt.colorbar(cax = cbar_ax)

    plt.savefig(out_pref + '.' + format, bbox_inches = 'tight')
    plt.clf()

    print('Visualization created!')

elif data_type == 'dist':
    row_titles = ['A', 'B', 'AB']

    distance_titles = list(average_compartment.keys())
    interval_number = len(distance_titles)

    if closed:
        interval_number -= 1 # Be careful if change --closed flag

    fig = plt.figure(figsize = ( interval_number * 4, 12 ))
    plt.suptitle(title, x = 0.5125, y = 0.98, fontsize = 22)

    for i in range(interval_number):
        for j in range(3):
            plt.subplot(3, interval_number, j*interval_number+i+1)
            plt.imshow(average_compartment[distance_titles[i]][row_titles[j]], cmap = cmap, norm = LogNorm(vmax = vmax, vmin = vmin))
            plt.title('{} {}'.format(distance_titles[i],row_titles[j]), fontsize = 20)
            plt.xticks([], [])
            plt.yticks([], [])

    cbar_ax = fig.add_axes([0.95, 0.25, 0.02, 0.5])
    cbar = plt.colorbar(cax = cbar_ax)

    plt.savefig(out_pref + '.' + format, bbox_inches = 'tight')
    plt.clf()

    print('Visualization created!')

else:
    raise ValueError('unknown data structure')
