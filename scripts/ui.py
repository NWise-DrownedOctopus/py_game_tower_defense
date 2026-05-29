import pygame
from scripts.utils import load_image, play_audio, draw_text


class UI:
    def __init__(self, scene):
        self.scene = scene
        self.buttons = []
        self.font = pygame.font.Font("fonts/Bandwidth8x8.ttf", 50)
        self.font_color = (198, 172, 201)
        self.sub_font = pygame.font.Font("fonts/Bandwidth8x8.ttf", 30)
        self.wave_font = pygame.font.Font("fonts/Bandwidth8x8.ttf", 20)
        self.context_font = pygame.font.Font("fonts/Bandwidth8x8.ttf", 10)
        self.context_text_color = (220, 220, 220)
        self.info_font = pygame.font.Font("fonts/Bandwidth8x8.ttf", 8)
        self.info_text_color = (247, 226, 107)
        self.wave_data = None

        self.assets = {
            'l_side_bar': load_image("ui/UI_L_SideBar.png"),
            'r_side_bar': load_image("ui/UI_R_SideBar.png"),
            'top_bar': load_image("ui/UI_TopBar.png"),
            'bottom_bar': load_image("ui/UI_BottomBar.png"),
            'play_button': load_image("ui/play_button.png"),
            'pause_button': load_image("ui/pause_button.png"),
            'fast_forward_button': load_image("ui/fast_forward_button.png"),
            'tower_button': load_image("ui/tower_button.png"),
            'gem_button': load_image("ui/gem_button.png"),
            'tower_button_small': load_image("ui/tower_button_small.png"),
            'gem_button_small': load_image("ui/gem_button_small.png"),
            'mars_hex_01': load_image("ui/mars_hex_01.png"),
            'mars_hex_select_01': load_image("ui/mars_hex_select_01.png"),
            'planet_bg': load_image("ui/planet_bg.png"),
            'mouse_pointer': load_image("mouse_pointer.png"),
            'wave_button_hover': load_image("ui/wave_button_hover.png"),
            'wave_button': load_image("ui/wave_button.png"),
            'gem_stash': load_image("ui/gem_stash.png")
        }

    def create_level_buttons(self, surf):
        # This is for my pc
        if surf.get_size()[0] == 2560 and surf.get_size()[1] == 1440:
            pause_button = Button(self, 32, 32, (2250, 50), 'pause', self.assets["pause_button"])
            start_button = Button(self, 32, 32, (2350, 50), 'play', self.assets["play_button"])
            fast_forward_button = Button(self, 32, 32, (2450, 50), 'fast_forward',
                                         self.assets["fast_forward_button"])
            tower_button = Button(self, 128, 128, (2225, 500), 'tower_button', self.assets["tower_button"])
            gem_button = Button(self, 128, 128, (2400, 500), 'gem_button', self.assets["gem_button"])
        # This is for my laptop
        if surf.get_size()[0] == 1440 and surf.get_size()[1] == 900:
            pause_button = Button(self, 32, 32, (1150, 50), 'pause', self.assets["pause_button"])
            start_button = Button(self, 32, 32, (1250, 50), 'play', self.assets["play_button"])
            fast_forward_button = Button(self, 32, 32, (1350, 50), 'fast_forward',
                                         self.assets["fast_forward_button"])
        if surf.get_size()[0] == 1280 and surf.get_size()[1] == 720:
            pause_button = Button(self, 32, 32, (1100, 20), 'pause', self.assets["pause_button"])
            start_button = Button(self, 32, 32, (1165, 20), 'play', self.assets["play_button"])
            fast_forward_button = Button(self, 32, 32, (1230, 20), 'fast_forward',
                                         self.assets["fast_forward_button"])
            tower_button = Button(self, 64, 64, (1100, 300), 'tower_button', self.assets["tower_button_small"])
            gem_button = Button(self, 64, 64, (1200, 300), 'gem_button', self.assets["gem_button_small"])

    def check_click(self):
        print("We called check_click")
        if len(self.buttons) > 0:
            print("We detect: ", len(self.buttons), " buttons")
            for button in self.buttons:
                # Check if we have a collision with the mpos point
                if self.scene == "ow_map":
                    print("We are in ow_map scene")
                    if button.rect.collidepoint(pygame.mouse.get_pos()[0] / 2, pygame.mouse.get_pos()[1] / 2):
                        play_audio('button')
                        return button.name
                if button.rect.collidepoint(pygame.mouse.get_pos()):
                    play_audio('button')
                    return button.name
        else:
            print("No buttons were found when checking for click")

    def create_wave_display(self, waves):
        print("We created a wave_display, we have ", len(waves), " waves")
        print(waves)
        self.wave_data = waves
        count = 0
        for wave in waves:
            w_data = self.wave_data[str(count+1)]
            wave_button = Button(self, 32, 80, (0, int(80 * count)), ('w', + count), self.assets['wave_button'], self.assets['wave_button_hover'], w_data)
            count += 1

    def draw_gem_stash(self, surf):
        surf.blit(pygame.transform.scale(self.assets['gem_stash'], (165, 165)), (1100, 400))


    def update_wave_display(self, ff=False):
        movement = 80 / 14 / 60
        if ff:
            movement = 80 / 14 / 30
        for button in self.buttons:
            if button.name[0] == 'w':
                button.pos = (button.pos[0], button.pos[1] - movement)
                if button.pos[1] < 0:
                    self.buttons.remove(button)


class Button:
    def __init__(self, ui, width, height, pos, name, img=None, hover_img=None, context=None):
        self.ui = ui
        self.width, self.height = width, height
        self.pos = pos
        self.rect = pygame.Rect(pos[0], pos[1], self.width, self.height)
        self.img = img
        self.hover_img = hover_img
        self.name = name
        self.context = context
        ui.buttons.append(self)

    def button_presed(self, action):
        print("We clicked on a button")

    def draw_button(self, surf):
        if self.img is not None:
            surf.blit(self.img, self.pos)
            if self.name[0] == 'w':
                wave_num = str(self.name[1] + 1)
                wave_num = self.ui.wave_font.render(wave_num, True, self.ui.font_color)
                wave_num_rect = wave_num.get_rect(center=(self.rect.width / 2, self.pos[1] + 70))
                # draw_text(surf, wave_num, self.ui.wave_font, self.ui.font_color, self.rect.x + 10, self.rect.y - 70)
                surf.blit(wave_num, wave_num_rect)


    def draw_button_hover(self, surf):
        if self.hover_img is not None:
            print("We called draw_button_hover")
            surf.blit(self.hover_img, self.pos)
        if self.context is not None:
            self.draw_context(surf)

    def draw_context(self, surf):
        if self.name:
            if self.name[0] == 'w':
                mpos = pygame.mouse.get_pos()
                if mpos[1] < 230:
                    s = pygame.Surface((350, 200))
                    context_pos = (mpos[0] + 20, 20)
                elif mpos[0] > 900:
                    s = pygame.Surface((350, 200))
                    context_pos = (mpos[0] - 320, mpos[1] - 200)
                else:
                    s = pygame.Surface((350, 200))
                    context_pos = (mpos[0] + 20, mpos[1] - 200)
                l_bar = pygame.Surface((5, 200))
                l_bar.fill((0, 0, 0))
                r_bar = pygame.Surface((5, 200))
                r_bar.fill((0, 0, 0))
                top_bar = pygame.Surface((350, 5))
                top_bar.fill((0, 0, 0))
                bot_bar = pygame.Surface((350, 5))
                bot_bar.fill((0, 0, 0))
                s.set_alpha(200)  # alpha level
                s.fill((20, 20, 20))
                s.blit(l_bar, (0, 0))
                s.blit(r_bar, (345, 0))
                s.blit(top_bar, (0, 0))
                s.blit(bot_bar, (0, 195))

                wave_data = self.ui.wave_data[str(self.name[1] + 1)]
                text = 'Wave ' + str(self.name[1] + 1) + ' of ' + str(len(self.ui.wave_data))
                wavenum_text = self.ui.context_font.render(text, True, self.ui.context_text_color)
                wavenum_text_rect = wavenum_text.get_rect(center=(s.get_width() / 2, 20))
                s.blit(wavenum_text, wavenum_text_rect)

                text = str(wave_data[0]) + ' ' + str(wave_data[1])
                enemy_count_text = self.ui.context_font.render(text, True, self.ui.context_text_color)
                enemy_count_text_rect = enemy_count_text.get_rect(center=(s.get_width() / 2, 45))
                s.blit(enemy_count_text, enemy_count_text_rect)

                break_bar = pygame.Surface((250, 3))
                break_bar.fill((0, 0, 0))
                s.blit(break_bar, (50, 60))

                text = 'Hitpoints: ' + str(wave_data[2])
                hit_points_text = self.ui.context_font.render(text, True, self.ui.context_text_color)
                hit_points_text_rect = hit_points_text.get_rect(center=(s.get_width() / 2, 80))
                s.blit(hit_points_text, hit_points_text_rect)

                if str(wave_data[1]) == "big":
                    speed = .02
                elif str(wave_data[1]) == "normal":
                    speed = .05
                elif str(wave_data[1]) == "fast":
                    speed = .1
                text = 'Speed: ' + str(speed)
                speed_text = self.ui.context_font.render(text, True, self.ui.context_text_color)
                speed_text_rect = speed_text.get_rect(center=(s.get_width() / 2, 105))
                s.blit(speed_text, speed_text_rect)

                if str(wave_data[1]) == "big":
                    steel = 12
                elif str(wave_data[1]) == "normal":
                    steel = 8
                elif str(wave_data[1]) == "fast":
                    steel = 2
                text = 'Steel gain per kill: ' + str(steel)
                steel_text = self.ui.context_font.render(text, True, self.ui.context_text_color)
                steel_text_rect = steel_text.get_rect(center=(s.get_width() / 2, 130))
                s.blit(steel_text, steel_text_rect)

                break_bar = pygame.Surface((250, 3))
                break_bar.fill((0, 0, 0))
                s.blit(break_bar, (50, 150))

                info_text = self.ui.info_font.render('Click to start this and all waves above now', True, self.ui.info_text_color)
                info_text_rect = info_text.get_rect(center=(s.get_width() / 2, 175))
                s.blit(info_text, info_text_rect)

                surf.blit(s, context_pos)

    def check_hover(self):
        if self.ui.scene == "ow_map":
            if self.rect.collidepoint(pygame.mouse.get_pos()[0] / 2, pygame.mouse.get_pos()[1] / 2):
                return True
        else:
            if self.rect.collidepoint(pygame.mouse.get_pos()):
                return True
