from Algorithms_help_functions import *
from Agent import Agent
from Target import Target


def get_SR_max_values_TAC(SR, tuple_inbox, target_pos, message_to_name, message_type_of_receiver):
    # 0 - INSIDE SR | 1 - OUTSIDE of SR
    max_values = {}
    for (nei_name, type_of_message) in tuple_inbox.keys():
        if nei_name == message_to_name:
            max_values[message_to_name] = {0: 0, 1: 0}
        else:
            # here -1 remains -1 if all the positions are inside SR or all of them outside SR
            max_values[nei_name] = {0: -1, 1: -1}
            last_message = tuple_inbox[(nei_name, message_type_of_receiver)]
            for pos, pos_value in last_message.items():
                if distance(pos, target_pos) < SR:
                    # in SR range
                    max_values[nei_name][0] = pos_value if max_values[nei_name][0] < pos_value else \
                        max_values[nei_name][0]
                else:
                    # out of SR range
                    max_values[nei_name][1] = pos_value if max_values[nei_name][1] < pos_value else \
                        max_values[nei_name][1]
    return max_values


def target_func_to_robot_var_message_TAC(target, nei, index_of_iteration,
                                         message_type_of_sender, message_type_of_receiver, addings):

    tuple_keys_inbox = target.get_access_to_inbox_TAC(copy_types.copy)
    named_inbox = tuple_keys_inbox[index_of_iteration]
    target_pos = target.get_pos()
    target_req = target.get_req()
    target_num = target.get_num_of_agent()
    cred, SR = nei.cred, nei.SR
    fmr_nei = addings['fmr_nei']

    inside_fmr = nei in fmr_nei
    received_message = named_inbox[(nei.name, message_type_of_receiver)]
    possible_pos = received_message.keys()

    if not inside_fmr:
        return max_sum_create_null_variable_message(possible_pos)  # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

    max_values = get_SR_max_values_TAC(SR, named_inbox, target_pos, nei.name, message_type_of_receiver)  # max_values is dictionary
    tuple_for_new_message = get_SR_new_message(max_values, target_req, target_num, cred, nei.name)

    return new_function_message(possible_pos, target, SR, tuple_for_new_message)  # TAC


def select_FMR_nei_TAC(target, curr_robot_nei, for_alg):
    """
    Assumptions: homogeneous agents and targets, in Fsum mode
    """
    target_needs = target.get_req()
    agent_gives = for_alg['cred']
    r_value = int(target_needs / agent_gives + 1)
    SR = for_alg['SR']

    total_set = []
    SR_set = []
    rest_set = []

    for nei in curr_robot_nei:
        total_set.append(nei)
        if distance(nei.pos, target.get_pos()) < SR:
            SR_set.append(nei)
        else:
            rest_set.append(nei)

    while len(total_set) > r_value:
        max_degree, min_degree = 0, 0
        for nei in total_set:
            degree = nei.num_of_target_nei
            if nei in rest_set:
                max_degree = degree if max_degree < degree else max_degree
            if nei in SR_set:
                min_degree = degree if min_degree > degree else min_degree

        if len(rest_set) > 0:
            selected_to_remove = rest_set[0]
            for nei in rest_set:
                if nei.num_of_target_nei == max_degree:
                    selected_to_remove = nei
                    break
            total_set.remove(selected_to_remove)
            rest_set.remove(selected_to_remove)
        else:
            selected_to_remove = SR_set[0]
            for nei in SR_set:
                if nei.num_of_target_nei == min_degree:
                    selected_to_remove = nei
                    break
            total_set.remove(selected_to_remove)
            SR_set.remove(selected_to_remove)
    return total_set


def get_sum_of_all_func_messages_TAC(agent, index_of_last_iteration):
    possible_pos = get_possible_pos_with_MR_general(agent)
    named_inbox = agent.get_access_to_inbox_TAC(copy_types.copy)
    tuple_inbox = named_inbox[index_of_last_iteration]
    # sum of all messages
    sum_of_all_messages = max_sum_create_null_variable_message(possible_pos)
    for (name, type_of_message), message in tuple_inbox.items():
        if type_of_message in from_func_to_var_types:
            for pos, value in message.items():
                if pos in sum_of_all_messages:
                    if sum_of_all_messages[pos] < 0:
                        continue
                    if value < 0:
                        sum_of_all_messages[pos] = -1
                        continue
                    sum_of_all_messages[pos] += value

    return sum_of_all_messages


def var_message_to_func_TAC(sender, receiver, index_of_iteration, message_type_of_sender, message_type_of_receiver, addings):
    possible_pos = get_possible_pos_with_MR_general(sender)
    receiver_name = receiver.name
    new_message = max_sum_create_null_variable_message(possible_pos)

    # return new_message
    if index_of_iteration == 0:
        return new_message
    tuple_keys_inbox = sender.get_access_to_inbox_TAC(copy_types.copy)
    named_inbox = tuple_keys_inbox[index_of_iteration-1]

    for (name, type_of_message), message in named_inbox.items():
        if type_of_message in from_func_to_var_types:
            if (name, type_of_message) != (receiver_name, message_type_of_receiver):
                for pos, value in message.items():
                    if pos in new_message:
                        if new_message[pos] < 0:
                            continue
                        elif value < 0:
                            new_message[pos] = -1
                            continue
                        else:
                            new_message[pos] += value

    # subtract discount factor alpha
    alpha = max(new_message.values())
    if alpha < 0:
        print('[ERROR]: [1] alpha < 0 in var_message_to_func()', alpha, 'the sender:', sender.get_name(),
              'the receiver:', receiver.name)
    # min value that also above zero
    for val in new_message.values():
        if val < 0:
            continue
        alpha = val if val < alpha else alpha

    for pos in possible_pos:
        if new_message[pos] < 0:
            continue
        new_message[pos] -= alpha

    return new_message


def func_dir_clns_robot_to_var_robot_message_TAC(sender, receiver, index_of_iteration,
                                                 message_type_of_sender, message_type_of_receiver, addings):
    inbox = sender.get_access_to_inbox_TAC(copy_types.copy)
    inbox = inbox[index_of_iteration]
    new_message = inbox[(receiver.name, message_type_of_receiver)]

    for nei in sender.all_nei_tuples:
        if receiver.name != nei.name:
            for pos in new_message.keys():
                if pos != receiver.pos:
                    angle = getAngle(nei.pos, receiver.pos, pos)
                    if angle < 90:
                        dist_from_nei = distance(receiver.pos, nei.pos)
                        hypotenuse = dist_from_nei/math.cos(math.radians(angle))
                        distance_of_receiver_from_pos = distance(receiver.pos, pos)
                        if distance_of_receiver_from_pos > hypotenuse:
                            new_message[pos] = -1

    return new_message


def func_pos_clns_robot_to_var_robot_message_TAC(sender, receiver, index_of_iteration,
                                                 message_type_of_sender, message_type_of_receiver, addings):
    # possible_pos = get_possible_pos_with_MR_general(sender)
    # return max_sum_create_null_variable_message(possible_pos)
    inbox = sender.get_access_to_inbox_TAC(copy_types.copy)
    inbox = inbox[index_of_iteration]

    new_message = inbox[(receiver.name, message_type_of_receiver)]

    for nei in sender.robot_nei_tuples:
        message = inbox[(nei.name, message_type_of_receiver)]
        if nei.num < receiver.num:
            for pos, value in message.items():
                if pos in new_message:
                    new_message[pos] = -1

    # print('------ %s came until this point while sending to %s AFTER -------' % (sender.get_name(), receiver.name))

    return new_message


def wait_to_receive_certain_named_TAC(to_agent, from_list_of_senders, index_of_iteration, message_type_to_wait):
    # wait for the messages
    not_received = True
    while not_received:
        not_received = False
        tuple_inbox = to_agent.get_access_to_inbox_TAC(copy_types.copy)
        for sender in from_list_of_senders:
            if (sender.name, message_type_to_wait) not in tuple_inbox[index_of_iteration]:
                not_received = True
                time.sleep(1)
                break


def convert_message_to_json_format(sender, message_to_nei, message_type_of_sender, index_of_iteration):
    new_message_to_nei = {}

    if message_type_of_sender in dictionary_message_types:
        for k, v in message_to_nei.items():
            new_message_to_nei[json.dumps(k)] = v

    if message_type_of_sender == message_types.from_var_to_func_only_pos:
        new_message_to_nei = json.dumps(message_to_nei)

    return json.dumps((sender, new_message_to_nei, message_type_of_sender, index_of_iteration))


def send_TAC(sender_object, receivers_named_tuples, message_func,
             message_type_of_sender, message_type_of_receiver, index_of_iteration, addings=None):
    for nei_named_tuple in receivers_named_tuples:
        message_to_nei = message_func(sender_object, nei_named_tuple, index_of_iteration,
                                      message_type_of_sender, message_type_of_receiver, addings)
        # if addings and addings['kind'] == 3:
        #     print('%s created the message for %s and the message is: %s' %
        #           (sender_object.get_name(), nei_named_tuple.name, message_to_nei))
        str_message_to_nei = convert_message_to_json_format(sender_object.get_name(),
                                                            message_to_nei, message_type_of_sender, index_of_iteration)
        send_to(receiver=nei_named_tuple.name, message=str_message_to_nei)


def get_next_pos_out_of_sum_of_all_TAC_messages(agent, for_alg):
    mini_iterations = for_alg['mini_iterations']
    sum_of_all_TAC_messages = get_sum_of_all_func_messages_TAC(agent, mini_iterations - 1)
    if max(sum_of_all_TAC_messages.values()) < 0:
        return agent.get_pos()

    set_of_max_pos = get_set_of_max_pos(agent, sum_of_all_TAC_messages, for_alg['pos_policy'])
    return random.choice(set_of_max_pos)


def final_pos_func(agent, next_pos, iteration_to_look_in, message_type_to_look_for):
    inbox = agent.get_access_to_inbox_TAC(copy_types.copy)
    inbox = inbox[iteration_to_look_in]
    for nei in agent.robot_nei_tuples:
        if nei.num < agent.get_num_of_agent():
            if inbox[(nei.name, message_type_to_look_for)] == next_pos:
                return agent.get_pos()
    return next_pos


def send_and_receive_TAC(sender_object, receivers_named_tuples, message_func,
                         message_type_of_sender, message_type_of_receiver, index_of_iteration, addings=None):
    send_TAC(sender_object, receivers_named_tuples, message_func,
             message_type_of_sender, message_type_of_receiver, index_of_iteration, addings)
    wait_to_receive_certain_named_TAC(from_list_of_senders=receivers_named_tuples, to_agent=sender_object,
                                      index_of_iteration=index_of_iteration,
                                      message_type_to_wait=message_type_of_receiver)


def receive_and_send_TAC(sender_object, receivers_named_tuples, message_func,
                         message_type_of_sender, message_type_of_receiver, index_of_iteration, addings=None):
    wait_to_receive_certain_named_TAC(from_list_of_senders=receivers_named_tuples, to_agent=sender_object,
                                      index_of_iteration=index_of_iteration,
                                      message_type_to_wait=message_type_of_receiver)
    send_TAC(sender_object, receivers_named_tuples, message_func,
             message_type_of_sender, message_type_of_receiver, index_of_iteration, addings)


def max_sum_TAC_function_node(target, for_alg):
    # target.robot_nei_tuples
    mini_iterations = for_alg['mini_iterations']
    fmr_nei = select_FMR_nei_TAC(target, target.robot_nei_tuples, for_alg)
    for index_of_iteration in range(mini_iterations):
        receive_and_send_TAC(sender_object=target, receivers_named_tuples=target.robot_nei_tuples,
                             message_func=target_func_to_robot_var_message_TAC,
                             message_type_of_sender=message_types.from_func_target_to_var,
                             message_type_of_receiver=message_types.from_var_to_func,
                             index_of_iteration=index_of_iteration,
                             addings={'fmr_nei': fmr_nei})


def max_sum_TAC_variable_node(agent, for_alg):
    mini_iterations = for_alg['mini_iterations']

    for index_of_iteration in range(mini_iterations):
        # print('agent %s is in %s loop' % (agent.get_name(), i))
        # var-robots to func-targets
        send_and_receive_TAC(sender_object=agent, receivers_named_tuples=agent.target_nei_tuples,
                             message_func=var_message_to_func_TAC,
                             message_type_of_sender=message_types.from_var_to_func,
                             message_type_of_receiver=message_types.from_func_target_to_var,
                             index_of_iteration=index_of_iteration,
                             addings={'kind': 3}
                             )

    next_pos = get_next_pos_out_of_sum_of_all_TAC_messages(agent, for_alg)

    # var-robots to func-pos-robots
    send_and_receive_TAC(sender_object=agent, receivers_named_tuples=agent.robot_nei_tuples,
                         message_func=lambda *x: next_pos,
                         message_type_of_sender=message_types.from_var_to_func_only_pos,
                         message_type_of_receiver=message_types.from_var_to_func_only_pos,
                         index_of_iteration=(mini_iterations - 1),
                         addings=None
                         )

    return final_pos_func(agent, next_pos, (mini_iterations - 1), message_types.from_var_to_func_only_pos)

    # var-robots to func-dir-robots
    # send_and_receive_TAC(sender_object=agent, receivers_named_tuples=agent.robot_nei_tuples,
    #                      message_func=var_message_to_func_TAC,
    #                      message_type_of_sender=message_types.from_var_to_func_dir,
    #                      message_type_of_receiver=message_types.from_var_to_func_dir,
    #                      index_of_iteration=index_of_iteration,
    #                      addings={'kind': 3}
    #                      )

    # func-robots to var-robots
    # send_and_receive_TAC(sender_object=agent, receivers_named_tuples=agent.robot_nei_tuples,
    #                      message_func=func_pos_clns_robot_to_var_robot_message_TAC,
    #                      message_type_of_sender=message_types.from_func_pos_collisions_to_var,
    #                      message_type_of_receiver=message_types.from_var_to_func,
    #                      index_of_iteration=index_of_iteration,
    #                      addings={'kind': 3}
    #                      )

    # func-dir-robots to var-robots
    # send_and_receive_TAC(sender_object=agent, receivers_named_tuples=agent.robot_nei_tuples,
    #                      message_func=func_dir_clns_robot_to_var_robot_message_TAC,
    #                      message_type_of_sender=message_types.from_func_dir_collisions_to_var,
    #                      message_type_of_receiver=message_types.from_var_to_func_dir,
    #                      index_of_iteration=index_of_iteration,
    #                      addings={'kind': 3}
    #                      )

    # sum_of_all_TAC_messages = get_sum_of_all_func_messages_TAC(agent, mini_iterations-1)
    # if max(sum_of_all_TAC_messages.values()) < 0:
    #     return agent.get_pos()
    #
    # set_of_max_pos = get_set_of_max_pos(agent, sum_of_all_TAC_messages, for_alg['pos_policy'])
    # next_pos = get_next_pos_out_of_sum_of_all_TAC_messages(agent, for_alg)

    # return next_pos


def Max_sum_TAC(kwargs):
    """
    :param kwargs:
    :return:
    """
    agent = kwargs['agent']
    for_alg = kwargs['for_alg']

    if isinstance(agent, Target):
        max_sum_TAC_function_node(agent, for_alg)

    if isinstance(agent, Agent):
        # logging.info("Thread %s : in FOO", threading.get_ident())
        return max_sum_TAC_variable_node(agent, for_alg)
