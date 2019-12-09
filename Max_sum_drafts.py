from Algorithms_help_functions import *
from Agent import Agent
from Target import Target

'''
OUTER WORLD - ALL FUNCTIONS HERE SUPPOSE TO BE TRANSPARENT TO SIMULATION
'''


def select_FMR_nei(target, curr_nei, for_alg):
    '''
    Assumptions: homogeneous agents and targets, in Fsum mode
    '''
    target_needs = target.get_req()
    agent_gives = for_alg[1]
    r_value = int(target_needs/agent_gives + 1)
    SR = for_alg[2]

    total_set = []
    SR_set = []
    rest_set = []

    for nei in curr_nei:
        total_set.append(nei)
        if distance(nei.get_pos(), target.get_pos()) < SR:
            SR_set.append(nei)
        else:
            rest_set.append(nei)

    while len(total_set) > r_value:
        max_degree, min_degree = 0, 0
        for nei in total_set:
            degree = len(nei.get_curr_nei())
            if nei in rest_set:
                max_degree = degree if max_degree < degree else max_degree
            if nei in SR_set:
                min_degree = degree if min_degree > degree else min_degree

        if len(rest_set) > 0:
            selected_to_remove = rest_set[0]
            for nei in rest_set:
                if len(nei.get_curr_nei()) == max_degree:
                    selected_to_remove = nei
                    break
            total_set.remove(selected_to_remove)
            rest_set.remove(selected_to_remove)
        else:
            selected_to_remove = SR_set[0]
            for nei in SR_set:
                if len(nei.get_curr_nei()) == min_degree:
                    selected_to_remove = nei
                    break
            total_set.remove(selected_to_remove)
            SR_set.remove(selected_to_remove)
    return total_set


def max_sum_function_node(target, for_alg):
    curr_nei = target.get_curr_nei()
    max_sum_nei_check(curr_nei, Agent)
    mini_iterations = for_alg[0]
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
            new_message = for_alg[3](nei, inbox, possible_pos, inside_fmr,
                                                        target, for_alg[1], for_alg[2])
            send_message_to(nei, target, new_message)

            # if target.get_num_of_agent() == 1:  # and nei.get_num_of_agent() == curr_nei[0].get_num_of_agent():
            #     print('before ', i)
            #     print('nei: ', nei.get_num_of_agent(), 'max of messages: ', max(new_message.values()))




def max_sum_variable_node(agent, cells, targets, agents, for_alg):
    curr_nei = agent.get_curr_nei()
    max_sum_nei_check(curr_nei, Target)
    mini_iterations = for_alg[0]
    # print('Robot: ', agent.get_num_of_agent(), ' its neighbors: ', curr_nei)
    possible_pos = get_possible_pos_with_MR_general(agent, cells, targets, agents)
    message = max_sum_create_null_variable_message(possible_pos)
    send_and_receive_messages_to_curr_nei(agent, message, 1)
    # print("V: max_sum_variable_node received 1 messages")
    for i in range(mini_iterations - 1):
        order_of_message = i + 1
        inbox = agent.get_access_to_inbox('copy')
        # print_inbox_len(1, agent, inbox)
        for nei in curr_nei:
            message = max_sum_variable_message_to(nei, inbox, order_of_message, possible_pos)
            send_message_to(nei, agent, message)
        receive_all_messages(agent, order_of_message + 1)
    # print("HERE")
    return max_sum_choose_position_for(agent, possible_pos)


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

