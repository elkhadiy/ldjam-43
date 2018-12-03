from ulis43.asset_manager import AssetManager


class TitleScreen():

    def __init__(self):
        self.start = False

    def draw(self, ctx):
        title_surf, title_rect = AssetManager().getFont("title").render(
            "ULIS-43", fgcolor=(255, 255, 255)
        )
        center_x = title_rect.left + title_rect.width / 2
        center_y = title_rect.top + title_rect.height / 2
        delta_x = center_x - 400
        delta_y = center_y - 300
        ctx.blit(title_surf, title_rect.move(
            title_rect.left - delta_x, title_rect.top + delta_y
        ))

        white = (255, 255, 255)
        yellow = (255, 255, 0)
        start_surf, start_rect = AssetManager().getFont("subtitle").render(
            "START", fgcolor=yellow if self.start else white  #,
            # bgcolor=white if self.start else black
        )
        center_x = start_rect.left + start_rect.width / 2
        center_y = start_rect.top + start_rect.height / 2
        delta_x = center_x - 400
        delta_y = center_y - 300
        start_rect = title_rect.move(
            start_rect.left - delta_x, start_rect.top - delta_y
        )
        ctx.blit(start_surf, start_rect)

        self.start_button_rect = start_rect

    def click_event(self, pos, event):
        self.start = (
            self.start_button_rect.left <= pos[0]
            and pos[0] <= self.start_button_rect.left + self.start_button_rect.width
            and self.start_button_rect.top <= pos[1]
            and pos[1] <= self.start_button_rect.top + self.start_button_rect.height)
        if event == "up" and not self.start:
            self.start = False
        return self.start
