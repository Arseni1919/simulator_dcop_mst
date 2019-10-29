# Import the pygame module
from CONSTANTS import *


# Define the cell object by extending pygame.sprite.Sprite
# Use an image for a better-looking sprite
class Cell(pygame.sprite.Sprite):
    def __init__(self, cell_size=CELL_SIZE['BIG'], surf_center=-1):
        super(Cell, self).__init__()
        self.cell_size = cell_size
        self.surf = pygame.Surface((cell_size, cell_size))
        self.surf.fill((255, 255, 255))
        # The starting position is randomly generated
        if surf_center == -1:
            # self.rect = self.surf.get_rect(
            #     center=(
            #         random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
            #         random.randint(0, SCREEN_HEIGHT),
            #     )
            # )
            raise ValueError('surf_center == -1 in Cell')
        else:
            self.surf_center = surf_center
            self.rect = self.surf.get_rect(
                center=surf_center
            )
        self.prop = None

    # Move the cloud based on a constant speed
    # Remove the cloud when it passes the left edge of the screen
    def update(self):
        self.rect.move_ip(-5, 0)
        if self.rect.right < 0:
            self.kill()

    def add_property(self, prop):
        self.prop = prop

    def get_prop(self):
        return self.prop

    def get_pos(self):
        return self.surf_center
