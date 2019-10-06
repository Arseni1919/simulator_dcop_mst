# Import the pygame module
import pygame
import threading
import sys
# bla bla
from CONSTANTS import *

# Import random for random numbers
import random


# Define a player object by extending pygame.sprite.Sprite
# The surface drawn on the screen is now an attribute of 'player'
class Agent(pygame.sprite.Sprite):
    def __init__(self,
                 cell_size=CELL_SIZE['BIG'],
                 number_of_robot=0,
                 surf_center=-1,
                 MR=round(3.5*CELL_SIZE['BIG']),
                 SR=int(2.5*CELL_SIZE['BIG']),
                 show_ranges=False
                 ):
        super(Agent, self).__init__()
        self.number_of_robot = number_of_robot
        self.MR = int(MR)
        self.SR = int(SR)
        self.show_ranges = show_ranges

        self.surf = pygame.Surface((2*MR, 2*MR), pygame.SRCALPHA)
        if show_ranges:
            pygame.draw.circle(self.surf, (0, 0, 255, 20), self.surf.get_rect().center, self.MR)
            pygame.draw.circle(self.surf, (255, 0, 0, 40), self.surf.get_rect().center, self.SR)

        self.car_surf = pygame.transform.scale(pygame.image.load("hamster2.png"), (cell_size, int(0.73*cell_size)))
        self.car_surf.set_colorkey((255, 255, 255), RLEACCEL)
        # Number of Robot
        font = pygame.font.SysFont("comicsansms", int(cell_size * 0.25))
        text = font.render("%s" % number_of_robot, True, (225, 0, 0))
        wt, ht = text.get_size()
        self.car_surf.blit(text, (cell_size - wt, 0))
        self.surf.blit(self.car_surf, self.car_surf.get_rect(center=self.surf.get_rect().center))
        # self.rect = self.surf.get_rect()
        if surf_center == -1:
            self.rect = self.surf.get_rect()
            raise ValueError('surf_center == -1 in Agent')
        else:
            self.surf_center = surf_center
            self.rect = self.surf.get_rect(
                center=surf_center
            )

    # Move the sprite based on user keypresses
    def update(self, pressed_keys=None):
        print(threading.get_ident())
        self.rect.move_ip(3, -3)
        # if pressed_keys[K_UP]:
        #     self.rect.move_ip(0, -5)
        # if pressed_keys[K_DOWN]:
        #     self.rect.move_ip(0, 5)
        # if pressed_keys[K_LEFT]:
        #     self.rect.move_ip(-5, 0)
        # if pressed_keys[K_RIGHT]:
        #     self.rect.move_ip(5, 0)
        #
        # # Keep player on the screen
        # if self.rect.left < 0:
        #     self.rect.left = 0
        # if self.rect.right > SCREEN_HEIGHT:
        #     self.rect.right = SCREEN_HEIGHT
        # if self.rect.top <= 0:
        #     self.rect.top = 0
        # if self.rect.bottom >= SCREEN_HEIGHT:
        #     self.rect.bottom = SCREEN_HEIGHT


