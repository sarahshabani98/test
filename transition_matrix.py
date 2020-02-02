# for a given set of values for B1, B0, C;
# this code generates the transition matrices for the 16 deterministic strategies
# strategies are numbered form 0 to 15
# and saves it in a file named B1-B0-C-transition_matrices.npy
# to access the matrices you should load the P_array using this line of code:
# code: P_array = np.load('B1-B0-C-transition_matrices.npy')
# suppose two players with strategies sA and sB are playing and we need the transition matrix for this match
# s1 : number of strategy sA (a number between 0 and 15 assigned to sA)
# s2 : number of strategy sB (a number between 0 and 15 assigned to sB)
# to access the transition matrix, just feed s1 and s2 in P_array:
# P_array[s1, s2] : is the desired transition matrix

import numpy as np

# reward parameters, other than these three numbers, do not change the rest of the code!
B1 = 4
B0 = 3
C = 2


# do not change
def reward_generator(b0, b1, c):  # c < b0 < b1, (w, action, action)
    r_dict = dict(
        {(0, 0, 0): 0, (0, 0, 1): b0, (0, 1, 0): -c, (0, 1, 1): b0 - c, (1, 0, 0): 0, (1, 0, 1): b1, (1, 1, 0): -c,
         (1, 1, 1): b1 - c})
    r_vector = [0, b0, -c, b0 - c, 0, b1, -c, b1 - c]
    return r_dict, r_vector


reward, reward_vector = reward_generator(B0, B1, C)

Q = dict({(0, 0, 0): 0, (0, 0, 1): 0, (0, 1, 0): 0, (0, 1, 1): 1, (1, 0, 0): 0, (1, 0, 1): 0, (1, 1, 0): 0,
          (1, 1, 1): 1})  # world transition
Q_vector = [0, 0, 0, 1, 0, 0, 0, 1]


def strategy_generator(p1, p2, p3, p4):
    strategy = dict({(1, 1): p1, (1, 0): p2, (0, 1): p3, (0, 0): p4})
    return strategy

# generating the 16 deterministic strategies:
i = 0
strategy_list = []
for p1 in range(2):
    for p2 in range(2):
        for p3 in range(2):
            for p4 in range(2):
                strategy_list.append(strategy_generator(p1, p2, p3, p4))
                i += 1

state = [(0, 0, 0), (0, 0, 1), (0, 1, 0), (0, 1, 1), (1, 0, 0), (1, 0, 1), (1, 1, 0),
         (1, 1, 1)]  # (world, action1, action2)

def transition_matrix_generator(s1, s2):  # s1 = first player's strategy, s2 = second player's strategy
    P = np.ndarray((8, 8))
    for i in range(8):
        for j in range(8):
            wj, a1j, a2j = state[j]

            if wj == Q_vector[i]:

                wi, a1i, a2i = state[i]
                q1 = s1[(a1i, a2i)]
                q2 = s2[(a2i, a1i)]

                if not a1j:
                    q1 = 1 - q1

                if not a2j:
                    q2 = 1 - q2

                transition_probability = q1 * q2

            else:

                transition_probability = 0

            P[j, i] = transition_probability # from state[i] to state[j]

    return P

# main goal of this file:
# calculating transition matrices for all possible pairs of strategies:
P_array = np.ndarray((16, 16, 8, 8))  # 16 strategies, 8 states, P[strategy1, strategy2] is an 8 x 8 transition matrix
for s1 in range(16):
    for s2 in range(16):
        P_array[s1, s2] = transition_matrix_generator(strategy_list[s1], strategy_list[s2])

np.save(str(B1)+'-'+str(B0)+'-'+str(C)+'-transition_matrices.npy', P_array)