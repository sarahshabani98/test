# -*- coding: utf-8 -*-
"""
Created on Sun Feb  2 23:40:37 2020

@author: Sara
"""

# -*- coding: utf-8 -*-
"""
Created on Sun Feb  2 23:18:54 2020

@author: Sara
"""

# for a given set of values for B1, B0, C;
# this code generates the transition matrices for the 16 almost deterministic strategies
# and calculates the corresponding S matrix
# strategies are numbered form 0 to 15
# and saves it in a file named B1-B0-C-s_matrix.npy
# to access the matrices you should load the S_array using this line of code:
# code: S_array = np.load('B1-B0-C-s_matrix.npy')
# suppose two players with strategies sA and sB are playing and we need the transition matrix for this match
# s1 : number of strategy sA (a number between 0 and 15 assigned to sA)
# s2 : number of strategy sB (a number between 0 and 15 assigned to sB)

import numpy as np

# reward parameters, other than these three numbers, do not change the rest of the code!
B1 = 2
B0 = 1.2
C = 1

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

# generating the 16 almost deterministic strategies:
epsilon = 0.01
q = 1-epsilon
probability_list = [epsilon, q]
strategy_list = []
for p1 in probability_list:
    for p2 in probability_list:
        for p3 in probability_list:
            for p4 in probability_list:
                strategy_list.append(strategy_generator(p1, p2, p3, p4))

state = [(0, 0, 0), (0, 0, 1), (0, 1, 0), (0, 1, 1), (1, 0, 0), (1, 0, 1), (1, 1, 0),
         (1, 1, 1)]  # (world, action1, action2)

def transition_matrix_generator(s1_index, s2_index):  # s1 = first player's strategy index, s2 = second player's strategy index
    P = np.ndarray((8, 8))
    s1 = strategy_list[s1_index]
    s2 = strategy_list[s2_index]

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
# calculating transition matrices for all possible pairs of strategies in order to find their fixed points
P_array = np.ndarray((16, 16, 8, 8))  # 16 strategies, 8 states, P[strategy1, strategy2] is an 8 x 8 transition matrix
S_array=np.zeros((16,16))

for s1 in range (16):
    for s2 in range (16):

        m = transition_matrix_generator(s1, s2) - np.identity(8)
        a = m[1:, 1:]
        b = -m[1:, 0]
        v_star = np.concatenate(([1], np.linalg.solve(a, b)))
        v_star = v_star / np.linalg.norm(v_star)
        # print(np.dot(m, v_star))

        for i in range(8):
            S_array[s1, s2] += reward_vector[i] * v_star[i]

np.save('S_matrix.npy', S_array)