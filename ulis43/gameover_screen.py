from ulis43.asset_manager import AssetManager

import pygame


class GameOverScreen():

    def __init__(self):
        self.start = False

    def draw(self, ctx):
        title_surf, title_rect = AssetManager().getFont("title").render(
            "GAMEOVER", fgcolor=(255, 255, 255), size=150
        )
        ctx.blit(title_surf, title_rect.move(50, 0))

        white = (255, 255, 255)
        black = (0, 0, 0)
        start_surf, start_rect = AssetManager().getFont("subtitle").render(
            "RESTART", fgcolor=white, bgcolor=black
        )
        start_rect.move_ip(
            start_rect.left + 300, start_rect.top + 300
        )
        ctx.blit(start_surf, start_rect)

        self.start_button_rect = start_rect

        pos = pygame.mouse.get_pos()

        if ((self.start_button_rect.left <= pos[0])
            and (pos[0] <= self.start_button_rect.left + self.start_button_rect.width)
            and (self.start_button_rect.top <= pos[1])
            and (pos[1] <= self.start_button_rect.top + self.start_button_rect.height)):
            delta = 15
            start_rect.w += delta * 2
            start_rect.h += delta * 2
            start_rect.move_ip(-delta, -delta)
            pygame.draw.rect(ctx, white, start_rect, 5)
            if self.start:
                buttonbg = pygame.Surface((start_rect.w, start_rect.h))
                buttonbg.fill(white)
                ctx.blit(buttonbg, start_rect)
                start_surf, start_rect = AssetManager().getFont("subtitle").render(
                    "RESTART", fgcolor=black, bgcolor=white
                )
                start_rect.move_ip(
                    start_rect.left + 300, start_rect.top + 300
                )
                ctx.blit(start_surf, start_rect)

    def click_event(self, pos, event):
        self.start = (
            (self.start_button_rect.left <= pos[0])
            and (pos[0] <= self.start_button_rect.left + self.start_button_rect.width)
            and (self.start_button_rect.top <= pos[1])
            and (pos[1] <= self.start_button_rect.top + self.start_button_rect.height))
        if event == "up" and not self.start:
            self.start = False
        return self.start
