import pygame
import sys
from player_init import *

# Инициализация Pygame
pygame.init()

# Константы
MAIN_COLOR = (212, 207, 201)
PLAYER_SIZE = 100
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

# Шрифт / Font creator: Nate Halley
FONT_PATH = "data/fonts/NineByFiveNbp.ttf"
try:
    font = pygame.font.Font(FONT_PATH, FONT_SIZE)
except FileNotFoundError:
    print(f"Error: Could not find the font file at {FONT_PATH}")
    font = pygame.font.Font(None, FONT_SIZE)  # Используйте стандартный шрифт Pygame в случае ошибки

def draw_button_with_shadow(screen, x, y, w, h, button_color, active_color, text, text_color, font):
    # Определяем положение мыши и нажатие кнопок
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    # Проверяем, находится ли курсор мыши над кнопкой
    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        current_color = active_color
        if click[0] == 1:
            return True
    else:
        current_color = button_color

    # Рисуем тень кнопки
    shadow_rect = pygame.Rect(x + 3, y + 3, w, h)
    pygame.draw.rect(screen, DARK_GREY, shadow_rect)
    
    # Рисуем кнопку
    button_rect = pygame.Rect(x, y, w, h)
    pygame.draw.rect(screen, current_color, button_rect)
    
    # Рисуем текст
    text_surf = font.render(text, True, text_color)
    text_rect = text_surf.get_rect(center=button_rect.center)
    screen.blit(text_surf, text_rect)
    
    return button_rect

def draw_gradient_rect(screen, rect, start_color, end_color):
    x, y, w, h = rect
    for i in range(w):
        # Calculate the color for the current line
        color_ratio = i / w
        color = (
            int(start_color[0] * (1 - color_ratio) + end_color[0] * color_ratio),
            int(start_color[1] * (1 - color_ratio) + end_color[1] * color_ratio),
            int(start_color[2] * (1 - color_ratio) + end_color[2] * color_ratio)
        )
        pygame.draw.line(screen, color, (x + i, y), (x + i, y + h))

def draw_static_window_with_shadow(screen, x, y, w, h, window_color):
    # Рисуем тень окна
    shadow_rect = pygame.Rect(x + 5, y + 5, w, h)
    pygame.draw.rect(screen, DARK_GREY, shadow_rect)
    
    # Рисуем окно
    window_rect = pygame.Rect(x, y, w, h)
    pygame.draw.rect(screen, window_color, window_rect)

def draw_header(screen, width, height):
    # Рисуем градиентную полосу заголовка
    draw_gradient_rect(screen, (0, 0, width, HEADER_HEIGHT), DARK_BLUE, LIGHT_BLUE)
    
    # Текст заголовка
    title_surface = font.render("The Bunker", True, WHITE_COLOR)
    screen.blit(title_surface, (10, 2))
    
    # Кнопка выхода с тенью
    exit_button = draw_button_with_shadow(screen, width - BUTTON_SIZE - 10, 5, BUTTON_SIZE, BUTTON_SIZE, MAIN_COLOR, LIGHT_GREY, "X", BLACK_COLOR, font)
    
    # Кнопка сворачивания с тенью
    minimize_button = draw_button_with_shadow(screen, width - 2 * BUTTON_SIZE - 20, 5, BUTTON_SIZE, BUTTON_SIZE, MAIN_COLOR, LIGHT_GREY, "—", BLACK_COLOR, font)
    
    # Неподвижное окно с тенью
    static_window_x = width - 520  # Отступ от правого края
    static_window_y = HEADER_HEIGHT + 20  # Отступ от нижнего края заголовка
    static_window_width = 500
    static_window_height = 800
    draw_static_window_with_shadow(screen, static_window_x, static_window_y, static_window_width, static_window_height, LIGHT_GREY)

    # Градиентная полоса сверху серого окна с текстом "Information"
    info_header_height = 35
    info_header_rect = pygame.Rect(static_window_x, static_window_y, static_window_width, info_header_height)
    draw_gradient_rect(screen, info_header_rect, BLUE, BLUE)
    
    info_title_surface = font.render("Information", True, WHITE_COLOR)
    info_title_rect = info_title_surface.get_rect(center=(static_window_x + static_window_width / 2, static_window_y + info_header_height / 2))
    screen.blit(info_title_surface, info_title_rect)
    
    return exit_button, minimize_button

def main():
    pygame.init()

    # Создание окна в полном экране
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    pygame.display.set_caption("The Bunker")

    # Получаем текущее разрешение экрана после установки полноэкранного режима
    screen_width, screen_height = pygame.display.get_window_size()

    players = []
    n = 4
    a = 100
    b = 100
    for i in range(n):
        players.append(create_player(a, b, i+1))
        a = a + 250

    selected_player = None
    clock = pygame.time.Clock()

    running = True
    while running:
        screen.fill(MAIN_COLOR)
        exit_button, minimize_button = draw_header(screen, screen_width, screen_height)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if exit_button.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()
                elif minimize_button.collidepoint(event.pos):
                    pygame.display.iconify()
                else:
                    for player in players:
                        if player.rect.collidepoint(event.pos):
                            selected_player = player
        
        for player in players:
            player.draw(screen)

        if selected_player:
            selected_player.draw_characteristics(screen, font)

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()
