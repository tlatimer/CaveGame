from collections import deque
from random import choices

INITIAL_ALIVE = 0.62
CA_STEPS = 2


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

        self.groups = self.get_groups()

        self.score = self.get_score()

        self.close_groups()

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

    def close_groups(self):
        for g in self.groups[1:]:
            for cell in g:
                self.alive_cells.remove(cell)

    def get_score(self):
        s1 = len(self.alive_cells) / (self.w * self.h) * 100
        s2 = 0
        if len(self.groups) > 1:
            s2 = len(self.groups[0]) / len(self.groups[1])

        print(f'{s1:4}\t{s2:4}')

        return s1 * 15 + s2 * 40

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
    for _ in range(100):
        GenerateBoard(140, 82).get_walls_coords()
