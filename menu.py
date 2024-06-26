import pygame
import sys
from sup import *
import datetime
from bunker import create_bunker
from player import new_game
from random import randint
import random
import subprocess
import os

font = init_font()

def run_server():
    subprocess.Popen(["python", "server.py"])

def changed_color(color, amount, action):
    if(action): return tuple(min(value + amount, 255) for value in color)   # "Увеличение" цвета (к белому)
    else: return tuple(max(value - amount, 0) for value in color)           # "Уменьшение" цвета (к чёрному)

def draw_button(screen, x, y, w, h, default_color, active_color, text, text_color, font):
    # Определяем положение мыши и нажатик кнопок
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    # Проверяем, находится ли курсор мыши над кнопкой
    if x < mouse[0] < x + w and y < mouse[1] < y + h:
        current_color = active_color
        if click[0] == 1:
            return True
    else:
        current_color = default_color

    # Рисуем тень кнопки
    shadow_rect = pygame.Rect(x + 3, y + 3, w, h)
    pygame.draw.rect(screen, changed_color(BLACK_COLOR, 70, 1), shadow_rect)

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

def draw_header(screen, width, height):
    draw_gradient_rect(screen, (0, 0, width, 35), changed_color(BLUE, 75, 0), changed_color(BLUE, 70, 1))   # Рисуем градиентную полосу заголовка

    # Загрузка изображения радиации
    radiation_image = pygame.image.load("data/radiation.png").convert_alpha()
    radiation_image = pygame.transform.scale(radiation_image, (25, 25))
    radiation_rect = radiation_image.get_rect()
    radiation_rect.topleft = (10, 5)  # Позиция изображения

    # Текст заголовка
    title_surface = font.render("The Bunker.exe", True, WHITE_COLOR)
    title_rect = title_surface.get_rect()
    title_rect.topleft = (radiation_rect.right + 10, 2)  # Позиция текста заголовка рядом с изображением

    # Отображение изображения и текста заголовка
    screen.blit(radiation_image, radiation_rect.topleft)
    screen.blit(title_surface, title_rect.topleft)

    # Отрисовка кнопок
    exit_button = draw_button(screen, width - BUTTON_SIZE - 10, 5, BUTTON_SIZE, BUTTON_SIZE, MAIN_COLOR, LIGHT_GREY, "X", BLACK_COLOR, font)
    minimize_button = draw_button(screen, width - 2*BUTTON_SIZE - 20, 5, BUTTON_SIZE, BUTTON_SIZE, MAIN_COLOR, LIGHT_GREY, "_", BLACK_COLOR, font)
    return exit_button, minimize_button

def draw_lower(screen, width, height):
    lower_rect = pygame.Rect(0, height-51, width, 51)           # Отрисовка прямоугольника (панели задач)
    pygame.draw.rect(screen, LIGHT_GREY, lower_rect)
    time_rect = pygame.Rect(width-88, height - 43, 80, 35)      # Отрисовка прямоугольника времени
    pygame.draw.rect(screen, MAIN_COLOR, time_rect, border_radius=8)
    date_rect = pygame.Rect(width-88-152, height - 43, 140, 35) # Отрисовка прямоугольника даты
    pygame.draw.rect(screen, MAIN_COLOR, date_rect, border_radius=8)
    name_rect = pygame.Rect(8, height - 43, width-260, 35)      # Отрисовка прямоугольника имени
    pygame.draw.rect(screen, MAIN_COLOR, name_rect, border_radius=8)

    current_time = datetime.datetime.now().strftime("%H:%M")    # Определение времени
    current_date = datetime.datetime.now().strftime("%d-%m-%Y") # Определение даты

    title_surface = font.render("The Bunker 1.02 - Ready (Registred)", True, BLACK_COLOR)
    screen.blit(title_surface, (20, height - 43))               # Отрисовка текста имени
    
    title_surface = font.render(current_date, True, BLACK_COLOR)
    screen.blit(title_surface, (width-234, height - 43))        # Отрисовка даты

    title_surface = font.render(current_time, True, BLACK_COLOR)
    screen.blit(title_surface, (width-73, height - 43))         # Отрисовка времени

def draw_option(screen, width, height, default_color, active_color, font_color):
    font = pygame.font.Font(FONT_PATH, 50)
    button_width = 350
    button_height = 100
    spacing = 10

    button_y_start = (height - 3 * button_height - 20) // 2  # Центрируем кнопки по вертикали
    button_x = (width - button_width) // 2                   # Центрируем кнопки по горизонтали

    new_game_button_y = button_y_start
    help_button_y = button_y_start + 1 * (button_height + spacing)
    exit_button_y = button_y_start + 2 * (button_height + spacing)

    new_game_button = draw_button(screen, button_x, new_game_button_y, button_width, button_height, default_color, active_color, "НОВАЯ ИГРА", font_color, font)
    help_button = draw_button(screen, button_x, help_button_y, button_width, button_height, default_color, active_color, "ПОМОЩЬ", font_color, font)
    exit_button = draw_button(screen, button_x, exit_button_y, button_width, button_height, default_color, active_color, "ВЫХОД", font_color, font)

    return new_game_button, help_button, exit_button

def draw_help_window(screen, width, height, text):
    window_width = 400
    window_height = 600
    window_x = (width - window_width) // 2
    window_y = (height - window_height) // 2        # Центрируем всё

    pygame.draw.rect(screen, WHITE_COLOR, (window_x, window_y, window_width, window_height), border_radius=10)      # Рисуем окошко
    pygame.draw.rect(screen, LIGHT_GREY, (window_x, window_y, window_width, window_height), 4, border_radius=10)

    font = pygame.font.Font(FONT_PATH, 30)
    max_width = window_width - 40
    words = text.split(' ')
    lines = []
    current_line = ""
    
    for word in words:                              # Переносим слова, если они не помещаются
        test_line = current_line + word + " "
        if font.size(test_line)[0] <= max_width:
            current_line = test_line
        else:
            lines.append(current_line)
            current_line = word + " "
    lines.append(current_line)

    for i, line in enumerate(lines):
        text_surface = font.render(line, True, BLACK_COLOR)
        text_rect = text_surface.get_rect(midtop=(window_x + window_width // 2, window_y + 20 + i * 40))
        screen.blit(text_surface, text_rect)

    close_button = draw_button(screen, window_x + window_width - 100, window_y + window_height - 60, 83, 40, LIGHT_GREY, changed_color(LIGHT_GREY, 15, 0), " Закрыть", BLACK_COLOR, font)
    return close_button

def draw_input_window(screen, width, height, input_text, input_active, error_message):
    window_width = 400
    window_height = 250
    window_x = (width - window_width) // 2
    window_y = (height - window_height) // 2

    pygame.draw.rect(screen, WHITE_COLOR, (window_x, window_y, window_width, window_height), border_radius=10)
    pygame.draw.rect(screen, LIGHT_GREY, (window_x, window_y, window_width, window_height), 4, border_radius=10)

    font = pygame.font.Font(FONT_PATH, 35)
    prompt_surface = font.render("Введите количество игроков:", True, BLACK_COLOR)
    prompt_rect = prompt_surface.get_rect(center=(window_x + window_width // 2, window_y + 40))
    screen.blit(prompt_surface, prompt_rect)

    input_rect = pygame.Rect(window_x + 50, window_y + 80, window_width - 100, 40)
    pygame.draw.rect(screen, LIGHT_GREY, input_rect, border_radius=5)

    input_surface = font.render(input_text, True, BLACK_COLOR)
    screen.blit(input_surface, (input_rect.x + 10, input_rect.y + 5))

    if input_active:
        cursor_surface = font.render("|", True, BLACK_COLOR)
        cursor_x = input_rect.x + 10 + input_surface.get_width()
        screen.blit(cursor_surface, (cursor_x, input_rect.y + 5))

    close_button = draw_button(screen, window_x + window_width - 120, window_y + window_height - 55, 100, 40, LIGHT_GREY, changed_color(LIGHT_GREY, 15, 0), "Закрыть", BLACK_COLOR, font)

    if error_message:
        error_surface = font.render(error_message, True, (255, 0, 0))
        error_rect = error_surface.get_rect(center=(window_x + window_width // 2, window_y + 150))
        screen.blit(error_surface, error_rect)

    return input_rect, close_button

def display_bunker(screen, bunker, screen_width):
    y_offset = 50
    #max_width = screen_width - 100  # Define maximum width for text wrapping
    max_width = 720
    for line in bunker:
        words = line.split()
        current_line = ""
        for word in words:
            if font.size(current_line + word)[0] < max_width:
                current_line += word + " "
            else:
                text_surface = font.render(current_line, True, BLACK_COLOR)
                screen.blit(text_surface, (50, y_offset))
                y_offset += 40
                current_line = word + " "
        text_surface = font.render(current_line, True, BLACK_COLOR)
        screen.blit(text_surface, (50, y_offset))
        y_offset += 40

def clear_players_data():
    for i in range(1, 13):
        try:
            os.remove(f'data/players/player_{i}.txt')
        except:
            break

def main():
    pygame.init()

    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    screen_width, screen_height = pygame.display.get_window_size()
    pygame.display.set_caption("The Bunker")
    pygame.display.set_icon(pygame.image.load("data/radiation.png"))
    cursor_image = pygame.image.load("data/cursor.png").convert_alpha()
    cursor_image = pygame.transform.scale(cursor_image, (BUTTON_SIZE, BUTTON_SIZE + 5))
    pygame.mouse.set_visible(False)
    clock = pygame.time.Clock()

    show_help = False
    show_input = False
    input_text = ""
    input_active = False
    error_message = ""
    game_begin = 0
    n = 0

    clear_players_data()
    with open("data/help.txt", 'r', encoding='utf-8') as file:
        help_text = file.read()

    bunker = []
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if show_help:
                    if close_button.collidepoint(event.pos):
                        show_help = False
                elif show_input:
                    if close_input_button.collidepoint(event.pos):
                        show_input = False
                        input_active = False
                        error_message = ""
                    elif input_rect.collidepoint(event.pos):
                        input_active = True
                    else:
                        input_active = False
                elif exit_button.collidepoint(event.pos):
                    clear_players_data()
                    pygame.quit()
                    sys.exit()
                elif minimize_button.collidepoint(event.pos):
                    pygame.display.iconify()
                elif (game_begin == 0):
                    if help_button and help_button.collidepoint(event.pos):
                        show_help = True
                    elif new_game_button and new_game_button.collidepoint(event.pos):
                        show_input = True
                        input_active = True
                    elif exit_option_button and exit_option_button.collidepoint(event.pos):
                        running = False

            elif event.type == pygame.KEYDOWN and show_input:
                if event.key == pygame.K_RETURN:
                    try:
                        n = int(input_text)
                        if 1 <= n <= 12:
                            game_begin = 1
                            show_input = False
                            input_active = False
                            input_text = ""
                            error_message = ""
                            bunker, image = create_bunker(n)
                            new_game(n)
                            run_server()
                            
                        else:
                            error_message = "Введите число от 1 до 12!"
                    except ValueError:
                        error_message = "Неверный ввод! Введите число!"
                elif event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                else:
                    input_text += event.unicode

            elif event.type == pygame.QUIT:
                running = False

        screen.fill(MAIN_COLOR)
        exit_button, minimize_button = draw_header(screen, screen_width, screen_height)
        draw_lower(screen, screen_width, screen_height)

        if (game_begin == 0):
            new_game_button, help_button, exit_option_button = draw_option(screen, screen_width, screen_height, LIGHT_GREY, changed_color(LIGHT_GREY, 15, 0), BLACK_COLOR)

        if show_help:
            close_button = draw_help_window(screen, screen_width, screen_height, help_text)
        if show_input:
            input_rect, close_input_button = draw_input_window(screen, screen_width, screen_height, input_text, input_active, error_message)

        if game_begin and bunker:
            display_bunker(screen, bunker, screen_width)

        pygame.draw.circle(screen, WHITE_COLOR, pygame.mouse.get_pos(), 1)
        screen.blit(cursor_image, (pygame.mouse.get_pos()[0] - 5, pygame.mouse.get_pos()[1] - 5))
        pygame.display.flip()
        clock.tick(60)

    clear_players_data()
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
