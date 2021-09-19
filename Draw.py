import pygame as pg


class Draw:
    def __init__(self, screen):
        self.screen = screen

    def draw_bg(self, color='black'):
        bg = pg.Surface(self.screen.get_size())
        bg = bg.convert()
        bg.fill(color)
        self.screen.blit(bg, (0, 0))

    def draw_text(self, message, size=36, color='white'):
        # noinspection PyTypeChecker
        text = pg.font.Font(None, size).render(message, True, color)

        text_pos = text.get_rect(
            centerx=self.screen.get_width() / 2,
            centery=self.screen.get_height() / 2
        )
        self.screen.blit(text, text_pos)

    def wait_for_resize(self):
        is_resized = False
        while not is_resized:
            self.draw_bg()
            self.draw_text('Please resize window then press SPACE', 24)
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
