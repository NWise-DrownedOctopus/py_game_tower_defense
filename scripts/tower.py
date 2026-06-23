import pygame
from scripts.utils.assets import load_image
from scripts.utils.ui_utils import build_context_panel

class Tower (pygame.sprite.Sprite):

    def __init__(self, pos, tile_pos, surface, game):
        super().__init__()
        self.pos = pos
        self.gem = None
        self.game = game
        self.tile_pos = tile_pos
        self.surface = surface
        self.tower_img = load_image('tower.png')
        self.tower_hover_img = load_image('tower_hover.png')
        self.has_gem = False
        self.rect = pygame.Rect(pos[0], pos[1], game.tile_size, game.tile_size)

    def draw(self):
        self.surface.blit(self.tower_img, self.pos)

    def check_hover(self):
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            return True
        return False

    def hover(self, surf):
        surf.blit(self.tower_hover_img, (self.pos[0], self.pos[1] + 8))
        self.draw_context(surf)

    def draw_context(self, surf):
        width = 225
        mpos = pygame.mouse.get_pos()
            
        if not self.has_gem:            
            height = 100
            s = pygame.Surface((width, height))
            context_pos = (mpos[0] + 20, mpos[1] - height)
            if mpos[0] > (self.game.display.get_width() - width):
                context_pos = (mpos[0] - width, mpos[1] - height)
            lable_text = self.game.game_ui.context_font.render('Tower', True, self.game.game_ui.context_text_color)
            self._draw_context_panel(s, width, height, lable_text)
            
            info_text = self.game.game_ui.info_font.render('Insert a gem to activate', True, self.game.game_ui.info_text_color)
            info_text_rect = info_text.get_rect(center=(s.get_width() / 2, 65))
            s.blit(info_text, info_text_rect)

            surf.blit(s, context_pos)
            
        else:
            height = 150
            s = pygame.Surface((width, height))
            context_pos = (mpos[0] + 20, mpos[1] - height)
            if mpos[0] > (self.game.display.get_width() - width):
                context_pos = (mpos[0] - width, mpos[1] - height)
            lable_text = self.game.game_ui.context_font.render('Grade 1 Gem', True, self.game.game_ui.context_text_color)
            self._draw_context_panel(s, width, height, lable_text)
            
            text = 'Damage: ' + str(self.gem.damage)
            damage_text = self.game.game_ui.info_font.render(text, True, self.game.game_ui.info_text_color)
            damage_text_rect = damage_text.get_rect(center=(s.get_width() / 2, 60))
            s.blit(damage_text, damage_text_rect)

            text = 'Range: ' + str(self.gem.range / 10)
            range_text = self.game.game_ui.info_font.render(text, True, self.game.game_ui.info_text_color)
            range_text_rect = range_text.get_rect(center=(s.get_width() / 2, 80))
            s.blit(range_text, range_text_rect)

            text = 'Shots per second: ' + str(1 / self.gem.shot_delay)
            sps_text = self.game.game_ui.info_font.render(text, True, self.game.game_ui.info_text_color)
            sps_text_rect = sps_text.get_rect(center=(s.get_width() / 2, 100))
            s.blit(sps_text, sps_text_rect)

            text = 'Hits: ' + str(self.gem.hit_count)
            hits_text = self.game.game_ui.info_font.render(text, True, self.game.game_ui.context_text_color)
            hits_text_rect = hits_text.get_rect(center=(s.get_width() / 2, 120))
            s.blit(hits_text, hits_text_rect)

            surf.blit(s, context_pos)
        
    def draw_context(self, surf):
        width = 225
        mpos = pygame.mouse.get_pos()
        display_width = self.game.display.get_width()

        if not self.has_gem:
            height = 100
            label_text = self.game.game_ui.context_font.render('Tower', True, self.game.game_ui.context_text_color)
            s, context_pos = build_context_panel(mpos, width, height, label_text, display_width)

            info_text = self.game.game_ui.info_font.render('Insert a gem to activate', True, self.game.game_ui.info_text_color)
            s.blit(info_text, info_text.get_rect(center=(width / 2, 65)))
            surf.blit(s, context_pos)

        else:
            height = 150
            label_text = self.game.game_ui.context_font.render('Grade 1 Gem', True, self.game.game_ui.context_text_color)
            s, context_pos = build_context_panel(mpos, width, height, label_text, display_width)

            for text, y in [
                ('Damage: ' + str(self.gem.damage), 60),
                ('Range: ' + str(self.gem.range / 10), 80),
                ('Shots per second: ' + str(1 / self.gem.shot_delay), 100),
                ('Hits: ' + str(self.gem.hit_count), 120)
            ]:
                rendered = self.game.game_ui.info_font.render(text, True, self.game.game_ui.info_text_color)
                s.blit(rendered, rendered.get_rect(center=(width / 2, y)))
            surf.blit(s, context_pos)   
            