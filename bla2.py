from CONSTANTS import *

# graphs = {'DSA': [1,2,3,4]}
# # Save the results
# file_Name = "testfile.data"
# # open the file for writing
# with open(file_Name, 'wb') as fileObject:
#     # this writes the object a to the file named 'testfile.data'
#     pickle.dump(graphs, fileObject)
from networkx import is_empty
import numpy as np
import math
from Algorithms import *
# from Target import *

# pygame.init()
# b= [1,2,3]
# targets = []
# targets.append((Target(req=1, surf_center=(8,4)), 7))
# targets.append((Target(req=1, surf_center=(9,5)), 5))
# targets.append((Target(req=1, surf_center=(10,2)), 5))
# targets.append((Target(req=1, surf_center=(1,4)), 4))
# targets.append((Target(req=300, surf_center=(6,1)), 3))
# targets.append((Target(req=1, surf_center=(10,6)), 3))
# pos_set = [(5,7),(6,4),(7,2),(9,3),(10,4),(10,8),]
# print(select_pos(pos_set, targets, 1))
# time1 = time.time()
# print(time.sleep(0.001))
# time2 = time.time()
# print(time2 - time1)

# a = np.random.randint(5, size=(2, 10))
# from scipy.stats import t
# alpha = 0.025
#
# t_value = t.ppf(1 - alpha, df=9)
# # print(get_cov([(Target(req=1, surf_center=(1,4)), 4),(Target(req=1, surf_center=(10,6)), 3)],(1,2),3))
#
# avr = np.average(a, 1)
# std = np.std(a, 1)
# import matplotlib
# markers=[',', '+', '-', '.', 'o', '*']

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

lines = ['-', '--', '-.', ':',]
# print(matplotlib.markers)
algorithms = ['DSA_PILR',]
algorithms = ['DSA_PILR', 'DSA',]
algorithms = ['DSA_PILR', 'DSA', 'MGM',]
# algorithms = ['DSA_PILR', 'DSA', 'MGM','DSA_PILR', 'DSA', 'MGM',]

file_name = "data/13.10.2019-16:30:05_for_graph_file.data"
# open the file for writing
# with open(file_name, 'wb') as fileObject:
#     # this writes the object a to the file named 'testfile.data'
#     pickle.dump(graphs, fileObject)

from main_help_functions import *
with open(file_name, 'rb') as fileObject:
    # load the object from the file into var b
    graph = pickle.load(fileObject)
    num = 0
    for k, v in graph.items():
        num += 1
        v = v * num
    plot_results_if(True, graph, algorithms, 0.025)

import time
timestr = time.strftime("%Y.%m.%d-%H:%M:%S")
print(timestr)










