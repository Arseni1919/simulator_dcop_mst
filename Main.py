from Agent import *
from Target import *
from Cell import *
from CONSTANTS import *
from Algorithms import *
from help_functions import *

# ---------------------------
# ------INPUT SETTINGS-------
# ---------------------------

cell_size = CELL_SIZE['BIG']
cell_size = CELL_SIZE['MEDIUM']
# cell_size = CELL_SIZE['SMALL']
show_ranges = True
need_to_save_results = False
need_to_plot_results = False
speed = 10  # bigger -slower, smaller - faster. don't ask why

num_of_agents = 5
algorithms = ['DSA',]
target_rate = 0.05
MR = 2.5*cell_size
SR = 1.5*cell_size
MAX_ITERATIONS = 10
# ---------------------------

# ---------------------------
# ----------GRAPHS-----------
# ---------------------------
graphs = {}
for algorithm in algorithms:
    graphs[algorithm] = []
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
              num_of_agents=num_of_agents,
              MR=MR,
              SR=SR,
              show_ranges=show_ranges,
              speed=speed)


def main():
    # Variable to keep the main loop running
    time1 = pygame.time.get_ticks()
    time3 = pygame.time.get_ticks()
    counter = 0
    iteration = 0
    convergence = 0
    running = True

    # Main loop
    while iteration < MAX_ITERATIONS and running:
        running = False if iteration == MAX_ITERATIONS else True
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
                # time1 = pygame.time.get_ticks()
                pass

        time2 = pygame.time.get_ticks()
        if not all_arrived(agents):
            counter += 1
            # makes a join to everybody
            with concurrent.futures.ThreadPoolExecutor(max_workers=len(agents.sprites())) as executor:
                for agent in agents.sprites():
                    executor.submit(agent.move)
            # logging.info("Thread %s : finishing moving!", threading.get_ident())

        if all_arrived(agents) and time2 - time1 > 1000:
            # -----------------------------------------
            # UPDATING
            # -----------------------------------------
            iteration += 1
            convergence = convergence_update(iteration)
            graphs[algorithms[0]].append(convergence)
            # -----------------------------------------
            # print(time2 - time3)
            # print(counter)
            counter = 0
            time3 = pygame.time.get_ticks()
            # makes a join to everybody
            with concurrent.futures.ThreadPoolExecutor(max_workers=len(agents.sprites())) as executor:
                for agent in agents.sprites():
                    executor.submit(agent.update, dict_alg[algorithms[0]], targets, cells)
            # logging.info("Thread %s : finishing updating!", threading.get_ident())
            time1 = pygame.time.get_ticks()

        # Get the set of keys pressed and check for user input
        pressed_keys = pygame.key.get_pressed()
        # agents.sprites()[0].update(pressed_keys)

        # Update what is necessary
        targets.update()
        titles.update(iteration, convergence)

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
            pass

        # Update the display
        pygame.display.flip()

    # All done! Stop and quit the mixer.
    pygame.mixer.music.stop()
    pygame.mixer.quit()

    # Done! Time to quit.
    pygame.quit()

    # Save the results
    pickle_results_if(need_to_save_results, graphs)

    # Plot results
    plot_results_if(need_to_plot_results, graphs, algorithms)


if __name__ == '__main__':
    main()

'''
 - dictionary of algorithms - correct
 - clean code in main
 - make algorithms transparent to robots ans simulator
 - save initial positions for specific problem
 - make more beautiful graphs
 - update temp_req in targets
 - 
'''



