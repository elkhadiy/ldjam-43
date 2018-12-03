from ulis43.asset_manager import AssetManager


class TitleScreen():

    def __init__(self):
        self.start = False

    def draw(self, ctx):
        title_surf, title_rect = AssetManager().getFont("title").render(
            "ULIS-43", fgcolor=(255, 255, 255)
        )
        ctx.blit(title_surf, title_rect.move(100, 0))
        # ctx.blit(title_surf, title_rect.move(800-576, 600-108*2))

        white = (255, 255, 255)
        yellow = (255, 255, 0)
        start_surf, start_rect = AssetManager().getFont("subtitle").render(
            "START", fgcolor=yellow if self.start else white
        )
        start_rect.move_ip(
            start_rect.left + 300, start_rect.top + 300
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
