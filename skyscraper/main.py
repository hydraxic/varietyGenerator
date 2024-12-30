# Planning:
# generate solution and create puzzle based off solution

# rules:
# It is an N x N grid
# each row and column contains the numbers 1 to N only once
# the numbers outside the grid indicate how many skyscrapers can be seen from that direction
# taller skyscrapers block the view of smaller skyscrapers

import random
import numpy as np

class Skyscraper:
    def __init__(self, size):
        self.size = size
        self.puzzle = [([0] * size) for _ in range(size)]
        self.clues = [[] * 4] # top, right, bottom, left clues
    
    def consecutive_array(self, arr):
        nums = sorted(set(arr))
        return nums == list(range(1, len(nums) + 1))

    def valid(self, puzzle):
        for row in puzzle:
            if self.consecutive_array(row) == False:
                return False
        for i in range(self.size):
            col = [puzzle[j][i] for j in range(self.size)]
            if self.consecutive_array(col) == False:
                return False

    def generate_cyclic_latin_square(self):
        # generate a cyclic latin square of n size
        return np.array([(i + j) % self.size + 1 for j in range(self.size)] for i in range(self.size))
    
    def is_valid_cycle(self, square, r1 ,r2, c1, c2):
        # using Jacobson matthew's algorithm
        # check if the 2x2 grid is valid - contains two occurences of two distinct numbers
        nums = {square[r1][c1], square[r1][c2], square[r2][c1], square[r2][c2]}
        return len(nums) == 2
    
    def switch_nums(self, square, r1, r2, c1, c2):
        # switch the two numbers in the 2x2 grid
        square[r1][c1], square[r2][c2] = square[r2][c2], square[r1][c1]
        square[r1][c2], square[r2][c1] = square[r2][c1], square[r1][c2]

    def generate_random_latin_square(self, iterations):
        # generate a random latin square of n size
        square = self.generate_cyclic_latin_square()
        for _ in range(iterations):
            r1, r2 = random.sample(range(self.size), 2)
            c1, c2 = random.sample(range(self.size), 2)

            if self.is_valid_cycle(square, r1, r2, c1, c2):
                self.switch_nums(square, r1, r2, c1, c2)

        return square

    def generate_random_puzzle(self):
        # recursive backtracking function that generates a random puzzle
        if self.valid(self.puzzle):
            return self.puzzle
        
        for i in range(self.size):
            for j in range(self.size):
                if self.puzzle[i][j] == 0:
                    for num in range(1, self.size + 1):
                        if num not in self.puzzle[i] and num not in [self.puzzle[k][j] for k in range(self.size)]:
                            self.puzzle[i][j] = num
                            if self.generate_random_puzzle():
                                return self.puzzle
                            self.puzzle[i][j] = 0

skyscraper = Skyscraper(5)
print(skyscraper.generate_random_latin_square(1000))