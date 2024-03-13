import pygame

pygame.init()

SCREEN_WIDTH = pygame.display.get_desktop_sizes()[0][0]
SCREEN_HEIGHT = pygame.display.get_desktop_sizes()[0][1]

# screen is now a "Surface" as that is the return type from setting the display mode
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)

bg_border = 25
bg_color = (25,25,25)
game_bg_rect_width = SCREEN_WIDTH - (bg_border*2)
game_bg_rect_height = SCREEN_HEIGHT - (bg_border*2)
game_bg_rect = (bg_border, bg_border, game_bg_rect_width, game_bg_rect_height)

bg_grid_width_count = 5
bg_grid_height_count = 5
bg_grid_color = (50,50,50)

# Here is the game Loop
run = True
while run:

    # Here is where we are initializing the bg and bg grid
    pygame.draw.rect(screen, bg_color, game_bg_rect)
    # for count in range(bg_grid_width):
    pygame.draw.line(screen, bg_grid_color, (bg_border, (game_bg_rect_height/5 + bg_border)), ((game_bg_rect_width + bg_border), (game_bg_rect_height/5 + bg_border)))

    # This is the event checker for each frame
    for event in pygame.event.get():
        # This is where we make sure the game breaks out of the loop when the player wishes to exit
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

pygame.quit()