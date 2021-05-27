from collections import deque
from random import choices


def main():
    w = 140
    h = 82
    gb = GenerateBoard(w, h)


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

        if len(self.groups) > 1:
            self.score2 = len(self.groups[0]) / len(self.groups[1])
        self.score = len(self.groups[0]) / (self.w * self.h)

        self.close_groups()

        self.alive_cells = set()
        for x, y in self.all_coords:
            if not self.walls[x][y]:
                self.alive_cells.add((x, y))

    def get_score(self):
        return self.score2

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
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if (dx, dy) == (0, 0):
                    continue
                elif not corners and (dx + dy in [-2, 0, 2]):
                    continue
                if not walls_grid[x + dx][y + dy]:
                    neighbors.append((x + dx, y + dy))

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


if __name__ == '__main__':
    main()
