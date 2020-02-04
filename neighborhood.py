import numpy as np
import matplotlib.pyplot as plt

S = 10000*np.load('S_matrix.npy')

def allele(arr,a,b):
    a_size=np.size(np.where(arr==a))//2
    b_size=np.size(np.where(arr==b))//2
    return [a_size,b_size]

def autocorelate(arr1):
    n=np.correlate(arr1,arr1,mode='full')
    N=n[np.size(n)//2:]/np.max(n)
    for i in N:
        if i <= 1/np.exp(1):
            Z=i
            break
    return Z

# 2D grid
class neighborhood:

    def __init__(self, s_array, neighboring_mode=4):
        self.neighboring_mode = neighboring_mode
        self.s_array = s_array

        self.height = np.size(self.s_array, axis=0)
        self.width = np.size(self.s_array, axis=1)

        self.PI_array = np.ndarray((self.width, self.height))

        self.time = 0
        self.equilibrium = False
    def next_generation(self):
        self.adaptive_learning()

        for i in range(self.height):
            for j in range(self.width):
                PI = 0
                s = self.s_array[i, j]

                if self.neighboring_mode == 4 or self.neighboring_mode == 8:
                    up = i - 1
                    down = int((i + 1) % self.height)
                    left = j - 1
                    right = int((j + 1) % self.width)

                    PI += S[s, self.s_array[i, right]]  # right
                    PI += S[s, self.s_array[i, left]]  # left
                    PI += S[s, self.s_array[down, j]]  # down
                    PI += S[s, self.s_array[up, j]]  # up

                    if self.neighboring_mode == 8:
                        PI += S[s, self.s_array[up, right]]  # upper right
                        PI += S[s, self.s_array[up, left]]  # upper left
                        PI += S[s, self.s_array[down, right]]  # lower right
                        PI += S[s, self.s_array[down, left]]  # lower left

                elif self.neighboring_mode == 'all':
                    for i in range(self.height):
                        for j in range(self.width):
                            PI += S[s, self.s_array[i, j]]

                self.PI_array[i, j] = PI

        self.time += 1

    # def wright_fischer(self, beta=10):


    def adaptive_learning(self, beta=10000):

        def rho(r, l):  # l:learner
            return 1 / (1 + np.exp(-beta * (r - l)))

        for i in range(self.height):
            for j in range(self.width):
                c = []
                s = []
                PI = self.PI_array[i, j]

                if self.neighboring_mode == 4 or self.neighboring_mode == 8:

                    up = i - 1
                    down = (i + 1) % self.height
                    left = j - 1
                    right = (j + 1) % self.width
                    c.append(rho(PI, PI))  # 0
                    c.append(rho(self.PI_array[up, j], PI))  # up
                    c.append(rho(self.PI_array[down, j], PI))  # down
                    c.append(rho(self.PI_array[i, left], PI))  # left
                    c.append(rho(self.PI_array[i, right], PI))  # right

                    s.append(self.s_array[i, j])
                    s.append(self.s_array[up, j])
                    s.append(self.s_array[down, j])
                    s.append(self.s_array[i, left])
                    s.append(self.s_array[i, right])

                    if self.neighboring_mode == 8:
                        c.append(rho(self.PI_array[up, right], PI))
                        c.append(rho(self.PI_array[up, left], PI))
                        c.append(rho(self.PI_array[down, right], PI))
                        c.append(rho(self.PI_array[down, left], PI))

                        s.append(self.s_array[up, right])
                        s.append(self.s_array[up, left])
                        s.append(self.s_array[down, right])
                        s.append(self.s_array[down, left])

                    c = np.asarray(c)
                    c = c / np.sum(c)
                    self.s_array[i, j] = s[np.random.choice(self.neighboring_mode+1, 1, p=c)[0]]

    # def wright_fischer_learning(self):

# setting up initial s_array
s1 = 14
s2 = 10
w = 10
h = 10
invader_positions = [[0,0],[0,1],[1,0],[1,1]]
initial_s_array = np.zeros((h, w), dtype='int')

for i in range(h):
    for j in range(w):
        if [i, j] in invader_positions:
            initial_s_array[i, j] = s1
        else:
            initial_s_array[i, j] = s2

Neighborhood4 = neighborhood(initial_s_array, neighboring_mode=4)
allele1_4 = []
allele2_4 = []

Neighborhood8 = neighborhood(initial_s_array, neighboring_mode=8)
allele1_8 = []
allele2_8 = []

while not Neighborhood4.equilibrium:
    Neighborhood4.next_generation()
    # print(Neighborhood4.s_array)
    allele1, allele2 = allele(Neighborhood4.s_array, s1, s2)
    # print(allele1, allele2)
    allele1_4.append(allele1)
    allele2_4.append(allele2)
    if allele1 == 0 or allele2 == 0:
        print(4,Neighborhood4.time)
        Neighborhood4.equilibrium = True

#print(Neighborhood4.s_array)

while not Neighborhood8.equilibrium:
    Neighborhood4.next_generation()
    allele1, allele2 = allele(Neighborhood8.s_array, s1, s2)
    allele1_8.append(allele1)
    allele2_8.append(allele2)
    if allele1 == 0 or allele2==0:
        print(8,Neighborhood8.time)
        Neighborhood8.equilibrium = True

a1_4 = np.array(allele1_4)
a2_4 = np.array(allele2_4)
a1_8 = np.array(allele1_8)
a2_8 = np.array(allele2_8)
time_array4 = np.arange(np.alen(a1_4))
time_array8 = np.arange(np.alen(a1_8))

#fig = plt.figure()
#ax = fig.add_subplot(111)
#ax.plot(time_array4, a1_4, label='4'+str(s1))
#ax.plot(time_array4, a2_4, label='4'+str(s2))
#ax.plot(time_array8, a1_8, label='8'+str(s1))
#ax.plot(time_array8, a2_8, label='8'+str(s2))

#plt.show()

