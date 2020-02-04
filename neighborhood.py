import numpy as np

S = np.load('S_matrix.npy')

# 2D grid
class neighborhood:

    def __init__(self, s_array, neighboring_mode=4):
        self.neighboring_mode = neighboring_mode

        self.height = np.size(self.s_array, axis=0)
        self.width = np.size(self.s_array, axis=1)

        self.s_array = s_array
        self.PI_array = np.ndarray((self.width, self.height))

    def next_generation(self):
        self.adaptive_learning()

        for i in range(self.height):
            for j in range(self.width):
                PI = 0
                s = self.s_array[i, j]

                if self.neighboring_mode == 4 or self.neighboring_mode == 8:
                    up = i - 1
                    down = (i + 1) % self.height
                    left = j - 1
                    right = (j + 1) % self.width

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
                    for i in range(self.width):
                        for j in range(self.height):
                            PI += S[s, self.s_array[i, j]]

                self.PI_array[i, j] = PI

    def adaptive_learning(self, beta=0.7):

        def rho(r, l):  # l:learner
            return 1 / (1 + np.exp(-beta * (r - l)))

        for i in range(self.width):
            for j in range(self.height):
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