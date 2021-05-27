from collections import deque
from random import choices

INITIAL_ALIVE = 0.6
CA_STEPS = 2

NUM_BINS = 4


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

        for _ in range(CA_STEPS):
            self.do_ca_step()

        groups = self.get_groups()
        self.close_groups(groups)

        # self.score = self.get_score()

    def get_random_alive(self):
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
        deltas = [
            (x + 1, y),
            (x - 1, y),
            (x, y + 1),
            (x, y - 1),
        ]

        for p in deltas.copy():
            if p not in self.alive_cells:
                deltas.remove(p)

        return deltas

    def close_groups(self, groups):
        for g in groups[1:]:
            for cell in g:
                self.alive_cells.remove(cell)

    def get_score(self):
        #  Attempt 1
        # s1 = len(self.alive_cells) / (self.w * self.h) * 100
        # s2 = 0
        # if len(self.groups) > 1:
        #     s2 = len(self.groups[0]) / len(self.groups[1])
        #
        # print(f'{s1:4}\t{s2:4}')
        #
        # return s1 * 15 + s2 * 40

        #  Attempt 2
        # min_x = self.w
        # min_y = self.h
        # max_x = 0
        # max_y = 0
        # for x, y in self.alive_cells:
        #     min_x = min(x, min_x)
        #     min_y = min(y, min_y)
        #     max_x = max(x, max_x)
        #     max_y = max(y, max_y)
        #
        # score = min_x
        # score += min_y
        # score += self.w - max_x
        # score += self.h - max_y
        #
        # return -score

        #  Attempt 3
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

        bin_num_tiles = bin_w * bin_h
        score = 1.0
        for x, y in corners:
            corner_score = len(bins[x][y]) / bin_num_tiles
            print(f'score: {corner_score:3}')
            score += corner_score / 2

        print(f'Total: {score} \n')
        return score


if __name__ == '__main__':
    for _ in range(100):
        GenerateBoard(140, 82)
