import pygame
from scripts.utils import load_image, load_images


class Tower (pygame.sprite.Sprite):

    def __init__(self, pos, tile_pos, surface, game):
        super().__init__()
        pygame.init()
        self.pos = pos
        self.gem = None
        self.game = game
        self.tile_pos = tile_pos
        self.surface = surface
        self.tower_img = load_image('Tower.png')
        self.tower_hover_img = load_image('tower_hover.png')
        self.has_gem = False
        self.rect = pygame.Rect(pos[0], pos[1], game.tile_size, game.tile_size)

    def draw(self):
        self.surface.blit(self.tower_img, self.pos)

    def check_hover(self):
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            return True

    def hover(self, surf):
        surf.blit(self.tower_hover_img, (self.pos[0], self.pos[1] + 8))
        self.draw_context(surf)

    def draw_context(self, surf):
        mpos = pygame.mouse.get_pos()

        if not self.has_gem:
            s = pygame.Surface((225, 100))
            context_pos = (mpos[0] + 20, mpos[1] - 100)
            if mpos[0] > 863:
                context_pos = (mpos[0] - 225, mpos[1] - 100)

            l_bar = pygame.Surface((5, 100))
            l_bar.fill((0, 0, 0))
            r_bar = pygame.Surface((5, 100))
            r_bar.fill((0, 0, 0))
            top_bar = pygame.Surface((225, 5))
            top_bar.fill((0, 0, 0))
            bot_bar = pygame.Surface((225, 5))
            bot_bar.fill((0, 0, 0))
            s.set_alpha(200)  # alpha level
            s.fill((20, 20, 20))
            s.blit(l_bar, (0, 0))
            s.blit(r_bar, (220, 0))
            s.blit(top_bar, (0, 0))
            s.blit(bot_bar, (0, 95))

            lable_text = self.game.game_ui.context_font.render('Tower', True,
                                                           self.game.game_ui.context_text_color)
            lable_text_rect = lable_text.get_rect(center=(s.get_width() / 2, 20))
            s.blit(lable_text, lable_text_rect)

            break_bar = pygame.Surface((170, 3))
            break_bar.fill((0, 0, 0))
            s.blit(break_bar, (25, 40))

            info_text = self.game.game_ui.info_font.render('Insert a gem to activate', True,
                                                              self.game.game_ui.info_text_color)
            info_text_rect = info_text.get_rect(center=(s.get_width() / 2, 65))
            s.blit(info_text, info_text_rect)

            surf.blit(s, context_pos)

        else:
            s = pygame.Surface((225, 150))
            context_pos = (mpos[0] + 20, mpos[1] - 150)
            if mpos[0] > 863:
                context_pos = (mpos[0] - 225, mpos[1] - 150)

            l_bar = pygame.Surface((5, 150))
            l_bar.fill((0, 0, 0))
            r_bar = pygame.Surface((5, 150))
            r_bar.fill((0, 0, 0))
            top_bar = pygame.Surface((225, 5))
            top_bar.fill((0, 0, 0))
            bot_bar = pygame.Surface((225, 5))
            bot_bar.fill((0, 0, 0))
            s.set_alpha(200)  # alpha level
            s.fill((20, 20, 20))
            s.blit(l_bar, (0, 0))
            s.blit(r_bar, (220, 0))
            s.blit(top_bar, (0, 0))
            s.blit(bot_bar, (0, 145))


            lable_text = self.game.game_ui.context_font.render('Grade 1 Gem', True,
                                                               self.game.game_ui.context_text_color)
            lable_text_rect = lable_text.get_rect(center=(s.get_width() / 2, 20))
            s.blit(lable_text, lable_text_rect)

            break_bar = pygame.Surface((170, 3))
            break_bar.fill((0, 0, 0))
            s.blit(break_bar, (25, 40))

            text = 'Damage: ' + str(self.gem.damage)
            damage_text = self.game.game_ui.info_font.render(text, True,
                                                           self.game.game_ui.info_text_color)
            damage_text_rect = damage_text.get_rect(center=(s.get_width() / 2, 60))
            s.blit(damage_text, damage_text_rect)

            text = 'Range: ' + str(self.gem.range / 10)
            range_text = self.game.game_ui.info_font.render(text, True,
                                                           self.game.game_ui.info_text_color)
            range_text_rect = range_text.get_rect(center=(s.get_width() / 2, 80))
            s.blit(range_text, range_text_rect)

            text = 'Shots per second: ' + str(self.gem.shot_delay)
            sps_text = self.game.game_ui.info_font.render(text, True,
                                                            self.game.game_ui.info_text_color)
            sps_text_rect = sps_text.get_rect(center=(s.get_width() / 2, 100))
            s.blit(sps_text, sps_text_rect)

            text = 'Hits: ' + str(self.gem.hit_count)
            hits_text = self.game.game_ui.info_font.render(text, True,
                                                          self.game.game_ui.context_text_color)
            hits_text_rect = hits_text.get_rect(center=(s.get_width() / 2, 120))
            s.blit(hits_text, hits_text_rect)

            surf.blit(s, context_pos)

