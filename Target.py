# Import the pygame module
from CONSTANTS import *
# Import random for random numbers
import random


# Define the enemy object by extending pygame.sprite.Sprite
# The surface you draw on the screen is now an attribute of 'enemy'
class Target(pygame.sprite.Sprite):
    def __init__(self, cell_size=CELL_SIZE['BIG'], req=1, surf_center=-1):
        super(Target, self).__init__()
        self.req = req
        self.temp_req = req
        self.surf = pygame.Surface((cell_size, cell_size), pygame.SRCALPHA)
        pygame.draw.circle(self.surf, (0, 0, 255), [int(cell_size/2), int(cell_size/2)], int(cell_size/2 - 2))
        # Number of Requirement
        font = pygame.font.SysFont("comicsansms", int(cell_size * 0.8))
        text = font.render("%s" % self.req, True, (255,255,0))
        wt, ht = text.get_size()
        self.surf.blit(text, (int((cell_size - wt)/2), int((cell_size - ht)/2)))

        if surf_center == -1:
            # self.rect = self.surf.get_rect(
            #     center=(
            #         random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
            #         random.randint(0, SCREEN_HEIGHT),
            #     )
            # )
            raise ValueError('surf_center == -1 in Target')
        else:
            self.surf_center = surf_center
            self.rect = self.surf.get_rect(
                center=surf_center
            )
        # self.speed = random.randint(1, 4)

    # Move the sprite based on speed
    # Remove the sprite when it passes the left edge of the screen
    def update(self):
        # update self.temp_req
        pass

    def get_pos(self):
        return self.surf_center

    def get_req(self):
        return self.req

    def get_temp_req(self):
        return self.temp_req

    def set_temp_req(self, temp_req):
        self.temp_req = temp_req


