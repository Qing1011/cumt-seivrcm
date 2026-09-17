import numpy as np
import matplotlib.pyplot as plt
from scipy.io import loadmat, savemat
import pandas as pd
import scipy.special as SS
import scipy.stats as SSA
import copy
import random
import math
import matplotlib.dates as mdates
import sys
sys.path.append('../codes/')
from data_input import *

data_path = '../data/github/'

### Contact matrix
# The rows, similarly, represent the race/ethnicity groups. However, when looking at a row, you're focusing on that specific race/ethnicity group and seeing how many effective contacts it has with each of the groups listed in the columns.


def get_CM_normalised(race_list, populations_loc, CM_loc_community, CM_loc_household, CM_loc_school,CM_loc_work):
    
    student_percent = populations_loc[(populations_loc['demographic_category'] == 'age')&(populations_loc['demographic_value'] == '0-17')]['percent'].values[0]
    work_percent = populations_loc[(populations_loc['demographic_category'] == 'age')&(populations_loc['demographic_value'] == '18-64')]['percent'].values[0]

    CM_loc = {}
    for race in race_list:
        CM_loc[race] = CM_loc_community.loc[race] + CM_loc_household.loc[race] + student_percent*CM_loc_school.loc[race] + work_percent*CM_loc_work.loc[race]

    df = pd.DataFrame(CM_loc) ### the columns are for a given races, the number of contacts with people of other races
    df_normalized = df.div(df.sum(axis=0), axis=1)

    CM_loc_arrary = pd.DataFrame(CM_loc).to_numpy().T
    CM_loc_normalised = CM_loc_arrary/np.sum(CM_loc_arrary, axis = 1)[:,None] 

    return df_normalized, CM_loc_normalised

