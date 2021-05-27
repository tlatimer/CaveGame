import pygame as pg

from old import GenerateBoard as gb


class CaveGame:
    def __init__(self):

        pg.init()

        pg.display.set_caption('Cave Game')
        self.screen = pg.display.set_mode((0, 0), pg.WINDOWMAXIMIZED)

        bg = pg.Surface(self.screen.get_size())
        bg = bg.convert()
        bg.fill('blue4')
        self.screen.blit(bg, (0, 0))

        loading = pg.font.Font(None, 36).render("LOADING", 1, 'white')
        loading_pos = loading.get_rect(centerx=bg.get_width() / 2, centery=bg.get_height() / 2)
        self.screen.blit(loading, loading_pos)
        pg.display.flip()
        # leave loading screen up while generating board

        tile_size = 16  # TODO: make this dynamic
        gb_args = (self.screen.get_width() / tile_size, self.screen.get_height() / tile_size)
        self.board = gb.GenerateBoard(*gb_args)

        self.screen.blit(bg, (0, 0))
        # reblank background before drawing tiles
        for x, y in self.board.get_walls_coords():
            r = pg.Rect(
                x * tile_size,
                y * tile_size,
                tile_size,
                tile_size,
            )
            pg.draw.rect(self.screen, 'black', r)

    def main(self):
        print('Entering Main Loop')
        try:
            while True:
                pg.display.flip()

                event = pg.event.wait()
                if event.type == pg.QUIT:
                    break
                elif event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                    break
                elif event.type == pg.MOUSEBUTTONDOWN:
                    # TODO: figure out where the click was and do stuff
                    self.__init__()
        finally:
            pg.quit()


if __name__ == '__main__':
    CaveGame().main()
