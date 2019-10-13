# Import the pygame module
from CONSTANTS import *
from Target import *
from Cell import *
from Title import *
from Agent import *


# Create Side-Titles
def create_side_titles(alg_name, all_sprites, titles):

    for title in titles.sprites():
        title.kill()

    order = 0
    alg_title = Title(alg_name=alg_name, order=order)
    titles.add(alg_title)
    all_sprites.add(alg_title)

    order += 1
    other_title = Title(alg_name="Problem:", order=order)
    titles.add(other_title)
    all_sprites.add(other_title)

    order += 1
    other_title = Title(alg_name="Algorithm:", order=order)
    titles.add(other_title)
    all_sprites.add(other_title)

    order += 1
    other_title = Title(alg_name="Iteration:", order=order)
    titles.add(other_title)
    all_sprites.add(other_title)

    order += 1
    other_title = Title(alg_name="Convergence:", order=order)
    titles.add(other_title)
    all_sprites.add(other_title)

    order += 1
    other_title = Title(alg_name="Remained:", order=order)
    titles.add(other_title)
    all_sprites.add(other_title)




# Create Field
def create_field(cell_size, all_sprites, cells):
    for i in range(int(SCREEN_HEIGHT / (cell_size + 2))):
        for j in range(int(SCREEN_HEIGHT / (cell_size + 2))):
            surf_center = (
                2 + i * (cell_size + 2) + (cell_size / 2),
                2 + j * (cell_size + 2) + (cell_size / 2)
            )
            new_cell = Cell(cell_size, surf_center)
            cells.add(new_cell)
            all_sprites.add(new_cell)


# Create targets
def create_targets(cell_size, all_sprites, targets, titles, cells, ratio=0.3, target_range=(1, 4)):
    for cell in cells.sprites():
        if random.random() < ratio:
            new_target = Target(
                cell_size,
                req=random.randint(target_range[0], target_range[1]),
                surf_center=cell.surf_center
            )
            cell.prop = new_target
            targets.add(new_target)
            all_sprites.add(new_target)
    # titles.update(len(targets.sprites()))


# Create agents
def create_agents(cell_size, all_sprites, agents, cells,
                  num_of_agents=4,
                  ratio=0.05,
                  MR=round(3.5 * CELL_SIZE['BIG']),
                  SR=int(2.5 * CELL_SIZE['BIG']),
                  cred=5,
                  show_ranges=False,
                  speed=10):
    for agent in range(1, num_of_agents + 1):
        assigned = False
        while not assigned:
            indexes = [i for i in range(len(cells.sprites()))]
            random.shuffle(indexes)
            for index in indexes:
                cell = cells.sprites()[index]
                if random.random() < ratio and cell.prop is None:
                    new_agent = Agent(cell_size=cell_size,
                                      number_of_robot=agent,
                                      surf_center=cell.surf_center,
                                      MR=MR,
                                      SR=SR,
                                      cred=cred,
                                      show_ranges=show_ranges,
                                      speed=speed)
                    cell.prop = new_agent
                    agents.add(new_agent)
                    all_sprites.add(new_agent)
                    assigned = True
                    break


def all_arrived(agents):
    for agent in agents.sprites():
        if not agent.arrived:
            return False
    return True


def convergence_update(targets, agents):
    convergence = 0
    for target in targets:
        curr_conv = target.get_req()
        for agent in agents:
            if distance(target.get_pos(), agent.get_pos()) < agent.get_SR():
                curr_conv = max(0, curr_conv - agent.get_cred())
        convergence += curr_conv
    return convergence


def plot_results_if(need_to_plot_results, graphs, algorithms, alpha=0.025):
    if need_to_plot_results:
        # plt.style.use('fivethirtyeight')
        # plt.style.use('bmh')
        lines = ['-', '--', '-.', ':', ]
        lines.reverse()
        markers = [',', '+', '_', '.', 'o', '*']
        markers.reverse()
        marker_index, line_index = 0, 0
        num_of_iterations, num_of_problems = graphs[algorithms[0]].shape
        t_value = t.ppf(1 - alpha, df=(num_of_problems - 1))
        iterations = [i for i in range(num_of_iterations)]
        # avr = np.average(a, 1)
        # std = np.std(a, 1)

        fig, ax = plt.subplots()

        for algorithm in algorithms:

            line_index = 0 if line_index == len(lines) else line_index
            marker_index = 0 if marker_index == len(markers) else marker_index

            matrix = graphs[algorithm]
            avr = np.average(matrix, 1)
            std = np.std(matrix, 1)

            line = lines[line_index]
            marker = markers[marker_index]

            ax.plot(iterations, avr, '%s%s' % (marker, line), label=algorithm)

            line_index += 1
            marker_index += 1

            # confidence interval
            ax.fill_between(iterations, avr - t_value * std, avr + t_value * std,
                             alpha=0.2, antialiased=True)

        ax.legend(loc='upper right')
        ax.set_title('Results')
        ax.set_ylabel('Convergence')
        ax.set_xlabel('Iterations')
        fig.tight_layout()
        plt.show()


def pickle_results_if(need_to_save_results, graphs, adding_to_file_name=''):
    if need_to_save_results:
        timestr = time.strftime("%d.%m.%Y-%H:%M:%S")
        file_name = "data/%s_%s_file.data" % (timestr, adding_to_file_name)
        # open the file for writing
        with open(file_name, 'wb') as fileObject:
            # this writes the object a to the file named 'testfile.data'
            pickle.dump(graphs, fileObject)


def nei_update(agents):
    for agent in agents:
        agent.nei_update(agents)


def go_back_to_initial_positions(cells):
    for cell in cells:
        if cell.prop:
            cell.prop.set_pos(cell.get_pos())









