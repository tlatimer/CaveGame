import random
from collections import deque

import pygame as pg

from Draw import Draw
from LoadBoard import LoadBoard
from Player import Player

NUM_PLAYERS = 10


class CaveGame:
    def __init__(self):
        pg.init()
        pg.display.set_caption('Cave Game')
        self.screen = pg.display.set_mode((600, 400), pg.RESIZABLE)
        self.clock = pg.time.Clock()

        self.draw = Draw(self.screen)
        self.draw.wait_for_resize()
        # TODO: set mode to static size and/or scaled?

        self.lb = LoadBoard(self.draw)
        self.tiles = self.lb.tiles

        self.players = []
        for pos in self.get_player_pos_s(NUM_PLAYERS):
            self.players.append(Player(pos, self.lb.tile_size))

        self.draw_board()
        while True:
            event = pg.event.wait()
            if event.type == pg.QUIT:
                pg.quit()
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    pg.quit()
                elif event.key == pg.K_SPACE:
                    break

    def get_player_pos_s(self, num_players):
        first_pos = random.choices(list(self.tiles))
        new_pos = self.find_furthest(first_pos)
        self.players.append(Player(new_pos, self.lb.tile_size))

        while len(self.players) < num_players:
            self.draw_board()
            player_pos_s = [p.pos for p in self.players]
            new_pos = self.find_furthest(player_pos_s)
            self.players.append(Player(new_pos, self.lb.tile_size))

        return player_pos_s

    def find_furthest(self, player_pos_s):
        unvisited = set(self.tiles)
        visited = []

        to_visit = []  # list of deques, indexes match w players
        for i in range(len(player_pos_s)):
            to_visit.append(deque())
            to_visit[i].append(player_pos_s[i])

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

                if cur not in player_pos_s:
                    pg.draw.rect(self.draw.screen, 'red', self.tiles[cur].get_rect())

                for n in self.tiles[cur].neighbors:
                    if n in unvisited:
                        que.append(n)

                flip_counter += 1
                if flip_counter % 30 == 0:
                    pg.display.flip()
                    self.clock.tick(120)

            events = pg.event.get()
            for e in events:
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
