from help_functions import *

'''
OUTER WORLD - ALL FUNCTIONS HERE SUPPOSE TO BE TRANSPARENT TO SIMULATION
'''

def DSA(kwargs):
    for key, value in kwargs.items():
        print(key, value)
    curr_pose = kwargs['curr_pose']
    cell_size = kwargs['cell_size']
    MR = kwargs['MR']
    SR = kwargs['SR']
    curr_nei = kwargs['curr_nei']
    number_of_robot = kwargs['number_of_robot']
    targets = kwargs['targets']
    cells = kwargs['cells']

    curr_x, curr_y = curr_pose
    future_pos = (curr_x + 1 * (cell_size + 2), curr_y - 1 * (cell_size + 2))
    logging.info("Thread %s : in DSA", threading.get_ident())
    return future_pos


def MGM(curr_pose):
    logging.info("Thread %s : in DSA", threading.get_ident())
    return curr_pose

def select_pos():
    pass

dict_alg = {
    'DSA': DSA,
    'MGM': MGM,
}

