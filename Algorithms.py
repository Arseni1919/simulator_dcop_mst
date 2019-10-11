
from CONSTANTS import *
from pure_functions import *
'''
OUTER WORLD - ALL FUNCTIONS HERE SUPPOSE TO BE TRANSPARENT TO SIMULATION
'''


def FOO(kwargs):
    agent = kwargs['agent']
    curr_pose = kwargs['curr_pose']
    cell_size = kwargs['cell_size']
    targets = kwargs['targets']
    cells = kwargs['cells']
    for_alg = kwargs['for_alg']
    logging.info("Thread %s : in FOO", threading.get_ident())

    return curr_pose


def DSA(kwargs):
    # logging.info("Thread %s : in DSA", threading.get_ident())
    # for key, value in kwargs.items():
    #     print(key, value)
    agent = kwargs['agent']
    curr_pose = kwargs['curr_pose']
    targets = kwargs['targets']
    cells = kwargs['cells']
    for_alg = kwargs['for_alg']

    send_curr_pose_to_curr_nei(agent)
    # ---------------------------------------------------
    while not received_all_messages(agent)[0]:
    #     # pass
    #     # logging.info("agent: %s  Thread %s : in DSA, inbox: %s", agent.number_of_robot, threading.get_ident(), agent.inbox)
        time.sleep(1)
    # ---------------------------------------------------
    logging.info("agent: %s  Inbox: %s  Thread: %s",
                 agent.number_of_robot,
                 received_all_messages(agent)[1],
                 threading.get_ident()
                 )
    possible_pos = get_possible_pos_with_MR(agent, cells, targets, agent.curr_nei)
    temp_req_set = calculate_temp_req(agent, targets, agent.curr_nei)  # form: [(target,temp_req),(target,temp_req),..]
    new_pos = select_pos(possible_pos, temp_req_set, agent.get_SR())
    if random.random() < for_alg[0]:
        return new_pos
    return curr_pose


def MGM(kwargs):
    agent = kwargs['agent']
    curr_pose = kwargs['curr_pose']
    cell_size = kwargs['cell_size']
    targets = kwargs['targets']
    cells = kwargs['cells']
    for_alg = kwargs['for_alg']
    logging.info("Thread %s : in MGM", threading.get_ident())

    return curr_pose


# ------ ------ ------ ------ ------ ------ ------ ------ ------ ------ ------ ------ ------ ------ ------ ------ ------
# ------ ------ ------ ------ ------ ------ ------ ------ ------ ------ ------ ------ ------ ------ ------ ------ ------
# help Algorithms functions
# ------ ------ ------ ------ ------ ------ ------ ------ ------ ------ ------ ------ ------ ------ ------ ------ ------
# ------ ------ ------ ------ ------ ------ ------ ------ ------ ------ ------ ------ ------ ------ ------ ------ ------
def received_all_messages(self_agent):
    curr_inbox = self_agent.get_access_to_inbox('copy', self_agent.get_num_of_agent())
    for _, messages in curr_inbox.items():
        if len(messages) == 0:
            return False, curr_inbox
    return True, curr_inbox


def calculate_temp_req(self_agent, targets, neighbours):
    curr_inbox = self_agent.get_access_to_inbox('copy')
    temp_req_set = []
    for target in targets:
        curr_tuple = (target, target.get_req())
        for agent in neighbours:
            if in_area(curr_inbox[agent.number_of_robot][0], target.get_pos(), agent.get_SR()):
                curr_tuple = (target, max(0, curr_tuple[1] - agent.get_cred()))
        temp_req_set.append(curr_tuple)
    return temp_req_set


def get_possible_pos_with_MR(self_agent, cells, targets, neighbours):
    possible_pos = []
    cell_set1 = []
    cell_set2 = []
    cell_set3 = []
    curr_inbox = self_agent.get_access_to_inbox('copy')

    for cell in cells:
        if distance(self_agent.get_pos(), cell.get_pos()) < self_agent.get_MR():
            cell_set1.append(cell)

    for cell in cell_set1:
        captured = False
        for target in targets:
            if target.get_pos() == cell.get_pos():
                captured = True
                break
        if not captured:
            cell_set2.append(cell)

    for cell in cell_set2:
        captured = False
        for agent in neighbours:
            if curr_inbox[agent.get_num_of_agent()][0] == cell.get_pos():
                captured = True
                break
        if not captured:
            cell_set3.append(cell)

    for cell in cell_set3:
        possible_pos.append(cell.get_pos())

    return possible_pos


def send_curr_pose_to_curr_nei(self_agent):
    curr_nei = self_agent.get_curr_nei()
    for agent in curr_nei:
        if agent is self_agent:
            raise ValueError('Ups')
        agent.get_access_to_inbox('message', self_agent.get_num_of_agent(), self_agent.get_pos())


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
    """
    input:
    pos_set = [(x1, y1),(x2, y2),..]
    targets = [(target, temp_req), (target, temp_req), ..]
    SR = int()
    output:
    pos = (x, y)
    """
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
Target() -> get_req(), 
            get_pos(), 
            get_temp_req(), 
            set_temp_req()
            
Agent()  -> get_pos() 
            get_num_of_agent() 
            get_access_to_inbox()
            get_SR()
            get_MR()
            nei_update(agents)
            
Cell()   -> get_pos()
'''




