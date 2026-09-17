import numpy as np
import matplotlib.pyplot as plt
import os
from mcmc_fun_06 import *  
# from mcmc_fun import *  

def adjust_array(array, col_idx=1):
    """
    Adjusts the array such that for each time step, 
    all columns are compared with the column at col_idx.
    If a value in any column is greater than the value in col_idx, 
    it is set to the value in col_idx; otherwise, it remains the same.
    
    Parameters:
    array (np.ndarray): Input array of shape (T, n_r).
    col_idx (int): Index of the column to compare with (default is 1).
    
    Returns:
    np.ndarray: Adjusted array.
    """
    # Get the values of the column at col_idx
    col_values = array[:, col_idx]
    # Use broadcasting to create a mask where values greater than col_idx values
    mask = array > col_values[:, np.newaxis]
    col_ls = range(array.shape[1])
    for r_idx in col_ls:
        mask_r = mask[:,r_idx]
        array[mask_r,r_idx] = col_values[mask_r]
    return array


def plot_ifr_comparison(ts_ifr, ts_ifr_adj, race_list, custom_colors, text):
    """
    Plots the IFR comparison for each race in separate subplots.

    Parameters:
    ts_ifr_over65 (np.ndarray): The original IFR data array of shape (T, 5).
    ts_ifr_over65_adj (np.ndarray): The adjusted IFR data array of shape (T, 5).
    race_list (list): List of race names corresponding to the columns of the arrays.
    custom_colors (dict): Dictionary mapping race names to their respective colors.
    """
    n_r = len(race_list)
    fig, axes = plt.subplots(nrows=1, ncols=n_r, figsize=(3*n_r, 3), sharey=True)
    # Plot each race in a separate subplot
    for r_idx in range(n_r):
        ax = axes[r_idx]
        r = race_list[r_idx]
        ax.plot(ts_ifr[:, r_idx], label=f'{r} (original)', c=custom_colors[r])
        ax.plot(ts_ifr[:, 1], label=f'White (comparison)', c='black')
        ax.plot(ts_ifr_adj[:, r_idx], '--', label=f'{r} (adjusted)', c=custom_colors[r])
        ax.set_title(r)
        ax.legend()

    # Add a title to the entire figure
    fig.suptitle('Comparison of {} by Race'.format(text))
    plt.tight_layout()
    plt.show()


def simulate_scenario(thin, n_windows, T, n_states, n_races, global_N, 
                   M_trace_steady, M_eta_06, IFR_06_daily_wd_adj, delay_dist_init, death_06_wk_s,location, M_beta_adj=None):
    """
    Simulates the scenarios over a time period for given parameters.
    """
    # Initialize result arrays
    # n_windows = 14 #9 #14
    M_death_wk = np.zeros((thin,n_windows*4-2,n_races))
    M_State = np.zeros((thin,n_windows*28,7,n_races))
    if M_beta_adj is not None:
        M_beta = M_beta_adj
    else:
        M_beta = np.zeros((thin,n_windows*28,n_races))
    # M_trace_steady = M_trace[[-(n_mcmc - burn_in)+step*k1+1 for k1 in range(thin)]]
    
    for s_i in range(thin):
        seed_post_i = M_trace_steady[s_i, 0, :]
        State = np.zeros((T, n_states, n_races))
        statestart = getStart(seed=seed_post_i, factor=3, N_all=global_N)
        State[0] = statestart
        state_check = State
        factor_post_i = M_trace_steady[s_i, 1:n_windows+1, :]
        if M_beta_adj is not None:
            beta_t_check = M_beta_adj[s_i, :, :]
        else:
            beta_t_check = np.repeat(factor_post_i, 28, axis=0)
            M_beta[s_i, :, :] = beta_t_check
        _, _, death_wk, state_alltime = para_LKH(state_check, beta_t_check, M_eta_06, IFR_06_daily_wd_adj, delay_dist_init, 0, T, death_06_wk_s, location)
        M_death_wk[s_i, :, :] = death_wk
        M_State[s_i, :, :, :] = state_alltime[:, :, :]

    return M_beta, M_death_wk, M_State