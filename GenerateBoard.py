from collections import deque
from random import choices

INITIAL_ALIVE = 0.6
CA_STEPS = 2

NUM_BINS = 3


class GenerateBoard:
    def __init__(self, w, h):
        self.w = w
        self.h = h

        self.all_cells = []
        for x in range(self.w):
            for y in range(self.h):
                self.all_cells.append((x, y))

        # alive is CA terminology, these are 'spaces' or 'not walls'
        self.alive_cells = self.get_random_alive()

    def main(self):
        for _ in range(CA_STEPS):
            self.do_ca_step()

        self.close_groups()

    def get_random_alive(self):  # TODO: add a way to specify seed
        num_to_live = int(self.w * self.h * INITIAL_ALIVE)
        return set(choices(self.all_cells, k=num_to_live))

    def do_ca_step(self):
        old_cells = self.alive_cells.copy()
        for pos in self.all_cells:
            if self.count_neighbors(pos, old_cells) < 3 and pos in self.alive_cells:
                self.alive_cells.remove(pos)
            elif self.count_neighbors(pos, old_cells) > 4:
                self.alive_cells.add(pos)

    def count_neighbors(self, pos, cell_list):
        x, y = pos
        num_alive = 0
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if (dx, dy) == (0, 0):  # don't need to count your own cell
                    continue
                elif (x + dx, y + dy) in cell_list:
                    num_alive += 1

        return num_alive

    def close_groups(self):
        groups = self.get_groups()
        for g in groups[1:]:
            for cell in g:
                self.alive_cells.remove(cell)

    def get_groups(self):
        groups = []
        visited = set()
        to_visit = deque()
        for cell in self.alive_cells:
            if cell in visited:
                continue
            else:
                # begin BFS from this point
                to_visit.append(cell)
                my_group = []
                while to_visit:
                    cur = to_visit.popleft()
                    my_group.append(cur)
                    visited.add(cur)

                    for n in self.get_neighbors(cur):
                        if n not in visited and n not in to_visit:
                            to_visit.append(n)

                groups.append(my_group)

        groups.sort(key=lambda i: len(i), reverse=True)
        return groups

    def get_neighbors(self, pos):
        x, y = pos
        n_pos = [
            (x + 1, y),
            (x - 1, y),
            (x, y + 1),
            (x, y - 1),
        ]

        for p in n_pos.copy():
            if p not in self.alive_cells:
                n_pos.remove(p)

        return n_pos

    def get_score(self):
        bin_w = self.w / NUM_BINS
        bin_h = self.h / NUM_BINS

        bins = [[list() for x in range(NUM_BINS)] for y in range(NUM_BINS)]

        for cell in self.alive_cells:
            x = int(cell[0] / bin_w)
            y = int(cell[1] / bin_h)
            bins[x][y].append(cell)

        n = NUM_BINS - 1
        corners = [
            (0, 0),
            (0, n),
            (n, 0),
            (n, n)
        ]

        corner_scores = []
        bin_num_tiles = bin_w * bin_h
        for x, y in corners:
            corner_scores.append(len(bins[x][y]) / bin_num_tiles)

        return min(corner_scores)
