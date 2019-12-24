from Algorithms_help_functions import *
from Agent import Agent
from Target import Target

'''
OUTER WORLD - ALL FUNCTIONS HERE SUPPOSE TO BE TRANSPARENT TO SIMULATION
'''


def max_sum_function_node(target, for_alg):
    curr_nei = target.get_curr_nei()
    max_sum_nei_check(curr_nei, Agent)
    mini_iterations = for_alg['mini_iterations']
    for i in range(mini_iterations):
        order_of_message = i + 1
        receive_all_messages(target, order_of_message)

        inbox = target.get_access_to_inbox('copy')
        # print_inbox_len(1, target, inbox)
        fmr_nei = select_FMR_nei(target, curr_nei, for_alg)
        # print('fmr_nei length: ', len(fmr_nei))

        for nei in curr_nei:
            received_message = inbox[nei.get_num_of_agent()][i]
            possible_pos = received_message.keys()
            inside_fmr = nei in fmr_nei
            new_message = max_sum_function_message_to(nei, inbox, possible_pos, inside_fmr,
                                                        target, for_alg['cred'], for_alg['SR'])
            send_message_to(nei, target, new_message)


def get_set_of_higher_hierarchy(curr_robot_nei, num_of_agent):
    higher_hierarchy = []
    for curr_nei in curr_robot_nei:
        if curr_nei.get_num_of_agent() < num_of_agent:
            higher_hierarchy.append(curr_nei)
    return higher_hierarchy


def get_corrected_sum_of_all_messages(sum_of_all_messages, messages):
    for message in messages:
        if message in sum_of_all_messages.keys():
            sum_of_all_messages[message] = -1
    return sum_of_all_messages


def calculate_pos_for_HPA(agent, possible_pos, for_alg):
    num_of_agent = agent.get_num_of_agent()
    curr_robot_nei = agent.get_curr_robot_nei()
    order_of_message = 1
    higher_hierarchy = get_set_of_higher_hierarchy(curr_robot_nei, num_of_agent)
    messages = receive_messages_from_higher_hierarchy(higher_hierarchy, agent, order_of_message)
    sum_of_all_messages = get_sum_of_all_messages(agent.get_access_to_inbox('copy'), possible_pos)
    corrected_sum_of_all_messages = get_corrected_sum_of_all_messages(sum_of_all_messages, messages)
    set_of_max_pos = get_set_of_max_pos(agent, corrected_sum_of_all_messages, for_alg['pos_policy'])
    choosed_pos = random.choice(set_of_max_pos)
    for nei in curr_robot_nei:
        if nei.get_num_of_agent() > num_of_agent:
            send_named_message_to(nei, agent, choosed_pos)
    return choosed_pos


def receive_messages_from_higher_hierarchy(higher_hierarchy, agent, order_of_message):
    not_received = True
    messages = []
    # wait for the messages
    while not_received:
        not_received = False
        curr_named_inbox = agent.get_access_to_named_inbox('copy')
        for curr_nei in higher_hierarchy:
            if len(curr_named_inbox[curr_nei.get_name()]) < order_of_message:
                not_received = True
                time.sleep(1)
                break
    curr_named_inbox = agent.get_access_to_named_inbox('copy')
    for curr_nei in higher_hierarchy:
        messages.append(curr_named_inbox[curr_nei.get_name()][-1])
    return messages


def max_sum_variable_node(agent, cells, targets, agents, for_alg):
    curr_nei = agent.get_curr_nei()
    max_sum_nei_check(curr_nei, Target)
    HPA = for_alg['HPA']
    mini_iterations = for_alg['mini_iterations']
    order_of_message = 0

    possible_pos = get_possible_pos_with_MR_general(agent, cells, targets, agents)
    message = max_sum_create_null_variable_message(possible_pos)

    send_and_receive_messages_to_curr_nei(agent, message, 1)

    order_of_message += 1

    for i in range(mini_iterations - 1):
        inbox = agent.get_access_to_inbox('copy')
        # print_inbox_len(1, agent, inbox)
        for nei in curr_nei:
            message = max_sum_variable_message_to(nei, inbox, order_of_message, possible_pos)
            send_message_to(nei, agent, message)
        order_of_message += 1
        receive_all_messages(agent, order_of_message)

    if not HPA:
        return max_sum_choose_position_for(agent, possible_pos, for_alg)

    return calculate_pos_for_HPA(agent, possible_pos, for_alg)

    # for nei in curr_robot_nei:
    #     if nei.get_num_of_agent > agent.get_num_of_agent():
    #         send_named_message_to(nei, agent, future_pos)
    #
    # # print('here robot ', agent.get_num_of_agent())
    # receive_all_messages(agent, 1, prefix=['agent'], HPA=HPA)
    #
    # return max_sum_choose_position_for(agent, possible_pos, for_alg, HPA={'prefix': 'agent_', 'HPA': HPA})

def Max_sum(kwargs):
    """
    :param kwargs:
    :return:
    """
    agent = kwargs['agent']
    curr_pose = kwargs['curr_pose']
    for_alg = kwargs['for_alg']
    cell_size = kwargs['cell_size']
    agents = kwargs['agents']
    targets = kwargs['targets']
    cells = kwargs['cells']

    if isinstance(agent, Target):
        max_sum_function_node(agent, for_alg)

    if isinstance(agent, Agent):

        # logging.info("Thread %s : in FOO", threading.get_ident())
        return max_sum_variable_node(agent, cells, targets, agents, for_alg)


# hierarchical position assignment = HPA