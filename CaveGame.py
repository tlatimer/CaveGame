import pygame as pg

import GenerateBoard as gb

NUM_BOARDS_TO_TRY = 30
MIN_NUM_TILES = 10000


class CaveGame:
    def __init__(self):
        pg.init()
        pg.display.set_caption('Cave Game')
        self.screen = pg.display.set_mode((838, 978), pg.RESIZABLE)

        self.wait_for_resize()
        # TODO: set mode to static size and/or scaled?

        self.tile_size = None  # set when board is loaded
        self.board = self.load_board()

        while True:
            event = pg.event.wait()
            if event.type == pg.QUIT:
                pg.quit()
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    pg.quit()
                elif event.key == pg.K_SPACE:
                    self.__init__()

    def wait_for_resize(self):
        is_resized = False
        while not is_resized:
            bg = pg.Surface(self.screen.get_size())
            bg = bg.convert()
            bg.fill('black')
            self.screen.blit(bg, (0, 0))

            message = "Please resize window then press SPACE."
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

    def load_board(self):
        bg = pg.Surface(self.screen.get_size())
        bg = bg.convert()
        bg.fill('black')
        self.screen.blit(bg, (0, 0))

        message = "GENERATING"
        text = pg.font.Font(None, 36).render(message, 1, 'white')
        text_pos = text.get_rect(centerx=bg.get_width() / 2, centery=bg.get_height() / 2)

        x, y, self.tile_size = self.calc_tiles()

        max_board = None
        max_score = 0

        for _ in range(NUM_BOARDS_TO_TRY):
            self.screen.blit(text, text_pos)
            pg.display.flip()

            # give an opportunity to quit while generating
            event = pg.event.get()
            for e in event:
                if e.type == pg.QUIT or e.type == pg.KEYDOWN and e.key == pg.K_ESCAPE:
                    pg.quit()

            # gen the board
            cur_board = gb.GenerateBoard(x, y)
            cur_score = cur_board.get_score()
            if cur_score > max_score:
                max_board = cur_board
                max_score = cur_score

            # redraw after the generation
            self.screen.blit(bg, (0, 0))
            self.draw_live_cells(cur_board)

        self.screen.blit(bg, (0, 0))
        self.draw_live_cells(max_board)
        pg.display.flip()

        return max_board

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

    def draw_live_cells(self, board):
        for x, y in board.alive_cells:
            r = pg.Rect(
                x * self.tile_size,
                y * self.tile_size,
                self.tile_size,
                self.tile_size,
            )
            pg.draw.rect(self.screen, 'blue4', r)


if __name__ == '__main__':
    CaveGame()
