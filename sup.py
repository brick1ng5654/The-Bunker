import pygame
pygame.init()   # Инициализация Pygame

# Констнанты
BUTTON_SIZE = 25
FONT_SIZE = 35
FONT_PATH = "static/NineByFiveNbp.ttf"

# Цвета
MAIN_COLOR = (212, 207, 201)
WHITE_COLOR = (255, 255, 255)
BLACK_COLOR = (0, 0, 0)
LIGHT_GREY = (180, 180, 180)
BLUE = (90, 110, 195)

def init_font():
    try:
        font = pygame.font.Font(FONT_PATH, FONT_SIZE)
    except FileNotFoundError:
        print(f"Error: Could not find the font file at {FONT_PATH}")
        font = pygame.font.Font(None, FONT_SIZE)  # Используйте стандартный шрифт Pygame в случае ошибки
    return font
