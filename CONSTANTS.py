import pygame
import sys
import random
import logging
import threading
import time
import concurrent.futures
import matplotlib.pyplot as plt
import math
import numpy as np
import pickle
import copy
from scipy.stats import t


# Define constants for the screen width and height
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 690

# have to be odd number for move method of Agent
CELL_SIZE = {
    'SMALL': 18,
    'MEDIUM': 34,
    'BIG': 74,
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

