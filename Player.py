import pygame as pg


class Player:
    def __init__(self, pos, tile_size):
        self.pos = pos
        self.tile_size = tile_size

    def get_rect(self):
        return pg.Rect(
            self.pos[0] * self.tile_size,
            self.pos[1] * self.tile_size,
            self.tile_size,
            self.tile_size
        )
