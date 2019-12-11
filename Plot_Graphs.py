from main_help_functions import *

# ---------------------------
# ------INPUT SETTINGS-------
# ---------------------------
file_name = "11.12.2019-15:15:43__Max_sum_4__file.data"
need_to_plot_variance = False
need_to_plot_min_max = False
# ---------------------------

file_name = 'data/%s' % file_name

file_name = file_name[:-5] + '.info'
with open(file_name, 'rb') as fileObject:
    # load the object from the file into var b
    info = pickle.load(fileObject)
    pprint.pprint(info)
    print(info)

file_name = file_name[:-5] + '.data'
with open(file_name, 'rb') as fileObject:
    # load the object from the file into var b
    graphs = pickle.load(fileObject)
    algorithms = list(graphs.keys())
    plot_results_if(True, need_to_plot_variance, need_to_plot_min_max, graphs, algorithms, alpha=0.025)


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













