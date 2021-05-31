import pygame as pg


class Tile:
    def __init__(self, pos, tile_size):
        self.x, self.y = pos  # TODO: coords are technically stored in two places.. mh.
        self.tile_size = tile_size

        self.neighbors = set()
        self.contents = []

    def get_rect(self):
        return pg.Rect(
            self.x * self.tile_size,
            self.y * self.tile_size,
            self.tile_size,
            self.tile_size
        )
