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
        font = pygame.font.SysFont("comicsansms", 30)
        text = font.render("%s" % alg_name, True, (0, 0, 0))
        wt, ht = self.surf.get_size()
        self.surf.blit(text, (0, 0))

        # self.surf.fill((255, 255, 255))
        self.rect = self.surf.get_rect(
            center=(int((SCREEN_WIDTH - 200)), int(ht/2) + ht*order)
        )

    # Move the sprite based on speed
    # Remove the sprite when it passes the left edge of the screen
    def update(self, iter=0):
        if self.alg_name == "Iteration:":
            self.surf.fill(SKY_COLOR)
            font = pygame.font.SysFont("comicsansms", 30)
            text = font.render("%s" % self.alg_name, True, (0, 0, 0))
            self.surf.blit(text, (0, 0))
            text = font.render("%s" % iter, True, (0, 0, 0))
            self.surf.blit(text, (0, 40))
        if self.alg_name == "Convergence:":
            self.surf.fill(SKY_COLOR)
            font = pygame.font.SysFont("comicsansms", 30)
            text = font.render("%s" % self.alg_name, True, (0, 0, 0))
            self.surf.blit(text, (0, 0))
            text = font.render("%s" % int(iter/2), True, (0, 0, 0))
            self.surf.blit(text, (0, 40))
