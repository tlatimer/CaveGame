import pygame as pg

import GenerateBoard as gb

NUM_BOARDS_TO_TRY = 30
MIN_NUM_TILES = 10000


class CaveGame:
    def __init__(self):
        pg.init()
        self.clock = pg.time.Clock()
        pg.display.set_caption('Cave Game')
        self.screen = pg.display.set_mode((838, 978), pg.RESIZABLE)

        self.wait_for_resize()
        # TODO: set mode to static size and/or scaled?

        board_w, board_h, self.tile_size = self.calc_tiles()
        self.board = self.load_board(board_w, board_h)

        while True:
            event = pg.event.wait()
            if event.type == pg.QUIT:
                pg.quit()
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    pg.quit()
                elif event.key == pg.K_SPACE:
                    self.board = self.load_board(board_w, board_h)

    def wait_for_resize(self):
        is_resized = False
        while not is_resized:
            bg = pg.Surface(self.screen.get_size())
            bg = bg.convert()
            bg.fill('black')
            self.screen.blit(bg, (0, 0))

            message = "Please resize window then press SPACE."
            # noinspection PyTypeChecker
            text = pg.font.Font(None, 24).render(message, 1, 'white')

            text_pos = text.get_rect(centerx=bg.get_width() / 2, centery=bg.get_height() / 2)
            self.screen.blit(text, text_pos)
            pg.display.flip()

            event = pg.event.wait()
            if event.type == pg.VIDEORESIZE:
                print(f'Resized to {self.screen.get_size()}')
            elif event.type == pg.QUIT:
                pg.quit()
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    pg.quit()
                elif event.key == pg.K_SPACE:
                    is_resized = True

    def calc_tiles(self):
        sx, sy = self.screen.get_size()
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
        max_score = 0

        for _ in range(NUM_BOARDS_TO_TRY):
            # give an opportunity to quit while generating
            event = pg.event.get()
            for e in event:
                if e.type == pg.QUIT or e.type == pg.KEYDOWN and e.key == pg.K_ESCAPE:
                    pg.quit()

            # gen the board
            cur_board = gb.GenerateBoard(board_w, board_h)
            self.draw_live_cells(cur_board, "GENERATING")

            for _2 in range(gb.CA_STEPS):
                cur_board.do_ca_step()
                self.draw_live_cells(cur_board, "GENERATING")

            cur_board.close_groups()
            self.draw_live_cells(cur_board, "GENERATING")

            cur_score = cur_board.get_score()
            if cur_score > max_score:
                max_board = cur_board
                max_score = cur_score

        # print the best board
        self.draw_live_cells(max_board)
        return max_board

    def draw_live_cells(self, board, text=None):
        bg = pg.Surface(self.screen.get_size())
        bg = bg.convert()
        bg.fill('black')

        # noinspection PyTypeChecker
        text = pg.font.Font(None, 36).render(text, True, 'white')
        text_pos = text.get_rect(centerx=bg.get_width() / 2, centery=bg.get_height() / 2)

        self.screen.blit(bg, (0, 0))

        for x, y in board.alive_cells:
            r = pg.Rect(
                x * self.tile_size,
                y * self.tile_size,
                self.tile_size,
                self.tile_size,
            )
            pg.draw.rect(self.screen, 'blue4', r)

        if text:
            self.screen.blit(text, text_pos)

        pg.display.flip()
        self.clock.tick(12)


if __name__ == '__main__':
    CaveGame()
