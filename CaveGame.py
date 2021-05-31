import random
from collections import deque

import pygame as pg

from Draw import Draw
from LoadBoard import LoadBoard
from Player import Player

NUM_PLAYERS = 5


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

        while unvisited:
            for i in range(len(players)):
                if len(to_visit[i]) == 0:
                    continue
                cur = to_visit[i].popleft()
                if cur not in unvisited:
                    continue

                pg.draw.rect(self.draw.screen, 'yellow', self.tiles[cur].get_rect())

                unvisited.remove(cur)
                visited.append(cur)
                for n in self.tiles[cur].neighbors:
                    if n in unvisited:
                        to_visit[i].append(n)
            if len(unvisited) % 10 == 0:  # TODO: turn this into some kind of tick based thing
                pg.display.flip()

        return visited[-1]

    def draw_board(self):
        for tile in self.tiles.values():
            pg.draw.rect(self.draw.screen, 'blue4', tile.get_rect())

        for p in self.players:
            pg.draw.rect(self.draw.screen, 'red', p.get_rect())

        pg.display.flip()


if __name__ == '__main__':
    CaveGame()
