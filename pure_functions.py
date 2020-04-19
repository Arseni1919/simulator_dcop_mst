from CONSTANTS import *


def distance(pos1, pos2):
    """
    input:
    output:
    """
    return math.sqrt(math.pow(pos1[0] - pos2[0], 2) + math.pow(pos1[1] - pos2[1], 2))


def in_area(pos_1, pos_2, SR):
    """
    input:
    output:
    """
    px, py = pos_1
    tx, ty = pos_2
    return math.sqrt(math.pow(px - tx, 2) + math.pow(py - ty, 2)) < SR


def foo():
    print('here')
    logging.info("Thread %s : starting foo", threading.get_ident())
    time.sleep(0.1)
    logging.info("Thread %s : finishing foo", threading.get_ident())


def create_tuple_of_agent(agent):
    # AgentTuple = namedtuple('AgentTuple', ['pos', 'num_of_robot_nei', 'num_of_target_nei', 'name', 'num', 'cred'])
    return AgentTuple(pos=agent.get_pos(), num=agent.get_num_of_agent(), cred=agent.get_cred(), name=agent.get_name(),
                      num_of_target_nei=len(agent.get_curr_nei()), num_of_robot_nei=len(agent.get_curr_robot_nei()),
                      SR=agent.get_SR(), MR=agent.get_MR())


def create_tuple_of_target(target):
    return TargetTuple(pos=target.get_pos(),
                       req=target.get_req(),
                       name=target.get_name(),
                       num=target.get_num_of_agent())
