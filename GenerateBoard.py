from collections import deque
from random import choices

INITIAL_ALIVE = 0.55
CA_STEPS = 2


class GenerateBoard:
    def __init__(self, w, h):
        self.w = w
        self.h = h

        # alive is CA terminology, these are 'spaces' or 'not walls'
        self.alive_cells = self.get_random_alive()

        for _ in range(CA_STEPS):
            self.do_ca_step()

        groups = self.get_groups()
        # self.close_groups(groups)

        self.score2 = len(self.alive_cells) / (w * h)

    def get_random_alive(self):
        cells = []
        for x in range(self.w):
            for y in range(self.h):
                cells.append((x, y))

        num_to_live = int(self.w * self.h * INITIAL_ALIVE)

        return set(choices(cells, k=num_to_live))

    def do_ca_step(self):
        old_cells = self.alive_cells.copy()
        for x in range(self.w):
            for y in range(self.h):
                if self.count_neighbors(x, y, old_cells) < 3 and (x, y) in self.alive_cells:
                    self.alive_cells.remove((x, y))
                elif self.count_neighbors(x, y, old_cells) > 4:
                    self.alive_cells.add((x, y))

    def count_neighbors(self, x, y, cell_list):
        num_alive = 0
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if (dx, dy) == (0, 0):  # don't need to count your own cell
                    continue
                elif (x + dx, y + dy) in cell_list:
                    num_alive += 1

        return num_alive

    def get_groups(self):
        groups = []
        visited = set()
        to_visit = deque()
        for x, y in self.alive_cells:
            if (x, y) in visited:
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

    def get_neighbors(self, x, y):
        poss = [
            (x + 1, y),
            (x - 1, y),
            (x, y + 1),
            (x, y - 1),
        ]

        for p in poss.copy():
            if p not in self.alive_cells:
                poss.remove(p)

        return poss

    def close_groups(self, groups):
        for g in groups[1:]:
            for cell in g:
                self.alive_cells.remove(cell)

        return groups

    def get_tiles(self):
        return self.alive_cells

    def get_walls_coords(self):
        coords = []
        for x in range(self.w):
            for y in range(self.h):
                if (x, y) not in self.alive_cells:
                    coords.append((x, y))

        return coords


if __name__ == '__main__':
    GenerateBoard(140, 82).get_walls_coords()
