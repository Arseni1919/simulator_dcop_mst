# Import the pygame module
import sys, os
import pygame
import sys
import random
import pygame.freetype as freetype
from Agent import *
# from Target import *
# from Cell import *
# from CONSTANTS import *

# rect = pygame.Rect([10,10,10,10])
# # print(rect._lock)
# # raise ValueError('surf_center == -1 in Agent')
pygame.init()
# screen = pygame.display.set_mode((SCREEN_HEIGHT,SCREEN_HEIGHT))
# font = pygame.font.SysFont("comicsansms", 50)
# text2 = font.render("Hello, World", True, (225, 0, 0))
# text1 = font.render("Hello, World", False, (225, 0, 0))
#
# circle_surf = pygame.Surface((100, 100), pygame.SRCALPHA)
# # circle_surf.get_rect().center
# pygame.draw.circle(circle_surf, (0, 0, 255, 100), circle_surf.get_rect().center, 50)
# pygame.draw.circle(circle_surf, (30, 224, 33, 100), (0,0), 100)

# fontdir = os.path.dirname(os.path.abspath (__file__))
# font = pygame.font.SysFont('arial', 5)
# font = freetype.Font(font)
# font = freetype.Font(os.path.join (fontdir, "data", "sans.ttf"))

# Variable to keep the main loop running
# running = True
# size = 18
# print(int(SCREEN_HEIGHT/(size + 2)))
# # Main loop
# while running:
#     # Look at every event in the queue
#     for event in pygame.event.get():
#         # Did the user hit a key?
#         if event.type == KEYDOWN:
#             # Was it the Escape key? If so, stop the loop.
#             if event.key == K_ESCAPE:
#                 running = False
#
#         # Did the user click the window close button? If so, stop the loop.
#         elif event.type == QUIT:
#             running = False
#
#         # Fill the screen with white
#         screen.fill((255, 255, 255))
#
#         # Create a surface and pass in a tuple containing its length and width
#
#         # surf = pygame.Surface((size, size))
#         #
#         # # Give the surface a color to separate it from the background
#         # surf.fill((0, 0, 0))
#         # rect = surf.get_rect()
#         #
#         # # Put the center of surf at the center of the display
#         # surf_center = (
#         #     (SCREEN_HEIGHT - surf.get_width()) / 2,
#         #     (SCREEN_HEIGHT - surf.get_height()) / 2
#         # )
#         #
#         # # This line says "Draw surf onto the screen at the center"
#         # screen.blit(surf, surf_center)
#
#         for i in range(int(SCREEN_HEIGHT/(size + 2))):
#             for j in range(int(SCREEN_HEIGHT/(size + 2))):
#                 surf = pygame.Surface((size, size))
#                 surf.fill((0, 0, 0))
#                 rect = surf.get_rect()
#                 surf_center = (
#                 2 + i*(size + 2),
#                 2 + j*(size + 2)
#                 )
#                 screen.blit(surf, surf_center)
#         screen.blit(text1, (int(SCREEN_HEIGHT/2), int(SCREEN_HEIGHT/2)))
#         screen.blit(text2, (int(SCREEN_HEIGHT / 2), int(SCREEN_HEIGHT / 2 + 50)))
#         pygame.draw.circle(circle_surf, (30, 224, 33, 100), (250, 100), 10)
#         screen.blit(circle_surf, screen.get_rect().center)
#         # freetype.Font.render_to(screen, (265, 237), "or BLAND!")
#         # font.render_to(screen, (265, 237), "or BLAND!",
#
#
#         pygame.display.flip()


# from main_help_functions import *
# file_name = 'data/02.12.2019-14:55:52_Max_sum__DSA_PILR__DSA__MGM_file.data'
# with open(file_name, 'rb') as fileObject:
#     graphs = pickle.load(fileObject)
#     print_t_test_table(graphs)


def foo():
    print('a')

def foo():
    print('b')

foo()
# print(a)
    # time.sleep()
# print(np.random.randint(180))


