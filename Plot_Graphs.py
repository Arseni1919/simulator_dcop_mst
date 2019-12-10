from CONSTANTS import *
from main_help_functions import *

# '.'
# ','
# 'o'
# 'v'
# '^'
# '<'
# '>'
# '1'
# '2'
# '3'
# '4'
# 's'
# 'p'
# '*'
# 'h'
# 'H'
# '+'
# 'x'
# 'D'
# 'd'
# '|'
# '_'

# ---------------------------
# ------INPUT SETTINGS-------
# ---------------------------
file_name = "10.12.2019-14:08:26__Max_sum_3__Max_sum_2__Max_sum_1__DSA__file.data"
need_to_plot_variance = False
need_to_plot_min_max = False
# ---------------------------
file_name = 'data/%s' % file_name
with open(file_name, 'rb') as fileObject:
    # load the object from the file into var b
    graphs = pickle.load(fileObject)
    algorithms = list(graphs.keys())
    plot_results_if(True, need_to_plot_variance, need_to_plot_min_max, graphs, algorithms, alpha=0.025)











