import pygame

# Инициализация Pygame
pygame.init()

# Константы
MAIN_COLOR = (212, 207, 201)
PLAYER_SIZE = 125
BUTTON_SIZE = 25
PLAYER_COLOR = (90, 90, 90)
FONT_SIZE = 35
HEADER_HEIGHT = 35
DARK_BLUE = (18, 4, 150)
BLUE = (90, 110, 195)
LIGHT_BLUE = (160, 200, 240)
BLACK_COLOR = (0, 0, 0)
WHITE_COLOR = (255, 255, 255)
DARK_GREY = (70, 70, 70)
LIGHT_GREY = (180, 180, 180)

CPERCENT = 60
UPERCENT = 30

# Шрифт / Font creator: Nate Halley
FONT_PATH = "data/fonts/NineByFiveNbp.ttf"

def init_font():
    try:
        font = pygame.font.Font(FONT_PATH, FONT_SIZE)
    except FileNotFoundError:
        print(f"Error: Could not find the font file at {FONT_PATH}")
        font = pygame.font.Font(None, FONT_SIZE)  # Используйте стандартный шрифт Pygame в случае ошибки
    return font

font = init_font()