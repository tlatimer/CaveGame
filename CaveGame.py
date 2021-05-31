import random
from collections import deque

import pygame as pg

from Draw import Draw
from LoadBoard import LoadBoard
from Player import Player

NUM_PLAYERS = 10


class CaveGame:
    def __init__(self):
        self.draw = Draw()
        self.draw.wait_for_resize()
        # TODO: set mode to static size and/or scaled?

        lb = LoadBoard(self.draw)
        self.tiles = lb.tiles

        self.players = []
        for pos in self.get_player_pos_s(NUM_PLAYERS):
            self.players.append(Player(pos, lb.tile_size))

        self.draw_board()
        pg.time.wait(10000)

    def get_player_pos_s(self, num_players):
        player_pos_s = []
        first_pos = random.choices(list(self.tiles))
        player_pos_s.append(self.find_furthest(first_pos))

        while len(player_pos_s) < num_players:
            self.draw_board()
            player_pos_s.append(self.find_furthest(player_pos_s))

        return player_pos_s

    def find_furthest(self, players):
        unvisited = set(self.tiles)
        visited = []

        to_visit = []  # list of deques, indexes match w players
        for i in range(len(players)):
            to_visit.append(deque())
            to_visit[i].append(players[i])

        flip_counter = 0

        while unvisited:
            for que in to_visit:
                if len(que) == 0:
                    continue
                cur = que.popleft()
                if cur not in unvisited:
                    continue

                unvisited.remove(cur)
                visited.append(cur)

                if cur not in players:  # TODO: figure out why this isn't working
                    pg.draw.rect(self.draw.screen, 'red', self.tiles[cur].get_rect())

                for n in self.tiles[cur].neighbors:
                    if n in unvisited:
                        que.append(n)

                flip_counter += 1
                if flip_counter % 20 == 0:
                    pg.display.flip()

            event = pg.event.get()
            for e in event:
                if e.type == pg.QUIT or e.type == pg.KEYDOWN and e.key == pg.K_ESCAPE:
                    pg.quit()

        return visited[-1]

    def draw_board(self):
        for tile in self.tiles.values():
            pg.draw.rect(self.draw.screen, 'blue4', tile.get_rect())

        for p in self.players:
            pg.draw.rect(self.draw.screen, 'yellow', p.get_rect())

        pg.display.flip()


if __name__ == '__main__':
    CaveGame()
