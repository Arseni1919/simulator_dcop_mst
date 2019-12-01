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
            return False
    return True


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

    # all cells that are in MR range
    for cell in cells:
        if distance(self_agent.get_pos(), cell.get_pos()) < self_agent.get_MR():
            # cell_set1.append(cell)
            help_set.append(cell)

    cell_set = help_set
    help_set = []

    # minus targets' cells
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

    # minus neighbours' cells
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

    # copy only the positions
    for cell in cell_set:
        possible_pos.append(cell.get_pos())

    return possible_pos


def get_possible_pos_with_MR_general(self_agent, cells, targets, agents):
    """
    input:
    output:
    """
    possible_pos = []
    help_set = []

    # all cells that are in MR range
    for cell in cells:
        if distance(self_agent.get_pos(), cell.get_pos()) < self_agent.get_MR():
            help_set.append(cell)

    cell_set = help_set
    help_set = []

    # minus agents' cells
    for cell in cell_set:
        captured = False
        for agent in agents:
            if agent.get_pos() == cell.get_pos() and agent.get_num_of_agent() != self_agent.get_num_of_agent():
                captured = True
                break
        if not captured:
            # cell_set3.append(cell)
            help_set.append(cell)

    cell_set = help_set
    help_set = []

    # minus targets' cells
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

    # copy only the positions
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
            raise ValueError('agent is self_agent inside self_agent.get_curr_nei()!')
        agent.get_access_to_inbox('message', self_agent.get_num_of_agent(), message)
    # ---------------------------------------------------
    while not received_all_messages(self_agent, ord_of_message):
        time.sleep(1)
    # ---------------------------------------------------


def send_message_to(receiver, self_agent, message):
    """
    input:
    output:
    """
    if receiver is self_agent:
        raise ValueError('receiver is self_agent inside send_message_to()!')
    # print('HERE')
    receiver.get_access_to_inbox('message', self_agent.get_num_of_agent(), message)


def receive_all_messages(self_agent, ord_of_message=1):
    """
    input:
    output:
    """
    # ---------------------------------------------------
    while not received_all_messages(self_agent, ord_of_message):
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
# For Max_sum:
# ------ ------ ------ ------ ------ ------ ------ ------ ------ ------ ------ ------ ------ ------ ------ ------ ------


def max_sum_create_null_variable_message(possible_pos):
    message = {}
    for pos in possible_pos:
        message[pos] = 0
    return message


def max_sum_variable_message_to(nei, inbox, order_of_message, possible_pos):

    # sum of the messages together
    new_message = max_sum_create_null_variable_message(possible_pos)
    for target_num, set_of_messages in inbox.items():
        if target_num != nei.get_num_of_agent():
            last_received_message = set_of_messages[order_of_message - 1]
            for pos, value in last_received_message.items():
                new_message[pos] += value

    # subtract discount factor alpha
    alpha = min(new_message.values())
    for pos in possible_pos:
        new_message[pos] -= alpha

    if min(new_message.values()) < 0:
        raise ValueError('new_message[pos] < 0 in max_sum_variable_message_to()')

    return new_message


def max_sum_function_message_to(nei, inbox, order_of_message, possible_pos, max_contribution, target):

    new_message = max_sum_create_null_variable_message(possible_pos)
    self_num = nei.get_num_of_agent()

    # create two sets
    in_SR = []
    out_of_SR = []
    for pos in possible_pos:
        if distance(pos, target.get_pos()) < nei.get_SR():
            in_SR.append(pos)
        else:
            out_of_SR.append(pos)

    for pos in in_SR:
        new_message[pos] += max_contribution

    # for pos in out_of_SR:
    #     min_value = 10**10
    #     curr_value = 0
    #     for agent_num, set_of_messages in inbox.items():
    #         if agent_num != self_num:
    #             last_received_message = set_of_messages[order_of_message - 1]
    #             for pos, value in last_received_message.items():
    #                 pass
    return new_message


def max_sum_choose_position_for(agent, possible_pos):
    inbox = agent.get_access_to_inbox('copy')
    # sum of all messages
    sum_of_all_messages = max_sum_create_null_variable_message(possible_pos)
    for target_num, set_of_messages in inbox.items():
        last_received_message = set_of_messages[-1]
        for pos, value in last_received_message.items():
            sum_of_all_messages[pos] += value
    # the max value
    max_value = max(sum_of_all_messages.values())

    # array of positions with maximal value
    set_of_max_pos = []
    for pos, value in sum_of_all_messages.items():
        if value == max_value:
            set_of_max_pos.append(pos)
    return random.choice(set_of_max_pos)


def max_sum_nei_check(curr_nei, instance):
    for nei in curr_nei:
        if not isinstance(nei, instance):
            raise ValueError('nei is not correct instance inside this Node')


def print_inbox_len(required_num, agent, inbox):
    if required_num == agent.get_num_of_agent():
        if len(inbox.keys()) == 0:
            # print(agent.get_name(), agent.get_num_of_agent(), 'empty')
            return
        # print(agent.get_name(), agent.get_num_of_agent(), '\'s inbox: ', len(inbox[random.choice(list(inbox.keys()))]))


# ------ ------ ------ ------ ------ ------ ------ ------ ------ ------ ------ ------ ------ ------ ------ ------ ------
# ------ ------ ------ ------ ------ ------ ------ ------ ------ ------ ------ ------ ------ ------ ------ ------ ------
# ------ ------ ------ ------ ------ ------ ------ ------ ------ ------ ------ ------ ------ ------ ------ ------ ------
# ------ ------ ------ ------ ------ ------ ------ ------ ------ ------ ------ ------ ------ ------ ------ ------ ------
