from Algorithms_help_functions import *
from Agent import Agent
from Target import Target

'''
OUTER WORLD - ALL FUNCTIONS HERE SUPPOSE TO BE TRANSPARENT TO SIMULATION
'''


def max_sum_function_node(target, for_alg):
    curr_nei = target.get_curr_nei()
    max_sum_nei_check(curr_nei, Agent)
    mini_iterations = for_alg[0]
    # print('Target: ', target.get_num_of_agent(), ' its neighbors: ', curr_nei)
    # print('Here Function Node:', threading.get_ident())
    for i in range(mini_iterations):
        order_of_message = i + 1
        pass


def max_sum_variable_node(agent, cells, targets, agents, for_alg):
    curr_nei = agent.get_curr_nei()
    max_sum_nei_check(curr_nei, Target)
    mini_iterations = for_alg[0]
    # print('Robot: ', agent.get_num_of_agent(), ' its neighbors: ', curr_nei)
    possible_pos = get_possible_pos_with_MR_general(agent, cells, targets, agents)
    message = max_sum_create_null_variable_message(possible_pos)
    send_and_receive_messages_to_curr_nei(agent, message, 1)
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
        max_sum_function_node(agent)

    if isinstance(agent, Agent):

        # logging.info("Thread %s : in FOO", threading.get_ident())
        # print("Agent in Max_sum")
        return max_sum_variable_node(agent, cells, targets, agents, for_alg)

