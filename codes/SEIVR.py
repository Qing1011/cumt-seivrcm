import pandas as pd
import numpy as np
import os
import csv
import datetime as dt
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import random
import time
import math
import scipy
from scipy import stats
from scipy.stats import norm
from data_input import *

def SEIRV_count(currState, currConM, N_t, para_dic, beta_t, eta_t, dt):  # SEIRV
    """
    state: 
    0:S, 1:E, 2:I, 3:R, 4:V, 5:Ev, 6:Iv
    """
    # assume the CM and other
    n_r = currConM.shape[0]
    n_states = currState.shape[0]
    S = currState[0]
    E = currState[1]
    I = currState[2]
    R = currState[3]
    V = currState[4]
    Ev = currState[5]
    Iv = currState[6]
    newState = np.zeros((n_states, n_r))
    newcase = np.zeros(n_states)
    
    L = para_dic['L']
    Z = para_dic['Z']
    D = para_dic['D']
    P = para_dic['P']
    v = eta_t
    rho_c = para_dic['rho_c']
    # v = para_dic['v']  # can varry with time
    # Beta_t = (Rt*N_t)/(D*S)
    
    flag = 0  
    Inf_CM = np.dot(currConM, ((I+Iv)/N_t))
    d_S1 = Inf_CM*S*beta_t
    newState[0] = S + (- d_S1 + R/L - v*S + V/P)*dt  # S
    newState[1] = E + (d_S1 - E/Z)*dt  # E
    newState[2] = I + (E/Z - I/D)*dt  # I
    newState[3] = R + (I/D + Iv/D - R/L)*dt  # R
    ########### vaccination ###########
    d_S2 = Inf_CM*V*beta_t*(1-rho_c)
    newState[4] = V + (v*S - d_S2 - V/P)*dt  # V
    newState[5] = Ev + (d_S2 - Ev/Z)*dt  # Ev
    newState[6] = Iv + (Ev/Z - Iv/D)*dt  # Iv
    ########### new infections ###########
    newcase = (E/Z, Ev/Z)
    ########### check saturation ###########
    if np.min(newState) < 0:
        flag = 1
        print('Saturation')
    return newState, newcase, flag
