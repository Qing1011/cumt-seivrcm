import numpy as np
import pandas as pd
from scipy.interpolate import PchipInterpolator
import matplotlib.pyplot as plt
import os
import csv
import datetime as d
from datetime import datetime as D
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import random 
import time
import math
import scipy
from scipy import stats
from scipy.stats import norm
from scipy.optimize import curve_fit
from data_input import *

dates = pd.date_range(start='2020-03-11', periods=8, freq='MS') + pd.Timedelta(days=11)
dates_ihave = dates[[0,3,4,5,6,7]]
date_nums = dates_ihave.map(pd.Timestamp.toordinal)
daily_dates = pd.date_range(start=dates_ihave.min(), end=dates_ihave.max(), freq='D')
daily_date_nums = daily_dates.map(pd.Timestamp.toordinal)

def generate_random_between_bounds(lower_bound, upper_bound, must_be_larger_than=None):
    t = np.random.uniform(lower_bound, upper_bound)
    # Generate the random number
    return max(t, must_be_larger_than)




def distribution_daily(start_date, num_weeks, M_weekly,wd=7):
    # Generate the dates for the 31 weeks starting from 18 April 2020
    """
    Generate the daily distribution of cases from the weekly data
    """

    # Weekly dates (every Saturday)
    dates_weekly = pd.date_range(start=start_date, periods=num_weeks, freq='W-SAT')
    # Daily dates range for the entire period, aligning with the weekly start dates
    dates_daily = pd.date_range(start=dates_weekly[0] - pd.Timedelta(days=6), end=dates_weekly[-1], freq='D')
    # Initialize a daily DataFrame with zeros
    daily_df = pd.DataFrame(0.00, index=dates_daily, columns=range(5))
    # Distribute weekly values backward
    for i, date in enumerate(dates_weekly[1:]):
        # Find the start date of the week
        week_start = date - pd.Timedelta(days=6)
        # Assign and distribute weekly values to each day of the corresponding week
        for col in daily_df.columns:
            M_weekly[i, col] / 7
            up = M_weekly[i+1,col]
            low = M_weekly[i,col]
            step = (up - low)/7
            weekly_value = np.array([low + step * j for j in range(7)])
            daily_df.loc[week_start:date, col] = weekly_value

    # Calculate the 7-day rolling average for smoothing, aligning the window to end on the 'start_date'
    smoothed_daily_df = daily_df.rolling(window=wd, min_periods=1).mean()
    return smoothed_daily_df


# Redefining our model function to fit the curve_fit expectations
def model_func(x, a, b):
    y = a+ b*x
    return y