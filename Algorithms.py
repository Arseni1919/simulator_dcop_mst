from Algorithms_help_functions import *
'''
OUTER WORLD - ALL FUNCTIONS HERE SUPPOSE TO BE TRANSPARENT TO SIMULATION
'''


def FOO(kwargs):
    """
    :param kwargs:
    :return:
    """
    agent = kwargs['agent']
    curr_pose = kwargs['curr_pose']
    cell_size = kwargs['cell_size']
    targets = kwargs['targets']
    cells = kwargs['cells']
    for_alg = kwargs['for_alg']
    logging.info("Thread %s : in FOO", threading.get_ident())

    return curr_pose


def DSA(kwargs):
    """
    :param kwargs:
    :return:
    """
    agent = kwargs['agent']
    curr_pos = kwargs['curr_pose']
    targets = kwargs['targets']
    cells = kwargs['cells']
    for_alg = kwargs['for_alg']

    send_and_receive_messages_to_curr_nei(agent, agent.get_pos(), 1)
    possible_pos = get_possible_pos_with_MR(agent, cells, targets, agent.curr_nei)
    temp_req_set = calculate_temp_req(agent, targets, agent.curr_nei)  # form: [(target,temp_req),(target,temp_req),..]
    new_pos = select_pos(possible_pos, temp_req_set, agent.get_SR())
    if dsa_condition(agent, new_pos, curr_pos, temp_req_set, for_alg):
        return new_pos
    return curr_pos


def DSA_PILR(kwargs):
    """
    :param kwargs:
    :return:
    """
    agent = kwargs['agent']
    curr_pos = kwargs['curr_pose']
    targets = kwargs['targets']
    cells = kwargs['cells']
    for_alg = kwargs['for_alg']

    send_and_receive_messages_to_curr_nei(agent, agent.get_pos(), 1)
    possible_pos = get_possible_pos_with_MR(agent, cells, targets, agent.curr_nei)
    temp_req_set = calculate_temp_req(agent, targets, agent.curr_nei)  # form: [(target,temp_req),(target,temp_req),..]
    new_pos = select_pos(possible_pos, temp_req_set, agent.get_SR())
    if dsa_pilr_condition(agent, new_pos, curr_pos, temp_req_set, for_alg):
        return new_pos
    return curr_pos


def MGM(kwargs):
    """
    :param kwargs:
    :return:
    """
    agent = kwargs['agent']
    curr_pose = kwargs['curr_pose']
    cell_size = kwargs['cell_size']
    targets = kwargs['targets']
    cells = kwargs['cells']
    for_alg = kwargs['for_alg']
    # logging.info("Thread %s : in MGM", threading.get_ident())

    send_and_receive_messages_to_curr_nei(agent, agent.get_pos(), 1)
    # logging.info("agent: %s  Inbox after First loop: %s  Thread: %s",
    #              agent.number_of_robot,
    #              received_all_messages(agent)[1],
    #              threading.get_ident()
    #              )

    LR, new_pos = best_possible_local_reduction(agent, cells, targets, agent.get_curr_nei())

    send_and_receive_messages_to_curr_nei(agent, LR, 2)
    # logging.info("agent: %s  Inbox: %s  Thread: %s",
    #              agent.number_of_robot,
    #              received_all_messages(agent)[1],
    #              threading.get_ident()
    #              )
    if LR > 0:
        if mgm_condition(agent, LR):
            return new_pos
    return curr_pose

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




