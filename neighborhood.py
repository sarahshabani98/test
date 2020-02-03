# reference file
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

    def next_generation(self, new_s_array):
        self.s_array = new_s_array

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