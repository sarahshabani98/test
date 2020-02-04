#sahar_jafarbeglou

import numpy as np 

i0 = 0
j0 = 0
s1 = 0
s2 = 15
w = 10
h = 10
S_array = np.zeros((h,w))

for i in range (h):
    for j in range (w):
        if i is i0 and j is j0:
            S_array[i,j] = s1
        else: 
            S_array[i,j] = s2