# Import the pygame module
import pygame
import sys
import random
from Agent import *
from Target import *
from Cell import *
from CONSTANTS import *
from help_functions import *

# ---------------------------
# ------INPUT SETTINGS-------
# ---------------------------
cell_size = CELL_SIZE['BIG']
cell_size = CELL_SIZE['MEDIUM']
# cell_size = CELL_SIZE['SMALL']
algorithms = ['DSA',]
target_rate = 0.05
show_ranges = True
MR = 2.5*cell_size
SR = 1.5*cell_size
# ---------------------------
# INITIALIZATIONS:
clock = pygame.time.Clock()
pygame.mixer.init()
pygame.init()
screen = pygame.display.set_mode((SCREEN_HEIGHT + 202, SCREEN_HEIGHT), pygame.SRCALPHA)

# Create a custom event for adding a new enemy
ADDENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(ADDENEMY, 250)
MOVEAGENTS = pygame.USEREVENT + 2
pygame.time.set_timer(MOVEAGENTS, 2000)

# Instantiate player. Right now, this is just a rectangle.
# player = Agent(cell_size)

# Create groups to hold all kinds of sprites
# - all_sprites is used for rendering
agents = pygame.sprite.Group()
targets = pygame.sprite.Group()
cells = pygame.sprite.Group()
titles = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()

# Renders the titles aside of a field
create_side_titles(algorithms[0], all_sprites, titles)

# Create Field
create_field(cell_size, all_sprites, cells)
print(len(cells.sprites()))

# Create targets on field
create_targets(cell_size, all_sprites, targets, titles, cells, target_rate)

# Create agents on field
create_agents(cell_size, all_sprites, agents, cells,
              num_of_agents=4,
              MR=MR,
              SR=SR,
              show_ranges=show_ranges)


def main():
    # Variable to keep the main loop running
    running = True
    time1 = 0
    time2 = 0
    failed = False


    # Main loop
    while running:
        # for loop through the event queue
        for event in pygame.event.get():
            # Check for KEYDOWN event
            if event.type == KEYDOWN:
                # If the Esc key is pressed, then exit the main loop
                if event.key == K_ESCAPE:
                    running = False
            # Check for QUIT event. If QUIT, then set running to false.
            elif event.type == QUIT:
                running = False

            # Add a new enemy?
            elif event.type == ADDENEMY:
                # Create the new enemy and add it to sprite groups
                # new_enemy = Target(cell_size)
                # targets.add(new_enemy)
                # all_sprites.add(new_enemy)
                # titles.update(len(targets.sprites()))
                pass

            # Add a new cloud?
            elif event.type == MOVEAGENTS:
                # Create the new cloud and add it to sprite groups
                # new_cloud = Cell()
                # cells.add(new_cloud)
                # all_sprites.add(new_cloud)
                time1 = pygame.time.get_ticks()

        time2 = pygame.time.get_ticks()
        if time2 - time1 < 1000:
            agents.update()

        # Get the set of keys pressed and check for user input
        pressed_keys = pygame.key.get_pressed()

        # Update the player sprite based on user keypresses
        # agents.sprites()[0].update(pressed_keys)

        # Update enemy position
        targets.update()
        # cells.update()

        # Fill the screen with black
        screen.fill(SKY_COLOR)

        # Draw all sprites
        # all_sprites.draw(screen)
        for entity in all_sprites:
            screen.blit(entity.surf, entity.rect)

        # Check if any enemies have collided with the player
        if pygame.sprite.spritecollideany(agents.sprites()[0], targets):
            # If so, then remove the player and stop the loop
            # player.kill()
            # time1 = pygame.time.get_ticks()
            # failed = True
            # running = False
            pass

        # Update the display
        pygame.display.flip()

        # Ensure program maintains a rate of 30 frames per second
        #clock.tick(80)

    # All done! Stop and quit the mixer.
    pygame.mixer.music.stop()
    pygame.mixer.quit()

    # Done! Time to quit.
    pygame.quit()

if __name__ == '__main__':
    main()