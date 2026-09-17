import pandas as pd
import numpy as np
import csv
import random 
import time
import math
import scipy

# global_N_06 = np.array([6444728.556,  13719759.564, 2569983.78 , 15933899.436, 869840.664]) 
# global_N_37 = np.array([375820.524, 6420267.285, 2317559.898, 1273613.998])

global_N_06 = np.array([5743983,  14365145, 2142371, 15380929, 1713595]) 
global_N_37 = np.array([341052, 6497519, 2155650, 1704752])


race_list_06 = ['asian', 'white', 'black', 'latino','other']
race_list_37 = ['asian', 'white', 'black', 'other']

g_n_r_06 = 5
g_n_r_37 = 4

global_percent_06 = np.array([0.145986368, 0.365097764, 0.054449493, 0.390914452, 0.043551924])
global_percent_37 = np.array([0.031877078, 0.607303056, 0.201481955, 0.15933791])

custom_colors = {
    'white': '#A6DBD6',
    'black': '#E8E6A3',
    'asian': '#E8B5A4',
    'latino': '#C3A5CE',
    'other': '#E4E4E4',
    'unknown': 'black'
}

### almost fixed at the moment
parameters = {'L': 600 ,  # immunity period
              'Z': 5,  # latency period
              'D': 5,  # infectious duration
              'P': 730,  # duration of vaccination protection
              'rho_c':0.95} # vaccine protection efficacy against symptomatic disease

# ['asian', 'white', 'black', 'latino','other']
ifr_ratio_06 = np.array([0.0651/0.003, 0.0516/0.0024, 0.087/0.004, 0.0669/0.0031, 0.0206/0.0009])
ifr_over65_06 = np.array([0.0651, 0.0516, 0.087, 0.0669, 0.0206])
ifr_under65_06 = np.array([0.003, 0.0024, 0.004, 0.0031, 0.0009])
prob_65over_06 = np.array([16.17, 20.75, 13.17, 8.04, 10.54])/100

# ['asian', 'white', 'black','other']
ifr_ratio_37 = [0.0164/0.0008, 0.0331/0.0015, 0.0478/0.0022, 0.0102/0.0005]
prob_65over_37 = np.array([9.17, 19.06, 13.07, 8.08])/100

