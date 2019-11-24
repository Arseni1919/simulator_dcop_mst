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


def get_max_contribution(fmr_nei, nei, target):
    if nei in fmr_nei:
        return min(target.get_req(), nei.get_cred())
    return 0





def max_sum_function_node(target, for_alg):
    curr_nei = target.get_curr_nei()
    max_sum_nei_check(curr_nei, Agent)
    mini_iterations = for_alg[0]
    # print('Target: ', target.get_num_of_agent(), ' its neighbors: ', curr_nei)
    # print('Here Function Node:', threading.get_ident())
    for i in range(mini_iterations):
        order_of_message = i + 1
        receive_all_messages(target, order_of_message)

        inbox = target.get_access_to_inbox('copy')

        fmr_nei = select_FMR_nei(target, curr_nei, for_alg)

        for nei in curr_nei:
            received_message = inbox[nei.get_num_of_agent()][i]
            # print('HERE 1, target:', target.get_num_of_agent())
            # print('target: ', target.get_num_of_agent(), 'received_message: ', type(received_message))
            possible_pos = received_message.keys()
            # print(possible_pos)
            # print('HERE 2')
            max_contribution = get_max_contribution(fmr_nei, nei, target)
            # print('HERE')
            new_message = max_sum_function_message_to(nei, inbox, order_of_message, possible_pos, max_contribution,
                                                      target)
            send_message_to(nei, target, new_message)
            # print("F: max_sum_function_node send 1 message to ", nei.get_num_of_agent())
        # print("F: max_sum_function_node sent 1 messages")


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
        # print("Target in Max_sum")
        max_sum_function_node(agent, for_alg)

    if isinstance(agent, Agent):

        # logging.info("Thread %s : in FOO", threading.get_ident())
        # print("Agent in Max_sum")
        return max_sum_variable_node(agent, cells, targets, agents, for_alg)

