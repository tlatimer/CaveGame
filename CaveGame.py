import pygame as pg

import LoadBoard


# test


class CaveGame:
    def __init__(self):
        pg.init()

        pg.display.set_caption('Cave Game')
        self.screen = pg.display.set_mode((600, 400), pg.RESIZABLE)

        self.wait_for_resize()
        # TODO: set mode to static size and/or scaled?

        lb = LoadBoard.LoadBoard(self.screen)
        board = lb.board

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


if __name__ == '__main__':
    CaveGame()
