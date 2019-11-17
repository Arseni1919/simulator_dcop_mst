from pure_functions import *
'''
OUTER WORLD - ALL FUNCTIONS HERE SUPPOSE TO BE TRANSPARENT TO SIMULATION
'''

# ------ ------ ------ ------ ------ ------ ------ ------ ------ ------ ------ ------ ------ ------ ------ ------ ------
# ------ ------ ------ ------ ------ ------ ------ ------ ------ ------ ------ ------ ------ ------ ------ ------ ------
# help Algorithms functions
# ------ ------ ------ ------ ------ ------ ------ ------ ------ ------ ------ ------ ------ ------ ------ ------ ------
# ------ ------ ------ ------ ------ ------ ------ ------ ------ ------ ------ ------ ------ ------ ------ ------ ------
def foo():
    """
    input:
    output:
    """
    pass


def dsa_condition(agent, new_pos, curr_pos, temp_req_set, for_alg):
    """
    input:
    output:
    """
    curr_value = 0
    new_value = 0
    for (target, temp_req) in temp_req_set:
        if in_area(new_pos, target.get_pos(), agent.get_SR()):
            new_value += min(agent.get_cred(), temp_req)
        if in_area(curr_pos, target.get_pos(), agent.get_SR()):
            new_value += min(agent.get_cred(), temp_req)
    if new_value >= curr_value:
        return random.random() < for_alg[0]
    return False


def dsa_pilr_condition(agent, new_pos, curr_pos, temp_req_set, for_alg):
    """
    input:
    output:
    """
    curr_value = 0
    new_value = 0
    c = for_alg[1] if random.random() < for_alg[2] else 0  # from paper
    for (target, temp_req) in temp_req_set:
        if in_area(new_pos, target.get_pos(), agent.get_SR()):
            new_value += min(agent.get_cred(), temp_req)
        if in_area(curr_pos, target.get_pos(), agent.get_SR()):
            new_value += min(agent.get_cred(), temp_req)
    if new_value >= curr_value + c:
        return random.random() < for_alg[0]
    return False


def get_cov(temp_req_set, pos, SR):
    """
    input:
    output:
    """
    max_value = 0
    for (target, temp_req) in temp_req_set:
        if in_area(target.get_pos(), pos, SR):
            if temp_req > max_value:
                max_value = temp_req
    return max_value


def best_possible_local_reduction(self_agent, cells, targets, neighbours):
    """
    input:
    output:
    """
    possible_pos = get_possible_pos_with_MR(self_agent, cells, targets, neighbours)
    temp_req_set = calculate_temp_req(self_agent, targets, neighbours)  # form: [(target,temp_req),(target,temp_req),..]
    new_pos = select_pos(possible_pos, temp_req_set, self_agent.get_SR())
    # print('new_pos', new_pos)
    cur_cov = get_cov(temp_req_set, self_agent.get_pos(), self_agent.get_SR())
    # print('cur_cov', self_agent.get_num_of_agent(), cur_cov)
    new_cov = get_cov(temp_req_set, new_pos, self_agent.get_SR())
    # print('new_cov', self_agent.get_num_of_agent(), new_cov)
    return min(new_cov - cur_cov, self_agent.get_cred()), new_pos


def mgm_condition(self_agent, LR):
    """
    input:
    output:
    """
    curr_inbox = self_agent.get_access_to_inbox('copy', self_agent.get_num_of_agent())
    for k, v in curr_inbox.items():
        if LR < v[1]:
            return False
        if LR == v[1] and self_agent.get_num_of_agent() > k:
            return False
    return True


def received_all_messages(self_agent, ord_of_message=1):
    """
    input:
    output:
    """
    curr_inbox = self_agent.get_access_to_inbox('copy')
    for _, messages in curr_inbox.items():
        if len(messages) == (ord_of_message - 1):
            return False, curr_inbox
    return True, curr_inbox


def calculate_temp_req(self_agent, targets, neighbours):
    """
    input:
    output:
    """
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
    """
    input:
    output:
    """
    possible_pos = []
    cell_set = []
    help_set = []
    curr_inbox = self_agent.get_access_to_inbox('copy')

    for cell in cells:
        if distance(self_agent.get_pos(), cell.get_pos()) < self_agent.get_MR():
            # cell_set1.append(cell)
            help_set.append(cell)

    cell_set = help_set
    help_set = []

    # for cell in cell_set1:
    for cell in cell_set:
        captured = False
        for target in targets:
            if target.get_pos() == cell.get_pos():
                captured = True
                break
        if not captured:
            # cell_set2.append(cell)
            help_set.append(cell)

    cell_set = help_set
    help_set = []

    # for cell in cell_set2:
    for cell in cell_set:
        captured = False
        for agent in neighbours:
            if curr_inbox[agent.get_num_of_agent()][0] == cell.get_pos():
                captured = True
                break
        if not captured:
            # cell_set3.append(cell)
            help_set.append(cell)

    cell_set = help_set
    help_set = []

    # for cell in cell_set3:
    for cell in cell_set:
        possible_pos.append(cell.get_pos())

    return possible_pos


def send_and_receive_messages_to_curr_nei(self_agent, message, ord_of_message=1):
    """
    input:
    output:
    """
    curr_nei = self_agent.get_curr_nei()
    for agent in curr_nei:
        if agent is self_agent:
            raise ValueError('Ups')
        agent.get_access_to_inbox('message', self_agent.get_num_of_agent(), message)
    # ---------------------------------------------------
    while not received_all_messages(self_agent, ord_of_message)[0]:
        time.sleep(1)
    # ---------------------------------------------------





def get_req_list_max_to_min(targets):
    """
    input:
    output:
    """
    req_list_max_to_min = []
    for target_tuple in targets:
        target, temp_req = target_tuple
        req_list_max_to_min.append(temp_req)
    return sorted(req_list_max_to_min, reverse=True)


def get_new_targets(target_set, targets):
    """
    input:
    output:
    """
    new_targets = []
    for target in targets:
        if target not in target_set:
            new_targets.append(target)
    return new_targets


def get_possible_pos(pos_set, target_set, SR):
    """
    input:
    output:
    """
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
    """
    input:
    output:
    """
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
