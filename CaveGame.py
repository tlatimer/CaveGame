import pygame as pg
import pygame.draw

import GenerateBoard as gb


WIDTH = 1024
HEIGHT = 768

TILE_SIZE = 8

assert WIDTH % TILE_SIZE == 0 and HEIGHT % TILE_SIZE == 0


class CaveGame:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption('Cave Game')

        background = pg.Surface(self.screen.get_size())
        background = background.convert()
        background.fill('blue4')
        self.screen.blit(background, (0,0))

        loading = pg.font.Font(None, 36).render("LOADING", 1, 'white')
        loading_pos = loading.get_rect(centerx=background.get_width() / 2, centery=background.get_height() / 2)
        self.screen.blit(loading, loading_pos)
        pg.display.flip()
        # leave loading screen up while generating board

        self.board = gb.GenerateBoard(WIDTH / TILE_SIZE, HEIGHT / TILE_SIZE)

        self.screen.blit(background, (0, 0))
        # reblank background before drawing tiles
        for x, y in self.board.get_walls_coords():
            r = pg.Rect(
                x * TILE_SIZE,
                y * TILE_SIZE,
                TILE_SIZE,
                TILE_SIZE,
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
                elif event.type == pg.MOUSEBUTTONDOWN:
                    # TODO: figure out where the click was and do stuff
                    self.__init__()
                    pass
        finally:
            pg.quit()



if __name__ == '__main__':
    CaveGame().main()
