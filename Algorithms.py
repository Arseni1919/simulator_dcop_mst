
from CONSTANTS import *
'''
OUTER WORLD - ALL FUNCTIONS HERE SUPPOSE TO BE TRANSPARENT TO SIMULATION
'''

def DSA(kwargs):
    # logging.info("Thread %s : in DSA", threading.get_ident())
    # for key, value in kwargs.items():
    #     print(key, value)
    agent = kwargs['agent']
    curr_pose = kwargs['curr_pose']
    cell_size = kwargs['cell_size']
    MR = kwargs['MR']
    SR = kwargs['SR']
    curr_nei = kwargs['curr_nei']
    number_of_robot = kwargs['number_of_robot']
    targets = kwargs['targets']
    cells = kwargs['cells']
    for_alg = kwargs['for_alg']

    agent.send_curr_pose_to_curr_nei()
    # while not agent.received_all_messages():
    #     # logging.info("agent: %s  Thread %s : in DSA, inbox: %s", agent.number_of_robot, threading.get_ident(), agent.inbox)
    #     time.sleep(1)
    # logging.info("agent: %s  Inbox: %s ", agent.number_of_robot, agent.inbox)
    possible_pos = agent.get_possible_pos_with_MR(cells, targets)
    temp_req_set = agent.calculate_temp_req(targets)  # form: [(target, temp_req), (target, temp_req), ..]
    new_pos = select_pos(possible_pos, temp_req_set, agent.get_SR())
    if random.random() < for_alg[0]:
        return new_pos
    return curr_pose

    # curr_x, curr_y = curr_pose
    # future_pos = (curr_x + 1 * (cell_size + 2), curr_y - 1 * (cell_size + 2))
    #
    # return future_pos


def MGM(curr_pose):
    logging.info("Thread %s : in DSA", threading.get_ident())
    return curr_pose


# ------ ------ ------ ------ ------ ------ ------ ------ ------ ------ ------ ------ ------ ------ ------ ------ ------
# ------ ------ ------ ------ ------ ------ ------ ------ ------ ------ ------ ------ ------ ------ ------ ------ ------
# help outer functions
# ------ ------ ------ ------ ------ ------ ------ ------ ------ ------ ------ ------ ------ ------ ------ ------ ------
# ------ ------ ------ ------ ------ ------ ------ ------ ------ ------ ------ ------ ------ ------ ------ ------ ------

def in_area(pos_1, pos_2, SR):
    px, py = pos_1
    tx, ty = pos_2
    return math.sqrt(math.pow(px - tx, 2) + math.pow(py - ty, 2)) < SR


def get_req_list_max_to_min(targets):
    req_list_max_to_min = []
    for target_tuple in targets:
        target, temp_req = target_tuple
        req_list_max_to_min.append(temp_req)
    return sorted(req_list_max_to_min, reverse=True)


def get_new_targets(target_set, targets):
    new_targets = []
    for target in targets:
        if target not in target_set:
            new_targets.append(target)
    return new_targets


def get_possible_pos(pos_set, target_set, SR):
    best_value = 0
    new_target_set = []
    possible_pos = []
    for pos in pos_set:
        pos_cart = []
        for target_tuple in target_set:
            target, temp_req = target_tuple
            if in_area(pos, target.get_pos(), SR):
                pos_cart.append(target_tuple)
        if len(pos_cart) > best_value:
            best_value = len(pos_cart)
            new_target_set = pos_cart

    for pos in pos_set:
        good = True
        for target_tuple in new_target_set:
            target, temp_req = target_tuple
            if not in_area(pos, target.get_pos(), SR):
                good = False
                break
        if good:
            possible_pos.append(pos)

    return possible_pos, new_target_set


def get_target_set_with_SR_range(pos_set, targets, SR):
    target_set = []
    req_list_max_to_min = get_req_list_max_to_min(targets)
    for max_req in req_list_max_to_min:
        for target_tuple in targets:
            target, temp_req = target_tuple
            if temp_req == max_req:
                for pos in pos_set:
                    if in_area(pos, target.get_pos(), SR):
                        target_set.append(target_tuple)
        if len(target_set) > 0:
            return target_set
    return target_set


# return tuple (x, y)
def select_pos(pos_set, targets, SR):
    if len(pos_set) == 1:
        return pos_set[0]
    target_set = get_target_set_with_SR_range(pos_set, targets, SR)
    # print(target_set)
    if len(target_set) == 0:
        # print(pos_set)
        return random.choice(pos_set)
    # target_set changes if not all targets can fit
    possible_pos, target_set = get_possible_pos(pos_set, target_set, SR)
    new_targets = get_new_targets(target_set, targets)
    return select_pos(possible_pos, new_targets, SR)


# ------ ------ ------ ------ ------ ------ ------ ------ ------ ------ ------ ------ ------ ------ ------ ------ ------
# ------ ------ ------ ------ ------ ------ ------ ------ ------ ------ ------ ------ ------ ------ ------ ------ ------
# ------ ------ ------ ------ ------ ------ ------ ------ ------ ------ ------ ------ ------ ------ ------ ------ ------
# ------ ------ ------ ------ ------ ------ ------ ------ ------ ------ ------ ------ ------ ------ ------ ------ ------


# ------ ------ ------ ------ ------ ------ ------ ------ ------ ------ ------ ------ ------ ------ ------ ------ ------
# ------ ------ ------ ------ ------ ------ ------ ------ ------ ------ ------ ------ ------ ------ ------ ------ ------
# dictionary
# ------ ------ ------ ------ ------ ------ ------ ------ ------ ------ ------ ------ ------ ------ ------ ------ ------
# ------ ------ ------ ------ ------ ------ ------ ------ ------ ------ ------ ------ ------ ------ ------ ------ ------
dict_alg = {
    'DSA': (DSA, [0.8]),
    'MGM': (MGM, []),
}

# ------ ------ ------ ------ ------ ------ ------ ------ ------ ------ ------ ------ ------ ------ ------ ------ ------
'''
REQUIREMENTS:
Target() -> get_req(), get_pos(), get_temp_req(), set_temp_req()
Agent() -> get_curr_pos()
'''




