from Algorithms import *
from Max_sum_drafts import *
from main_help_functions import *
from CONSTANTS import *

# ---------------------------
# ------INPUT SETTINGS-------
# ---------------------------
# SET CELL SIZE THIS WAY:
# cell_size = CELL_SIZE['BIG']
# cell_size = CELL_SIZE['MEDIUM']
# cell_size = CELL_SIZE['SMALL']
# ---
# OR THIS WAY:
grid_size = 50
CELL_SIZE['CUSTOM'] = int(SCREEN_HEIGHT/grid_size - 2)
cell_size = CELL_SIZE['CUSTOM']
# ---
show_ranges = True
need_to_save_results = False
adding_to_file_name = ''
need_to_plot_results = True
need_to_plot_variance = False
need_to_plot_min_max = True
alpha = 0.025  # for confidence intervals in graphs
speed = 5  # bigger -slower, smaller - faster. don't ask why
num_of_agents = 10
num_of_targets = 10
use_rate = False  # if False - it uses the num_of_targets variable, but still also uses target_rate
target_rate = 0.055

target_range = (100, 100)  # max and min value of target
MR = 5.5 * cell_size
SR = 5.5 * cell_size
cred = 30
MAX_ITERATIONS = 25
NUMBER_OF_PROBLEMS = 10

algorithms = ['Max_sum_4', 'Max_sum_3', 'Max_sum_2', 'Max_sum_1', 'DSA']
# algorithms = ['Max_sum_2', 'Max_sum_1', ]
# algorithms = ['DSA_PILR_0.2','DSA_PILR_0.5','DSA_PILR_0.8',]
# algorithms = ['DSA_PILR', ]
# algorithms = ['Max_sum', 'DSA_PILR_1', 'DSA_PILR_2', 'DSA_PILR_3', 'DSA_PILR_4', 'DSA', 'MGM', ]
# algorithms = ['DSA_PILR', 'DSA', 'MGM', ]
# algorithms = [
#     # 'DSA_PILR_1',
#     # 'DSA_PILR_2',
#     # 'DSA_PILR_3',
#     # 'DSA_PILR_4',
#     # 'DSA_PILR_5',
#     'DSA_PILR_6',
#     'DSA_PILR_7',  # best
#     'DSA_PILR_8',
#     'DSA_PILR_9',
#     # 'MGM',
#     # 'DSA_4',
#     'DSA_5',
# ]
# algorithms = ['DSA_PILR', 'DSA', 'MGM',]

# ---------------------------

# ------ ------ ------ ------ ------ ------ ------ ------ ------ ------ ------ ------ ------ ------ ------ ------ ------
# ------ ------ ------ ------ ------ ------ ------ ------ ------ ------ ------ ------ ------ ------ ------ ------ ------
# dictionary
# ------ ------ ------ ------ ------ ------ ------ ------ ------ ------ ------ ------ ------ ------ ------ ------ ------
# ------ ------ ------ ------ ------ ------ ------ ------ ------ ------ ------ ------ ------ ------ ------ ------ ------
dict_alg = {
    'Max_sum_1': (Max_sum, [1, cred, SR, max_sum_1_function_message_to, 'random']),
    'Max_sum_2': (Max_sum, [5, cred, SR, max_sum_2_function_message_to, 'random']),
    'Max_sum_3': (Max_sum, [5, cred, SR, max_sum_2_function_message_to, 'random_furthest']),
    'Max_sum_4': (Max_sum, [5, cred, SR, max_sum_2_function_message_to, 'random_furthest_directed']),
    'DSA': (DSA, [0.7]),
    'DSA_2': (DSA, [0.5]),
    'DSA_3': (DSA, [0.3]),
    'DSA_4': (DSA, [0.6]),
    'DSA_5': (DSA, [0.7]),
    'MGM': (MGM, []),
    'DSA_PILR': (DSA_PILR, [0.7, 20, 0.5]),
    'DSA_PILR_1': (DSA_PILR, [0.7, 20, 0.2]),
    'DSA_PILR_2': (DSA_PILR, [0.7, 20, 0.4]),
    'DSA_PILR_3': (DSA_PILR, [0.7, 20, 0.6]),
    'DSA_PILR_4': (DSA_PILR, [0.7, 20, 0.8]),
    'DSA_PILR_5': (DSA_PILR, [0.8, 3, 0.5]),
    'DSA_PILR_6': (DSA_PILR, [0.5, 3, 0.5]),
    'DSA_PILR_7': (DSA_PILR, [0.8, 3, 0.5]),
    'DSA_PILR_8': (DSA_PILR, [0.7, 3, 0.5]),
    'DSA_PILR_9': (DSA_PILR, [0.6, 3, 0.5]),
}

factor_graph = {
    Max_sum: True,
    DSA: False,
    MGM: False,
    DSA_PILR: False,
}
for algorithm in algorithms:
    if dict_alg[algorithm][0] not in factor_graph.keys():
        raise ValueError('dict_alg[algorithms][0] not in factor_graph.keys()')
# ------ ------ ------ ------ ------ ------ ------ ------ ------ ------ ------ ------ ------ ------ ------ ------ ------

# ---------------------------
# ----------GRAPHS-----------
# ---------------------------
graphs = {}
for algorithm in algorithms:
    graphs[algorithm] = np.zeros((MAX_ITERATIONS, NUMBER_OF_PROBLEMS))
    if algorithm not in dict_alg.keys():
        raise ValueError('algorithm not in dict')
# ---------------------------
# INITIALIZATIONS:
clock = pygame.time.Clock()
pygame.mixer.init()
pygame.init()
screen = pygame.display.set_mode((SCREEN_HEIGHT + 202, SCREEN_HEIGHT), pygame.SRCALPHA)
finish_sound = pygame.mixer.Sound("sounds/Bell_2.ogg")

# Create a custom event for adding a new enemy
ADDENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(ADDENEMY, 250)
MOVEAGENTS = pygame.USEREVENT + 2
pygame.time.set_timer(MOVEAGENTS, 2000)

if __name__ == '__main__':
    # Variable to keep the main loop running
    running = True
    time1 = pygame.time.get_ticks()
    time3 = pygame.time.get_ticks()
    interval = 2

    # Main loop
    for problem in range(NUMBER_OF_PROBLEMS):
        logging.info("---------- ---------- Problem: %s ---------- ----------" % (problem + 1))
        # Create groups to hold all kinds of sprites
        # - all_sprites is used for rendering
        agents = pygame.sprite.Group()
        targets = pygame.sprite.Group()
        cells = pygame.sprite.Group()
        titles = pygame.sprite.Group()
        all_sprites = pygame.sprite.Group()

        # Create Field
        create_field(cell_size, all_sprites, cells)
        print('height/weight: ', math.sqrt(len(cells.sprites())))

        # Create targets on field
        create_targets(cell_size, all_sprites, targets, cells, target_rate, target_range, use_rate, num_of_targets)

        # Create agents on field
        create_agents(cell_size, all_sprites, agents, cells,
                      num_of_agents=num_of_agents,
                      MR=MR,
                      SR=SR,
                      cred=cred,
                      show_ranges=show_ranges,
                      speed=speed)

        for algorithm in algorithms:
            logging.info("---------- Algorithm: %s ----------" % algorithm)
            fg = factor_graph[dict_alg[algorithm][0]]
            # Renders the titles aside of a field
            create_side_titles(algorithm, all_sprites, titles)
            go_back_to_initial_positions(cells)
            iteration = 0
            convergence = 0

            while iteration < MAX_ITERATIONS and running:
                # running = False if iteration == MAX_ITERATIONS else True
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

                if not all_arrived(agents):
                    # makes a join to everybody
                    with concurrent.futures.ThreadPoolExecutor(max_workers=len(agents.sprites())) as executor:
                        for agent in agents.sprites():
                            executor.submit(agent.move)
                    # logging.info("Thread %s : finishing moving!", threading.get_ident())
                    # print('-----%s iteration -------' % iteration)
                time2 = pygame.time.get_ticks()
                if all_arrived(agents) and time2 - time1 > 1000:
                    # -----------------------------------------
                    # UPDATING
                    # -----------------------------------------
                    convergence = convergence_update(targets.sprites(), agents.sprites())
                    graphs[algorithm][iteration][problem] = convergence
                    iteration += 1

                    nei_update(agents.sprites(), targets.sprites(), fg)

                    # print('---')
                    # logging.info("iteration: %s  Thread %s : ", iteration, threading.get_ident())
                    # -----------------------------------------

                    # makes a join to everybody
                    max_workers = (len(agents.sprites()) + len(targets.sprites()) + 1) if fg else len(agents.sprites())
                    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
                        alg, for_alg = dict_alg[algorithm]
                        for agent in agents.sprites():
                            executor.submit(agent.alg_update,
                                            alg, agents.sprites(), targets.sprites(), cells.sprites(), for_alg)
                        if fg:
                            for target in targets.sprites():
                                executor.submit(target.alg_update,
                                                alg, agents.sprites(), targets.sprites(), cells.sprites(), for_alg)
                    logging.info("finishing iteration: %s ----------" % iteration)
                    # , threading.get_ident())
                    time3 = pygame.time.get_ticks()
                    interval = (time3 - time2) / 1000 + 1  # for Title of time

                # Get the set of keys pressed and check for user input
                pressed_keys = pygame.key.get_pressed()
                # agents.sprites()[0].update(pressed_keys)

                # Update what is necessary
                targets.update()
                titles.update(iteration, MAX_ITERATIONS,
                              convergence,
                              problem, NUMBER_OF_PROBLEMS,
                              algorithm, algorithms, interval)

                # Fill the screen with black
                screen.fill(SKY_COLOR)

                # Draw all sprites
                # all_sprites.draw(screen)
                for entity in all_sprites:
                    screen.blit(entity.surf, entity.rect)

                # # Check if any enemies have collided with the player
                # if pygame.sprite.spritecollideany(agents.sprites()[0], targets):
                #     # If so, then remove the player and stop the loop
                #     # player.kill()
                #     pass


                # Update the display
                pygame.display.flip()

    finish_sound.play()
    time.sleep(2)
    # All done! Stop and quit the mixer.
    pygame.mixer.music.stop()
    pygame.mixer.quit()

    # time.sleep(2)
    # Done! Time to quit.
    pygame.quit()

    # Save the results
    pickle_results_if(need_to_save_results, graphs, adding_to_file_name)

    # Plot results
    plot_results_if(need_to_plot_results, need_to_plot_variance, need_to_plot_min_max, graphs, algorithms, alpha)

'''
 - dictionary of algorithms - correct
 - clean code in main
 - make algorithms transparent to robots ans simulator
 - save initial positions for specific problem
 - make more beautiful graphs!
 - make less heavy methods in agent and more functional code in Algorithms.py
 - output as PDF - beautifully organized report
 - the sending message logic has to go inside the agent
 - delete send_curr_pose_to_curr_nei(agent) and put instead send_message_to_curr_nei(agent, agent.get_pos())
 - prevent collisions in DSA, DSA_PIRL and others
 - make the change of the size screen depend on amount of cells in one side
 - make variable of amount of targets
 - use tqdm
 - save information about experiment
'''
