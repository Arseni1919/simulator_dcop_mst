# Import the pygame module
from CONSTANTS import *
from pure_functions import *



# Define a player object by extending pygame.sprite.Sprite
# The surface drawn on the screen is now an attribute of 'player'
class Agent(pygame.sprite.Sprite):
    def __init__(self,
                 cell_size=CELL_SIZE['BIG'],
                 number_of_robot=0,
                 surf_center=-1,
                 MR=round(3.5 * CELL_SIZE['BIG']),
                 SR=int(2.5 * CELL_SIZE['BIG']),
                 show_ranges=False,
                 speed=10,
                 cred=5,
                 ):
        super(Agent, self).__init__()
        self.cell_size = cell_size
        self.number_of_robot = number_of_robot
        self.name = 'agent_%s' % number_of_robot
        self.MR = int(MR)
        self.SR = int(SR)
        self.cred = cred
        self.show_ranges = show_ranges
        self.curr = (3, -3)
        self.future_pos = None
        self.arrived = True
        self.step_x = 0
        self.step_y = 0
        self.speed = speed
        self.direction = np.random.randint(360)  # degrees
        self.curr_nei = []
        self.curr_robot_nei = []
        self.inbox = {}
        self.named_inbox = {}
        self._lock = threading.RLock()

        self.surf = pygame.Surface((2 * MR, 2 * MR), pygame.SRCALPHA)

        if show_ranges:
            pygame.draw.circle(self.surf, (0, 0, 255, 20), self.surf.get_rect().center, self.MR)
            pygame.draw.circle(self.surf, (255, 0, 0, 40), self.surf.get_rect().center, self.SR)

        self.car_surf = pygame.transform.scale(pygame.image.load("pics/hamster2.png"), (cell_size, int(0.73 * cell_size)))
        self.car_surf.set_colorkey((255, 255, 255), RLEACCEL)

        # Number of Robot
        font = pygame.font.SysFont("comicsansms", int(cell_size * 0.25))
        text = font.render("%s" % number_of_robot, True, (225, 0, 0))
        wt, ht = text.get_size()
        self.car_surf.blit(text, (cell_size - wt, 0))

        self.surf.blit(self.car_surf, self.car_surf.get_rect(center=self.surf.get_rect().center))

        if surf_center == -1:
            self.rect = self.surf.get_rect()
            print('[ERROR]: surf_center == -1 in Agent')
        else:
            self.surf_center = surf_center
            self.rect = self.surf.get_rect(
                center=surf_center
            )
            self.radius = MR

    # Move the sprite based on user keypresses
    def move(self):
        # logging.info("Thread %s : starting moving", threading.get_ident())

        self.arrived = self.rect.center == self.future_pos

        if not self.arrived:

            curr_x, curr_y = self.rect.center
            future_x, future_y = self.future_pos

        # if self.rect.center == self.future_pos:
        #     self.arrived = True
        # else:

            x = self.step_x if abs(curr_x - future_x) > abs(self.step_x) else (future_x - curr_x)
            y = self.step_y if abs(curr_y - future_y) > abs(self.step_y) else (future_y - curr_y)

            # self.rect.move_ip(x, y)
            self.rect.center = (curr_x + x, curr_y + y)

            # print(self.get_name(), ' in move function', ' ', self.rect.center, ' ', self.future_pos,
            #       ' steps:', self.step_x, self.step_y, ' x and y:', x, y)

    def alg_update(self, algorithm, agents, targets, cells, for_alg):
        self.future_pos = algorithm(self.preprocessing(
            agent=self,
            curr_pose=self.rect.center,
            cell_size=self.cell_size,
            agents=agents,
            targets=targets,
            cells=cells,
            for_alg=for_alg,
        ))
        self.arrived = False

        # for rendering
        curr_x, curr_y = self.rect.center
        new_x, new_y = self.future_pos
        self.step_x = int((new_x - curr_x) / self.speed)
        self.step_y = int((new_y - curr_y) / self.speed)

        time.sleep(1)

    def preprocessing(self, **kwargs):
        # print('in preprocessing')
        return kwargs

    # def get_pos(self):
    #     return self.rect.center

    # different from other because the agent is moving -> NOT self.surf_center
    def get_pos(self):
        return self.rect.center

    def get_cell_size(self):
        return self.cell_size

    def set_pos(self, pos):
        self.rect.center = pos
        self.future_pos = pos

    def get_access_to_inbox(self, type_of_requirement, num_of_agent=None, message=None, name=None):
        with self._lock:
            # logging.info("Thread %s has the lock inside %s", num_of_agent, self.number_of_robot)
            if type_of_requirement == 'message':
                # logging.info("Thread %s has the message: %s", num_of_agent, message)
                if num_of_agent in self.inbox:
                    self.inbox[num_of_agent].append(message)
                    self.named_inbox[name].append(message)
                else:
                    print('[ERROR]: num_of_agent is NOT in self.inbox')
                    # print(num_of_agent, ' inside Agent')
                # logging.info("Agent %s after update has the inbox: %s", self.number_of_robot, self.inbox)

            if type_of_requirement == 'copy':
                # logging.info("Thread %s about to release the lock!!!! inbox: %s", num_of_agent, self.inbox)
                return copy.deepcopy(self.inbox)
            # logging.info("Thread %s about to release lock inside %s", num_of_agent, self.number_of_robot)

    def get_access_to_named_inbox(self, type_of_requirement, name_of_agent=None, message=None):

        with self._lock:

            if type_of_requirement == 'message':
                # print(name_of_agent, 'is inside the ', self.name, '. Here $$$$$$$$$$$$$$$$$$$$$$')
                # print(list(self.named_inbox.keys()))
                if name_of_agent in self.named_inbox:

                    self.named_inbox[name_of_agent].append(message)

                else:
                    print('[ERROR]: num_of_agent is not in self.inbox')
            if type_of_requirement == 'copy':
                return copy.deepcopy(self.named_inbox)
        # print(name_of_agent, 'get_access_to_named_inbox!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')

    def get_SR(self):
        return self.SR

    def get_MR(self):
        return self.MR

    def get_name(self):
        return self.name

    def get_cred(self):
        return self.cred

    def get_direction(self):
        return self.direction

    def set_direction(self, direction):
        self.direction = direction

    def get_curr_nei(self):
        return self.curr_nei

    def get_curr_robot_nei(self):
        return self.curr_robot_nei

    def get_num_of_agent(self):
        return self.number_of_robot

    def nei_update(self, agents, targets, factor_graph):
        # Update self.curr_nei
        self.curr_nei = []
        if not factor_graph:
            for agent in agents:
                if self.number_of_robot != agent.number_of_robot:
                    if distance(self.get_pos(), agent.get_pos()) < (self.SR + self.MR + agent.get_SR() + agent.get_MR()):
                        self.curr_nei.append(agent)
                    if distance(self.get_pos(), agent.get_pos()) < (self.MR + agent.get_MR()):
                        self.curr_robot_nei.append(agent)
        else:
            self.curr_robot_nei = []
            for target in targets:
                if distance(self.get_pos(), target.get_pos()) < (self.SR + self.MR):
                    self.curr_nei.append(target)
            for agent in agents:
                if self.number_of_robot != agent.number_of_robot:
                    if distance(self.get_pos(), agent.get_pos()) < (self.MR + agent.get_MR()):
                        self.curr_robot_nei.append(agent)

        # Update self.inbox
        self.inbox = {}
        self.named_inbox = {}
        for agent in self.curr_nei:
            self.inbox[agent.get_num_of_agent()] = []
            self.named_inbox[agent.get_name()] = []
        for agent in self.curr_robot_nei:
            self.named_inbox[agent.get_name()] = []

        self.future_pos = self.rect.center


        # logging.info("Thread %s : finishing update", threading.get_ident())

        # if pressed_keys[K_UP]:
        #     self.rect.move_ip(0, -5)
        # if pressed_keys[K_DOWN]:
        #     self.rect.move_ip(0, 5)
        # if pressed_keys[K_LEFT]:
        #     self.rect.move_ip(-5, 0)
        # if pressed_keys[K_RIGHT]:
        #     self.rect.move_ip(5, 0)
        #
        # # Keep player on the screen
        # if self.rect.left < 0:
        #     self.rect.left = 0
        # if self.rect.right > SCREEN_HEIGHT:
        #     self.rect.right = SCREEN_HEIGHT
        # if self.rect.top <= 0:
        #     self.rect.top = 0
        # if self.rect.bottom >= SCREEN_HEIGHT:
        #     self.rect.bottom = SCREEN_HEIGHT


