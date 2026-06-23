import pygame

LINE_WIDTH = 5

def build_context_panel(mpos, width, height, label_text, display_width):                     
    s = pygame.Surface((width, height))
    context_pos = (mpos[0] + 20, mpos[1] - height)
    if mpos[0] > (display_width - width):
        context_pos = (mpos[0] - width, context_pos[1])
    if mpos[1] < height:
        context_pos = (context_pos[0], 0)
        
    l_bar = pygame.Surface((LINE_WIDTH, height))
    l_bar.fill((0, 0, 0))
    r_bar = pygame.Surface((LINE_WIDTH, height))
    r_bar.fill((0, 0, 0))
    top_bar = pygame.Surface((width, LINE_WIDTH))
    top_bar.fill((0, 0, 0))
    bot_bar = pygame.Surface((width, LINE_WIDTH))
    bot_bar.fill((0, 0, 0))
    s.set_alpha(200)  # alpha level
    s.fill((20, 20, 20))
    s.blit(l_bar, (0, 0))
    s.blit(r_bar, ((width - LINE_WIDTH), 0))
    s.blit(top_bar, (0, 0))
    s.blit(bot_bar, (0, (height - LINE_WIDTH)))
    label_text_rect = label_text.get_rect(center=(s.get_width() / 2, 20))
    s.blit(label_text, label_text_rect)        
    break_bar = pygame.Surface((170, 3))
    break_bar.fill((0, 0, 0))
    s.blit(break_bar, (25, 40))  
    return s, context_pos

def draw_text(surf, text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    surf.blit(img, (x, y))
            