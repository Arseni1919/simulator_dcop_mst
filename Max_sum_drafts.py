from Algorithms_help_functions import *
'''
OUTER WORLD - ALL FUNCTIONS HERE SUPPOSE TO BE TRANSPARENT TO SIMULATION
'''


def select_new_pos():
    return None


def max_sum_function():
    pass


def max_sum_variable(iteration):
    if iteration % 5 == 0:
        return select_new_pos()


def Max_sum(kwargs):
    """
    :param kwargs:
    :return:
    """
    agent = kwargs['agent']
    curr_pose = kwargs['curr_pose']
    cell_size = kwargs['cell_size']
    targets = kwargs['targets']
    cells = kwargs['cells']
    for_alg = kwargs['for_alg']
    logging.info("Thread %s : in FOO", threading.get_ident())

    iteration = 0 # also input
    function_node = False
    variable_node = False

    if function_node:
        max_sum_function()
    if variable_node:
        max_sum_variable(iteration)


    return curr_pose