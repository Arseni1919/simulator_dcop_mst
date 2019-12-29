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


def max_sum_variable_node(agent, cells, targets, agents, for_alg):
    curr_nei = agent.get_curr_nei()
    max_sum_nei_check(curr_nei, Target)
    HPA = for_alg['HPA'] if 'HPA' in for_alg else False
    MSHPA = for_alg['MSHPA'] if 'MSHPA' in for_alg else False
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

    if HPA:
        return calculate_pos_for_HPA(agent, possible_pos, for_alg)

    if MSHPA:
        return calculate_pos_for_MSHPA(agent, possible_pos, for_alg)

    return max_sum_choose_position_for(agent, possible_pos, for_alg)


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