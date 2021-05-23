from random import choices
from copy import copy

def main():
    b = Board(120, 40)

class Board:
    def __init__(self, w, h):
        self.w = w
        self.h = h
        self.walls = []
        for x in range(w):
            self.walls.append([True] * h)

        self.generate_cave()

    def print_walls(self):
        for y in range(self.h):
            for x in range(self.w):
                if self.walls[x][y]:
                    print('#', end='')
                else:
                    print(' ', end='')
            print()
        print('\n')

    def generate_cave(self):
        self.all_coords = []
        for x in range(1, self.w - 1):
            for y in range(1, self.h - 1):
                self.all_coords.append((x, y))

        # initialize to random
        num_to_blank = int(self.h * self.w * 0.45)
        for coords in choices(self.all_coords, k=num_to_blank):
            x, y = coords
            self.walls[x][y] = False

        for _ in range(2):
            self.print_walls()
            self.do_ca_step()

    def do_ca_step(self):
        walls_copy = copy(self.walls)
        for x, y in self.all_coords:
            if self.count_nonwall_neighbor(x, y, walls_copy) < 3:
                self.walls[x][y] = True
            elif self.count_nonwall_neighbor(x, y, walls_copy) > 4:
                self.walls[x][y] = False

    def count_nonwall_neighbor(self, x, y, walls_list):
        num_nonwall = 0
        for xvar in [-1, 0, 1]:
            for yvar in [-1, 0, 1]:
                if (xvar, yvar) == (0, 0):
                    continue
                if not walls_list[x + xvar][y + yvar]:
                    num_nonwall += 1
        return num_nonwall


if __name__ == '__main__':
    main()