from ulis43.asset_manager import AssetManager


class GameOverScreen():

    def __init__(self):
        self.start = False

    def draw(self, ctx):
        title_surf, title_rect = AssetManager().getFont("title").render(
            "GAMEOVER", fgcolor=(255, 255, 255), size=150
        )
        center_x = title_rect.left + title_rect.width / 2
        center_y = title_rect.top + title_rect.height / 2
        delta_x = center_x - 400
        delta_y = center_y - 300
        ctx.blit(title_surf, title_rect.move(
            title_rect.left - delta_x, title_rect.top + delta_y / 2
        ))

        white = (255, 255, 255)
        yellow = (255, 255, 0)
        start_surf, start_rect = AssetManager().getFont("subtitle").render(
            "RESTART", fgcolor=yellow if self.start else white
        )
        center_x = start_rect.left + start_rect.width / 2
        center_y = start_rect.top + start_rect.height / 2
        delta_x = center_x - 400
        delta_y = center_y - 300
        start_rect.move_ip(
            start_rect.left - delta_x, start_rect.top - delta_y
        )
        ctx.blit(start_surf, start_rect)

        self.start_button_rect = start_rect

    def click_event(self, pos, event):
        self.start = (
            (self.start_button_rect.left <= pos[0])
            and (pos[0] <= self.start_button_rect.left + self.start_button_rect.width)
            and (self.start_button_rect.top <= pos[1])
            and (pos[1] <= self.start_button_rect.top + self.start_button_rect.height))
        if event == "up" and not self.start:
            self.start = False
        return self.start
