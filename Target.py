# Import the pygame module
from pure_functions import *
# Import random for random numbers
import random


# Define the enemy object by extending pygame.sprite.Sprite
# The surface you draw on the screen is now an attribute of 'enemy'
class Target(pygame.sprite.Sprite):
    def __init__(self, cell_size=CELL_SIZE['BIG'], order=-1, req=1, surf_center=-1):
        super(Target, self).__init__()
        self.cell_size = cell_size
        self.req = req
        self.temp_req = req
        self.curr_nei = []
        self.inbox = {}
        self.named_inbox = {}
        self.tuple_keys_inbox = {}
        self.robot_nei_tuples = []

        if order == -1:
            print('[ERROR]: order of Target == -1')
        self.num_of_agent = order
        self.name = 'target_%s' % order

        self.surf = pygame.Surface((cell_size, cell_size), pygame.SRCALPHA)
        pygame.draw.circle(self.surf, (0, 0, 255), [int(cell_size/2), int(cell_size/2)], int(cell_size/2 - 2))
        # Number of Requirement
        font = pygame.font.SysFont("comicsansms", int(cell_size * 0.4))
        text = font.render("%s" % self.req, True, (255,255,0))
        wt, ht = text.get_size()
        self.surf.blit(text, (int((cell_size - wt)/2), int((cell_size - ht)/2)))

        if surf_center == -1:
            print('[ERROR]: surf_center == -1 in Target')
        else:
            self.surf_center = surf_center
            self.rect = self.surf.get_rect(
                center=surf_center
            )
        # Number of Robot
        font = pygame.font.SysFont("comicsansms", int(cell_size * 0.25))
        text = font.render("%s" % order, True, (225, 0, 0))
        wt, ht = text.get_size()
        self.surf.blit(text, (cell_size - wt, 0))

        self._lock = threading.RLock()

    # Move the sprite based on speed
    # Remove the sprite when it passes the left edge of the screen
    def update(self):
        # update self.temp_req
        pass

    def get_num_of_agent(self):
        return self.num_of_agent

    def find_all_nei(self, agents, factor_graph):
        if factor_graph:
            # Update self.curr_nei
            self.curr_nei = []
            for agent in agents:
                if distance(self.get_pos(), agent.get_pos()) < (agent.SR + agent.MR):
                    self.curr_nei.append(agent)

            # Update self.inbox
            self.inbox = {}
            for agent in self.curr_nei:
                self.inbox[agent.get_num_of_agent()] = []

    def nei_tuple_update(self, factor_graph, for_alg):
        if factor_graph:
            self.named_inbox = {}
            self.robot_nei_tuples = []
            for agent in self.curr_nei:
                self.robot_nei_tuples.append(create_tuple_of_agent(agent))
                self.named_inbox[agent.get_name()] = []

            self.tuple_keys_inbox = {}
            for i in range(for_alg['mini_iterations']):
                self.tuple_keys_inbox[i] = {}

    def get_curr_nei(self):
        return self.curr_nei

    def get_access_to_inbox(self, type_of_requirement, num_of_agent=None, message=None, name=None):
        with self._lock:
            # logging.info("Thread %s has the lock inside %s", num_of_agent, self.number_of_robot)
            if type_of_requirement == 'message':
                # logging.info("Thread %s has the message: %s", num_of_agent, message)
                self.inbox[num_of_agent].append(message)
                # logging.info("Agent %s after update has the inbox: %s", self.number_of_robot, self.inbox)
            if type_of_requirement == 'copy':
                # logging.info("Thread %s about to release the lock!!!! inbox: %s", num_of_agent, self.inbox)
                return copy.deepcopy(self.inbox)
            # logging.info("Thread %s about to release lock inside %s", num_of_agent, self.number_of_robot)

    def get_access_to_named_inbox(self, type_of_requirement, name_of_agent=None, message=None):
        with self._lock:
            if type_of_requirement == 'message':
                if name_of_agent in self.named_inbox:
                    self.named_inbox[name_of_agent].append(message)
                else:
                    print('[ERROR]: num_of_agent is not in self.inbox')
            if type_of_requirement == 'copy':
                return copy.deepcopy(self.named_inbox)

    def get_access_to_inbox_TAC(self, type_of_requirement, name_of_agent=None, message=None, index_of_iteration=0):
        with self._lock:

            if type_of_requirement == copy_types.copy:
                return copy.deepcopy(self.tuple_keys_inbox)

            if type_of_requirement in message_types:
                self.tuple_keys_inbox[index_of_iteration][(name_of_agent, type_of_requirement)] = message

    def alg_update(self, algorithm, agents, targets, cells, for_alg):
        algorithm(self.preprocessing(
            agent=self,
            curr_pose=self.rect.center,
            cell_size=self.cell_size,
            agents=agents,
            targets=targets,
            cells=cells,
            for_alg=for_alg,
        ))

    def preprocessing(self, **kwargs):
        return kwargs

    def get_pos(self):
        return self.rect.center

    def set_pos(self, pos):
        self.rect.center = pos

    def get_req(self):
        return self.req

    def get_temp_req(self):
        return self.temp_req

    def set_temp_req(self, temp_req):
        self.temp_req = temp_req

    def get_name(self):
        return self.name




