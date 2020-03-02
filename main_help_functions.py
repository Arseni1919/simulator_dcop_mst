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
    alg_title = Title(title_name=alg_name, order=order)
    titles.add(alg_title)
    all_sprites.add(alg_title)

    order += 1
    other_title = Title(title_name="Problem:", order=order)
    titles.add(other_title)
    all_sprites.add(other_title)

    order += 1
    other_title = Title(title_name="Algorithm:", order=order)
    titles.add(other_title)
    all_sprites.add(other_title)

    order += 1
    other_title = Title(title_name="Iteration:", order=order)
    titles.add(other_title)
    all_sprites.add(other_title)

    order += 1
    other_title = Title(title_name="Convergence:", order=order)
    titles.add(other_title)
    all_sprites.add(other_title)

    order += 1
    other_title = Title(title_name="Remained:", order=order)
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

    # for cell in cells:
    #     print(cell.get_pos())


# Create targets
def create_targets(cell_size, all_sprites, targets, cells,
                   ratio=0.3,
                   target_range=(1, 4),
                   use_rate=True,
                   num_of_targets=-1):
    order = 1
    if use_rate:
        for cell in cells.sprites():
            if random.random() < ratio:
                new_target = Target(
                    cell_size,
                    order=order,
                    req=random.randint(target_range[0], target_range[1]),
                    surf_center=cell.surf_center
                )
                cell.prop = new_target
                targets.add(new_target)
                all_sprites.add(new_target)
                order += 1
    else:
        if num_of_targets == -1:
            print('[ERROR]: bad')
        while True:
            cell = random.choice(cells.sprites())
            new_target = Target(
                cell_size,
                order=order,
                req=random.randint(target_range[0], target_range[1]),
                surf_center=cell.surf_center
            )
            cell.prop = new_target
            targets.add(new_target)
            all_sprites.add(new_target)
            order += 1
            if num_of_targets == len(targets.sprites()):
                break

    # for target in targets:
    #     print(target.get_pos())


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


def print_t_test_table(graphs):
    keys = graphs.keys()
    num_of_algs = len(keys)
    print_array = [[] for _ in range(num_of_algs + 1)]
    for i in range(num_of_algs + 1):
        for _ in range(num_of_algs + 1):
            print_array[i].append('')
    max_length = 0
    for k in keys:
        if len(k) > max_length:
            max_length = len(k)

    print_array[0][0] = '\t%s' % (' ' * len('1.000'))
    i = 0
    for k1 in keys:
        adding_string = ' ' * (max_length - len(k1))
        j = 0
        print_array[0][i + 1] = '\t%s%s' % (k1, adding_string)
        print_array[i + 1][0] = '%s%s\t' % (k1, adding_string)
        for k2 in keys:
            adding_string2 = ' ' * (max_length - len('1.000'))
            stat, p_value = stats.ttest_ind(graphs[k1][-1], graphs[k2][-1])
            print_array[i + 1][j + 1] = '{:.3f}{adding_string2}\t'.format(p_value, adding_string2=adding_string2)
            j += 1
        i += 1

    # printing
    tab = 2
    eq_str = '*' * (max_length + tab)
    print('{eq_str}'.format(eq_str=eq_str) * (num_of_algs + 1))
    eq_str = ' ' * max_length
    print('{eq_str}\t'.format(eq_str=eq_str) * int(num_of_algs / 3 + 1), end='')
    print('P-VALUE TABLE\t', end='')
    print('{eq_str}\t'.format(eq_str=eq_str) * int(num_of_algs / 3 + 1))
    eq_str = '*' * (max_length + tab)
    print('{eq_str}'.format(eq_str=eq_str) * (num_of_algs + 1))
    for i in range(num_of_algs + 1):
        for j in range(num_of_algs + 1):
            print(print_array[i][j], end='')
        print()
        eq_str = '=' * max_length
        print('{eq_str}\t'.format(eq_str=eq_str), end='')
        eq_str = '=' * max_length if i == 0 else '-' * max_length
        print('{eq_str}\t'.format(eq_str=eq_str) * num_of_algs)
    eq_str = '*' * (max_length + tab)
    print('{eq_str}'.format(eq_str=eq_str) * (num_of_algs + 1))


def plot_results_if(need_to_plot_results, need_to_plot_variance, need_to_plot_min_max, graphs, algorithms, alpha=0.025):
    if need_to_plot_results:
        print_t_test_table(graphs)
        # plt.style.use('fivethirtyeight')
        plt.style.use('bmh')
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

            if need_to_plot_variance:
                # confidence interval
                ax.fill_between(iterations, avr - t_value * std, avr + t_value * std,
                                alpha=0.2, antialiased=True)

            if need_to_plot_min_max:
                # confidence interval
                ax.fill_between(iterations, np.min(matrix, 1), np.max(matrix, 1),
                                alpha=0.2, antialiased=True)

        ax.legend(loc='upper right')
        ax.set_title('Results')
        ax.set_ylabel('Convergence')
        ax.set_xlabel('Iterations')
        # ax.set_xlim(xmin=iterations[0], xmax=iterations[-1])
        fig.tight_layout()
        plt.show()


def pickle_results_if(need_to_save_results, graphs, collisions, adding_to_file_name='',
                      grid_size=-1, num_of_targets=-1, num_of_agents=-1, target_range=-1, MR=-1, SR=-1, cred=-1,
                      MAX_ITERATIONS=-1, NUMBER_OF_PROBLEMS=-1):
    if need_to_save_results:
        timestr = time.strftime("%d.%m.%Y-%H:%M:%S")
        algorithms = graphs.keys()
        for alg in algorithms:
            timestr = timestr + '__%s' % alg
        file_name = "data/%s_%s_file.data" % (timestr, adding_to_file_name)
        # open the file for writing
        with open(file_name, 'wb') as fileObject:
            pickle.dump(graphs, fileObject)

        file_name = "data/%s_%s_file.info" % (timestr, adding_to_file_name)
        # open the file for writing
        with open(file_name, 'wb') as fileObject:
            info = {'graphs': list(graphs.keys()), 'collisions': collisions, 'grid_size': grid_size, 'num_of_targets': num_of_targets,
                    'num_of_agents': num_of_agents, 'target_range': target_range, 'MR': MR, 'SR': SR, 'cred': cred,
                    'MAX_ITERATIONS': MAX_ITERATIONS, 'NUMBER_OF_PROBLEMS': NUMBER_OF_PROBLEMS}
            pickle.dump(info, fileObject)

def nei_update(agents, targets, factor_graph):
    for agent in agents:
        agent.nei_update(agents, targets, factor_graph)

    for target in targets:
        target.nei_update(agents, factor_graph)


def go_back_to_initial_positions(cells):
    for cell in cells:
        if cell.prop:
            cell.prop.set_pos(cell.get_pos())
