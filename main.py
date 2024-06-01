import pygame
import sys
from player_init import *

# Инициализация Pygame
pygame.init()

# Константы
WIDTH, HEIGHT = 1200, 800
BG_COLOR = (120, 111, 110)
PLAYER_SIZE = 100
PLAYER_COLOR = (255, 0, 0)
TEXT_COLOR = (255, 255, 255)
FONT_SIZE = 35
BUTTON_COLOR = (200, 0, 0)
BUTTON_HOVER_COLOR = (255, 0, 0)
BUTTON_TEXT_COLOR = (255, 255, 255)
BUTTON_WIDTH, BUTTON_HEIGHT = 150, 50

# Шрифт / Font creator: Nate Halley
FONT_PATH = "data/fonts/NineByFiveNbp.ttf"
try:
    font = pygame.font.Font(FONT_PATH, FONT_SIZE)
except FileNotFoundError:
    print(f"Error: Could not find the font file at {FONT_PATH}")
    font = pygame.font.Font(None, FONT_SIZE)  # Используйте стандартный шрифт Pygame в случае ошибки

def draw_button(screen, text, x, y, w, h, inactive_color, active_color, text_color, font):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        pygame.draw.rect(screen, active_color, (x, y, w, h))
        if click[0] == 1:
            return True
    else:
        pygame.draw.rect(screen, inactive_color, (x, y, w, h))

    text_surf = font.render(text, True, text_color)
    text_rect = text_surf.get_rect(center=((x + (w / 2)), (y + (h / 2))))
    screen.blit(text_surf, text_rect)
    
    return False

def main():
    pygame.init()

    # Создание окна в полном экране
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    pygame.display.set_caption("The Bunker")

    players = []
    n = 3
    a = 100
    b = 100
    for i in range(n):
        players.append(create_player(a, b))
        a = a + 150

    selected_player = None
    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for player in players:
                    if player.rect.collidepoint(event.pos):
                        selected_player = player

        screen.fill(BG_COLOR)

        for player in players:
            player.draw(screen)

        if selected_player:
            selected_player.draw_characteristics(screen, font)

        # Рисуем кнопку выхода
        screen_width, screen_height = screen.get_size()
        if draw_button(screen, "Exit", screen_width - BUTTON_WIDTH - 20, screen_height - BUTTON_HEIGHT - 20, BUTTON_WIDTH, BUTTON_HEIGHT, BUTTON_COLOR, BUTTON_HOVER_COLOR, BUTTON_TEXT_COLOR, font):
            pygame.quit()
            sys.exit()

        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    main()
