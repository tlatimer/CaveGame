import pygame as pg

import GenerateBoard
import Tile

NUM_BOARDS_TO_TRY = 20
MIN_NUM_TILES = 10000

SHOW_GEN = False


# TODO: reduce ambiguity between board: 'set of live cell coords' and board: 'list of Tile objects'
class LoadBoard:
    def __init__(self, draw):
        self.draw = draw
        self.clock = pg.time.Clock()

        board_w, board_h, self.tile_size = self.calc_tiles()
        board_approved = False
        while not board_approved:
            alive_board = self.load_board(board_w, board_h)
            board_approved = self.approve_board(alive_board)

        print('Board Approved!')
        self.draw_live_cells(alive_board)
        self.tiles = self.alive_to_tiles(alive_board.alive_cells)

    def calc_tiles(self):
        sx, sy = self.draw.screen.get_size()
        x, y = 1, 1

        while x * y < MIN_NUM_TILES:  # TODO: Can this be done with simple math? (not that it takes that long)
            if x / y > sx / sy:
                y += 1
            else:
                x += 1

        tile_size = int(min(sx / x, sy / y))

        x = int(sx / tile_size)
        y = int(sy / tile_size)

        print(f'Calculated {x}*{y} tiles for the board.')
        return x, y, tile_size

    def load_board(self, board_w, board_h):
        max_board = None
        max_score = -1

        for _ in range(NUM_BOARDS_TO_TRY):
            # give an opportunity to quit while generating
            event = pg.event.get()
            for e in event:
                if e.type == pg.QUIT or e.type == pg.KEYDOWN and e.key == pg.K_ESCAPE:
                    pg.quit()

            # gen the board
            cur_board = GenerateBoard.GenerateBoard(board_w, board_h)
            self.draw_live_cells(cur_board, 'GENERATING')

            for _2 in range(GenerateBoard.CA_STEPS):
                cur_board.do_ca_step()
                self.draw_live_cells(cur_board, 'GENERATING')

            cur_board.close_groups()
            self.draw_live_cells(cur_board, 'GENERATING')

            cur_score = cur_board.get_score()
            if cur_score > max_score:
                max_board = cur_board
                max_score = cur_score

        assert len(max_board.alive_cells) > 0
        return max_board

    def draw_live_cells(self, board, text=None):
        if text == 'GENERATING' and not SHOW_GEN:
            return
        self.draw.draw_bg()
        for x, y in board.alive_cells:
            r = pg.Rect(
                x * self.tile_size,
                y * self.tile_size,
                self.tile_size,
                self.tile_size,
            )
            pg.draw.rect(self.draw.screen, 'blue4', r)

        if text:
            self.draw.draw_text(text)

        pg.display.flip()
        # self.clock.tick(12)

    def approve_board(self, board):
        self.draw_live_cells(board, "[A]pprove or [R]eject?")
        while True:
            event = pg.event.wait()
            if event.type == pg.QUIT:
                pg.quit()
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    pg.quit()
                elif event.key in [pg.K_SPACE, pg.K_a]:
                    return True
                elif event.key == pg.K_r:
                    return False

    def alive_to_tiles(self, board):
        tiles = {}

        # populate tiles
        for pos in board:
            tiles[pos] = Tile.Tile(pos, self.tile_size)

        # populate tiles.neighbors
        for pos in board:
            x, y = pos
            neighbor_pos = [
                (x + 1, y),
                (x - 1, y),
                (x, y + 1),
                (x, y - 1),
            ]

            for n in neighbor_pos:
                if n in board:
                    tiles[pos].neighbors.add(n)

        return tiles
