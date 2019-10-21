# Import the pygame module
import pygame
import sys
import random
from Agent import *
from Target import *
from Cell import *
from CONSTANTS import *

# Define the enemy object by extending pygame.sprite.Sprite
# The surface you draw on the screen is now an attribute of 'enemy'
class Title(pygame.sprite.Sprite):
    def __init__(self, alg_name='None', order=0):
        super(Title, self).__init__()
        self.surf = pygame.Surface((200, 100), pygame.SRCALPHA)
        self.alg_name = alg_name
        # Number of Requirement
        font = pygame.font.SysFont("comicsansms", 25)
        text = font.render("%s" % alg_name, True, (0, 0, 0))
        wt, ht = self.surf.get_size()
        self.surf.blit(text, (0, 0))
        self.dont_kill = False
        # self.surf.fill((255, 255, 255))
        self.rect = self.surf.get_rect(
            center=(int((SCREEN_WIDTH - 200)), int(ht/2) + ht*order)
        )

    # Move the sprite based on speed
    # Remove the sprite when it passes the left edge of the screen
    def update(self, iteration=0, MAX_ITERATIONS=0,
               conv=0,
               problem=0, NUMBER_OF_PROBLEMS=0,
               algorithm=None, algorithms=[],
               interval=2):

        index_of_alg = algorithms.index(algorithm) + 1
        length_of_algs = len(algorithms)
        total = NUMBER_OF_PROBLEMS * length_of_algs * MAX_ITERATIONS

        if self.alg_name == "Algorithm:":
            self.surf.fill(SKY_COLOR)
            font = pygame.font.SysFont("comicsansms", 30)
            text = font.render("%s" % self.alg_name, True, (0, 0, 0))
            self.surf.blit(text, (0, 0))
            text = font.render("%s out of %s" % (index_of_alg, length_of_algs), True, (0, 0, 0))
            self.surf.blit(text, (0, 40))

        if self.alg_name == "Problem:":
            self.surf.fill(SKY_COLOR)
            font = pygame.font.SysFont("comicsansms", 30)
            text = font.render("%s" % self.alg_name, True, (0, 0, 0))
            self.surf.blit(text, (0, 0))
            text = font.render("%s out of %s" % (problem + 1, NUMBER_OF_PROBLEMS), True, (0, 0, 0))
            self.surf.blit(text, (0, 40))

        if self.alg_name == "Iteration:":
            self.surf.fill(SKY_COLOR)
            font = pygame.font.SysFont("comicsansms", 30)
            text = font.render("%s" % self.alg_name, True, (0, 0, 0))
            self.surf.blit(text, (0, 0))
            text = font.render("%s out of %s" % (iteration, MAX_ITERATIONS), True, (0, 0, 0))
            self.surf.blit(text, (0, 40))

        if self.alg_name == "Convergence:":
            self.surf.fill(SKY_COLOR)
            font = pygame.font.SysFont("comicsansms", 30)
            text = font.render("%s" % self.alg_name, True, (0, 0, 0))
            self.surf.blit(text, (0, 0))
            text = font.render("%s" % conv, True, (0, 0, 0))
            self.surf.blit(text, (0, 40))

        if self.alg_name == "Remained:":
            did_prop_it = problem * length_of_algs * MAX_ITERATIONS
            did_alg_it = (index_of_alg - 1) * MAX_ITERATIONS
            did_it = iteration
            rem_iter = total - did_prop_it - did_alg_it - did_it
            minutes = int(rem_iter*interval/60)
            seconds = int((rem_iter*interval/60 - int(rem_iter*interval/60))*60)
            self.surf.fill(SKY_COLOR)
            font = pygame.font.SysFont("comicsansms", 30)
            text = font.render("%s" % self.alg_name, True, (0, 0, 0))
            self.surf.blit(text, (0, 0))
            text = font.render("~ %s m %s s" % (minutes, seconds), True, (0, 0, 0))
            self.surf.blit(text, (0, 40))
