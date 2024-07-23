import pygame
from scripts.utils import load_image, play_audio, draw_text


class UI:
    def __init__(self, scene):
        self.scene = scene
        self.buttons = []
        self.font = pygame.font.Font("fonts/Bandwidth8x8.ttf", 50)
        self.font_color = (198, 172, 201)
        self.sub_font = pygame.font.Font("fonts/Bandwidth8x8.ttf", 30)
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
            'wave_button': load_image("ui/wave_button.png")
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
            wave_button = Button(self, 32, 150, (0, int(150 * count)), ('w', + count), self.assets['wave_button'], self.assets['wave_button_hover'], w_data)
            count += 1


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

    def draw_button_hover(self, surf):
        if self.hover_img is not None:
            print("We called draw_button_hover")
            surf.blit(self.hover_img, self.pos)
        if self.context is not None:
            self.draw_context()

    def draw_context(self):
        print(self.context)

    def check_hover(self):
        if self.ui.scene == "ow_map":
            if self.rect.collidepoint(pygame.mouse.get_pos()[0] / 2, pygame.mouse.get_pos()[1] / 2):
                return True
        else:
            if self.rect.collidepoint(pygame.mouse.get_pos()):
                return True
