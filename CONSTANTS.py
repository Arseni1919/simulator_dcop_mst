import pygame
import sys
import random
import logging
import threading
import time
import concurrent.futures
import matplotlib
# matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import math
import numpy as np
import pickle
import json
import copy
from scipy.stats import t
from scipy import stats
import itertools
# from tqdm import tqdm
from pprint import pprint
import statistics
from collections import namedtuple

CellTuple = namedtuple('CellTuple', ['pos',])
TargetTuple = namedtuple('TargetTuple', ['pos', 'req', 'name', 'num'])
AgentTuple = namedtuple('AgentTuple', ['pos', 'num_of_robot_nei', 'num_of_target_nei', 'name', 'num', 'cred', 'SR', 'MR'])
MessageType = namedtuple('MessageType', ['from_var_to_func',
                                         'from_func_pos_collisions_to_var',
                                         'from_func_dir_collisions_to_var',
                                         'from_func_target_to_var'])
message_types = MessageType(from_var_to_func='from_var_to_func',
                            from_func_pos_collisions_to_var='from_func_pos_collisions_to_var',
                            from_func_dir_collisions_to_var='from_func_dir_collisions_to_var',
                            from_func_target_to_var='from_func_target_to_var')
from_func_to_var_types = (message_types.from_func_pos_collisions_to_var, message_types.from_func_target_to_var,
                          message_types.from_func_dir_collisions_to_var)
TypesOfRequirement = namedtuple('TypesOfRequirement', ['copy', 'copy_var_dicts', 'copy_func_dicts'])
copy_types = TypesOfRequirement('copy', 'copy_var_dicts', 'copy_func_dicts')


OBJECTS = {}


# Define constants for the screen width and height
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 690
# SCREEN_HEIGHT = 850

# have to be odd number for move method of Agent
CELL_SIZE = {
    'SMALL': 18,
    'MEDIUM': 34,
    'BIG': 74,
    'CUSTOM': 10,
}

SKY_COLOR = (135, 206, 250)
# SPEED_MOVING = 10

# Import pygame.locals for easier access to key coordinates
# Updated to conform to flake8 and black standards
from pygame.locals import (
    RLEACCEL,
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

# for logging
_format = "%(asctime)s: %(message)s"
logging.basicConfig(format=_format, level=logging.INFO,
                    datefmt="%H:%M:%S")
# logging.getLogger().setLevel(logging.DEBUG)

