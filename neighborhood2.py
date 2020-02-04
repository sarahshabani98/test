import numpy as np
import matplotlib.pyplot as plt
S = 1000*np.load('S_matrix.npy')

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


    def adaptive_learning(self, beta=1):
        def rho(r, l):  # l:learner
            return 1 / (1 + np.exp(-beta * (r - l)))

        for i in range(self.height):
            for j in range(self.width):
                s = self.s_array[i, j]
                PI = self.PI_array[i, j]

                if self.neighboring_mode == 4 or self.neighboring_mode == 8:

                    up = i - 1
                    down = (i + 1) % self.height
                    left = j - 1
                    right = (j + 1) % self.width
                    rho_up = rho(self.PI_array[up, j], PI)  # up
                    if np.random.rand() < rho_up:
                        s = self.s_array[i, j]

                    rho_down = rho(self.PI_array[down, j], PI)  # down
                    if np.random.rand() < rho_down:
                        s = self.s_array[up, j]

                    rho_left = rho(self.PI_array[i, left], PI)  # left
                    if np.random.rand() < rho_left:
                        s = self.s_array[down, j]

                    rho_right = rho(self.PI_array[i, right], PI)  # right
                    if np.random.rand() < rho_right:
                        s = self.s_array[i, right]

                    if self.neighboring_mode == 8:

                        rho_up_right = rho(self.PI_array[up, right], PI)
                        if np.random.rand() < rho_up_right:
                            s = self.s_array[up, right]

                        rho_up_left = rho(self.PI_array[up, left], PI)
                        if np.random.rand() < rho_up_left:
                            s = self.s_array[up, left]

                        rho_down_right = rho(self.PI_array[down, right], PI)
                        if np.random.rand() < rho_down_right:
                            s = self.s_array[down, right]

                        rho_down_left = rho(self.PI_array[down, left], PI)
                        if np.random.rand() < rho_down_left:
                            s = self.s_array[down, left]

                self.s_array[i, j] = s

    # def wright_fischer_learning(self):

strategy_dict = dict({9:'WSLS', 0:'All D', 15:'All C', 10:'Tit for Tat'})
color_dict = dict({9:'-r',0:'-k', 15:'-y', 10:'-b'})
# setting up initial s_array
def invasion(s1, s2):
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

        if allele1 == 0:
            print(4, Neighborhood4.time, 'invader extinct')
            invasion_value4 = 1
            Neighborhood4.equilibrium = True

        if allele2 == 0:
            print(4, Neighborhood4.time, 'host extinct')
            invasion_value4 = 0
            Neighborhood4.equilibrium = True

    #print(Neighborhood4.s_array)
    while not Neighborhood8.equilibrium:
        Neighborhood8.next_generation()
        allele1, allele2 = allele(Neighborhood8.s_array, s1, s2)
        allele1_8.append(allele1)
        allele2_8.append(allele2)

        if allele1 == 0:
            print(8,Neighborhood8.time, 'invader extinct')
            invasion_value8 = 1
            Neighborhood8.equilibrium = True

        if allele2 == 0:
            print(8, Neighborhood8.time, 'host extinct')
            invasion_value8 = 0
            Neighborhood8.equilibrium = True


    return np.array([invasion_value4, invasion_value8, Neighborhood4.time, Neighborhood8.time])
    #a1_4 = np.array(allele1_4)
    #a2_4 = np.array(allele2_4)
    #a1_8 = np.array(allele1_8)
    #a2_8 = np.array(allele2_8)
    #time_array4 = np.arange(np.alen(a1_4))
    #time_array8 = np.arange(np.alen(a1_8))

    #fig4 = plt.figure()
    #ax4 = fig4.add_subplot(111)
    #ax4.plot(time_array4, a1_4, color_dict[s1], label=strategy_dict[s1])
    #ax4.plot(time_array4, a2_4, color_dict[s2], label=strategy_dict[s2])
    #ax4.set_xlabel('time step')
    #ax4.set_ylabel('population (allele)')
    #ax4.text(0.0, 1.0, '4 neighbors', horizontalalignment='left', verticalalignment='bottom',
     #          transform=ax4.transAxes)
    #ax4.text(1.0, 1.0, 'extinction time: %.d'%Neighborhood4.time, horizontalalignment='right', verticalalignment='bottom',
     #          transform=ax4.transAxes)
    #plt.legend()

    #plt.title('invader: '+strategy_dict[s1]+' host: '+strategy_dict[s2])
    #fig4.savefig('4 invader:'+str(s1)+' host:'+str(s2))

    #fig8 = plt.figure()
    #ax8 = fig8.add_subplot(111)
    #ax8.plot(time_array8, a1_8, color_dict[s1], label=strategy_dict[s1])
    #ax8.plot(time_array8, a2_8, color_dict[s2], label=strategy_dict[s2])
    #ax8.set_xlabel('time step')
    #ax8.set_ylabel('population (allele)')
    #ax8.text(0.0, 1.0, '8 neighbors', horizontalalignment='left', verticalalignment='bottom',
    #           transform=ax8.transAxes)
    #ax8.text(1.0, 1.0, 'extinction time: %.d'%Neighborhood8.time, horizontalalignment='right', verticalalignment='bottom',
    #           transform=ax8.transAxes)
    #plt.legend()
    #plt.title('invader: '+strategy_dict[s1]+' host: '+strategy_dict[s2])
    #fig8.savefig('8 invader:'+str(s1)+' host:'+str(s2))

probability4 = np.ndarray((4,4))
probability8 = np.ndarray((4,4))
extinction_time4 = np.ndarray((4,4))
extinction_time8 = np.ndarray((4,4))
strategy_list = [0, 9, 10, 15]
for k1 in range(4):
    for k2 in range(k1+1, 4):
        extinction_array = np.array([0,0,0,0])
        extinction_array_inverse = np.array([0,0,0,0])

        for i in range(10):
            extinction_array += invasion(strategy_list[k1], strategy_list[k2])
            extinction_array_inverse += invasion(strategy_list[k2], strategy_list[k1])

            print(i)

        extinction_array = extinction_array/10

        probability4[k1, k2] = extinction_array[0]
        probability8[k1, k2] = extinction_array[1]
        extinction_time4[k1, k2] = extinction_array[2]
        extinction_time8[k1, k2] = extinction_array[3]

        probability4[k2, k1] = extinction_array_inverse[0]
        probability8[k2, k1] = extinction_array_inverse[1]
        extinction_time4[k2, k1] = extinction_array_inverse[2]
        extinction_time8[k2, k1] = extinction_array_inverse[3]

def plot(array, text):
    fig =  plt.figure()
    ax = fig.add_subplot(111)
    ax.imshow(array, cmap='plasma')
    plt.title(text)
    fig.savefig(text)


plot(probability4, 'p4')
plot(probability8, 'p8')
plot(extinction_time4, 't4')
plot(extinction_time8, 't8')