# Import the pygame module
from CONSTANTS import *



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
        self.curr_nei = []
        self.inbox = {}
        self._lock = threading.Lock()

        self.surf = pygame.Surface((2 * MR, 2 * MR), pygame.SRCALPHA)

        if show_ranges:
            pygame.draw.circle(self.surf, (0, 0, 255, 20), self.surf.get_rect().center, self.MR)
            pygame.draw.circle(self.surf, (255, 0, 0, 40), self.surf.get_rect().center, self.SR)

        self.car_surf = pygame.transform.scale(pygame.image.load("hamster2.png"), (cell_size, int(0.73 * cell_size)))
        self.car_surf.set_colorkey((255, 255, 255), RLEACCEL)

        # Number of Robot
        font = pygame.font.SysFont("comicsansms", int(cell_size * 0.25))
        text = font.render("%s" % number_of_robot, True, (225, 0, 0))
        wt, ht = text.get_size()
        self.car_surf.blit(text, (cell_size - wt, 0))

        self.surf.blit(self.car_surf, self.car_surf.get_rect(center=self.surf.get_rect().center))

        if surf_center == -1:
            self.rect = self.surf.get_rect()
            raise ValueError('surf_center == -1 in Agent')
        else:
            self.surf_center = surf_center
            self.rect = self.surf.get_rect(
                center=surf_center
            )
            self.radius = MR

    # Move the sprite based on user keypresses
    def move(self, pressed_keys=None):
        # logging.info("Thread %s : starting moving", threading.get_ident())
        # self.rect.move_ip(self.curr)
        if self.rect.center == self.future_pos:
            self.arrived = True
        else:
            curr_x, curr_y = self.rect.center
            future_x, future_y = self.future_pos

            x = self.step_x if abs(curr_x - future_x) > abs(self.step_x) else (future_x - curr_x)
            y = self.step_y if abs(curr_y - future_y) > abs(self.step_y) else (future_y - curr_y)

            # print('before', self.rect.center)
            self.rect.move_ip(x, y)
            # print('after', self.rect.center)

        # time.sleep(0.1)
        # logging.info("Thread %s : finishing moving", threading.get_ident())

    def update(self, algorithm, agents, targets, cells, for_alg):
        self.nei_update(agents)
        self.future_pos = algorithm(self.preprocessing(
            agent=self,
            curr_pose=self.rect.center,
            cell_size=self.cell_size,
            MR=self.MR,
            SR=self.SR,
            curr_nei=self.curr_nei,
            number_of_robot=self.number_of_robot,
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
        return kwargs

    def get_pos(self):
        return self.rect.center

    def get_message_from(self, num_of_agent, message):
        logging.info("Thread %s: starting update", num_of_agent)
        logging.info("Thread %s about to lock", num_of_agent)
        with self._lock:
            logging.info("Thread %s has lock", num_of_agent)
            self.inbox[num_of_agent].append(message)
            logging.info("Thread %s about to release lock", num_of_agent)
        logging.info("Thread %s after release", num_of_agent)
        logging.info("Thread %s: finishing update", num_of_agent)


    def send_curr_pose_to_curr_nei(self):
        # time.sleep(self.number_of_robot * 0.001)  # for stability: preventing deadlock
        for agent in self.curr_nei:
            if agent is self: raise ValueError('Ups')
            # with threading.Lock():
            # agent.inbox[self.number_of_robot].append(self.get_pos())
            agent.get_message_from(self.number_of_robot, self.get_pos())

    def get_possible_pos_with_MR(self, cells, targets):

        possible_pos = []
        cell_set1 = []
        cell_set2 = []
        cell_set3 = []

        for cell in cells:
            if pygame.sprite.collide_circle(self, cell):
                cell_set1.append(cell)

        for cell in cell_set1:
            captured = False
            for target in targets:
                if target.get_pos() == cell.get_pos():
                    captured = True
                    break
            if not captured:
                cell_set2.append(cell)

        for cell in cell_set2:
            captured = False
            for agent in self.curr_nei:
                if agent.get_pos() == cell.get_pos():
                    captured = True
                    break
            if not captured:
                cell_set3.append(cell)

        for cell in cell_set3:
            possible_pos.append(cell.get_pos())

        return possible_pos

    def calculate_temp_req(self, targets):

        def in_area(pos_1, pos_2, SR):
            px, py = pos_1
            tx, ty = pos_2
            return math.sqrt(math.pow(px - tx, 2) + math.pow(py - ty, 2)) < SR

        temp_req_set = []
        for target in targets:
            curr_tuple = (target, target.get_req())
            for agent in self.curr_nei:
                if in_area(agent.get_pos(), target.get_pos(), agent.get_SR()):
                    curr_tuple = (target, max(0, curr_tuple[1] - agent.get_cred()))
            temp_req_set.append(curr_tuple)

        return temp_req_set

    def received_all_messages(self):
        for _, messages in self.inbox.items():
            if len(messages) == 0:
                return False
        return True

    def get_SR(self):
        return self.SR

    def get_MR(self):
        return self.MR

    def get_cred(self):
        return self.cred

    def nei_update(self, agents):

        def distance(pos1, pos2):
            return math.sqrt(math.pow(pos1[0] - pos2[0], 2) + math.pow(pos1[1] - pos2[1], 2))

        # Update self.curr_nei
        self.curr_nei = []
        for agent in agents:
            if self.number_of_robot != agent.number_of_robot:
                if distance(self.get_pos(), agent.get_pos()) < self.SR + self.MR + agent.get_SR() + agent.get_MR():
                    self.curr_nei.append(agent)

        # Update self.inbox
        self.inbox = {}
        for agent in self.curr_nei:
            self.inbox[agent.number_of_robot] = []

        # print(self.number_of_robot, ': ', self.inbox)


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


