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
import scipy.stats as SS
from SEIVR import SEIRV_count
from data_input import *

# global_N_06 = np.array([ 6444728.556,  13719759.564, 2569983.78 , 15933899.436, 869840.664]) 
# global_N_37 = np.array([375820.524, 6420267.285, 2317559.898, 1273613.998])
global_N_06 = np.array([5743983,  14365145, 2142371, 15380929, 1713595]) 
global_N_37 = np.array([341052, 6497519, 2155650, 1704752])

CM_37 = np.loadtxt('CM_37_normalised.csv', delimiter=',')
CM_06 = np.loadtxt('CM_06_normalised.csv', delimiter=',')


def delay_dist(aver_delay, a, cut):
    """
    a # shape parameter
    cut  # cut off at 30 days
    """
    x = np.arange(0.0, cut+1, 1)
    y1 = SS.gamma.pdf(x, a, scale=aver_delay/a)  # ? not sure why this gamma
    raw = np.array([y1[i+1] for i in range(cut)])
    prob_gamma = (raw/np.sum(raw)).reshape(cut, 1)
    return prob_gamma


def getStart(seed, factor, N_all):  # 初始状态样本生成
    """
    seed: the list of the number of infected people in each race
    factor:  the ratio of E/I
    N_all: is the list of the total number of people in each race
    """
    n_races = len(seed)
    StateStart = np.zeros((7, n_races))  # 7 states and 5 races
    for i in range(n_races):
        s = seed[i]
        StateStart[2][i] = random.uniform(max(s-5, 1), s+5) ###I people
        StateStart[1][i] = factor*StateStart[2][i]
        StateStart[3][i] = 0  # random.uniform(10,100)
        StateStart[0][i] = N_all[i] - StateStart[1][i] - StateStart[2][i]- StateStart[3][i]
    return StateStart


def simulate_T(State, Beta_t, Eta_t, parameters, location, T, delay_prob_gamma):
    """
    Simulate the number of new cases for T days using the SEIRV model
    the return new cases is a T by n, the first time step is set to be zero, can not be used
    State (T, num_states, num_races)
    location: 06 or 37, specify the MC and the population
    """
    if location == 6:
        global_N = global_N_06
        CM_XX = CM_06
    else:
        global_N = global_N_37
        CM_XX = CM_37
    dt = 1
    # n_states = State.shape[1]  # SEEIIRV
    n_races = State.shape[2]
    # startcase = np.zeros((T,n_races))
    new_case = np.zeros((T,n_races))
    new_case[0] = State[0,1,:]/parameters['Z'] 

    new_case_v = np.zeros((T,n_races))
    new_case_v[0] = State[0,5,:]/parameters['Z']
    # print(new_case[0])
    shift_t = len(delay_prob_gamma)

    for t in range(1, T):  # Starting from 1 because we already initialized NewInf at time 0
        for _ in range(int(1 / dt)):
            Betat = Beta_t[t]
            Etat = Eta_t[t]
            State[t], (deltacase1, deltacase2), flag = SEIRV_count(
                State[t-1], CM_XX, global_N, parameters, Betat, Etat, dt)
            if flag == 0:
                deltacase1 = deltacase1.reshape(1, n_races)
                prob_case1 = delay_prob_gamma.dot(deltacase1) ## delay to observe
                new_case[t:min(t+shift_t,T)] += prob_case1[:min(T-t,shift_t)]
                
                deltacase2 = deltacase2.reshape(1, n_races)
                prob_case2 = delay_prob_gamma.dot(deltacase2) ## delay to observe
                new_case_v[t:min(t+shift_t,T)] += prob_case2[:min(T-t,shift_t)]
    return (new_case, new_case_v), State, flag


# def GetLogLikelihood(M_real_races, M_obs_races):  # calculate likelihood
#     n_races = M_obs_races.shape[1]
#     loglikelihood = 0
#     likelihood = SS.norm.pdf(
#         M_real_races, loc=M_obs_races, scale=0.4*M_obs_races+20)
#     likelihood[likelihood == 0] = 0.0000001
#     loglikelihood = np.sum(np.log(likelihood))
#     return loglikelihood

def GetLogLikelihood(M_real_races, M_obs_races):  # calculate likelihood
    multiplier = np.array([[0.2, 0.1, 0.1, 0.3]])
    adder = np.array([[5, 20, 20, 1]])
    M_scale = multiplier*M_obs_races + adder
    # M_scale[M_real_races>300] = 0.5*M_real_races[M_real_races>300]
    loglikelihood = 0
    likelihood = SS.norm.pdf(
        M_real_races, loc=M_obs_races, scale=M_scale)
    likelihood[likelihood == 0] = 0.0000001
    loglikelihood = np.sum(np.log(likelihood))
    return loglikelihood


def Reshape_WK(daily_obs, idx_start, num_week, location):
    """
    Generate the weekly simulated cases from the daily simulated cases
    location: 06 or 37, specify the MC and the population
    """
    if location == 6:
        n_r = 5
    else:
        n_r = 4
    # Generate the array of dates, starting from one day after the start_date
    compare_weeks = daily_obs[idx_start-7:idx_start+7*(num_week-1)]
    reshaped_compare_weeks = compare_weeks.reshape((num_week,7,n_r))
    weekly_simu = np.sum(reshaped_compare_weeks,axis=1)
    return weekly_simu


def get_wk_death(state_check,Beta_t_wd, M_eta_l, IFR_daily_wd_l, death_delay, T, rho_d, loc=6):
    (delayed_infnew_T,delayed_infnew_T_v), states_all, saturation = simulate_T(state_check, Beta_t_wd, M_eta_l, parameters, loc, T, death_delay)
    idx_to_start_fit = 21 #+real_wk_idx*7
    num_week = np.int64(T/7-2) #34
    death_daily_sim = delayed_infnew_T*IFR_daily_wd_l + delayed_infnew_T_v*IFR_daily_wd_l*(1-rho_d) 
    ########## get the log likelihood #####
    weekly_sim_death = Reshape_WK(death_daily_sim, idx_to_start_fit, num_week,loc)
    return saturation, weekly_sim_death, states_all

### current back is 14 days it can be changed to 21 days
def para_LKH(state_check,Beta_t_wd, M_eta_l, IFR_daily_wd_l, death_delay, real_wk_idx, T, death_wk_l, loc=6):
    
    (delayed_infnew_T,delayed_infnew_T_v), states_all, saturation = simulate_T(state_check, Beta_t_wd, M_eta_l, parameters, loc, T, death_delay)

    idx_to_start_fit = 21 #+real_wk_idx*7
    # num_week = 34
    num_week = np.int64(T/7-2)
    # if real_wk_idx == 0:
    #     num_week z= 2
    # else:
    #     num_week = int((T - real_wk_idx*7)//7-2) #30-3 #3 if t_start == 0 else 4
    death_daily_sim = delayed_infnew_T*IFR_daily_wd_l + delayed_infnew_T_v*IFR_daily_wd_l*(1-0.95)
    ########## get the log likelihood #####
    weekly_sim_death = Reshape_WK(death_daily_sim, idx_to_start_fit, num_week, loc)
    weekly_sim_death[weekly_sim_death<1] = 1

    L_deaths = GetLogLikelihood(death_wk_l[real_wk_idx:real_wk_idx+num_week], weekly_sim_death)

    return L_deaths, saturation, weekly_sim_death, states_all