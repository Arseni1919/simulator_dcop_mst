
# Define constants for the screen width and height
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 690

CELL_SIZE = {
    'SMALL': 18,
    'MEDIUM': 35,
    'BIG': 74,
}

SKY_COLOR = (135, 206, 250)

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