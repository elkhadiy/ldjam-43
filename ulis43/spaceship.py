from ulis43.asset_manager import AssetManager


class Spaceship():

    def __init__(self, ressources, crew, rooms):
        self.ressources = ressources
        self.crew = crew
        self.rooms = rooms

    def tick(self):
        for crew_member in self.crew:
            self.ressources = crew_member.tick(self.ressources)
        for room in self.rooms:
            self.ressources = room.tick(self.ressources)

    def draw(self, ctx):
        elec_surf, elec_rect = AssetManager().getFont("hud").render(
            "ELEC: {}".format(self.ressources["ELECTRICITY"]),
            fgcolor=(251, 242, 54)
        )
        water_surf, water_rect = AssetManager().getFont("hud").render(
            "WATER: {}".format(self.ressources["WATER"]),
            fgcolor=(99, 155, 255)
        )
        oxy_surf, oxy_rect = AssetManager().getFont("hud").render(
            "OXYGEN: {}".format(self.ressources["OXYGEN"]),
            fgcolor=(233, 233, 233)
        )
        food_surf, food_rect = AssetManager().getFont("hud").render(
            "FOOD: {}".format(self.ressources["FOOD"]),
            fgcolor=(138, 111, 48)
        )
        ctx.blit(elec_surf, elec_rect.move(620, 20))
        ctx.blit(water_surf, water_rect.move(620, 40))
        ctx.blit(oxy_surf, water_rect.move(620, 60))
        ctx.blit(food_surf, food_rect.move(620, 80))
        for room in self.rooms:
            room.draw(ctx)
        for crew_member in self.crew:
            crew_member.draw(ctx)

    def __repr__(self):
        return """Ressources: {}\nCrew: {}\nRooms: {}\n""".format(
            self.ressources, self.crew, self.rooms
        )
