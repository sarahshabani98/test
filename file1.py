import numpy as np

def reward_generator(b0, b1, c):  # c < b0 < b1, (w, action, action)
    r_dict = dict({(0,0,0):0, (0,0,1):b0, (0,1,0):-c, (0,1,1):b0-c, (1,0,0):0, (1,0,1):b1, (1,1,0):-c, (1,1,1):b1-c})
    r_vector = [0, b0, -c, b0-c, 0, b1, -c, b1-c]
    return r_dict, r_vector

reward, reward_vector = reward_generator(3, 4, 2)

Q = dict({(0,0,0):0, (0,0,1):0, (0,1,0):0, (0,1,1):1, (1,0,0):0, (1,0,1):0, (1,1,0):0, (1,1,1):1})  # world transition
Q_vector = [0,0,0,1,0,0,0,1]
# Q is symmetric w.r.t action1 and action2

def strategy_generator(p1, p2, p3, p4):
    strategy = dict({(1,1):p1, (1,0):p2, (0,1):p3, (0,0):p4})
    return strategy

# generating the 16 deterministic strategies:
i = 0
strategy_list = []
for p1 in range(1):
    for p2 in range(1):
        for p3 in range(1):
            for p4 in range(1):
                strategy_list.append(strategy_generator(p1, p2, p3, p4))
                i += 1

state = [(0,0,0), (0,0,1), (0,1,0), (0,1,1), (1,0,0), (1,0,1), (1,1,0), (1,1,1)]  # (world, action1, action2)

class player:

    def __init__(self, p0):
        self.wallet = 0
        self.PI = 0
        self.memory = ()
        self.world = 1
        self.action = 0
        self.p = p0
        self.strategy = strategy_generator(*self.p)

    def choose_action(self):
        probability = self.strategy[self.memory]
        if np.random.rand() < probability:
            self.action = 1
        else:
            self.action = 0


def initialize_match(p1, p2):
    p1.world = 1  # p1.world = p2.world, first round in the good world
    p1.action = int(2*np.random.rand())
    p2.action = int(2*np.random.rand())

def round(p1, p2):
    p1.wallet += reward[(p1.world, p1.action, p2.action)]
    p2.wallet += reward[(p1.world, p2.action, p1.action)]
    p1.memory = (p1.action, p2.action)
    p2.memory = (p2.action, p1.action)
    p1.world = Q[(p1.world, p1.action, p2.action)]
    p1.choose_action()
    p2.choose_action()

def match(p1, p2, N):
    for i in range(N):
        round(p1, p2)