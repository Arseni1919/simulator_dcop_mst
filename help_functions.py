# Import the pygame module

from Target import *
from Cell import *
from CONSTANTS import *
from Title import *
from Agent import *


# Create Side-Titles
def create_side_titles(alg_name, all_sprites, titles):

    alg_title = Title(alg_name=alg_name, order=0)
    titles.add(alg_title)
    all_sprites.add(alg_title)

    other_title = Title(alg_name="Iteration:", order=1)
    titles.add(other_title)
    all_sprites.add(other_title)

    other_title = Title(alg_name="Convergence:", order=2)
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
def create_targets(cell_size, all_sprites, targets, titles, cells, ratio=0.3):
    for cell in cells.sprites():
        if random.random() < ratio:
            new_target = Target(cell_size, req=random.randint(1, 2), surf_center=cell.surf_center)
            cell.prop = new_target
            targets.add(new_target)
            all_sprites.add(new_target)
    titles.update(len(targets.sprites()))


# Create agents
def create_agents(cell_size, all_sprites, agents, cells,
                  num_of_agents=4,
                  ratio=0.05,
                  MR=round(3.5 * CELL_SIZE['BIG']),
                  SR=int(2.5 * CELL_SIZE['BIG']),
                  show_ranges=False):
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
                                      show_ranges=show_ranges)
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


def convergence_update(iteration):
    return math.sqrt(iteration)


def plot_results_if(need_to_plot_results, graphs, algorithms):
    if need_to_plot_results:
        plt.figure()
        plt.plot(graphs[algorithms[0]])
        plt.title('Convergence per iteration')
        plt.show()


def pickle_results_if(need_to_save_results, graphs):
    if need_to_save_results:
        file_name = "testfile"
        # open the file for writing
        with open(file_name, 'wb') as fileObject:
            # this writes the object a to the file named 'testfile'
            pickle.dump(graphs, fileObject)



def foo():
    print('here')
    logging.info("Thread %s : starting foo", threading.get_ident())
    time.sleep(0.1)
    logging.info("Thread %s : finishing foo", threading.get_ident())






