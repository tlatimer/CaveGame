from random import choices
from copy import copy
from collections import deque


def main():
    b = Board(120, 40)


class Board:
    def __init__(self, w, h):
        self.w = w
        self.h = h
        self.walls = []
        for x in range(w):
            self.walls.append([True] * h)

        self.all_coords = []  # valid internal coords
        for x in range(1, self.w - 1):
            for y in range(1, self.h - 1):
                self.all_coords.append((x, y))

        self.generate_cave()
        self.groups = self.get_groups()
        self.print_board(True)
        print(len(self.groups[0]) / (self.w * self.h))

    def print_board(self, with_groups=False):
        for y in range(self.h):
            for x in range(self.w):
                if not with_groups:
                    if self.walls[x][y]:
                        print('#', end='')
                    else:
                        print(' ', end='')
                else:
                    if self.walls[x][y]:
                        print(' ', end='')
                        continue

                    for i, group in enumerate(self.groups):
                        if (x, y) in group:
                            print(chr(65 + i), end='')
            print()
        print('\n')

    def generate_cave(self):
        # initialize to random
        num_to_blank = int(self.h * self.w * 0.55)
        for x, y in choices(self.all_coords, k=num_to_blank):
            self.walls[x][y] = False

        for _ in range(2):
            self.do_ca_step()  # ca = cellular automata

    def do_ca_step(self):
        walls_old = copy(self.walls)
        for x, y in self.all_coords:
            if len(self.get_neighbors(x, y, walls_old)) < 3:
                self.walls[x][y] = True

            elif len(self.get_neighbors(x, y, walls_old)) > 4:
                self.walls[x][y] = False

    def get_neighbors(self, x, y, walls_grid=None):
        if not walls_grid:
            walls_grid = self.walls

        neighbors = []
        for xvar in [-1, 0, 1]:
            for yvar in [-1, 0, 1]:
                if (xvar, yvar) == (0, 0):
                    continue
                if not walls_grid[x + xvar][y + yvar]:
                    neighbors.append((x + xvar, y + yvar))

        return neighbors

    def get_groups(self):
        groups = []
        visited = set()
        to_visit = deque()
        for x, y in self.all_coords:
            if self.walls[x][y]:
                continue
            elif (x, y) in visited:
                continue
            else:
                # begin BFS from this point
                to_visit.append((x, y))
                my_group = []
                while to_visit:
                    cur = to_visit.popleft()
                    my_group.append(cur)
                    visited.add(cur)

                    cur_x, cur_y = cur
                    for n in self.get_neighbors(cur_x, cur_y):
                        if n not in visited and n not in to_visit:
                            to_visit.append(n)

                groups.append(my_group)

        groups.sort(key=lambda i: len(i), reverse=True)
        return groups


if __name__ == '__main__':
    main()
