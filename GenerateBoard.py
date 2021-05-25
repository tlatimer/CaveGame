from random import choices
from collections import deque


def main():
    w = 120
    h = 30
    gb = GenerateBoard(w, h)
    gb.print_board()


class GenerateBoard:
    def __init__(self, w, h):
        self.w = int(w)
        self.h = int(h)
        self.walls = []
        for x in range(self.w):
            self.walls.append([True] * self.h)

        self.all_coords = []  # valid internal coords
        for x in range(1, self.w - 1):
            for y in range(1, self.h - 1):
                self.all_coords.append((x, y))

        self.generate_cave()
        self.groups = self.get_groups()

        # TODO: instead of generating until it meets criteria, generate n boards and pull the best.
        self.score = len(self.groups[0]) / len(self.groups[1])
        self.score2 = len(self.groups[0]) / (self.w * self.h)
        if self.score < 40 or self.score2 < 0.5:
            # redo the generation
            print('Rebuilding...')
            self.__init__(w, h)

        self.close_groups()

    def print_board(self, with_groups=False):  # TODO: deprecate this mess
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
        walls_old = self.walls.copy()
        for x, y in self.all_coords:
            if len(self.get_neighbors(x, y, walls_old)) < 3:
                self.walls[x][y] = True

            elif len(self.get_neighbors(x, y, walls_old)) > 4:
                self.walls[x][y] = False

    def get_neighbors(self, x, y, walls_grid=None, corners=True):  # TODO: decide if corners should be their own func
        if not walls_grid:
            walls_grid = self.walls

        neighbors = []
        for xvar in [-1, 0, 1]:
            for yvar in [-1, 0, 1]:
                if (xvar, yvar) == (0, 0):
                    continue
                elif not corners and (xvar + yvar in [-2, 0, 2]):
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
                    for n in self.get_neighbors(cur_x, cur_y, corners=False):
                        if n not in visited and n not in to_visit:
                            to_visit.append(n)

                groups.append(my_group)

        groups.sort(key=lambda i: len(i), reverse=True)
        return groups

    def close_groups(self):
        for g in self.groups[1:]:
            for x, y in g:
                self.walls[x][y] = True

    def get_walls_coords(self):
        coords = []
        for x in range(self.w):
            for y in range(self.h):
                if self.walls[x][y]:
                    coords.append((x, y))

        return coords



if __name__ == '__main__':
    main()
