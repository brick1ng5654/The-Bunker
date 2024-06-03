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

def load_all_data():
    data = {
        "common_sex": load_array("data/sex/common_sex.txt"),
        "unusual_sex": load_array("data/sex/unusual_sex.txt"),
        "rare_sex": load_array("data/sex/rare_sex.txt"),
        "common_age": load_array("data/age/common_age.txt"),
        "unusual_age": load_array("data/age/unusual_age.txt"),
        "rare_age": load_array("data/age/rare_age.txt"),
        "common_gender": load_array("data/gender/common_gender.txt"),
        "unusual_gender": load_array("data/gender/unusual_gender.txt"),
        "rare_gender": load_array("data/gender/rare_gender.txt"),
        "common_job": load_array("data/job/common_job.txt"),
        "unusual_job": load_array("data/job/unusual_job.txt"),
        "rare_job": load_array("data/job/rare_job.txt"),
        "common_health": load_array("data/health/common_health.txt"),
        "unusual_health": load_array("data/health/unusual_health.txt"),
        "rare_health": load_array("data/health/rare_health.txt"),
        "common_hobby": load_array("data/hobby/common_hobby.txt"),
        "unusual_hobby": load_array("data/hobby/unusual_hobby.txt"),
        "rare_hobby": load_array("data/hobby/rare_hobby.txt"),
        "personality": load_array("data/personality.txt"),
        "common_fact": load_array("data/fact/common_fact.txt"),
        "unusual_fact": load_array("data/fact/unusual_fact.txt"),
        "rare_fact": load_array("data/fact/rare_fact.txt"),
        "common_bagage": load_array("data/bagage/common_bagage.txt"),
        "unusual_bagage": load_array("data/bagage/unusual_bagage.txt"),
        "rare_bagage": load_array("data/bagage/rare_bagage.txt"),
        "condition": load_array("data/condition.txt"),
        "fobia": load_array("data/fobia.txt"),
    }
    return data

def load_array(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            return [line.strip() for line in file]
    except:
        print("Error!")
        return []
